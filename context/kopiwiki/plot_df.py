#!/usr/bin/env python
"""
Extract Wikipedia article-term count matrix from KOPI plain text dump.
"""
import logging
from extract import build
from numpy import arange
from sklearn.feature_extraction.text import _document_frequency

MAXES = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO) # DEBUG, INFO, WARN, ERROR, CRITICAL

def plot(X):
    N = X.shape[0]
    dfs = _document_frequency(X)
    dfs = dfs / float(N)
    for max_df in MAXES:
        num_terms = len(dfs[dfs<=max_df])
        print '{},{}'.format(max_df, num_terms)

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Extract term matrix from kopiwiki')
    p.add_argument('root', help='Path to KOPI Wikipedia root')
    p.add_argument('date', help='KOPI extraction date')
    p.add_argument('lang', help='KOPI extraction language')
    p.add_argument('--max_df', help='Remove frequent', type=float,
                   default=1.0)
    args = p.parse_args()
    y, X, vocab = build(args)
    plot(X)
