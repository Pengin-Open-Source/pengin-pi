import logging
from flask import request

# config logfile path
log_file = "./logfile.log"
log_level = logging.DEBUG
logging.basicConfig(level=log_level, filename=log_file, filemode="w+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")



class ContextLogger(logging.Logger):
    def log(self, level, msg, *args, **kwargs):
        if "extra" not in kwargs:
            user_ip = request.remote_addr
            user_id = request.headers.get("User-Id") or request.headers.get("Session-Id")
            kwargs["extra"] = {"user_ip": user_ip, "user_id": user_id}
        super().log(level, msg, *args, **kwargs)
logging.setLoggerClass(ContextLogger)


class ContextFilter(logging.Filter):
    def filter(self, record):
        record.user_ip = request.remote_addr
        record.user_id = request.headers.get("User-Id") or request.headers.get("Session-Id")
        return True
logger = logging.getLogger("baker_logger")
logger.addFilter(ContextFilter())

