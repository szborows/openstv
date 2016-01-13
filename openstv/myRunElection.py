#!/usr/bin/env python
"run an election from the command line with optional profiling"

__revision__ = "$Id: runElection.py 715 2010-02-27 17:00:55Z jeff.oneill $"

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openstv.ballots import Ballots
from openstv.plugins import getMethodPlugins, getReportPlugins

methods = getMethodPlugins("byName", exclude0=False)
methodNames = methods.keys()
methodNames.sort()

reports = getReportPlugins("byName", exclude0=False)
reportNames = reports.keys()
reportNames.sort()

reps = 1
reportformat = "TextReport"
strongTieBreakMethod = None
weakTieBreakMethod = None
numSeats = int(sys.argv[3])
prec = None

name = 'WarrenSTV'
bltFn = sys.argv[1]

if name not in methodNames:
  print "Unrecognized method '%s'" % name
  print usage
  sys.exit(1)

try:
  dirtyBallots = Ballots()
  dirtyBallots.loadKnown(bltFn, exclude0=False)
  if numSeats:
    dirtyBallots.numSeats = numSeats
  cleanBallots = dirtyBallots.getCleanBallots()
except RuntimeError, msg:
  print msg
  sys.exit(1)

def doElection(reps=1):
  "run election with repeat count for profiling"
  for i in xrange(reps):
    e = methods[name](cleanBallots)
    if strongTieBreakMethod is not None:
      e.strongTieBreakMethod = strongTieBreakMethod
    if weakTieBreakMethod is not None:
      e.weakTieBreakMethod = weakTieBreakMethod
    if prec is not None:
      e.prec = prec
    e.runElection()
  return e

e = doElection()

with open(sys.argv[2], 'w') as fp:
    r = reports[reportformat](e, outputFile=fp)
    r.generateReport()
