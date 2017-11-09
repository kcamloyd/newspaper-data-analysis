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
    return get_result_table(
        '''select articles.title, views from articles,
        (select path, count(*) as views from log
        group by path
        order by views desc) as pathviews
        where pathviews.path like '%'||articles.slug
        order by views desc
        limit 3;''')


def get_pop_authors():
    return get_result_table(
        '''select name, sum(views) as views from authors,
        (select articles.title, articles.author, views
        from articles,
        (select path, count(*) as views from log
        group by path
        order by views desc) as pathviews
        where pathviews.path like '%'||articles.slug
        order by views desc) as titleviews
        where titleviews.author = authors.id
        group by name
        order by views desc;''')


def get_error_days():
    return get_result_table(
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
    articles = get_pop_articles()
    authors = get_pop_authors()
    errors = get_error_days()
    print("Top 3 Articles")
    for title, views in articles:
        print("- {} -- {} views".format(title, views))
    print("\nMost Popular Authors")
    for name, views in authors:
        print("- {} -- {} views".format(name, views))
    print("\nDays With More Than 1% Error Rate")
    for date, percent in errors:
        print("- {} -- {}% errors".format(date, percent))


if __name__ == "__main__":
    get_report()
