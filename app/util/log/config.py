import logging

# config logfile path
log_file = "./logfile.log"
log_level = logging.DEBUG
logging.basicConfig(level=log_level, filename=log_file, filemode="w+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger("baker_logger")
