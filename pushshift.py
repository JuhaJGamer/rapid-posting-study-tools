import requests
import datetime

### PUSHSHIFT
## Simple pushshift library for python
## Super simple in fact
## So simple it's like 30 lines

def get_posts(post_type,params, limit=-1):
    comments = []
    last = int(datetime.datetime.now().timestamp())
    got = 0
    while True:
        req_params = {
                **params,
                'limit':1000,
                'before':last
                }
        req_headers = {
                'User-Agent':'Python requests - Redditstat.py'
                }
        res = requests.get(f'https://api.pushshift.io/reddit/{post_type}/search', params=req_params, headers=req_headers)
        res.raise_for_status()
        data = res.json()["data"]
        comments += data
        if len(data) < 1000 or (limit != -1 and got >= limit):
            return comments
        else:
            last = data[-1]["created_utc"]
            got += 1000

def get_comments(params,limit=-1):
    return get_posts('comment',params,limit=limit)

def get_submissions(params,limit=-1):
    return get_posts('submission',params,limit=limit)

def get_all(params,limit=-1):
    lst = sorted(get_comments(params,limit=limit) + get_submissions(params,limit=limit), key=lambda k: k["created_utc"])
    if limit < 0:
        return lst
    else:
        return lst[0:limit-1]
