"""Validated angular/global and radial derivative checks for the fixed 5-shell Coulomb candidate.
All proof inequalities are evaluated with mpmath's outward-rounded interval context.
"""
import itertools, json, heapq, math
from heapq import heappush, heappop
from mpmath import mp, iv
from angular_interval import R, F, angular_lower, bnb, hessang
mp.dps=80; iv.dps=60

P=(0,1,2); Q=(0,3,4)
# High-precision centers from the simultaneous stationarity + equal-source-force solve.
CENTER=[
 mp.mpf('-2.31519449795229144495537793024521332991267343417911360489657'),
 mp.mpf('2.93625533340134823331274447381288438335285498495327179821596'),
 mp.mpf('1.99517837342569275658441495398085752254415210737441872519361'),
 mp.mpf('-2.38590226052078909118582472062049710156516203011416797569951'),
 mp.mpf('0.651229694383177673341856698546369810578028841843670943555922')]
ROOT_RADIUS=iv.mpf('1e-25')

# Scalar pair derivatives for h(a,b,t)=1/sqrt(a^2+b^2-2ab cos(t)).
def edge(ctx,a,b,t):
 c=ctx.cos(t); s=ctx.sin(t); d=a*a+b*b-2*a*b*c
 d3=d*ctx.sqrt(d); d5=d*d*ctx.sqrt(d)
 A=a-b*c; B=b-a*c
 return {
  'f':1/ctx.sqrt(d),
  'a':-A/d3, 'b':-B/d3,
  'aa':-1/d3+3*A*A/d5,
  'ab':c/d3+3*A*B/d5,
  'bb':-1/d3+3*B*B/d5,
  't':-a*b*s/d3,
  'tt':-a*b*c/d3+3*a*a*b*b*s*s/d5,
  'at':-b*s/d3+3*a*b*A*s/d5,
  'bt':-a*s/d3+3*a*b*B*s/d5,
 }

def profile_edges(ctx, radii, a, b):
 r0,r1,r2=radii
 return edge(ctx,r0,r1,a), edge(ctx,r0,r2,b), edge(ctx,r1,r2,a-b)

def angular_gradient(ctx,radii,a,b):
 e01,e02,e12=profile_edges(ctx,radii,a,b)
 return e01['t']+e12['t'], e02['t']-e12['t']

def source_force(ctx,radii,a,b):
 e01,e02,_=profile_edges(ctx,radii,a,b)
 return e01['a']+e02['a']

def reduced_radial_hessian(ctx,radii,alpha,beta):
 """Angular Schur complement C_rr-C_rθ(C_θθ)^-1 C_θr."""
 e01,e02,e12=profile_edges(ctx,radii,alpha,beta)
 t01,t02,t12=e01['tt'],e02['tt'],e12['tt']
 h11=t01+t12; h12=-t12; h22=t02+t12
 det=h11*h22-h12*h12
 # B = C_{r,theta}; rows correspond to (r0,r1,r2), columns to (alpha,beta).
 B=((e01['at'],e02['at']),
    (e01['bt']+e12['at'],-e12['at']),
    (e12['bt'],e02['bt']-e12['bt']))
 D=((e01['aa']+e02['aa'],e01['ab'],e02['ab']),
    (e01['ab'],e01['bb']+e12['aa'],e12['ab']),
    (e02['ab'],e12['ab'],e02['bb']+e12['bb']))
 Hinv=((h22/det,-h12/det),(-h12/det,h11/det))
 S=[]
 for i in range(3):
  row=[]
  for j in range(3):
   schur=sum((B[i][p]*Hinv[p][q]*B[j][q]
              for p in range(2) for q in range(2)),ctx.mpf(0))
   row.append(D[i][j]-schur)
  S.append(tuple(row))
 return tuple(S),det,(h11,h12,h22)

def G5(ctx,x):
 a,b,c,d,s=x
 pR=[ctx.mpf(1),ctx.mpf('3.7632172480656902'),ctx.mpf('0.4252867292159305')]
 qR=[ctx.mpf(1),ctx.mpf('1.7669840027711121'),s]
 gp=angular_gradient(ctx,pR,a,b); gq=angular_gradient(ctx,qR,c,d)
 return (gp[0],gp[1],gq[0],gq[1],source_force(ctx,pR,a,b)-source_force(ctx,qR,c,d))

