from sqlalchemy import func

from utils.db_api.db_gino import TimedBaseModel
from loader import db


class Account(TimedBaseModel):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.BigInteger, db.ForeignKey('users.user_id', ondelete="CASCADE"))
    login = db.Column(db.String)
    password = db.Column(db.String)
    token = db.Column(db.String)
    period_update = db.Column(db.Integer)
    data_display = db.Column(db.JSON, nullable=True)
    last_billing = db.Column(db.DateTime(True), server_default=func.now())
    last_update_billing = db.Column(db.DateTime(True), server_default=func.now())
    update_billing = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    correct = db.Column(db.Boolean, default=True)
