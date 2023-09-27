from tinydb import TinyDB, Query
from functools import lru_cache

db = TinyDB("database.json")


@lru_cache(maxsize=128, typed=True)
def get_all_messages(group: str):
    table = db.table(group)
    print(group)
    return table.all()