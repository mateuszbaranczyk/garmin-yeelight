import logging


logging.basicConfig(
    filename="bulbs",
    filemode="a",
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)

file_logger = logging.getLogger("Bulbs")
