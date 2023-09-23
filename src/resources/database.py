from tinydb import TinyDB, Query

db = TinyDB("database.json")


def get_all_messages(group: str):
    table = db.table(group)

    return table.all()