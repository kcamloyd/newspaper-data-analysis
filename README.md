Logs Analysis Project for Udacity Full Stack Web Developer Nanodegree
https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004
Supporting course: Intro to Relational Databases (ud197)
https://www.udacity.com/course/intro-to-relational-databases--ud197

Internal reporting tool for analyzing traffic to a newspaper website.

Uses PostgreSQL queries to pull data from a database containing 3 tables:
  1. articles (with information about each published article)
  2. authors (with information about each author)
  3. log (which logs every instance of a visitor viewing an article)

Returns a report to answer the following questions:
  1. What are the most popular three articles of all time?
  2. Who are the most popular article authors of all time?
  3. On which days did more than 1% of requests lead to errors?

Refer to sample_output.txt to see answers to the above questions.

To run newspaper.py:
Dependencies: Python3 interpreter, psycopg2 library, running PostgreSQL environment with "news" database (see further directions below).

Udacity uses a virtual machine that can be replicated by installing Virtual Box (https://www.virtualbox.org/) and Vagrant (https://www.vagrantup.com/).
Dependencies can also be installed locally.

newsdata.sql can be downloaded here - https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
(not included on GitHub due to large file size).

Once downloaded, newsdata.sql should be placed in the vagrant or working directory.
If using vagrant, run "vagrant ssh" in command line to connect to the server.
cd into working directory, then run "psql -d news -f newsdata.sql" in command line to create tables in the news database.

Run python code in command line using "python3 newspaper.py" or "./newspaper.py"
