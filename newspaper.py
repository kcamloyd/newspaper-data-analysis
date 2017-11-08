#!/usr/bin/env python3
import psychopg2

DBNAME = "news"

def get_pop_articles():
    db = psychopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        '''select articles.title, views from articles,
        (select path, count(*) as views from log
        group by path
        order by views desc) as pathviews
        where pathviews.path like '%'||articles.slug
        order by views desc
        limit 3;''')
    articles = c.fetchall()
    db.close()
    return articles

def get_pop_authors():
    db = psychopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        '''select name, sum(views) from authors, articles,
        (select articles.title, views from articles,
        (select path, count(*) as views from log
        group by path
        order by views desc) as pathviews
        where pathviews.path like '%'||articles.slug
        order by views desc) as titleviews
        where articles.author = authors.id
        group by name
        order by sum desc;''')
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
