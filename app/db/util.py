from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import desc, asc

def paginate(Model, page, pages=10):
    # Query the database for a list of items
    items = Model.query.order_by(desc(Model.id)).all()

    # Create a pagination object with the query results
    pagination = Pagination(query=items, page=page, per_page=pages)

    # Return Pagination
    return pagination

def paginate_date(Model, page, pages=10):
    # Query the database for a list of items
    items = Model.query.order_by(desc(Model.date)).all()
    # Create a pagination object with the query results
    pagination = Pagination(query=items, page=page, per_page=pages)
    # Return Pagination
    return pagination


def order_by_date(Model, order='desc'):
    if order != 'desc':
        return Model.query.order_by(asc(Model.date)).all() 
    return Model.query.order_by(desc(Model.date)).all()