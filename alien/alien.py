#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import traceback
import random
import logging
from .utils import get_random_user_agent, get_fixed_subreddit
from .submissions import Submission, UserSubmissions, SubredditSubmissions
from .comments import Comment, UserComments, SubredditComments, SubmissionComments

# TODO add instance parameters
# TODO avoid repeated items on stream methods


class Alien:
    def __init__(self):
        pass

    # All posts ################################################################
    def get_subreddit_posts(self, subreddit):
        yield from self.get_subreddit_submissions(subreddit)
        yield from self.get_subreddit_comments(subreddit)

    def get_posts(self):
        return self.get_subreddit_posts('all')

    def get_user_posts(self, user):
        yield from self.get_user_submissions(user)
        yield from self.get_user_comments(user)

    def stream_subreddit_posts(self, subreddit):
        while True:
            yield from self.get_subreddit_submissions(subreddit)
            yield from self.get_subreddit_comments(subreddit)

    def stream_posts(self):
        return self.stream_subreddit_posts('all')

    def stream_user_posts(self, user):
        while True:
            yield from self.get_user_posts(user)

    # Submissions ##############################################################
    def get_subreddit_submissions(self, subreddit, max_items=100):
        subreddit = get_fixed_subreddit(subreddit)
        for submission in SubredditSubmissions(subreddit):
            try:
                yield submission
            except Exception:
                continue

    def get_submissions(self):
        return self.get_subreddit_submissions('all')

    def get_user_submissions(self, user):
        for submission in UserSubmissions(user):
            try:
                yield submission
            except Exception:
                continue

    def stream_subreddit_submissions(self, subreddit):
        while True:
            yield from self.get_subreddit_submissions(subreddit)

    def stream_submissions(self):
        return self.stream_subreddit_submissions('all')

    def stream_user_submissions(self, user):
        while True:
            yield from self.get_user_submissions(user)

    # Comments #################################################################
    def get_subreddit_comments(self, subreddit, max_items=100):
        subreddit = get_fixed_subreddit(subreddit)
        for comment in SubredditComments(subreddit):
            try:
                yield comment
            except Exception:
                continue

    def get_comments(self):
        return self.get_subreddit_submissions('all')

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

    def stream_subreddit_comments(self, subreddit):
        while True:
            yield from self.get_subreddit_comments(subreddit)

    def stream_comments(self):
        return self.stream_subreddit_submissions('all')

    def stream_user_comments(self, user):
        while True:
            yield from self.get_user_comments(user)