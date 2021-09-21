from botoy import logger
from tinydb import where
from tinyrecord import transaction

from ._shared import word_table


def get_words(groupid) -> dict:
    with transaction(word_table) as tr:
        with tr.lock:
            freq_dict = {}
            data_tmp = word_table.get(where("group") == groupid)  # 如果有数据
    if data_tmp:
        for k in set(data_tmp["words"]):
            # if not k.isprintable():
            #     continue
            freq_dict[k] = data_tmp["words"].count(k)
        dict_finish = dict(sorted(freq_dict.items(), key=lambda d: d[1], reverse=True)[:85])
        logger.success(dict_finish)
        return dict_finish  # 按照value从大到小排序
    return {'无': 1}
