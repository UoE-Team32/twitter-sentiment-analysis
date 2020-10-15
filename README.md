# Twitter Sentiment Analysis

This is a Django Web App that was created in 3 days for an induction to Computer Science at Essex University. This means obviously this will be a tad rough around the edges in some places... 😅

It showcases:

- Django
- Natural Language Processing
- Google Maps API
- Map Quest Geocoding API
- Vue, ChartJS

It allows users to get an idea of the Sentiment of a certain topic and/or phrase that they enter using charts. It also allows users to easily access twitter's location data to know where people are located that are discussing a given topic using the Google Maps API.

## Deployment

### Tests

```bash
$ python3 mange.py test
...
----------------------------------------------------------------------
Ran x tests in w.xyzs
```

### Standalone

```bash
$ cp utils/.env_template utils/.env
...
$ pip3 install -r requirements.txt
...
$ python3 manage.py migrate
...
$ python3 manage.py runserver
...
```

### Docker

```bash
$ cp utils/.env_template utils/.env
...
$ docker-compose up -d
...
```

## API

### Search for a term and receive the sentiment

```bash
GET /app/piechart/?q=<QUERY>&maxResults=<MAX_RESULTS>
```

### Search for a term and receive the sentiment and location

```bash
GET /app/piechart/?q=<QUERY>&maxResults=<MAX_RESULTS>&locationRequired
```
