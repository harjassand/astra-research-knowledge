#!/usr/bin/env python3
"""Full normal-cell first-kill drift diagnostics in global invariants.

Finite floating diagnostics only. Positive first-kill values refute that stop,
not recurrence or the possibility of a longer actual stopped episode.
"""
from pathlib import Path
import importlib.util,sys,json
import numpy as np

P=Path(__file__).resolve().parent
OLD=P.parent/'astra-sol-subgeometric-synthesis-20261102'
spec=importlib.util.spec_from_file_location('preserved_normal_cell',OLD/'verify_normal_cell.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
Y=old.Y

def coords(x):
    A,B,C,D,E,F=x
    m=lambda a:(0,2,4)[a] if a<3 else 7
    return 15+sum(x)-m(A)-m(D),B-C-int(A==1),E-F-int(D==1)

def run(base):
    keys,xs,edges,kills,mu,rev=old.cell(base)
    n=len(keys);B=np.eye(n);rhs=np.zeros((n,8));qr=np.zeros(n)
    for a in range(n):
        q=float(sum(r for _,r,_ in edges[a])+sum(r for _,r,*_ in kills[a]));qr[a]=q
        rhs[a,0]=1/q
        for b,r,_ in edges[a]:B[a,b]-=float(r)/q
        before=coords(xs[a])
        for kind,rate,dn,block,source in kills[a]:
            out=list(xs[a]);off=3*block
            for j in range(3):out[off+j]+=Y[(source+1)%4][j]-Y[source][j]
            after=coords(out);delta=tuple(v-u for u,v in zip(before,after))
            assert delta[0]==dn
            weight=float(rate)/q
            rhs[a,1:4]+=weight*np.array(delta)
            rhs[a,4:7]+=weight*np.square(delta)
            rhs[a,7]+=weight
    solved=np.linalg.solve(B,rhs)
    residual=float(np.max(np.abs(B@solved-rhs)))
    assert residual<1e-5 and np.max(np.abs(solved[:,7]-1))<1e-3,(base,residual)
    z,r,s=coords(xs[0]);assert all(coords(v)==(z,r,s) for v in xs)
    rows=[]
    for lam in (0,1,2,3,4,6,10):
        change=2*z*solved[:,1]+solved[:,4]+lam*(2*r*solved[:,2]+2*s*solved[:,3]+solved[:,5]+solved[:,6])
        total=change+solved[:,0]
        worst=int(np.argmax(total));best=int(np.argmin(total))
        rows.append({'lambda':lam,'worst_time_plus_change':float(total[worst]),'worst_state':xs[worst],
                     'worst_mode':keys[worst],'best_time_plus_change':float(total[best]),
                     'positive_inputs':int(np.sum(total>0))})
    T=(sum(base)-abs(base[0]-base[1])-abs(base[2]-base[3]))//2
    return {'base':base,'shared_inventory_T':T,'normal_cell_states':n,
            'max_physical_first_kill_mean':float(np.max(solved[:,0])),
            'equation_max_abs_residual':residual,'candidate_values':rows}

def main():
    fixtures=[]
    for n in (100,1000):
        fixtures.extend(((n,0,0,0),(0,n,0,0),(n,0,0,n),(0,n,0,n),(n+2,2,0,n)))
    fixtures.extend(((10,10,10,10),(0,0,20,20)))
    rows=[]
    for base in fixtures:
        v=run(base);rows.append(v)
        l3=next(w for w in v['candidate_values'] if w['lambda']==3)
        print(json.dumps({'base':base,'T':v['shared_inventory_T'],'states':v['normal_cell_states'],
             'max_time':v['max_physical_first_kill_mean'],'lambda3_worst':l3['worst_time_plus_change'],
             'worst_state':l3['worst_state']}),flush=True)
    (P/'results').mkdir(exist_ok=True)
    (P/'results/global_receiver_probe.json').write_text(json.dumps({'finite_diagnostics':rows,
          'scope':'Finite floating first-kill diagnostics, not a global drift proof or recurrence test.'},indent=2)+'\n')

if __name__=='__main__':main()
