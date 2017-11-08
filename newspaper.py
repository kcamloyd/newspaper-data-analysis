#!/usr/bin/env python3
import psycopg2
from http.server import HTTPServer, BaseHTTPRequestHandler

root_page = '''<!DOCTYPE html>
    <title>Newspaper Analytics Report</title>
    <form method="GET">
        <button type="submit">Generate Report</button>
    </form>
      <pre>
          {}
      </pre>'''

DBNAME = "news"

def get_pop_articles():
    db = psycopg2.connect(database=DBNAME)
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
    db = psycopg2.connect(database=DBNAME)
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
    db = psycopg2.connect(database=DBNAME)
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

def get_report():
    art = get_pop_articles()
    auth = get_pop_authors()
    err = get_error_days()
    final = '''<h2>Most Popular Articles</h2>
        <ol>
            <li>{} -- {} views</li>
            <li>{} -- {} views</li>
            <li>{} -- {} views</li>
        </ol>
        <h2>Most Popular Authors</h2>
        <ol>
            <li>{} -- {} views</li>
            <li>{} -- {} views</li>
            <li>{} -- {} views</li>
            <li>{} -- {} views</li>
        </ol>
        <h2>Days With More Than 1% Error Rate</h2>
        <ol>
            <li>{} -- {}% errors</li>
        </ol>
        '''.format(art[0][0], art[0][1], art[1][0], art[1][1],
            art[2][0], art[2][1], auth[0][0], auth[0][1],
            auth[1][0], auth[1][1], auth[2][0], auth[2][1],
            auth[3][0], auth[3][1], err[0][0], err[0][1])
    return final

class ReportGenerator(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        report = root_page.format(get_report())
        self.wfile.write(report.encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, ReportGenerator)
    httpd.serve_forever()
