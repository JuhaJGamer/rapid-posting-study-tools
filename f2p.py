#!/usr/bin/env python3
from scipy.stats import f as fd
import numpy as np
from matplotlib import pyplot as plt
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(
        description="Convert f-value to p-value with plot"
    )
    parser.add_argument(
        'dfn',
        type=float,
        help='df_1 shape parameter'
    )
    parser.add_argument(
        'dfd',
        type=float,
        help='df_2 shape parameter'
    )
    parser.add_argument(
        'f',
        type=float,
        help='f-value'
    )
    args = parser.parse_args()
    fig, ax = plt.subplots(1,1)
    x = np.linspace(fd.ppf(0.01, args.dfn, args.dfd),
                    fd.ppf(0.99, args.dfn, args.dfd), 100)
    ax.plot(x, fd.pdf(x, args.dfn, args.dfd), 'k-', lw=2, label='F')
    px = x[np.logical_and(x >= args.f, x <= 100)]
    ax.fill_between(px, fd.pdf(px, args.dfn, args.dfd), color='red', alpha=1, lw=0)
    print(f"p = {1-fd.cdf(args.f, args.dfn, args.dfd)}")
    plt.grid(True)
    plt.title(f"F-distribution")

    plt.show()

