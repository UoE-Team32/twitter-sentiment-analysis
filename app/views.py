from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from utils.twitter import Twitter, tweepy
from app.tasks.analysis import analyse_polarity_text, Polarity
from app.tasks.geolocation import get_coords_location
import logging

import environ

# Load .env file and associated vars
env = environ.Env()
GMAPS_API_KEY = env.str("GOOGLE_MAPS_API_KEY")

logger = logging.getLogger(__name__)


def index(request):
    return render(request, "index.html", context={"title": "Sentiment Analysis"})


def map(request):
    return render(
        request,
        "map.html",
        context={"title": "Sentiment by Country", "GMAPS_API_KEY": GMAPS_API_KEY},
    )


class AnalysisEndpointMixin(View):
    def __init__(self):
        self.twitter = Twitter()
        self.search_query = ""
        self.maxResults = 0

    def get_default_url_params(self, request):
        try:
            self.search_query = request.GET["q"]
            self.maxResults = int(request.GET["maxResults"])
        except Exception as e:
            return JsonResponse(
                {"error": "Param/s of %s are required." % str(e)}, status=404
            )


class WorldAnalysisEndpoint(AnalysisEndpointMixin):
    def get_geo_location_id(self, country: str):
        places = self.twitter.api.geo_search(query=country, granularity="country")
        if len(places) > 0:
            return places[0].id
        else:
            return 0

    def get(self, request, *args, **kwargs):
        place_id = self.get_geo_location_id(request.GET["countrycode"])
        tweets = self.twitter.api.search(q="place:%s" % place_id)
        countries = {}
        for tweet in tweets:
            logger.info(
                tweet.text + " | " + tweet.place.name
                if tweet.place
                else "Undefined place"
            )
            if tweet.place.country_code in countries.keys():
                countries[tweet.place.country_code] += 1
            else:
                countries[tweet.place.country_code] = 1

        return JsonResponse(countries)


class ChartAnalysisEndpoint(AnalysisEndpointMixin):
    def get(self, request, *args, **kwargs):
        """
        Endpoint to produce a json representation of
        a Pie Chart given the correct query params

        Endpoint requires a param of "q" & "maxResults"
        escaped characters are supported.
        """

        all_tweets = []
        positive_tweets = []
        netural_tweets = []
        negative_tweets = []

        error = self.get_default_url_params(request)

        if error:
            return error

        location_required = True if "locationRequired" in request.GET else False

        logger.info("Searching Twitter for... ", self.search_query)

        for tweet_object in tweepy.Cursor(
            self.twitter.api.search,
            q=self.search_query + " -filter:retweets",
            lang="en",
            result_type="recent",
        ).items(self.maxResults):
            if tweet_object.place is None and location_required is True:
                if tweet_object.user.location != "":
                    coords = get_coords_location([tweet_object.user.location])
                    if not coords:
                        continue
                else:
                    continue
            elif location_required:
                if tweet_object.user.location != "":
                    coords = get_coords_location([tweet_object.user.location])
                    if not coords:
                        continue
                else:
                    continue
            else:
                coords = []

            logger.debug(coords)
            all_tweets.append(tweet_object.text)
            tweet = analyse_polarity_text(
                tweet_object.text, tweet_object.place, tweet_object.user, coords
            )
            if tweet.polarity == Polarity.POSITIVE:
                positive_tweets.append(
                    {
                        "text": tweet.text,
                        "location": tweet.country,
                        "coordinates": tweet.coords,
                    }
                )
            elif tweet.polarity == Polarity.NEUTRAL:
                netural_tweets.append(
                    {
                        "text": tweet.text,
                        "location": tweet.country,
                        "coordinates": tweet.coords,
                    }
                )
            elif tweet.polarity == Polarity.NEGATIVE:
                negative_tweets.append(
                    {
                        "text": tweet.text,
                        "location": tweet.country,
                        "coordinates": tweet.coords,
                    }
                )
        # using a percentage multiplier variable to save doing multiple calculations
        if len(all_tweets) > 0:
            percentage_multiplier = 100 / len(all_tweets)
        else:
            percentage_multiplier = 0

        return JsonResponse(
            {
                "results": len(all_tweets),
                "positive": {
                    "number": len(positive_tweets),
                    "details": positive_tweets,
                    "percentage": len(positive_tweets) * percentage_multiplier,
                },
                "netural": {
                    "number": len(netural_tweets),
                    "details": netural_tweets,
                    "percentage": len(netural_tweets) * percentage_multiplier,
                },
                "negative": {
                    "number": len(negative_tweets),
                    "details": negative_tweets,
                    "percentage": len(negative_tweets) * percentage_multiplier,
                },
            }
        )
