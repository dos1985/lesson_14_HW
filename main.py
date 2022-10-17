import json
import sqlite3
from flask import Flask

app = Flask(__name__)


def get_value_from_db(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(sql).fetchall()
        return result


def search_by_title(title):
    sql = f"""select * 
            from netflix
            where title = '#Roxy'
            order by release_year desc
            
    """
    result = get_value_from_db(sql)
    for item in result:
        return dict(item)


@app.get("/movie/<title>")
def search_by_title_view(title):
    result = search_by_title(title=title)
    return app.response_class(
        response=json.dump(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"

    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
