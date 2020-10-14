from textblob import TextBlob
from collections import namedtuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Polarity(Enum):
    POSITIVE = 1
    NEUTRAL = 2
    NEGATIVE = 3


Tweet = namedtuple('Tweet', 'polarity, text, country')


def analyse_polarity_text(text: str, geo: object, usr: object) -> Tweet:
    # Analyse the tweet
    analysis = TextBlob(text)
    if geo:
        geo = geo.__dict__
        geo.pop('_api')
        geo['bounding_box'] = geo['bounding_box'].__dict__ if geo['bounding_box'] is not None else None
        geo['bounding_box'].pop('_api')

    if analysis.sentiment.polarity > 0:
        logger.debug('Tweet: ' + text + ', Polarity: Positive')
        return Tweet(polarity=Polarity.POSITIVE, text=text, country=geo)
    elif analysis.sentiment.polarity == 0:
        logger.debug('Tweet: ' + text + ', Polarity: Neutral')
        return Tweet(polarity=Polarity.NEUTRAL, text=text, country=geo)
    else:
        print('Tweet: ' + text + ', Polarity: Negative' + ', Country: ' + str(geo))
        return Tweet(polarity=Polarity.NEGATIVE, text=text, country=geo)
