#!/usr/bin/env python
# Check installed packages using linux-info.eclass for necessary kernel options

import pdb, signal
import portage

def debug_signal(_signum, _frame):
	import pdb
	pdb.set_trace()

signal.signal(signal.SIGUSR1, debug_signal)

vartree = portage.db[portage.root]['vartree']

all_cpvs = vartree.dbapi.cpv_all()
settings = portage.config()

for cpv in all_cpvs:
    inherit = vartree.dbapi.aux_get(cpv, ['INHERITED'])[0]
    if 'linux-info' in inherit:
        pv = portage.catsplit(cpv)[1]
        cpvpath = vartree.dbapi.getpath(cpv)+'/'+pv+'.ebuild'
        print('Checking: '+cpv, flush=True)
        portage.doebuild(cpvpath, 'clean', settings=settings, tree='vartree',
                         vartree=vartree)
        portage.doebuild(cpvpath, 'setup', settings=settings, tree='vartree',
                         vartree=vartree)
        print('Finished: '+cpv, flush=True)
