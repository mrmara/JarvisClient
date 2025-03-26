
from src.jclient import jclient
import pprint
j = jclient()
last_diagnostic: dict = {}
logger = j.get_logger()
logger.info("Jarvis is initialized")
while True:
    if (j.spin() != last_diagnostic):
        last_diagnostic = j.spin()
        logger.debug("New diagnostic")
        logger.debug(pprint.pformat(last_diagnostic))
        