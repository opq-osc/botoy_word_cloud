from tinyrecord import transaction

from ._shared import word_table


def get_all_groups() -> dict:
    with transaction(word_table) as tr:
        with tr.lock:
            return {data['group']: data["bot_qq"] for data in word_table.all()}
