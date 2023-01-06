from flask_sqlalchemy import SQLAlchemy
import os

# from app.util.log import log
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self, db=SQLAlchemy(), conn=os.getenv('SQLALCHEMY_DATABASE_URI'), **kwargs ):
        self.db = db
        #use kwargs to send k/v from
        self.config = {'SQLALCHEMY_DATABASE_URI': conn}
        self.config.update({'SQLALCHEMY_TRACK_MODIFICATIONS': True})
        if kwargs:
            self.config.update(kwargs)     


database = Config()

