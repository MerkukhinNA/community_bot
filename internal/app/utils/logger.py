import logging, sys
from aio_pika import IncomingMessage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s -> %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def log_data_received(name: str, msg: IncomingMessage) -> None:
    msg = msg.body.decode()
    logger.info(f'\n\n{name}  |  Полученный msg.body  |  {msg}  |  {type(msg)}\n\n')
    
def log_data_sent(name: str, body: any) -> None:
    body = str(body.model_dump())
    logger.info(f'\n\n{name} |  Отправленный body  |  {body}  |  {type(body)}\n\n')
