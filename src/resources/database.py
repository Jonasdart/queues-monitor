from operator import contains
from tinydb import TinyDB, Query

db = TinyDB("database.json")


def get_all_messages(group: str, field: str = None, filter: str = None):
    table = db.table(group)
    if filter:
        return table.search(Query()[field] == filter)

    return table.all()
