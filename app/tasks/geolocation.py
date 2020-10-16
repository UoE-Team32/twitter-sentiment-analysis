import requests
import environ

from app.models import CachedGeoLocation

# Load .env file and associated vars
env = environ.Env()
API_KEY = env.str("MAPQUEST_API_KEY")


def check_cached_location(location_input: list):
    for location in location_input:
        location = location.lower()
        try:
            obj = CachedGeoLocation.objects.get(name=location)
            return [obj.lat, obj.lng]
        except Exception:
            return None


def get_coords_location(location_input: list):
    """
    get the coordinates of a location in EPSG4326 given a location string

    Parameters
    ----------
    country : str
        name of the place to search for

    Returns
    -------
    output : list
        list with coordinates as str if one result given else
        list with dictionaries of places with coordinates as str
    """
    url = "https://open.mapquestapi.com/geocoding/v1"
    valid_us_strings = ["usa", "us", "united states of america", "united states"]

    cached_location = check_cached_location(location_input)

    if cached_location:
        return cached_location

    if len(location_input) == 1:
        location_input = str(location_input[0])
        url += "/address?key=%s&location='%s'" % (API_KEY, location_input)
        print("GET " + url)
        try:
            response = requests.get(url).json()
            output = [
                response["results"][0]["locations"][0]["latLng"]["lat"],
                response["results"][0]["locations"][0]["latLng"]["lng"],
            ]
            if output == [39.78373, -100.445882]:
                if location_input.strip().lower() not in valid_us_strings:
                    return []
            cached_location = CachedGeoLocation(
                name=location_input.strip().lower(), lat=output[0], lng=output[1]
            )
            cached_location.save()
            return output
        except Exception as e:
            print("%s coords not found. ERROR:" % location_input[0], e)
    else:
        location_input_str = ""
        for country in location_input:
            location_input_str += "&location='%s'" % country
        url += "/batch?key=%s%s" % (API_KEY, location_input_str)
        print("GET " + url)
        try:
            response = requests.get(url).json()
            results = response["results"]
            output = []
            for location_name, result in zip(location_input, results):
                output.append(
                    {
                        location_name: [
                            result["locations"][0]["latLng"]["lat"],
                            result["locations"][0]["latLng"]["lng"],
                        ]
                    }
                )
            return output
        except Exception as e:
            print("%s coords not found. ERROR:" % location_input, e)
