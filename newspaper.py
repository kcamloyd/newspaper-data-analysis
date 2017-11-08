import psychopg2

DBNAME = "news"

def get_pop_articles():
    db = psychopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select ...")
    articles = c.fetchall()
    db.close()
    return articles

def get_pop_authors():
    db = psychopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select ...")
    authors = c.fetchall()
    db.close()
    return authors

def get_error_days():
    db = psychopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select ...")
    days = c.fetchall()
    db.close()
    return days
