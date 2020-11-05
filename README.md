<p align="center">
<img src="misc/alien.svg" alt="Ernie Logo" width="150"/></a>
</p>

<p align="center">
    <a href="https://pepy.tech/project/alien/"><img alt="Downloads" src="https://img.shields.io/badge/dynamic/json?style=flat-square&maxAge=3600&label=downloads&query=$.total_downloads&url=https://api.pepy.tech/api/projects/alien"></a>
    <a href="https://pypi.python.org/pypi/alien/"><img alt="PyPi" src="https://img.shields.io/pypi/v/alien.svg?style=flat-square"></a>
    <!--<a href="https://github.com/labteral/alien/releases"><img alt="GitHub releases" src="https://img.shields.io/github/release/labteral/alien.svg?style=flat-square"></a>-->
    <a href="https://github.com/labteral/alien/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/labteral/alien.svg?style=flat-square&color=green"></a>
</p>

<h3 align="center">
<b>Unofficial Python client for Reddit</b>
</h3>

<p align="center">
    <a href="https://www.buymeacoffee.com/brunneis" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="35px"></a>
</p>

# Installation
```bash
pip install alien
```

> The functionality of this library is limited on purpose so it respects the [`reddit.com/robots.txt`](https://www.reddit.com/robots.txt) rules.

# Instantiation
```python
from pygram import PyGram

alien = Alien()
```

# All posts

## Get new posts
```python
for post in alien.get_posts():
    print(post)
```

## Get subreddit's new posts
```python
for post in alien.get_subreddit_posts(subreddit):
    print(post)
```

## Get user's new posts
```python
for post in alien.get_user_posts(username):
    print(post)
```

# Submissions

## Get new submissions
```python
for post in alien.get_submissions():
    print(post)
```

## Get subreddit's new submissions
```python
for post in alien.get_subreddit_submissions(subreddit):
    print(post)
```

## Get user's new submissions
```python
for post in alien.get_user_submissions(username):
    print(post)
```

# Comments

## Get new comments
```python
for post in alien.get_comments():
    print(post)
```

## Get subreddit's new comments
```python
for post in alien.get_subreddit_comments(subreddit):
    print(post)
```

## Get submission's comments
```python
for post in alien.get_submission_comments(submission):
    print(post)
```

## Get user's new comments
```python
for post in alien.get_user_comments(username):
    print(post)
```
