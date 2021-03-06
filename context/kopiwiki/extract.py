#!/usr/bin/env python
"""
Extract Wikipedia article-term count matrix from KOPI plain text dump.
"""
import logging
from reader import KopiReader
from sklearn.feature_extraction.text import CountVectorizer
from writer import Writer

MAX_DF = 1.0

logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO) # DEBUG, INFO, WARN, ERROR, CRITICAL

def build(args):
    "Build article-term vectors."
    kr = KopiReader(args.root, args.date, args.lang)
    log.info('Reader:\n{}'.format(kr))
    v = CountVectorizer(max_df=args.max_df)
    log.info('Vectorizer:\n{}'.format(v))
    log.info('Building..')
    X = v.fit_transform(kr())
    log.info('..done {}.'.format(X.get_shape()))
    return kr.y, X, v.get_feature_names()

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Extract term matrix from kopiwiki')
    p.add_argument('root', help='Path to KOPI Wikipedia root')
    p.add_argument('date', help='KOPI extraction date')
    p.add_argument('lang', help='KOPI extraction language')
    p.add_argument('--max_df', help='Remove frequent', type=float,
                   default=MAX_DF)
    args = p.parse_args()
    y, X, vocab = build(args)
    Writer(y, X, vocab)()
