#!/usr/bin/env python3
import pushshift
from datetime import datetime
from typing import List
import argparse


def gather(
        subreddit: str,
        start_time: datetime, end_time: datetime,
        **params) -> List[dict]:
    return list(map(
        lambda d: {k: v for k, v in d.items() if k in [
            'created_utc',
            'num_comments',
            'score',
            'author'
        ]},
        pushshift.get_submissions(
            {
                'subreddit': subreddit,
                'after': str(int(start_time.timestamp())),
                'before': str(int(end_time.timestamp())),
                **params
            })
    ))


def filter_value(lst, key, value, keep=True):
    return list(filter(
        lambda d: (d[key] == value) == keep,
        lst
    ))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=''.join((
        "Garther interaction data from posts of a certain ",
        "subreddit, from a certain interval. ",
        "Dates/times in ISO format.")))
    parser.add_argument(
        'subreddit',
        type=str
    )
    parser.add_argument(
        'start_date',
        type=str
    ),
    parser.add_argument(
        'end_date',
        type=str
    )
    parser.add_argument(
        '-a', '--author',
        required=False,
        type=str,
        help='!{name} to exclude instead of include'
    )
    args = parser.parse_args()

    posts = gather(
        'SimDemocracy',
        datetime.fromisoformat(args.start_date),
        datetime.fromisoformat(args.end_date)
    )
    if args.author:
        posts = filter_value(
            posts,
            'author',
            (args.author
             if not args.author[0] == '!'
             else args.author[1:]),
            keep=args.author[0] != '!'
        )
    print('created_utc,author,comments,score')
    for post in posts:
        row = ''
        row += str(post['created_utc'])
        row += ','
        row += str(post['author'])
        row += ','
        row += str(post['num_comments'])
        row += ','
        row += str(post['score'])
        print(row)