def J5(ctx,x):
 a,b,c,d,s=x
 pR=[ctx.mpf(1),ctx.mpf('3.7632172480656902'),ctx.mpf('0.4252867292159305')]
 qR=[ctx.mpf(1),ctx.mpf('1.7669840027711121'),s]
 p01,p02,p12=profile_edges(ctx,pR,a,b)
 q01,q02,q12=profile_edges(ctx,qR,c,d)
 J=[[ctx.mpf(0) for _ in range(5)] for __ in range(5)]
 # P angular Hessian
 J[0][0]=p01['tt']+p12['tt']; J[0][1]=-p12['tt']
 J[1][0]=-p12['tt']; J[1][1]=p02['tt']+p12['tt']
 # Q angular Hessian
 J[2][2]=q01['tt']+q12['tt']; J[2][3]=-q12['tt']
 J[3][2]=-q12['tt']; J[3][3]=q02['tt']+q12['tt']
 # Q angular gradients versus r2=s
 J[2][4]=q12['bt']
 J[3][4]=q02['bt']-q12['bt']
 # force difference versus angles and s
 J[4][0]=p01['at']; J[4][1]=p02['at']
 J[4][2]=-q01['at']; J[4][3]=-q02['at']
 J[4][4]=-q02['ab']
 return J

def as_iv_point(x): return iv.mpf(x)
def mpf_iv_lo(x): return mp.mpf(x.a)
def mpf_iv_hi(x): return mp.mpf(x.b)

def root_box(x0):
 rad=ROOT_RADIUS
 return [iv.mpf(c)+iv.mpf([-rad.b,rad.b]) for c in x0]

def krawczyk():
 x0=CENTER; X=root_box(x0)
 G0=G5(iv,[as_iv_point(v) for v in x0])
 JX=J5(iv,X)
 J0=J5(mp,x0)
 A=mp.matrix(J0)**-1
 Aiv=[[iv.mpf(A[i,j]) for j in range(5)] for i in range(5)]
 K=[]; row_norm=[]
 for i in range(5):
  corr=iv.mpf(0); row_sum=iv.mpf(0)
  for j in range(5):
   corr += Aiv[i][j]*G0[j]
   Mij=iv.mpf(1 if i==j else 0)
   for k in range(5): Mij -= Aiv[i][k]*JX[k][j]
   row_sum += abs(Mij)
  # K_i = x0_i - A G(x0) + (I-AJ(X))(X-x0)
  ki=as_iv_point(x0[i])-corr
  for j in range(5):
   Mij=iv.mpf(1 if i==j else 0)
   for k in range(5): Mij -= Aiv[i][k]*JX[k][j]
   ki += Mij*(X[j]-as_iv_point(x0[j]))
  K.append(ki);row_norm.append(row_sum.b)
 incl=[]
 for i in range(5):
  incl.append((K[i].a > X[i].a) and (K[i].b < X[i].b))
 return {'X':[str(z) for z in X], 'G0':[str(z) for z in G0], 'K':[str(z) for z in K], 'inside':incl, 'row_sum_upper':[str(z) for z in row_norm], 'all_inside':all(incl), 'contraction':max(row_norm)<1}

def local_rect(center, half=mp.mpf('0.1')):
 return (center[0]-half,center[0]+half,center[1]-half,center[1]+half)

def rect_complement(local):
 a0,a1,b0,b1=local; edge=mp.mpf(4)  # exact integer, strictly larger than pi
 return [(-edge,edge,-edge,b0),(-edge,edge,b1,edge),(-edge,a0,b0,b1),(a1,edge,b0,b1)]

def cp_cq_potentials(X):
 rr=R.copy(); rr[4]=X[4]
 rp=[rr[i] for i in P]; rq=[rr[i] for i in Q]
 cp=F(rp,X[0],X[1]); cq=F(rq,X[2],X[3])
 u=[iv.mpf('0') for _ in range(5)]
 u[0]=iv.mpf('0.57511124'); u[1]=iv.mpf('-0.25224512')
 u[3]=iv.mpf('0.21401706')
 u[2]=cp-u[0]-u[1]; u[4]=cq-u[0]-u[3]
 return rr,cp,cq,u

