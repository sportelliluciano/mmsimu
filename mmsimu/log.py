import logging


logging.basicConfig(format="%(message)s")
logger = logging.getLogger("mmsimu")


def alloc(message):
    logger.getChild("alloc").info(message)


def uninit(message):
    logger.getChild("uninit").info(message)
