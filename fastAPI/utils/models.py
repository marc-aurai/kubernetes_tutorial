import utils.database as _database
import sqlalchemy as _sql


class Predictions(_database.Base):
    __tablename__ = "predictions"
    id = _sql.Column(_sql.String, primary_key=True, index=True)
    created_at = _sql.Column(_sql.TIMESTAMP, unique=True, index=True)
    predictions = _sql.Column(_sql.String, unique=False, index=True)

class RawInput(_database.Base):
    __tablename__ = "raw_input"
    id = _sql.Column(_sql.String, primary_key=True, index=True)
    created_at = _sql.Column(_sql.TIMESTAMP, unique=True, index=True)
    question1 = _sql.Column(_sql.String, unique=False, index=True)
    question2 = _sql.Column(_sql.String, unique=False, index=True)
    q1_words = _sql.Column(_sql.Integer, unique=False, index=True)
    q2_words = _sql.Column(_sql.Integer, unique=False, index=True)