def certify_global_and_finite_lp():
 X=root_box(CENTER)
 rr,cp,cq,u=cp_cq_potentials(X)
 # Strict angular convexity on a closed local box containing the certified root.
 local_data=[]
 for name, q, j, k in [('P',P,0,1),('Q',Q,2,3)]:
  rad=[rr[i] for i in q]
  box=local_rect(CENTER[j:k+1])
  A=iv.mpf([box[0],box[1]])
  B=iv.mpf([box[2],box[3]])
  H=hessang(rad,A,B)
  det=H[0][0]*H[1][1]-H[0][1]*H[1][0]
  local_data.append({'profile':name,'local_box':[str(z) for z in box], 'H11':str(H[0][0]), 'det':str(det), 'PD':(H[0][0].a>0 and det.a>0)})
 # Global search outside each local convex box; strict interval LB exceeds the enclosed contact value.
 glob=[]
 for name,q,j,k,contact in [('P',P,0,1,cp),('Q',Q,2,3,cq)]:
  rad=[rr[i] for i in q]
  rect=rect_complement(local_rect(CENTER[j:k+1]))
  result=bnb(rad,contact,rect,max_nodes=5_000_000,max_depth=90)
  result['profile']=name
  glob.append(result)
 # All 33 noncontact shell triples: global angular lower bound exceeds the dual sum by at least 0.006.
 noncontact=[]; edge=mp.mpf(4)  # exact interval cover for [-pi,pi]^2
 triples=list(itertools.combinations_with_replacement(range(5),3))
 for q in triples:
  if q in (P,Q): continue
  rad=[rr[i] for i in q]
  pot=u[q[0]]+u[q[1]]+u[q[2]]
  result=bnb(rad,pot+iv.mpf('0.006'),[(-edge,edge,-edge,edge)],max_nodes=5_000_000,max_depth=90)
  result['q']=q
  noncontact.append(result)
  print('triple',q,result,flush=True)
 return {'contact_costs':{'P':str(cp),'Q':str(cq)},
         'dual_potentials':[str(v) for v in u],
         'local_strict_convexity':local_data,
         'global_contact_exclusion':glob,
         'noncontact_triples':noncontact,
         'all_contact_PD':all(z['PD'] for z in local_data),
         'all_global_contact':all(z['certified'] for z in glob),
         'all_noncontact':all(z['certified'] for z in noncontact)}

# Alternative global covering coordinates: after fixing angle 0 at the first particle,
# every configuration is covered by the two cyclic orders 0-1-2 and 0-2-1, with
# successive gaps g1,g2,g3 >= 0 and g1+g2+g3=2*pi. This is an exact parametrization.
TWO_PI=2*iv.pi
GAP_EDGE=mp.mpf(7)     # exact integer edge; 2*pi < 7, so this covers the closed gap simplex

def gap_lower(r, order, g10,g11,g20,g21):
 # Boxes lie in the exact rational square [0,7]^2. Every valid configuration
 # has g3=2*pi-g1-g2 >= 0; interval clipping below retains all such points.
 A=iv.mpf([g10,g11])
 B=iv.mpf([g20,g21])
 G3=TWO_PI-A-B
 if G3.b < 0: return None
 g30=iv.mpf(0).a if G3.a < 0 else G3.a
 # Since 2*pi < 7 and A,B are nonnegative, G3.b is already below 7.
 C=iv.mpf([g30,G3.b])
 p0,p1,p2=(r[i] for i in order)
 # Since a gap is an unsigned cyclic increment, each order contributes its three edge distances.
 ds=[p0*p0+p1*p1-2*p0*p1*iv.cos(A),
     p1*p1+p2*p2-2*p1*p2*iv.cos(B),
     p2*p2+p0*p0-2*p2*p0*iv.cos(C)]
 if any(d.b<=0 for d in ds): return iv.mpf([0,mp.inf])
 return sum((1/iv.sqrt(d.b) for d in ds),iv.mpf(0))

