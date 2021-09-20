# from tinydb.storages import MemoryStorage
from pathlib import Path

from tinydb import TinyDB

curFileDir = Path(__file__).parent

# wordDB = TinyDB(storage=MemoryStorage)
wordDB = TinyDB(curFileDir / "DB" / "words.json", indent=4, encoding='utf-8')

word_table = wordDB.table("wordcloud")
