from tinydb import where

from ._shared import wordDB


def get_words(groupid) -> list:
    if data_tmp := wordDB.table("wordcloud").get(where("group") == groupid):  # 如果有数据
        return data_tmp["words"]
    return ['无数据']