def gap_bnb(r, order, threshold, rects, max_nodes=5_000_000, max_depth=90):
 heap=[]; serial=0; nodes=0; leaves=0; skipped=0; maxd=0; min_margin=None
 for a0,a1,b0,b1 in rects:
  lb=gap_lower(r,order,a0,a1,b0,b1)
  if lb is None: skipped+=1;continue
  heappush(heap,(float(lb.a),serial,a0,a1,b0,b1,0,lb));serial+=1
 while heap:
  _,_,a0,a1,b0,b1,d,lb=heappop(heap);nodes+=1;maxd=max(maxd,d)
  if lb.a > threshold.b:
   leaves+=1
   m=(lb-threshold).a
   if min_margin is None or m<min_margin:min_margin=m
   continue
  if nodes>=max_nodes:
   return {'certified':False,'nodes':nodes,'leaves':leaves,'max_depth':maxd,'remaining':len(heap)+1,'min_margin_lower':None if min_margin is None else str(iv.mpf([min_margin,min_margin]))}
  if d>=max_depth:
   return {'certified':False,'nodes':nodes,'leaves':leaves,'max_depth':maxd,'remaining':len(heap)+1,'min_margin_lower':None if min_margin is None else str(iv.mpf([min_margin,min_margin])),'depth_fail':(str(a0),str(a1),str(b0),str(b1),str(lb))}
  wa=a1-a0;wb=b1-b0
  if wa>=wb:
   m=(a0+a1)/2
   for lo,hi in ((a0,m),(m,a1)):
    z=gap_lower(r,order,lo,hi,b0,b1)
    if z is None:skipped+=1;continue
    heappush(heap,(float(z.a),serial,lo,hi,b0,b1,d+1,z));serial+=1
  else:
   m=(b0+b1)/2
   for lo,hi in ((b0,m),(m,b1)):
    z=gap_lower(r,order,a0,a1,lo,hi)
    if z is None:skipped+=1;continue
    heappush(heap,(float(z.a),serial,a0,a1,lo,hi,d+1,z));serial+=1
 return {'certified':True,'nodes':nodes,'leaves':leaves,'skipped':skipped,'max_depth':maxd,'min_margin_lower':str(iv.mpf([min_margin,min_margin]))}

def root_angles_to_gap(a,b):
 """Outward interval transform of a root angle box to its cyclic-gap chart."""
 def mod_2pi(x):
  if x.a > 0: return x
  if x.b < 0: return x+TWO_PI
  raise ValueError('root angle box crosses the zero cut')
 aa=mod_2pi(a); bb=mod_2pi(b)
 if aa.b < bb.a:
  return (0,1,2),(aa,bb-aa)
 if bb.b < aa.a:
  return (0,2,1),(bb,aa-bb)
 raise ValueError('root angle ordering is not certified')

def gap_local(order, center, half=mp.mpf('0.04')):
 (g1,g2)=center
 return (g1-half,g1+half,g2-half,g2+half)

def gap_rect_complement(local):
 a0,a1,b0,b1=local;edge=GAP_EDGE
 return [(mp.mpf(0),edge,mp.mpf(0),b0),
         (mp.mpf(0),edge,b1,edge),
         (mp.mpf(0),a0,b0,b1),
         (a1,edge,b0,b1)]

def gap_to_angle_box(order, local):
 a0,a1,b0,b1=local
 # Interval-valued affine transform; use interval 2*pi, never scalar mp.pi.
 A=iv.mpf([a0,a1])
 B=iv.mpf([b0,b1])
 theta_second=A+B-TWO_PI
 if order==(0,1,2):
  alpha=A
  beta=theta_second
 else:
  beta=A
  alpha=theta_second
 return alpha,beta

def interval_root_in_gap_box(root_gaps, local):
 a0,a1,b0,b1=local
 return (root_gaps[0].a > a0 and root_gaps[0].b < a1 and
         root_gaps[1].a > b0 and root_gaps[1].b < b1)

