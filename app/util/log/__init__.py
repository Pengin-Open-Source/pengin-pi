from app.util.log.config import logger

def log():
    """Logging Wrapper
    
    By: Stuart Anderson
    Copyright: Tobu Pengin, LLC. 2022
    """
    def pre(func):
        """ Pre function logging """
        logger.debug("Entered %s", func.__name__)	
    
    def post(func):
        """Post function logging"""
        logger.debug("Exited  %s", func.__name__)
        
    
    def decorate(func):
        """Decorator"""
        def call(*args, **kwargs):
            """Actual wrapping"""
            pre(func)
            result = func(*args, **kwargs)
            post(func)
            return result
        return call
    return decorate
    
    
