#!/usr/bin/env python
"""
Extract Wikipedia article-term count matrix from KOPI plain text dump.
"""
import logging
import sys
from itertools import izip
from sklearn.feature_extraction.text import CountVectorizer

logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO) # DEBUG, INFO, WARN, ERROR, CRITICAL

ENC = 'utf8'
TERM_FREQ_SEP = u'|'
COL_SEP = u' '

class Writer(object):
    "Write matrix to file."
    def __init__(self, y, X, vocab, fh=sys.stdout):
        self.y = y
        self.X = X
        self.vocab = vocab
        self.fh = fh

    def __call__(self):
        "Write matrix to file."
        log.info('Writing..')
        for i, row in enumerate(self.rows()):
            if i % 1000 == 0:
                log.info('..{}..'.format(i))
            self.fh.write(u'{}\n'.format(row).encode(ENC))
        log.info('..done.')

    def rows(self):
        "Yield formatted rows."
        for label, vector in izip(self.y, self.X):
            if vector.getnnz() > 0: # skip empty vectors
                yield COL_SEP.join(self.columns(label, vector))

    def columns(self, label, vector):
        "Yield formatted columns for given row data."
        yield label.replace(' ', '_')
        for i, freq in izip(vector.indices, vector.data):
            term = self.vocab[i]
            yield u"{}{}{}".format(term, TERM_FREQ_SEP, freq)
