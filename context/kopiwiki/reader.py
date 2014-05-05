#!/usr/bin/env python
"""
Extract Wikipedia article-term count matrix from KOPI plain text dump.
"""
import glob
import gzip
import logging
import os
import re

logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO) # DEBUG, INFO, WARN, ERROR, CRITICAL

KOPI_DIR_FMT = 'wikipedia.txt.dump.{}-{}.SZTAKI'
KOPI_FN_FMT = '{}-wiki-{}_*.txt.gz'
ARTICLE_NAME_OPEN = '[['
ARTICLE_NAME_CLOSE = ']]'
EMPTY_NAME_LINE = '{}{}'.format(ARTICLE_NAME_OPEN, ARTICLE_NAME_CLOSE)
DISAMBIGUATION_CLOSE = ' (disambiguation)'
ENC = 'utf8'
REDIRECT_RE = r'#redirect'
NAMESPACES = [
    u"Talk",
    u"User",
    u"User talk",
    u"Wikipedia",
    u"WP", # Wikipedia alias
    u"Project", # Wikipedia alias
    u"Wikipedia talk",
    u"WT", # Wikipedia talk alias
    u"Project talk", # Wikipedia talk alias
    u"File",
    u"Image", # File alias
    u"File talk",
    u"Image talk", # File talk alias
    u"MediaWiki",
    u"MediaWiki talk",
    u"Template",
    u"Template talk",
    u"Help",
    u"Help talk",
    u"Category",
    u"Category talk",
    u"Portal",
    u"Portal talk",
    u"Book",
    u"Book talk",
    u"Draft",
    u"Draft talk",
    u"Education Program",
    u"Education Program talk",
    u"TimedText",
    u"TimedText talk",
    u"Module",
    u"Module talk",
    u"Special",
    u"Media",
    ]
PSEUDONAMESPACES = [
    u"CAT",
    u"H",
    u"P",
    u"T",
    ]
NAMESPACE_RE = r'(?:{})'.format('|'.join(NAMESPACES))
PSEUDONAMESPACE_RE = r'(?:{})'.format('|'.join(PSEUDONAMESPACES))

class KopiReader(object):
    "Read Wikipedia article text from KOPI dump."
    def __init__(self, root, date, lang):
        self.root = root
        self.date = date
        self.lang = lang
        self.y = []
        self.namespace_re = re.compile(NAMESPACE_RE, re.I)
        self.pseudonamespace_re = re.compile(PSEUDONAMESPACE_RE)
        self.redirect_re = re.compile(REDIRECT_RE, re.I)

    def __str__(self):
        return 'KopiReader(root={},{}date={},{}lang={})'.format(
            self.root,
            '\n{:8s}'.format(''),
            self.date,
            '{:1s}'.format(''),
            self.lang
            )

    @property
    def path(self):
        "Path to directory containing KOPI plain text dump files."
        return os.path.join(
            self.root,
            KOPI_DIR_FMT.format(self.date, self.lang),
            KOPI_FN_FMT.format(self.date, self.lang)
            )

    def __call__(self):
        "Yield article text, saving names in same order."
        log.info('Reading..')
        for i, f in enumerate(sorted(glob.glob(self.path))):
            """
            if i >= 1: #TEST
                break #TEST
            """
            log.info('..{}..'.format(f))
            for name, text in self.read(gzip.open(f)):
                self.y.append(name)
                yield text
        log.info('..done.')

    def read(self, fh):
        "Yield (name,text) tuples from file."
        self.reset(EMPTY_NAME_LINE)
        for line in fh:
            line = line.decode(ENC).rstrip()
            if self.is_start(line):
                if self.is_article():
                    yield self.format()
                self.reset(line)
            elif self.is_redirect(line):
                self._redirect = True
            else:
                self._lines.append(line)
        if self.is_article():
            yield self.format()

    def reset(self, line):
        "Reset article variables."
        self._name = self.get_name(line)
        self._lines = []
        self._redirect = False

    def get_name(self, line):
        "Return text portion of article name line."
        return line[2:-2]

    def is_start(self, line):
        "Return true if line indicates and article start."
        if not line.startswith(ARTICLE_NAME_OPEN):
            return False
        if not line.endswith(ARTICLE_NAME_CLOSE):
            return False
        return True

    def is_redirect(self, line):
        "Return true if line indicates page is a redirect."
        return self.redirect_re.match(line)

    def is_article(self):
        "Return true if page is an article."
        if self._name == '':
            return False # empty name
        if self._redirect:
            return False # redirect page
        if self._name.endswith(DISAMBIGUATION_CLOSE):
            return False # disambiguation page
        if self.namespace_re.match(self._name):
            return False # not main article namespace
        if self.pseudonamespace_re.match(self._name):
            return False # not main article  namespace
        if len([l for l in self._lines if l != '']) == 0:
            return False # empty text
        return True

    def format(self):
        "Format article as (name,text) tuple."
        text = '\n'.join(self._lines)
        return self._name, text