def certify_gap_global_and_lp():
 X=root_box(CENTER)
 rr,cp,cq,u=cp_cq_potentials(X)
 local_results=[]; contact_result=[]
 # Each contact has two reflected angular minima, one in each cyclic order.
 for name,q,j,k,contact_center in [('P',P,0,1,(CENTER[0],CENTER[1])),('Q',Q,2,3,(CENTER[2],CENTER[3]))]:
  rad=[rr[i] for i in q]
  contact=cp if name=='P' else cq
  root_angles=[X[j:k+1],[-X[j],-X[k]]]
  profile_local=[]
  for idx,(a_box,b_box) in enumerate(root_angles):
   order, root_gaps = root_angles_to_gap(a_box,b_box)
   gapcenter=tuple((mp.mpf(g.a)+mp.mpf(g.b))/2 for g in root_gaps)
   loc=gap_local(order,gapcenter)
   root_inside=interval_root_in_gap_box(root_gaps,loc)
   abox,bbox=gap_to_angle_box(order,loc)
   H=hessang(rad,abox,bbox);det=H[0][0]*H[1][1]-H[0][1]*H[1][0]
   pdat={'profile':name,'mirror_index':idx,'order':order,'gap_center':[str(z) for z in gapcenter],
         'gap_local':[str(z) for z in loc],'angle_box':[str(abox),str(bbox)],
         'root_gaps':[str(z) for z in root_gaps], 'root_inside_local':root_inside,
         'H11':str(H[0][0]),'det':str(det),'PD':(H[0][0].a>0 and det.a>0)}
   local_results.append(pdat);profile_local.append((order,loc))
  for rel_order,loc in profile_local:
   result=gap_bnb(rad,rel_order,contact,gap_rect_complement(loc),max_nodes=5_000_000,max_depth=100)
   result.update({'profile':name,'order':rel_order})
   contact_result.append(result)
 # Finite shell dual: all 33 noncontacts, both cyclic orders.
 triples=list(itertools.combinations_with_replacement(range(5),3))
 noncontact=[]
 for q in triples:
  if q in (P,Q):continue
  rad=[rr[i] for i in q];pot=u[q[0]]+u[q[1]]+u[q[2]]
  for ord0 in ((0,1,2),(0,2,1)):
   res=gap_bnb(rad,ord0,pot+iv.mpf('0.006'),[(mp.mpf(0),GAP_EDGE,mp.mpf(0),GAP_EDGE)],max_nodes=5_000_000,max_depth=100)
   res.update({'q':q,'order':ord0});noncontact.append(res)
   print('gap-triple',q,ord0,res,flush=True)
 return {'contact_costs':{'P':str(cp),'Q':str(cq)},'dual_potentials':[str(z) for z in u],
  'local_reflection_boxes':local_results,'global_contact_exclusion':contact_result,
  'noncontact_triples':noncontact,
  'all_local_PD':all(z['PD'] for z in local_results),
  'all_root_gaps_inside_local':all(z['root_inside_local'] for z in local_results),
  'all_global_contact':all(z['certified'] for z in contact_result),
  'all_noncontact':all(z['certified'] for z in noncontact)}

def certify_reduced_radial(X):
 """Interval certificate for all reduced radial cross-derivatives at P and Q."""
 rr=R.copy(); rr[4]=X[4]
 out=[]
 for name,q,j,k in [('P',P,0,1),('Q',Q,2,3)]:
  radii=[rr[i] for i in q]
  angle_boxes=((X[j],X[k]),(-X[j],-X[k]))
  for mirror,(alpha,beta) in enumerate(angle_boxes):
   S,det,H=reduced_radial_hessian(iv,radii,alpha,beta)
   cross={'c01':S[0][1],'c02':S[0][2],'c12':S[1][2]}
   pos={key:(value.a>0) for key,value in cross.items()}
   out.append({'profile':name,'mirror_index':mirror,
               'angular_det':str(det),'angular_hessian_entries':[str(x) for x in H],
               'angular_pd':(H[0].a>0 and det.a>0),
               'cross_derivatives':{key:str(value) for key,value in cross.items()},
               'strictly_positive':pos,'all_nonzero':all(pos.values())})
 return {'root_box':[str(x) for x in X], 'branches':out,
         'all_contact_branch_cross_derivatives_positive':all(z['all_nonzero'] for z in out)}

if __name__=='__main__':
 import sys, time
 if len(sys.argv)>1 and sys.argv[1]=='all':
  start=time.time()
  fr=krawczyk(); X=root_box(CENTER)
  ans={'force_root':fr,'global_and_lp':certify_gap_global_and_lp(),
       'reduced_radial_derivatives':certify_reduced_radial(X)}
  ans['elapsed_seconds']=time.time()-start
  out='validated_certificate.json'
  with open(out,'w') as f: json.dump(ans,f,indent=2)
  print('wrote',out,'elapsed',ans['elapsed_seconds'],flush=True)
  print(json.dumps(ans['global_and_lp']['global_contact_exclusion'],indent=2),flush=True)
 else:
  print(json.dumps(krawczyk(),indent=2))
