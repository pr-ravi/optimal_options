import oo.models
from oo.storage import sql_env
from oo.platforms.loader import Loader
from oo.config import reader
from oo.models.instrument_data import InstrumentData
from oo.models.historical_data import HistoricalData
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date, timedelta

from nsepy import get_history

__historical_data_ceiling__ = 3 * 365 # 3 years
__update_threshold__ = 10 # 10 days, for update
__batch_size__ = 100 # sql batch size

class NseLoader(Loader):
    def load_platform_history(self):
        today = date.today()
        start_date = today - timedelta(days = __historical_data_ceiling__)

        session = Session(sql_env.engine)
        # query instrument list
        instruments = session.query(InstrumentData).filter(InstrumentData.type == 'nse')
        for instrument in instruments:

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
            
            # use pd to write using sqlalchemy
            history_df.to_sql(
                name=HistoricalData.__tablename__,
                con=sql_env.engine, 
                if_exists='append', 
                index_label='day',
                chunksize = __batch_size__
            )
            
        session.close() 
        


    def load_instrument_list(self):
        yaml_data = reader.read_yaml('nse.yaml')
        session = Session(sql_env.engine)
        for inst_name in yaml_data['instruments']:
            item = InstrumentData(type = "nse", instrument_name = inst_name)
            session.add(item)
        session.flush()
        session.commit()
        session.close()
        
