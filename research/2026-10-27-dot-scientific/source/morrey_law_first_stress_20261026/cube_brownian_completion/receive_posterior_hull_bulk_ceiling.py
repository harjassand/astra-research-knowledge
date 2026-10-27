"""Exact support geometry + inherited Fourier interpolation error: maximal finite-bulk credit."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,lcm
from functools import reduce
import json,hashlib,itertools,numpy as np,time
P=Path(__file__).resolve().parent;O=P/'same_law_AC';F=P/'fully_corrective141_half_K48';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sources=[('root',O/'local_posterior_feasibility_receipt.json'),('negative_helper',O/'negative_subtree_posterior_point_receipt.json')];families=[]
for name,path in sources:
 j=json.loads(path.read_text());pts=[list(map(Q,r['point']))for r in j['rows']]if'rows'in j else[list(map(Q,r))for r in j['frontier_points']];D=lcm(*(v.denominator for x in pts for v in x));X=[tuple(int(v*D)for v in x)for x in pts];facets=set()
 for i,j,k in itertools.combinations(range(len(X)),3):
  u=[X[j][a]-X[i][a]for a in range(3)];v=[X[k][a]-X[i][a]for a in range(3)];n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
  if n==[0,0,0]:continue
  b=sum(n[a]*X[i][a]for a in range(3));vals=[sum(n[a]*x[a]for a in range(3))-b for x in X]
  if max(vals)<=0:pass
  elif min(vals)>=0:n=[-a for a in n];b=-b
  else:continue
  gg=reduce(gcd,map(abs,n+[b]));facets.add(tuple(a//gg for a in n)+(b//gg,))
 assert len(facets)>=4;polys=set()
 for perm in itertools.permutations(range(3)):polys.add(tuple(sorted(tuple(f[i]for i in perm)+(f[3],)for f in facets)))
 families.append({'name':name,'source_path':str(path),'source_sha256':sha(path),'coordinate_denominator':D,'integer_points':X,'exact_supporting_facets':sorted(facets),'S3_polytopes':sorted(polys)})
V=np.load(F/'candidate_volume_nodes.npy',mmap_mode='r');n=np.arange(-128,129,dtype=np.int64);yy=n[:,None];zz=n[None,:];tot=[0,0,0];counts=[0,0,0];start=time.time()
for a in range(0,257,16):
 xx=n[a:a+16,None,None];masks=[]
 for fam in families:
  D=fam['coordinate_denominator'];mask=np.zeros((len(xx),257,257),dtype=bool)
  for poly in fam['S3_polytopes']:
   inside=np.ones_like(mask)
   for A,B,C,b in poly:inside&=D*(A*xx+B*yy+C*zz)<=128*b+D*(abs(A)+abs(B)+abs(C))
   mask|=inside
  masks.append(mask)
 masks.append(masks[0]|masks[1]);neg=np.ceil(np.maximum(-np.asarray(V[a:a+16]),0)*2**40).astype(np.int64)
 for i,mask in enumerate(masks):counts[i]+=int(mask.sum());tot[i]+=int(neg[mask].sum())
 print('block',a,'seconds',time.time()-start,flush=True)
cert=json.loads((F/'received_full_Gram_candidate.json').read_text());vg=Q(cert['own_volume_Gram_allowance']);rows=[]
for name,nn,ct in zip(['root','negative_helper','union'],tot,counts):
 nodal=Q(3*(nn+2048*ct),2**40*128**3);cap=nodal+vg;rows.append({'family':name,'outer_hat_support_node_count':ct,'exact_upward_nodal_numerator':str(nn),'finite_nodal_negative_bulk_upper':str(nodal),'entire_inherited_volume_Gram_error_paid':str(vg),'maximum_possible_finite_bulk_credit':str(cap),'decimal_credit_ceiling':float(cap)})
out={'status':'EXACT_POSTERIOR_HULL_FINITE_BULK_CEILING_PENDING_AUDIT','families':families,'rows':rows,'field_node_guard':'1/536870912','hat_support_outer_cover':'A node is selected if its full hat-support cube could meet every facet of at least one S3 hull; this is a conservative necessary-condition cover, not an asserted exact intersection test.','proof_note':'POSTERIOR_HULL_BULK_CEILING.md','dependencies':{str(p):sha(p)for p in[F/'candidate_volume_nodes.npy',F/'received_full_Gram_candidate.json',P/'exact_fourier_gram/EXACT_FOURIER_GRAM.md']if p.exists()},'script_sha256':sha(Path(__file__)),'scope':'Maximum negative finite-volume credit available to any positive occupation confined to these fixed helper convex hulls, independent of covariance selector, density concentration, stopping duration or incoming weight. Entire global Fourier interpolation error is paid again for each separate ceiling. No trueN lower bound or obstruction to other frontiers/source changes. Existing source/cubic/analytic fees remain unchanged.'};(O/'posterior_hull_bulk_ceiling_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print('DONE',[(r['family'],r['decimal_credit_ceiling'])for r in rows])
