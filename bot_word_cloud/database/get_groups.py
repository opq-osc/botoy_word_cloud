from tinydb import where

from ._shared import tmpDB


def get_all_groups() -> list:
    return [data['group'] for data in tmpDB.table("wordcloud").all()]
