"""Acquire an exact scalar-Hessian QC heat certificate at gamma=8/7."""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations_with_replacement
import sys,json,time
root=Path(__file__).resolve().parents[1];src=(root/'work/hessian_heat_sos.py').read_text();ns={'__file__':str(root/'work/hessian_heat_sos.py'),'__name__':'heat_helpers'};exec(src[:src.index('roc=m.Model()')],ns);globals().update({k:v for k,v in ns.items() if k not in ('__file__','__name__','__doc__')});sys.path.insert(0,str(root/'outputs/shared_mode_gluing'));import capacity as ca
start=time.perf_counter();H=b.add(norm4,b.scale(b.mul(norm,det),-R(16,7)));hc=[H.get(pw,R(0)) for pw in m.powers];model=HeatModel();proposal=model.solve(np.array(hc,float));assert proposal['maximum_Gram_margin']>1e-5,proposal['status'];pairs=list(combinations_with_replacement(range(12),2));E=[]
for i in range(60):E.append([R(float(gc[i,a,c]+(gc[i,c,a] if a!=c else 0))) for a,c in pairs]+[-R(float(v)) for v in oc[i]])
E += [[R(0)]*len(pairs)+[R(float(v)) for v in row] for row in closure];target=[sum(R(int(round(raw[i,j])))*hc[j] for j in range(15)) for i in range(60)]+[R(0)]*3;vv=[R(round(proposal['Gram'][i][j]*2**36),2**36) for i,j in pairs]+[R(round(v*2**36),2**36) for v in proposal['closed_two_form']];delta,_=ca.solve_range(E,[[t-sum(a*c for a,c in zip(row,vv))] for row,t in zip(E,target)]);vv=[a+row[0] for a,row in zip(vv,delta)];GG=[[R(0)]*12 for _ in range(12)]
for (i,j),v in zip(pairs,vv):GG[i][j]=GG[j][i]=v
assert all(sum(a*c for a,c in zip(row,vv))==t for row,t in zip(E,target));margin=R(1,2**16);b.pd([[v-(margin if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(GG)])
out={'gamma':'8/7','quartic_powers':m.powers,'quartic_coefficients':list(map(str,hc)),'Gram':[[str(v) for v in row] for row in GG],'shifted_PD_margin':str(margin),'two_form_pairs':pairs if False else [[0,1],[0,2],[1,2]],'quadratic_value_powers':qa,'closed_two_form_coefficients':list(map(str,vv[len(pairs):])),'seconds':time.perf_counter()-start,'scope':'Literal rational proposal, to be independently rebuilt and received by the sibling QC-extension receiver.'};(root/'outputs/hessian_frontier/dm_heat.json').write_text(json.dumps(out,indent=2)+'\n');print('exact DM Hessian heat Gram acquired, numerical proposal then rational projection; shifted margin',margin,flush=True)
