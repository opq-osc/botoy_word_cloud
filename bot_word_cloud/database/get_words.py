from tinydb import where

from ._shared import word_table


def get_words(groupid) -> list:
    if data_tmp := word_table.get(where("group") == groupid):  # 如果有数据
        return data_tmp["words"]
    return ['无数据']
