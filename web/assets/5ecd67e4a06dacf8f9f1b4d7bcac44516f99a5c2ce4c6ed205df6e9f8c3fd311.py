"""Small exact bookkeeping for coherent-bra and low-rank-tail obstructions."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import grassmann_bcs as g
import lowrank_bcs as lr
from fractions import Fraction as Q
from itertools import combinations
import json

def sector(F,k):
    n=len(F)
    out={}
    for I in combinations(range(n),k):
        for J in combinations([j for j in range(n) if j not in I],k):
            a=g.determinant([[F[i][j] for j in J] for i in I])
            if a!=g.ZERO: out[(I,J)]=g.abs2(a)
    z=sum(out.values())
    return z,{key:value/z for key,value in out.items()} if z else {}

def test():
    rows=[]
    for e in (Q(1,4),Q(1,256),Q(1,65536)):
        Fs=[]
        for i,j in ((0,1),(1,0)):
            F=[[g.qc(1) for _ in range(4)] for _ in range(4)]
            F[i][j]=g.qc(1+e)
            Fs.append(F)
        z0,p0=sector(Fs[0],2)
        z1,p1=sector(Fs[1],2)
        assert z0==z1==2*e*e
        keys=set(p0)|set(p1)
        tv=sum(abs(p0.get(k,0)-p1.get(k,0)) for k in keys)/2
        assert tv==1 and not set(p0)&set(p1)
        assert all(len(lr.factor(F)[1])==2 for F in Fs)
        rows.append({'epsilon':str(e),'norms_squared':[str(z0),str(z1)],
                     'TV':str(tv),'supports':[
                         [{'I':list(i),'J':list(j),'p':str(p)} for (i,j),p in d.items()]
                         for d in (p0,p1)]})
    same_norm=[]
    for sign in (-1,1):
        F=[[g.ZERO,g.ONE],[g.qc(sign),g.ZERO]]
        z,p=sector(F,1)
        amp=g.add(F[0][1],F[1][0])
        assert z==2
        same_norm.append({'relative_sign':sign,'hard_norm':str(z),
                          'coherent_bra_squared_amplitude':str(g.abs2(amp))})
    assert [d['coherent_bra_squared_amplitude'] for d in same_norm]==['0','4']
    out={'status':'PASS','lowrank_tail_discontinuity':rows,
         'diagonal_projector_vs_coherent_bra':same_norm,
         'magic_Pluecker_residual':'1',
         'scope':'Exact finite algebra; no universal FLO compiler or quantum circuit ran.'}
    Path(__file__).with_name('boundary_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','tail_cases':len(rows),'same_norm_cases':len(same_norm)},indent=2))

if __name__=='__main__': test()
