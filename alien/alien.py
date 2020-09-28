#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import traceback
import random
import logging
from .utils import get_random_user_agent, get_fixed_subreddit
from .submissions import Submission, UserSubmissions, SubredditSubmissions
from .comments import Comment, UserComments, SubredditComments, SubmissionComments


class Alien:
    def __init__(self):
        pass  # TODO

    def get_subreddit_submissions(self, subreddit, max_items=100):
        subreddit = get_fixed_subreddit(subreddit)
        for submission in SubredditSubmissions(subreddit):
            try:
                yield submission
            except Exception:
                continue

    def get_subreddit_comments(self, subreddit, max_items=100):
        subreddit = get_fixed_subreddit(subreddit)
        for comment in SubredditComments(subreddit):
            try:
                yield comment
            except Exception:
                continue

    def get_subreddit_texts(self, subreddit):
        yield from self.get_subreddit_submissions(subreddit)
        yield from self.get_subreddit_comments(subreddit)

    def get_submissions(self):
        return self.get_subreddit_submissions('all')

    def get_comments(self):
        return self.get_subreddit_submissions('all')

    def get_texts(self):
        return self.get_subreddit_texts('all')

    def stream_subreddit_submissions(self, subreddit):
        while True:
            yield from self.get_subreddit_submissions(subreddit)

    def stream_subreddit_comments(self, subreddit):
        while True:
            yield from self.get_subreddit_comments(subreddit)

    def stream_subreddit(self, subreddit):
        while True:
            yield from self.get_subreddit_submissions(subreddit)
            yield from self.get_subreddit_comments(subreddit)

    def stream_submissions(self):
        return self.stream_subreddit_submissions('all')

    def stream_comments(self):
        return self.stream_subreddit_submissions('all')

    def stream(self):
        return self.stream_subreddit('all')

    def get_user_submissions(self, user):
        for submission in UserSubmissions(user):
            try:
                yield submission
            except Exception:
                continue

    def get_submission_comments(self, submission):
        for comment in SubmissionComments(submission):
            try:
                yield comment
            except Exception:
                continue

    def get_user_comments(self, user):
        for comment in UserComments(user):
            try:
                yield comment
            except Exception:
                continue

    def get_user_texts(self, user):
        yield from self.get_user_submissions(user)
        yield from self.get_user_comments(user)