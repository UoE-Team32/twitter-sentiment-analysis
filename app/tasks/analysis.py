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


def analyse_polarity_text(text: str, geo: str) -> Tweet:
    # Analyse the tweet
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        logger.debug('Tweet: ' + text + ', Polarity: Positive')
        return Tweet(polarity=Polarity.POSITIVE, text=text, country=geo)
    elif analysis.sentiment.polarity == 0:
        logger.debug('Tweet: ' + text + ', Polarity: Neutral')
        return Tweet(polarity=Polarity.NEUTRAL, text=text, country=geo)
    else:
        print('Tweet: ' + text + ', Polarity: Negative' + ", Country: " + str(geo))
        return Tweet(polarity=Polarity.NEGATIVE, text=text, country=geo)
