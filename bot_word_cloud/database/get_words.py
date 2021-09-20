from tinydb import where
from tinyrecord import transaction

from ._shared import word_table


def get_words(groupid) -> list:
    with transaction(word_table) as tr:
        with tr.lock:
            if data_tmp := word_table.get(where("group") == groupid):  # 如果有数据
                return data_tmp["words"]
            return ['无数据']
