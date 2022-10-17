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


@app.get("/movie/<title>/")
def search_by_title_view(title):
    result = search_by_title(title=title)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"

    )


@app.get("/movie/<year1>/to/<year2>/")
def search_by_date_view(year1, year2):
    sql = f"""select title, release_year
             from netflix
             where release_year between '{year1}' and '{year2}'
             limit 100
         """

    result = []

    for item in get_value_from_db(sql=sql):
        result.append(dict(item))
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


@app.get("/rating/<rating>/")
def search_by_rating_view(rating):
    my_dict = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }

    sql = f"""
    select title, rating, description
    from netflix
    where rating in {my_dict.get(rating, ("R", "R"))} 
"""

    result = []

    for item in get_value_from_db(sql=sql):
        result.append(dict(item))
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
