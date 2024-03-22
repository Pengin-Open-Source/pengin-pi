from app.util.log.config import logger as _logger
from flask import request


def log(func):
    """Logging Wrapper
    By: Stuart Anderson
    Copyright: Tobu Pengin, LLC. 2023
    """
    def pre(func):
        """ Pre function logging """
        user_ip = request.remote_addr
        user_id = request.headers.get("User-Id") or request.headers.get("Session-Id")
        if user_ip and user_id:
            extra = {"user_ip": user_ip, "user_id": user_id}
            _logger.debug(f"Entered {func.__name__}", extra=extra)
        else:
            _logger.debug(f"Entered {func.__name__}")

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
