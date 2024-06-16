from botoy import contrib
from botoy import logger
from tinydb import where
from tinyrecord import transaction

from ._shared import word_table

# 用于累积操作的列表
batch_operations = []

@contrib.to_async
def log_words(groupid, bot_qq, words: list):
    """
    记录jieba处理后的关键词
    :return:
    """
    global batch_operations

    # 准备批量操作
    batch_operations.append((groupid, bot_qq, words))

    # 每次处理完毕后，检查是否需要提交事务（例如，每累积10次操作提交一次）
    if len(batch_operations) >= 10:
        with transaction(word_table) as tr:
            with tr.lock:
                for op in batch_operations:
                    groupid, bot_qq, words = op
                    data_tmp = word_table.get(where("group") == groupid)

                    if data_tmp:  # 如果有数据
                        tr.update(
                            {"words": data_tmp["words"] + words},
                            where("group") == groupid
                        )
                    else:  # 没数据
                        logger.info(f'词云: 首次记录{groupid}')
                        tr.insert(
                            {"group": groupid, "bot_qq": bot_qq, "words": words}
                        )

        # 提交后重置操作列表，准备下一轮批量操作
        batch_operations = []
