"""Literal mixed-flow map for the independently supplied symmetric target."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement as cwr
import json,sys,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
import verify_common as P
from maps import load as core_maps


def build():
    source=ROOT.parent.parent.parent/'common_cone_review/EXACT_SYMMETRIC_TARGET.json'
    raw=source.read_bytes();target=json.loads(raw);p=list(map(F,target['coefficients']))
    (ROOT/'SYMMETRIC_TARGET.json').write_bytes(raw)
    a=[P.var(i) for i in range(4)];z=[P.var(i+4) for i in range(6)]
    J1=[z[0],z[1],z[3],z[4]];J2=[z[1],z[2],z[4],z[5]]
    rotate=lambda B:[P.scale(B[2],-1),P.scale(B[3],-1),B[0],B[1]]
    JB1,JB2=rotate(J1),rotate(J2)
    monoms=[next(iter(P.product([a[i],a[j],z[k],z[l]]))) for i,j in cwr(range(4),2) for k,l in cwr(range(6),2)]
    lookup={e:i for i,e in enumerate(monoms)}
    def coefficients(poly):
        answer=[F(0)]*210
        for e,c in poly.items():answer[lookup[e]]=c
        return answer
    standard=[];mixed=[]
    for energy in P.bases(a):
        hess=[[P.diff(P.diff(energy,i),j) for j in range(4)] for i in range(4)]
        ei=P.add(*(P.mul(P.mul(B[i],B[j]),hess[i][j]) for B in [J1,J2] for i in range(4) for j in range(4)))
        ej=P.add(*(P.mul(P.add(P.mul(J1[i],JB2[j]),P.mul(J2[i],JB1[j])),hess[i][j]) for i in range(4) for j in range(4)))
        standard.append(coefficients(ei));mixed.append(coefficients(ej))
    E=np.array(standard,float).T;EJ=np.array(mixed,float).T;d=core_maps();assert np.array_equal(E,d['E'])
    Fstd=[sum(p[i]*standard[i][j] for i in range(9)) for j in range(210)]
    Fmixed=[sum(p[i]*mixed[i][j] for i in range(9)) for j in range(210)]
    detstd=[standard[2][j]-standard[3][j] for j in range(210)]
    detmixed=[mixed[2][j]-mixed[3][j] for j in range(210)]
    values=[F(-1),F(0),F(0),F(1),F(1),F(0),F(0),F(0),F(0),F(0)]
    def evaluate(v):
        answer=F(0)
        for e,c in zip(monoms,v):
            term=c
            for value,n in zip(values,e):term*=value**n
            answer+=term
        return answer
    gamma_bound=evaluate(Fstd)/evaluate(detstd)
    assert gamma_bound>0 and evaluate(Fmixed)==evaluate(detmixed)==0
    common=json.loads((ROOT.parent/'EXACT_COMMON_SEPARATOR.json').read_text());lh=list(map(F,common['heat_lambda']))
    pairings=[sum(lh[j]*mixed[i][j] for j in range(210)) for i in range(9)]
    out={'source_target_sha256':hashlib.sha256(raw).hexdigest(),'target_coefficients':list(map(str,p)),
         'flow':'v_t=Delta v+2b J partial12v; J=[[0,-1],[1,0]]',
         'mixed_map_by_energy_basis':[[str(c) for c in v] for v in mixed],
         'standard_F':list(map(str,Fstd)),'mixed_F':list(map(str,Fmixed)),
         'standard_det2':list(map(str,detstd)),'mixed_det2':list(map(str,detmixed)),
         'plane_wave_gamma_bound':str(gamma_bound),'old_common_heat_mixed_pairings':list(map(str,pairings)),
         'scope':'Literal new operator map; no wider-flow theorem from these pairings alone.'}
    (ROOT/'FLOW_MAPS.json').write_text(json.dumps(out,indent=2)+'\n')
    np.savez(ROOT/'FLOW_MAPS.npz',EJ=EJ,ef=np.array(Fstd,float),ejf=np.array(Fmixed,float),ed=np.array(detstd,float),ejd=np.array(detmixed,float))
    print(json.dumps({k:v for k,v in out.items() if k not in ['mixed_map_by_energy_basis','standard_F','mixed_F','standard_det2','mixed_det2']},indent=2))


if __name__=='__main__':build()
