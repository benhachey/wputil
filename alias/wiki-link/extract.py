#!/usr/bin/env python2.7
"""
Script to extract aliases from Google/UMass wiki-link data.
"""
import logging
import glob
import gzip
from collections import defaultdict
from operator import itemgetter

logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO) # DEBUG, INFO, WARN, ERROR, CRITICAL

class Aliases:
    def __init__(self):
        self._aliases = defaultdict(int) # {(wikititle,alias) => |pages]}
        self._priors = defaultdict(int) # {wikititle => |pages|}

    def iter_aliases(self):
        for (wikititle, alias), pagecount in self._aliases.iteritems():
            yield (wikititle, alias, pagecount)

    def iter_priors(self):
        for wikititle, pagecount in self._priors.iteritems():
            yield (wikititle, pagecount)

    def update(self, doc):
        for wikititle,alias in doc.iter_aliases():
            if wikititle.strip() != '' and alias.strip() != '':
                self._aliases[(wikititle,alias)] += 1
        for wikititle in doc.iter_titles():
            if wikititle.strip() != '':
                self._priors[wikititle] += 1

    @classmethod
    def from_wikilink_dir(cls, d):
        log.info('Extracting aliases from %s..' % d)
        a = cls()
        for f in glob.glob('%s/*.gz' % d):
            log.info('..%s..' % f)
            for i, d in enumerate(Doc.from_wikilink_file(f)):
                if i % 100000 == 0:
                    log.info('....%d....' % i)
                a.update(d)
        log.info('..done.')
        return a

    def write_aliases(self, f):
        log.info('Writing aliases..')
        w = open(f, 'w')
        for a in sorted(self.iter_aliases(), key=itemgetter(2), reverse=True):
            w.write('%s\t%s\t%d\n' % a)
        log.info('..done.')

    def write_priors(self, f):
        log.info('Writing priors..')
        w = open(f, 'w')
        for p in sorted(self.iter_priors(), key=itemgetter(1), reverse=True):
            w.write('%s\t%d\n' % p)
        log.info('..done.')

class Doc:
    def __init__(self, url):
        self._url = url
        self._mentions = []
        self._tokens = []

    def iter_aliases(self):
        for alias,wikiurl in set([(s,t) for s,o,t in self._mentions]):
            yield (self._title(wikiurl),alias)

    def iter_titles(self):
        for wikiurl in set([t for s,o,t in self._mentions]):
            yield self._title(wikiurl)

    def _title(self, wikiurl):
        return wikiurl[wikiurl.rfind('/')+1:]

    def add_mention(self, string, offset, target):
        self._mentions.append((string, offset, target))

    def add_token(self, string, offset):
        self._tokens.append((string, offset))

    @classmethod
    def from_wikilink_file(cls, f):
        d = None
        for line in gzip.open(f):
            fields = line.strip().split('\t')
            if len(fields) < 2:
                continue
            if fields[0] == 'URL':
                if d is not None:
                    yield d
                d = cls(fields[1])
            elif fields[0] == 'MENTION' and len(fields) == 4:
                string, offset, target = fields[1:4]
                d.add_mention(string, offset, target)
            elif fields[0] == 'TOKEN' and len(fields) == 3:
                string, offset = fields[1:3]
                d.add_token(string, offset)
        if d is not None:
            yield d
        

def main(wikilinkd, aliasf, priorf):
    a = Aliases.from_wikilink_dir(wikilinkd)
    a.write_aliases(aliasf)
    a.write_priors(priorf)

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Extract aliases from wiki-links')
    p.add_argument('dir', help='Path to Google wiki-link directory')
    p.add_argument('aliases', help='Output file for aliases')
    p.add_argument('priors', help='Output file for priors')
    args = p.parse_args()
    main(args.dir, args.aliases, args.priors)
