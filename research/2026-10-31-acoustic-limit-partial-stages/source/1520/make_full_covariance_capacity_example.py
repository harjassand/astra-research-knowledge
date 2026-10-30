"""An actual twelve-mode field and a 21-ray ordinary covariance catalogue."""
from pathlib import Path
from fractions import Fraction as R
import sys,json
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/acoustic_capacity'))
from receive import r
D=r.setup();cert=json.loads((root/'outputs/shared_mode_gluing/certificate.json').read_text());blocks=[([R(1),R(2),R(1),R(1,2)],(R(1),R(0))),([R(2),R(1),R(3),R(1)],(R(3,5),R(4,5))),([R(1),R(1),R(2),R(3,2)],(R(5,13),R(12,13)))]
payload={'modes':[],'catalogue':[],'requested_L4_gap':'1/200'}
for j,(amps,(c,s)) in enumerate(blocks):
    A=[v*v for v in amps];order=sorted(range(4),key=lambda i:(A[i],i));case=next(x for x in cert['charts'] if x['order']==order);bi=case['base'];ids=[(0,1,2),(0,2,3)][bi];m=min(A[i] for i in ids);eps=R(case['epsilon']);weights=[A[i]/2-eps*m for i in ids]+[eps*m*eta for eta in D['eta']]+[A[3 if bi==0 else 1]/2]
    def rotate(v):return [c*v[0]-s*v[2],c*v[1]-s*v[3],s*v[0]+c*v[2],s*v[1]+c*v[3]]
    payload['catalogue'] += [{'weight':str(w),'rank_one_direction':list(map(str,rotate(ray))),'kind':'ordinary'} for w,ray in zip(weights,D['rays'][bi])]
    L=9**j;vectors=[[amps[0],0],[0,amps[1]],[amps[2],amps[2]],[2*amps[3],amps[3]]]
    for k,v in zip(((1,0),(0,1),(1,1),(2,1)),vectors):
        u=[(c*v[0]-s*v[1])/L,(s*v[0]+c*v[1])/L]
        payload['modes'].append({'frequency':[L*x for x in k],'sine':list(map(str,u))})
(root/'outputs/acoustic_capacity/compression_input.json').write_text(json.dumps(payload,indent=2)+'\n')
