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
    c.execute(
        '''select daily_errors.date,
        round(daily_errors.sum / daily_logs.count * 100, 1) as percent
        from (select to_char(time, 'FMMonth FMDD, YYYY') as date, sum(errors)
        from (select time, count(*) as errors from log
        where status like '4%' group by time) as error_list
        group by date
        order by date) as daily_errors,
        (select to_char(time, 'FMMonth FMDD, YYYY') as date, count(id)
        from log group by date order by date) as daily_logs
        where daily_errors.date = daily_logs.date and
        round(daily_errors.sum / daily_logs.count * 100, 1) > 1
        order by daily_errors.date''')
    days = c.fetchall()
    db.close()
    return days
