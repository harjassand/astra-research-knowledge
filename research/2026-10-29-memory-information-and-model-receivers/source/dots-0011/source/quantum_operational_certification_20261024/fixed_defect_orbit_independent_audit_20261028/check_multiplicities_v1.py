#!/usr/bin/env python3
from pathlib import Path
import itertools,json,numpy as np
import check_orbit_v1 as c
HERE=Path(__file__).parent
rows=[]
for lam,mu in [((3,1),(2,2)),((3,2),(3,1,1)),((4,2),(4,2)),((4,2),(3,3))]:
 k=sum(lam);j=2;lt,ls=c.reps(lam);mt,ms=c.reps(mu);perms=list(itertools.permutations(range(k)));chprod=np.array([np.trace(c.permrep(g,ls))*np.trace(c.permrep(g,ms)) for g in perms]);sectors=[]
 for nu in [(k,),(k-1,1),(k-2,2),(k-2,1,1)]:
  nt,ns=c.reps(nu);ch=np.array([np.trace(c.permrep(g,ns)) for g in perms]);mult=float(chprod@ch/len(perms));assert abs(mult-round(mult))<1e-10;h=sum(all(v==0 for v in t[:k-j]) for t in nt)
  sectors.append({'nu':nu,'multiplicity':int(round(mult)),'dimension':len(nt),'H_fixed_dimension':h})
 rows.append({'lambda':lam,'mu':mu,'sectors':sectors,'selected_dimension':sum(s['multiplicity']*s['dimension'] for s in sectors),'selected_trivial_dimension':sectors[0]['multiplicity']})
 print(rows[-1],flush=True)
(HERE/'check_multiplicities_v1.json').write_text(json.dumps(rows,indent=2)+'\n')
