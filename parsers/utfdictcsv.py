#!/usr/bin/env python
#
# by John Kim
# Thanks to Securicon, LLC. for sponsoring development
#
#-*- coding:utf-8 -*-
#
# Last edited by Alexander Sferrella on 9/21/2017

import codecs
try: #python2
    from cStringIO import StringIO
except: #python3
    from io import StringIO
import csv

################################################################

class DictUnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        self.writer.writerow({k:v for k, v in D.items() if v})
        
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        try: #python2 
            data = data.decode("utf-8")
        except: #python3 
            data = str.encode(data).decode("utf-8")
        # ... and re-encode it into the target encoding
        data = self.encoder.encode(data)
        # Write to the target stream
        self.stream.write(data)
        # Empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()

