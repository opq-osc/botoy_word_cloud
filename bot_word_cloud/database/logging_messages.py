from botoy import logger
from tinydb import where

from ._shared import wordDB
from botoy.contrib import to_async


@to_async
def log_words(groupid, words: list):
    """
    记录jieba处理后的关键词
    :return:
    """
    if data_tmp := wordDB.table("wordcloud").get(where("group") == groupid):  # 如果有数据
        wordDB.table("wordcloud").update(
            {"words": (data_tmp["words"] + words)},
            where("group") == groupid
        )
    else:  # 没数据
        logger.info(f'词云: 首次记录{groupid}')
        wordDB.table("wordcloud").insert(
            {"group": groupid, "words": words}
        )
