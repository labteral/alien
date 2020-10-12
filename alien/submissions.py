from datetime import timezone
from .utils import (get_element_id, get_lxml_from_response, get_request, get_fixed_subreddit,
                    IterableResults, return_on_error)
import dateutil.parser
import logging
from urllib.request import urlopen


class Submission:
    def __init__(self, element, subreddit=None):
        self.element = element
        self._subreddit = subreddit

    @property
    @return_on_error
    def title(self) -> str:
        return self.element.xpath("." + "/div[@class='entry unvoted']" + "/p[@class='title']" +
                                  "/a[@class='may-blank']" +
                                  "/text()")[0].encode('utf-8').decode('utf-8')

    @property
    @return_on_error
    def id(self) -> str:
        return get_element_id(self.element)

    @property
    @return_on_error
    def submission_id(self) -> str:
        return self.id

    @property
    @return_on_error
    def subreddit(self) -> str:
        # Works only with the submissions page of a given author
        if self._subreddit:
            return self._subreddit

        try:
            subreddit = self.element.xpath("." + "/div[@class='entry unvoted']" +
                                           "/div[@class='tagline']" + "/span" +
                                           "/a[contains(@class, 'subreddit')]/text()")[0]
            type, subreddit = subreddit.split('/')
            if type == 'r':
                return f'r/{subreddit}'
            # The text was posted to the user's profile (no subreddit)
            elif type == 'u':
                return f'u/{subreddit}'
        except IndexError:
            return

    @property
    @return_on_error
    def timestamp(self) -> int:
        retrieved_datetime = self.element.xpath("." + "/div[@class='entry unvoted']" +
                                                "/div[@class='tagline']" + "/span" +
                                                "/time/@datetime")[0]

        return int(dateutil.parser.parse(retrieved_datetime) \
            .replace(tzinfo=timezone.utc).timestamp())

    @property
    @return_on_error
    def author(self) -> str:
        try:
            return self.element.xpath(
                "." + "/div[@class='entry unvoted']" + "/div[@class='tagline']" + "/span" +
                "/a[contains(@class, 'author')]/text()")[0].encode('utf-8').decode('utf-8')
        # Post written by a deleted user
        except IndexError:
            return

    @property
    @return_on_error
    def comments_count(self) -> int:
        return int(
            self.element.xpath("." + "/div[@class='commentcount']" + "/a" +
                               "/text()")[0].encode('utf-8').decode('utf-8'))

    @property
    @return_on_error
    def score(self) -> int:
        return int(
            self.element.xpath("." + "/div[@class='entry unvoted']" + "/div[@class='tagline']" +
                               "/span" + "/span[@class='score unvoted']" + "/@title")[0])

    @property
    @return_on_error
    def body(self) -> str:
        words = " ".join(text for text in self.element.xpath("." + "/div[@class='expando']" +
                                                             "/form[@class='usertext']" +
                                                             "/div[@class='usertext-body']" +
                                                             "/div[@class='md']//text()")).split()
        return " ".join(words)

    @property
    @return_on_error
    def url(self) -> str:
        return f'https://www.reddit.com/{self.subreddit}/comments/{self.id}/'

    @property
    @return_on_error
    def profile_post(self) -> bool:
        split_subreddit = self.subreddit.split('_')
        return len(split_subreddit) > 1 and split_subreddit[1] == self.author

    @property
    def dict(self) -> str:
        return {
            'submission_id': self.id,
            'type': 'submission',
            'subreddit': self.subreddit,
            'title': self.title,
            'author': self.author,
            'timestamp': self.timestamp,
            'body': self.body,
            'url': self.url
        }


class UserSubmissions(IterableResults):
    def __init__(self, author, max_items=100):
        self.author = author
        self.max_items = max_items
        self.results = [Submission(element)
                        for element in self._get_user_submissions_elements()][::-1]

    def _get_user_submissions_elements(self):
        try:
            doc = self._get_user_submissions_lxml()
            return doc.xpath("//div[contains(@class, 'thing')]")
        except Exception as e:
            logging.error(str(e))
            return []

    def _get_user_submissions_lxml(self):
        response = urlopen(get_request(self._get_user_submissions_url()))
        return get_lxml_from_response(response)

    def _get_user_submissions_url(self):
        url = ('https://www.reddit.com/user/' + self.author + '/submitted/.compact?limit=' +
               str(self.max_items))
        return url


class SubredditSubmissions(IterableResults):
    def __init__(self, subreddit, max_items=100):
        self.subreddit = get_fixed_subreddit(subreddit)
        self.max_items = max_items
        self.results = [
            Submission(element, self.subreddit)
            for element in self._get_subreddit_submissions_elements()
        ][::-1]

    def _get_subreddit_submissions_elements(self):
        try:
            doc = self._get_subreddit_submissions_lxml()
            return doc.xpath("//div[contains(@class, 'thing')]")
        except Exception as e:
            logging.error(str(e))
            return []

    def _get_subreddit_submissions_lxml(self):
        response = urlopen(get_request(self._get_subreddit_submissions_url()))
        return get_lxml_from_response(response)

    def _get_subreddit_submissions_url(self, sort='new'):
        url = f'https://www.reddit.com/{self.subreddit}/{sort}/.compact?limit={self.max_items}'
        return url
