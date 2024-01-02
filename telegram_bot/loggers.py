import logging

logging.basicConfig(level=logging.INFO)


def get_logger(name: str):
    logger = logging.getLogger(name)
    handler = logging.FileHandler('run.log')
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger
