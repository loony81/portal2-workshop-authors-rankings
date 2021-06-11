# Portal 2 Workshop Authors Rankings
A single page web app that lists the members of several Steam groups related to Portal 2 custom map development, such as ThinkingWithPortals Mapping, P2LC and others (but only those who have at least 5 followers). Authors are ranked by the number of followers by default, but can also be ranked by the number of submitted workshop items and the number of Portal 2 cooperative maps.

The backend is built with Django 3.2 and uses the Steam API and BeautifulSoup to collect authors' data. The collected data is stored in a PostgreSQL database and is updated once a week by using [APScheduler](https://apscheduler.readthedocs.io/en/3.0/). Bootstrap is used for frontend.
