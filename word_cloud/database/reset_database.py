from botoy import logger, contrib
from tinyrecord import transaction

from ._shared import wordDB, word_table


@contrib.to_async
def reset_database():
    with transaction(word_table) as tr:
        with tr.lock:
            logger.warning('重置词云数据库')
            wordDB.drop_table("wordcloud")
