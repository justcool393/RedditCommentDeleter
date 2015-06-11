import praw

# Requests' exceptions live in .exceptions and are called errors.
from requests.exceptions import ConnectionError, HTTPError
# Praw's exceptions live in .errors and are called exceptions.
from praw.errors import APIException, ClientException, RateLimitExceeded

PRINT_AT = 50

RECOVERABLE_ERROR = (APIException, HTTPError, ConnectionError,
                     ClientException, RateLimitExceeded)

r = praw.Reddit("Comment remover (/u/justcool393)")
r.login()
print("Logged in")

count = 0
me = r.user
after = ""
more = True

while more:
    comments = list(me.get_comments(limit=None, after_field=after))
    more = len(comments) > 1
    for comment in comments:
        try:
            comment.edit("deleted")
            count += 1
        except RECOVERABLE_ERROR as e:
            print("Error deleting comment ("
                  "http://www.reddit.com/api?info?id=" + comment.name + ")")
            print(str(e))
        after = comment.name
        if count % PRINT_AT == 0:
            print("Edited " + str(count) + " comments...")
print("Finished. Was able to delete " + str(count) + " comments.")
input()