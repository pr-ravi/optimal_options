from tracemalloc import start
from turtle import update
import oo.models
from oo.storage import sql_env
from oo.platforms.loader import Loader
from oo.config import reader
from oo.models.instrument_data import InstrumentData
from oo.models.historical_data import HistoricalData
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date, timedelta, datetime
import logging

from nsepy import get_history

__historical_data_ceiling__ = 3 * 365 # 3 years
__update_threshold__ = -1 # max days to process in update, -1 for no limit
__batch_size__ = 100 # sql batch size

class NseLoader(Loader):
    def __init__(self) -> None:
        self.logger = logging.Logger("NseLoader")

    def load_data(self, type):
        today = date.today()

        session = Session(sql_env.engine)
        # query instrument list
        instruments = session.query(InstrumentData).filter(InstrumentData.type == 'nse')
        for instrument in instruments:
            
            instrument_name = instrument.instrument_name
            stmt = select(HistoricalData) \
                .where(HistoricalData.instrument == instrument_name) \
                .order_by(HistoricalData.day.desc()) \
                .limit(1)  

            latest_history = session.execute(stmt) 
                
                
            latest_history = latest_history.scalars().all()
            
            if latest_history:
                start_date = latest_history[0].day
                self.logger.info("Latest entry for {instrument} is {start_date}")

                # query from the next day
                start_date = start_date + timedelta(days = 1)
                
            else:
                # if no record, set to max days
                start_date = today - timedelta(days = __historical_data_ceiling__)

            # for update, check threshold
            if type == update:
                diff_days = (today - start_date).days
                if __update_threshold__ != -1 and diff_days > __update_threshold__:
                    self.logger.error("There are more records than the update threshold allows, aborting")
                    return
            
            self.logger.info(f"Query nse for instrument {instrument_name}")
            
            history_df = get_history(symbol=instrument.instrument_name,
                start = start_date,
                end = today,
                index=True,
            )

            # unneeded rows
            history_df = history_df.drop('Turnover', 1)

            # 'Date' can be problematic
            history_df.rename(columns={"Date":"day"})

            # additional cols
            history_df['exchange'] = 'nse'
            history_df['instrument'] = instrument.instrument_name
            
            # postgres lower_case is recommended
            history_df.columns = history_df.columns.str.lower()
            
            self.logger.info(f"Inserting into db")

            # use pd to write using sqlalchemy
            history_df.to_sql(
                name=HistoricalData.__tablename__,
                con=sql_env.engine, 
                if_exists='append', 
                index_label='day',
                chunksize = __batch_size__
            )


    def update_platform_history(self):
        self.load_data("update")

    def load_platform_history(self):
        self.load_data("full_load")
        # today = date.today()
        # start_date = today - timedelta(days = __historical_data_ceiling__)

        # session = Session(sql_env.engine)
        # # query instrument list
        # instruments = session.query(InstrumentData).filter(InstrumentData.type == 'nse')
        # for instrument in instruments:
            
        #     self.logger.info(f"Query nse for instrument {instrument.instrument_name}")
            
        #     history_df = get_history(symbol=instrument.instrument_name,
        #         start = start_date,
        #         end = today,
        #         index=True,
        #     )

        #     self.logger.info(f"Got data, inserting")

        #     # unneeded rows
        #     history_df = history_df.drop('Turnover', 1)

        #     # 'Date' can be problematic
        #     history_df.rename(columns={"Date":"day"})

        #     # additional cols
        #     history_df['exchange'] = 'nse'
        #     history_df['instrument'] = instrument.instrument_name
            
        #     # postgres lower_case is recommended
        #     history_df.columns = history_df.columns.str.lower()
            
        #     # use pd to write using sqlalchemy
        #     history_df.to_sql(
        #         name=HistoricalData.__tablename__,
        #         con=sql_env.engine, 
        #         if_exists='append', 
        #         index_label='day',
        #         chunksize = __batch_size__
        #     )
            
        # session.close() 
        


    def load_instrument_list(self):
        yaml_data = reader.read_yaml('nse.yaml')
        session = Session(sql_env.engine)
        for inst_name in yaml_data['instruments']:
            item = InstrumentData(type = "nse", instrument_name = inst_name)
            session.add(item)
        session.flush()
        session.commit()
        session.close()
        
