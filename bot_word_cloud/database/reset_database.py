from ._shared import tmpDB
from botoy import logger


def reset_database():
    logger.warning('重置词云数据库')
    tmpDB.drop_table("wordcloud")
