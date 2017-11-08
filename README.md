Logs Analysis Project for Udacity Full Stack Web Developer Nanodegree
https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004
Supporting course: Intro to Relational Databases (ud197)
https://www.udacity.com/course/intro-to-relational-databases--ud197

Python3 application for analyzing traffic to a newspaper website.

Uses PostgreSQL queries to pull data from a database containing 3 tables:
  1. articles (with information about each published article)
  2. authors (with information about each author)
  3. log (which logs every instance of a visitor viewing an article)

(Database file not included on GitHub due to large file size)

Returns a report to answer the following questions:
  1. What are the most popular three articles of all time?
  2. Who are the most popular article authors of all time?
  3. On which days did more than 1% of requests lead to errors?

Refer to sample_output.txt to see answers to the above questions.

newspaper.py is run via a Linux virtual machine connected to the news database.
