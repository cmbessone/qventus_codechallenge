import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Loggers específicos
logger = logging.getLogger("parts_api")
db_logger = logging.getLogger("parts_api.database")
service_logger = logging.getLogger("parts_api.service")
