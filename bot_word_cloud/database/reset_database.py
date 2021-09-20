from botoy import logger

from ._shared import wordDB


def reset_database():
    logger.warning('重置词云数据库')
    wordDB.drop_table("wordcloud")
