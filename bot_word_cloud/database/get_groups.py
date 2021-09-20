from ._shared import word_table


def get_all_groups() -> list:
    return [data['group'] for data in word_table.all()]
