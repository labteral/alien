from .utils import (get_timestamp_from_text, get_lxml_from_response, get_element_id, get_response,
                    get_fixed_subreddit, IterableResults, return_on_error)
import logging
import traceback


class Comment:
    def __init__(self, element):
        self.element = element

    @property
    @return_on_error
    def subreddit(self) -> str:
        return 'r/' + self.element.xpath("."
            + "/div[@class='entry unvoted']"
            + "/div[contains(@class, 'options_expando')]"
            + "/a"
            + "/@href")[1] \
            .split("/")[2]

    @property
    @return_on_error
    def submission_id(self) -> str:
        return self.element.xpath("."
            + "/div[@class='entry unvoted']"
            + "/div[contains(@class, 'options_expando')]"
            + "/a"
            + "/@href")[1] \
            .split("/")[4]

    @property
    @return_on_error
    def submission_title(self) -> str:
        return self.element.xpath("." +
                                  "/a[@class='title']/text()")[0].encode('utf-8').decode('utf-8')

    @property
    @return_on_error
    def body(self) -> str:
        words = " ".join(text for text in self.element.xpath("." + "/div[@class='entry unvoted']" +
                                                             "/form[@class='usertext']" +
                                                             "/div[@class='usertext-body']" +
                                                             "/div[@class='md']//text()")).split()
        return " ".join(words)

    @property
    @return_on_error
    def id(self) -> str:
        return get_element_id(self.element)

    @property
    @return_on_error
    def comment_id(self) -> str:
        return self.id

    @property
    @return_on_error
    def timestamp(self) -> int:
        time_ago = self.element.xpath("."
            + "/div[@class='entry unvoted']"
            + "/div[@class='tagline']"
            + "/text()[normalize-space()]")[0] \
            .replace("[score hidden]", "").strip()
        return get_timestamp_from_text(time_ago)

    @property
    @return_on_error
    def author(self) -> str:
        return self.element.xpath("." + "/div[@class='entry unvoted']" + "/div[@class='tagline']" +
                                  "/a[contains(@class, 'author')]/text()")[0].encode(
                                      'utf-8').decode('utf-8')

    @property
    @return_on_error
    def url(self) -> str:
        return 'https://reddit.com' + self.element.xpath(
            "." + "/div[@class='entry unvoted']" + "/div[@class='clear options_expando hidden']" +
            "/a" + "/@href")[1]

    @property
    @return_on_error
    def profile_post(self) -> bool:
        split_subreddit = self.subreddit.split('_')
        return len(split_subreddit) > 1 and split_subreddit[1] == self.author

    @property
    def dict(self) -> dict:
        return {
            'comment_id': self.id,
            'submission_id': self.submission_id,
            'submission_title': self.submission_title,
            'type': 'comment',
            'subreddit': self.subreddit,
            'author': self.author,
            'timestamp': self.timestamp,
            'body': self.body,
            'url': self.url
        }


class UserComments(IterableResults):
    def __init__(self, author, max_items=100):
        self.author = author
        self.max_items = max_items
        self.results = [Comment(element) for element in self._get_user_comments_elements()][::-1]

    def _get_user_comments_elements(self):
        try:
            doc = self._get_user_comments_lxml()
            return doc.xpath("//div[contains(@class, 'thing')]")
        except Exception:
            traceback.print_exc()
            return []

    def _get_user_comments_lxml(self):
        response = get_response('https://www.reddit.com/user/' + self.author +
                                '/comments/.compact?limit=' + str(self.max_items))
        return get_lxml_from_response(response)


class SubredditComments(IterableResults):
    def __init__(self, subreddit, max_items=100):
        self.subreddit = get_fixed_subreddit(subreddit)
        self.max_items = max_items
        self.results = [Comment(element)
                        for element in self._get_subreddit_comments_elements()][::-1]

    def _get_subreddit_comments_elements(self):
        try:
            doc = self._get_subreddit_comments_lxml()
            return doc.xpath("//div[contains(@class, 'thing')]")
        except Exception:
            traceback.print_exc()
            return []

    def _get_subreddit_comments_lxml(self):
        response = get_response(
            f'https://www.reddit.com/{self.subreddit}/comments/.compact?limit={self.max_items}')
        return get_lxml_from_response(response)


class SubmissionComments(IterableResults):
    def __init__(self, submission, max_items=100):
        self.submission = submission
        self.max_items = max_items
        elements = self._get_submission_comments_elements()
        self.results = [Comment(element) for element in elements][::-1]

    def _get_submission_comments_elements(self):
        try:
            doc = self._get_submission_lxml()
            return doc.xpath("//div[contains(@class, 'thing')]")
        except Exception:
            traceback.print_exc()
            return []

    def _get_submission_lxml(self):
        response = get_response('https://www.reddit.com/' + self.submission.subreddit +
                                '/comments/' + self.submission.id + '/.compact?limit=' +
                                str(self.max_items))
        return get_lxml_from_response(response)
