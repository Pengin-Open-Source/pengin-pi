from math import ceil
from sqlalchemy import desc
    

def paginate(Model:object, page:int, **kwargs)->list:
    """Paginate Method
    This paginate method takes a SQLAlchemy model, a page number,
    and keywords: order, pages, key, filters. The output is a possible paginated list of SQL data or an empty list.
    
    Required Inputs:
        Model: SQLAlchemy ORM class
        page: int  the page number to be retrieved
    
    Optional Keywords:
        order=desc or asc (descending or ascending, from sqlalchemy)
        pages=int  the per_page attribute for a query, number of items per page
        key=str   Model attribute to look for IE: 'id','name', or 'date'  
        filters=dict    dictionary of filtering conditions
    
    Outputs:
        Your paginated SQL query data...hopefully.
    """
    if page < 1:
        page = 1
    pages = kwargs.get('pages', 10)
    order = kwargs.get('order', desc)
    filters = kwargs.get("filters", {})
    key = kwargs.get('key', 'id')
    try:
        query = Model.query
        if filters:
            query = Model.query.filter_by(**filters)

        if key:
            order_attr = getattr(Model, key)
            query = query.order_by(order(order_attr))
        return query.paginate(page=page, per_page=pages)
    except Exception as e:
        count = Model.query.count()
        end = ceil(count/pages)
        return query.paginate(page=end, per_page=pages)