# Portal 2 Workshop Authors Rankings
A single page web app that shows Portal 2 Workshop authors rankings. The rankings can be sorted by the number of followers or map submissions. Very useful for those who play Portal 2 custom maps.

The backend is built with Django 3.2 and uses the Steam API and BeautifulSoup to collect authors' data from several Steam groups related to Portal 2 custom map development. The collected data is stored in a sqlite database and is updated every 24 hours by using the django-crontab package.

Bootstrap and [Bootstrap Table](https://bootstrap-table.com/) are used for frontend.