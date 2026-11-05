"""Independent exact rooted-path normalization check, not a statistical test."""
from pathlib import Path
from fractions import Fraction as F
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'square_aklt_boundary_operation_20261105'))
from exact_loop_birth_sampler import LoopBirthSampler,canonical,D
from perfect_loop_sampler import exact_small_box
from crossed_loop_influence import variants
from torus_loop_birth_sampler import TorusLoopBirthSampler
s=TorusLoopBirthSampler(1) if "--torus" in sys.argv else LoopBirthSampler(1)
cat=json.loads((ROOT/'square_aklt_loop_audit_20261105/loop_catalog_through12.json').read_text())
loops={}
for item in cat:
 for p in variants(item['cyclic_vertices']):
  mx=max(x for x,y in p);my=max(y for x,y in p)
  for dx in range(3-mx):
   for dy in range(3-my):
    loops[canonical([(x+dx,y+dy) for x,y in p])]=F(item['activity'])
opts={tuple(h):(i,r,k) for k,(i,h,r) in enumerate(s.options)}
counts=0;verified=[]
for route,want in loops.items():
 n=len(route);encodings=set();total=F(0)
 for reverse in (False,True):
  r=list(route[::-1] if reverse else route)
  for shift in range(n):
   p=r[shift:]+r[:shift];p=p+[p[0]]
   dirs=tuple(D.index((b[0]-a[0],b[1]-a[1])) for a,b in zip(p,p[1:]))
   encodings.add((p[0],dirs));ori=dirs[0]
   norm=tuple((d-ori)%4 for d in dirs)
   h=norm if n<s.m else norm[:s.m]
   state,rm,oi=opts[h]
   prev=0 if oi==0 else s.cumulative[oi-1]
   # Per-root-and-initial-direction proposal intensity.
   intensity=F(s.cumulative[oi]-prev,s.den)
   if state>=0:
    px=sum(D[d][0] for d in dirs[:s.m]);py=sum(D[d][1] for d in dirs[:s.m])
    for d_world in dirs[s.m:]:
     d=(d_world-ori)%4;j=s.directions[state].index(d)
     target=int(s.to[state,j]);weight=int(s.w[state,j])
     newori=(ori+s.states[state][1])%4
     nx=px+D[d_world][0];ny=py+D[d_world][1]
     if hasattr(s,"g"):
      intensity*=F(weight*int(s.g[newori*len(s.states)+target,nx%s.side,ny%s.side]),15*int(s.g[ori*len(s.states)+state,px%s.side,py%s.side]))
     else:intensity*=F(weight*s.qnum[target],15*s.qnum[state])
     rm+=weight==3;ori=newori;state=target;px=nx;py=ny
    if hasattr(s,"g"):intensity*=F(s.scale,int(s.g[ori*len(s.states)+state,px%s.side,py%s.side]))
    else:intensity*=F(s.qden,s.qnum[state])
   degree={}
   for a,b in zip(p,p[1:]):degree[a]=degree.get(a,0)+1;degree[b]=degree.get(b,0)+1
   rt=sum(d==4 for d in degree.values());assert rm<=rt
   intensity*=F(3,2*n)*F(3,5)**(rt-rm)
   assert intensity==want/(2*n),(route,dirs,intensity,want)
   total+=intensity;counts+=1
 assert len(encodings)==2*n
 assert total==want
 verified.append({'length':n,'activity':str(want),'rooted_encodings':2*n})
result={'physical_loops':len(loops),'rooted_oriented_encodings':counts,'all_exact_intensities_match':True,'total_birth_intensity':str(sum(loops.values(),F(0))),'proposal_rate_per_vertex':str(s.rate_per_vertex),'by_loop':verified}
Path(__file__).with_name('exact_torus_sampler_audit_results.json' if hasattr(s,'g') else 'exact_sampler_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
