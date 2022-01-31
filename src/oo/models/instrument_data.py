from oo.storage import sql_env
import sqlalchemy as sa


class InstrumentData(sql_env.SqlBase):
    __tablename__ = 'instrument_list'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    type = sa.Column(sa.String(10))
    instrument_name = sa.Column(sa.String(15))


    def __repr__(self):
        return f"InstrumentData(id={self.id!r}, type={self.type!r}, instrument_name={self.instrument_name!r})"

