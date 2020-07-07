#!/usr/bin/env python3
import pandas as pd
from sys import stdout, stdin
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Removes a column from CSV, by name"
    )
    parser.add_argument(
        'col',
        type=str,
        help='Column to remove'
    )
    parser.add_argument(
        '-i', '--input-file',
        type=open,
        default=stdin,
        help='File to read, else STDIN'
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input_file)
    df = df.drop(args.col, axis=1)
    df.to_csv(stdout,index=False)

