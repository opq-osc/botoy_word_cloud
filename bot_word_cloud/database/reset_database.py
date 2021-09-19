from botoy import logger

from ._shared import tmpDB


def reset_database():
    logger.warning('重置词云数据库')
    tmpDB.drop_table("wordcloud")
