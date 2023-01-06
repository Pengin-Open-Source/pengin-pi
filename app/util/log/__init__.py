from app.util.log.config import logger as _logger


def log():
    """Logging Wrapper
    By: Stuart Anderson
    Copyright: Tobu Pengin, LLC. 2022
    """
    def pre(func):
        """ Pre function logging """
        _logger.debug("Entered %s", func.__name__)

    def post(func):
        """Post function logging"""
        _logger.debug("Exited  %s", func.__name__)

    def decorate(func):
        """Decorator"""
        def call(*args, **kwargs):
            """Log function call to be wrapped on target function
                logs entry, exit, and arguments of the target function
                Success Returns: func -> wrapped function
                Failure Returns: logger -> exception is logged
            """
            pre(func)
            result = func(*args, **kwargs)
            _logger.debug(str(result))
            post(func)
            try:
                return result
            except Exception as e:
                _logger.debug(str(e))
        return call
    return decorate
