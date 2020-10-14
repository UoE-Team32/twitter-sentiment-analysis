# Twitter Sentiment Analysis

## Deployment
### Standalone
```bash
$ pip3 install -r requirements.txt
$ python3 manage.py migrate
$ python3 manage.py runserver
```

### Docker
```bash
$ docker-compose up -d
```

## API
### Search for a term and receive the sentiment

```bash
GET http://localhost:8000/app/piechart/?q=<QUERY>&maxResults=<MAX_RESULTS>
```
