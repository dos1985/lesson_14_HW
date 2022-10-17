import sqlite3
import flask

def get_value_from_db(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(sql).fetchall()
        return result


def search_by_title(title):
    sql = f"""select * 
             from netflix
             where title = '{title}'
             and release_year =
             """
    result = get_value_from_db(sql)
    for item in result:
        return dict(result)