import sys
from loguru import logger

# < main logger init>
logger.remove()

LoggerLevel = "DEBUG"

logger.add("pysim.log",
    rotation = "500 MB",
    compression = "zip",
    backtrace = True,
    diagnose = True,
    level=LoggerLevel,
    format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

logger.add(sys.stdout,
    backtrace = True,
    diagnose = True,
    level=LoggerLevel,
    format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")


log = logger

# < END >