from math import ceil
from sqlalchemy import desc, asc

def paginate(Model:object, page:int, **kwargs)->list:
    """Paginate Method
    This paginate method takes a SQLAlchemy model, a page number,
    and keywords: order, pages and key.  The output is a possible paginated
    list of SQL data or an empty list.
    
    Required Inputs:
        Model: SQLAlchemy ORM class
        page: int  the page number to be retrieved
    
    Optional Keywords:
        order=desc or asc (descending or ascending, from sqlalchemy)
        pages=int  the per_page attribute for a query, number of items per page
        key=str   Model attribute to look for IE: 'id','name', or 'date'  
    
    Outputs:
        Your paginated SQL query data...hopefully.
    """
    if page < 1:
        page = 1
    pages = kwargs.get('pages', 10)
    order = kwargs.get('order', desc)
    key = kwargs.get('key', 'id')
    try:
        query = Model.query
        if key:
            order_attr = getattr(Model, key)
            query = query.order_by(order(order_attr))
        items = query.paginate(page=page, per_page=pages)
    except Exception as e:
        items = None
    if not items or not items.items:
        return []
    total_items = len(items.items) 
    total_pages = ceil(total_items/pages)
    if page > total_pages:
        page = total_pages
        items = query.paginate(page=total_pages, per_page=pages)
    return items