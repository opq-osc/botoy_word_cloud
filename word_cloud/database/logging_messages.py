from botoy import contrib
from botoy import logger
from tinydb import where
from tinyrecord import transaction

from ._shared import word_table


@contrib.to_async
def log_words(groupid, bot_qq, words: list):
    """
    记录jieba处理后的关键词
    :return:
    """
    with transaction(word_table) as tr:
        with tr.lock:
            if data_tmp := word_table.get(where("group") == groupid):  # 如果有数据
                tr.update(
                    {"words": (data_tmp["words"] + words)},
                    where("group") == groupid
                )
            else:  # 没数据
                logger.info(f'词云: 首次记录{groupid}')
                tr.insert(
                    {"group": groupid, "bot_qq": bot_qq, "words": words}
                )
