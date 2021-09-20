from ._shared import wordDB


def get_all_groups() -> list:
    return [data['group'] for data in wordDB.table("wordcloud").all()]
