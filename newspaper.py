#!/usr/bin/env python3
import psycopg2


def get_result_table(query):
    db = psycopg2.connect(database='news')
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


def get_pop_articles():
    articles = get_result_table(
        '''select articles.title, views from articles,
        (select path, count(*) as views from log
        group by path
        order by views desc) as pathviews
        where pathviews.path like '%'||articles.slug
        order by views desc
        limit 3;''')


def get_pop_authors():
    authors = get_result_table(
        '''select name, sum(views) from authors,
        (select articles.title, articles.author, views
        from articles,
        (select path, count(*) as views from log
        group by path
        order by views desc) as pathviews
        where pathviews.path like '%'||articles.slug
        order by views desc) as titleviews
        where titleviews.author = authors.id
        group by name
        order by sum desc;''')


def get_error_days():
    days = get_result_table(
        '''select to_char(daily_errors.date, 'FMMonth FMDD, YYYY') as date,
        round(daily_errors.sum / daily_logs.count * 100, 1) as percent
        from (select date(time) as date, count(*)::decimal as sum
        from log
        where status like '4%'
        group by date(time)) as daily_errors,
        (select date(time) as date, count(id)
        from log
        group by date(time)) as daily_logs
        where daily_errors.date = daily_logs.date
        and round(daily_errors.sum / daily_logs.count * 100, 1) > 1
        order by daily_errors.date;''')


def get_report():
    art = get_pop_articles()
    auth = get_pop_authors()
    err = get_error_days()
    print("Top 3 Articles")
    for ar in art:
        print("- {} -- {} views".format(ar[0], ar[1]))
    print("\nMost Popular Authors")
    for au in auth:
        print("- {} -- {} views".format(au[0], au[1]))
    print("\nDays With More Than 1% Error Rate")
    for e in err:
        print("- {} -- {}% errors".format(e[0], e[1]))

get_report()
