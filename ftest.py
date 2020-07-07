#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sys import stdin
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(
        description="F-test per column between two or more CSVS"
    )
    parser.add_argument(
        'file',
        type=open,
        nargs='+',
        help="File to read, two at minimum"
    )
    args = parser.parse_args()

    dfs = []
    for f in args.file:
        dfs.append(pd.read_csv(f))

    if len(dfs) < 2:
        print("ftest: Not enough data")
        exit(1)

    for i in range(dfs[0].shape[1]):
        cols = [
            df[df.columns.values[i]]
            for df
            in dfs
        ]

        print(f"TEST {i} for {len(cols)} columns")
        np_cols = map(lambda x: x.to_numpy(), cols)
        np_cols = list(np_cols)
        np_cols = np.array(np_cols)

        means = [
            np.mean(col)
            for col
            in np_cols
        ]
        for j in range(len(cols)):
            print(f"Mu_{{{j}}}: {means[j]}")
        mean = np.mean(means)
        print(f"Mu: {mean}")
        sizes = [ col.shape[0] for col in cols ]
        for j in range(len(cols)):
            print(f"n_{{{j}}}: {sizes[j]}")
        var_explained = []

        for j in range(len(cols)):
            var_explained.append(sizes[j]*pow(means[j]-mean,2)/(len(cols)-1))
        var_explained = sum(var_explained)
        print(f"Explained variance: {var_explained}")

        var_unexplained = []
        for j in range(len(cols)):
            var_unexplained_t = []
            for k in cols[j]:
                var_unexplained_t.append(
                    pow(k-means[j],2)/(sum(sizes)-len(cols))
                )
            var_unexplained.append(sum(var_unexplained_t))
        var_unexplained = sum(var_unexplained)
        print(f"Unaexplained variance: {var_unexplained}")
        print(f"F = {var_explained/var_unexplained}")
        print(f"Degrees of freedom: {len(cols)-1}, {sum(sizes)-len(cols)}")
