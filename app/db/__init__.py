print("init db")

from app.db.config import db
import app.db.models as models

print("db done")

print(db.Model.__getattribute__)