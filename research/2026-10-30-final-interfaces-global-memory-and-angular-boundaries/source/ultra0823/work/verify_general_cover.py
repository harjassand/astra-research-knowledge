"""Exact cover for the generic exposed-ray angular proposal."""
from pathlib import Path
from fractions import Fraction as R
import json,time,sympy as S,numpy as np,signal
from bernstein_cover import bernstein,good,split,inside
signal.alarm(180);start=time.perf_counter();here=Path(__file__).parent;case=here/'general_ray'
raw=json.loads((case/'candidate.json').read_text());data={}
for key,name in [('C','C_permuted'),('M','M')]:
    mat=raw[name];data[key]={'size':len(mat),'degrees':[max(z[0] for row in mat for ent in row for z in ent),max(z[1] for row in mat for ent in row for z in ent)],'entries':mat}
b,d=S.symbols('b d');bc,dc=map(R,raw['ray']['canonical_zero'])
mf=S.Matrix([[sum(S.Rational(n,dd)*b**ib*d**id_ for ib,id_,n,dd in ent) for ent in row] for row in raw['M']])
ev=np.linalg.eigvalsh(np.array(mf.subs({b:float(bc),d:float(dc)}),float));print('lifted eigenvalues',ev,flush=True)
local=None
for k in range(3,22):
    den=2**k;lb=(bc*den).__floor__();ld=(dc*den).__floor__();box=(R(lb,den),R(lb+1,den),R(ld,den),R(ld+1,den))
    ok=good(bernstein(data['M'],box));print('local depth',k,'positive',ok,flush=True)
    if ok:local=box;break
if local is None:raise ValueError('No positive local lift box')
root=(R(-1),R(1),R(-1),R(1));todo=[(root,bernstein(data['C'],root),0)];leaves=[];count=0;maxdepth=0
while todo:
    box,net,depth=todo.pop();count+=1;maxdepth=max(depth,maxdepth)
    if inside(box,local):leaves.append({'box':list(map(str,box)),'proof':'M'});continue
    if good(net):leaves.append({'box':list(map(str,box)),'proof':'C'});continue
    if depth>=60:
        point=[str((box[0]+box[1])/2),str((box[2]+box[3])/2)]
        path=case/'obligation_points.json';old=json.loads(path.read_text()) if path.exists() else []
        if point not in old:old.append(point);path.write_text(json.dumps(old,indent=2)+'\n')
        raise ValueError('Unresolved rectangle '+str(box)+'; center supplied as a new obligation, not a non-QC conclusion')
    axis=0 if box[1]-box[0]>=box[3]-box[2] else 1
    ll,rr=split(net,axis);mid=(box[2*axis]+box[2*axis+1])/2
    lb=list(box);rb=list(box);lb[2*axis+1]=mid;rb[2*axis]=mid
    todo.append((tuple(rb),rr,depth+1));todo.append((tuple(lb),ll,depth+1))
    if count%200==0:print('examined',count,'leaves',len(leaves),'depth',maxdepth,time.perf_counter()-start,flush=True)
area=sum((R(x['box'][1])-R(x['box'][0]))*(R(x['box'][3])-R(x['box'][2])) for x in leaves);assert area==4
out={'local_box':list(map(str,local)),'leaves':leaves,'leaf_count':len(leaves),'max_depth':maxdepth,'area':str(area),
     'seconds':time.perf_counter()-start,'scope':'Exact PSD of the entire canonical square, using coefficient-matrix signs and the supplied local identity.'}
(case/'cover.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='leaves'},indent=2),flush=True)
