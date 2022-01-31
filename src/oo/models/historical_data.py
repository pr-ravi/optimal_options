# from oo.storage import sql_env
from oo.storage import sql_env
import sqlalchemy as sa


class HistoricalData(sql_env.SqlBase):
    __tablename__ = 'historical_data'

    instrument = sa.Column(sa.String(15), primary_key= True)
    exchange = sa.Column(sa.String(15), primary_key=True)
    day = sa.Column(sa.Date, primary_key=True)
    open = sa.Column(sa.Numeric(10))
    close = sa.Column(sa.Numeric(10))
    high = sa.Column(sa.Numeric(10))
    low = sa.Column(sa.Numeric(10))
    volume = sa.Column(sa.Integer)
