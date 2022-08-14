import sqlite3


def write_scores(name, score):
    cur = bd.cursor()
    cur.execute("insert into RECORDS (name, score) values (?, ?)", (name, score))
    bd.commit()


def get_best():
    cur = bd.cursor()
    cur.execute("""
    SELECT name gamer, max(score) score from RECORDS
    GROUP by name
    ORDER by score DESC
    limit 3
    """)
    result = cur.fetchall()
    return result


bd = sqlite3.connect('2048.sqlite')

cur = bd.cursor()
cur.execute("""
create table if not exists RECORDS (
    name text,
    score integer   
)""")

cur.close()