"""Exact rational certificate for short-loop plus all-length-tail comparison."""
from short_tail_green_screen import *
from crossed_loop_influence import edgelist
import time
start=time.monotonic();cache=P/'raw_short_matrix_exact.json'
if cache.exists():raw=[[F(a)for a in row]for row in json.loads(cache.read_text())]
else:
 allvar=[]
 for typ in cat:
  allvar.append([(set(vs),edgelist(vs))for vs in variants(typ['cyclic_vertices'])])
 raw=[]
 for i,root in enumerate(cat):
  rv=set(map(tuple,root['cyclic_vertices']));re=edgelist(list(map(tuple,root['cyclic_vertices'])));row=[]
  for j,target in enumerate(cat):
   hard=0;soft=Counter()
   for vs,es in allvar[j]:
    shifts={(x-u,y-v)for x,y in rv for u,v in vs}
    for dx,dy in shifts:
     se={tuple(sorted(((x+dx,y+dy),(u+dx,v+dy))))for(x,y),(u,v)in es}
     if re&se:hard+=1
     else:soft[len(rv & {(x+dx,y+dy)for x,y in vs})]+=1
   mayer=F(hard)+sum((cnt*(1-F(3,5)**k)for k,cnt in soft.items()),F(0))
   row.append(F(target['activity'])*mayer)
  raw.append(row)
  if i%10==0:print('exactrow',i,'elapsed',time.monotonic()-start,flush=True)
 cache.write_text(json.dumps([[str(a)for a in row]for row in raw])+'\n')
Cexact=[[raw[i][j]*F(Ls[j],Ls[i])*tilt**Ls[j]for j in range(N)]for i in range(N)]
bexact=[(nss*as_t+ntt*at_t)/L+mt*(1 if rr==0 else F(1,L))for nss,ntt,rr,L in zip(ns,nt,rs,Ls)]
Asexact=[s/5+t/2 for s,t in zip(svec,tvec)];Atexact=[s/2+7*t/20 for s,t in zip(svec,tvec)]
# Select weights numerically, then verify all inequalities with Fractions.
vF=[F(round(float(a)*10**9),10**9)for a in v]
rawq=F(907806,10**6)
ratios=[]
for i in range(N):ratios.append((sum((Cexact[i][j]*vF[j]for j in range(N)),F(0))+bexact[i]*vF[-1])/vF[i])
ratios.append((max(sum((a*b for a,b in zip(Asexact,vF)),F(0)),sum((a*b for a,b in zip(Atexact,vF)),F(0)))+d*vF[-1])/vF[-1])
assert max(ratios)<rawq
# Nonlinear Schur map has tail value max(As·v,At·v)/(1-d).
sv=np.ones(N)
for it in range(10000):
 nv=Cs@sv+bvec*max(As@sv,At@sv)/(1-float(d));nv/=max(nv)
 if max(abs(nv-sv))<1e-13:sv=nv;break
 sv=nv
svF=[F(round(float(a)*10**9),10**9)for a in sv]
tailF=max(sum((a*b for a,b in zip(Asexact,svF)),F(0)),sum((a*b for a,b in zip(Atexact,svF)),F(0)))/(1-d)
sratios=[(sum((Cexact[i][j]*svF[j]for j in range(N)),F(0))+bexact[i]*tailF)/svF[i]for i in range(N)]
sq=F(857586,10**6);assert max(sratios)<sq
out=dict(short_types=N,tail_min_length=14,tilt_exact=str(tilt),tail_norm_upper=str(d),tail_norm_upper_decimal=float(d),weighted_full_kernel_upper=str(rawq),weighted_full_max_ratio=float(max(ratios)),full_weight_factors=[str(a)for a in vF],full_weight_factor_min=float(min(vF)),full_weight_factor_max=float(max(vF)),schur_norm_upper=str(sq),schur_max_ratio=float(max(sratios)),schur_weights=[str(a)for a in svF],schur_tail_weight=str(tailF),schur_weighted_green_upper=str(1/(1-sq)),notes='Every finite coefficient and comparison inequality is exact rational. Full kernel weights are L_i times type factor, not unmodified lengths. Tail moments inherit the independent all-length interval certificate. Schur bound is a monotone nonlinear comparison norm, not a claim that one fixed tail row entrywise dominates all spatial sources.',elapsed_seconds=time.monotonic()-start)
(P/'short_tail_exact_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:a for k,a in out.items()if not isinstance(a,list)},indent=2))
# Source-specific Green bound: expected number of ancestor nodes, includingroot.
source=[F(1,L)for L in Ls]+[F(1,14)]
u=np.zeros(N+1)
for it in range(10000):
 nu=np.array([float(a)for a in source])+np.r_[Cs@u[:N]+bvec*u[-1],max(As@u[:N],At@u[:N])+float(d)*u[-1]]
 if max(abs(nu-u))<1e-12:u=nu;break
 u=nu
uF=[F(int(np.ceil(a*10**9)),10**9)for a in u]
def exact_map(a):
 return [sum((Cexact[i][j]*a[j]for j in range(N)),F(0))+bexact[i]*a[-1]for i in range(N)]+[max(sum((aa*bb for aa,bb in zip(Asexact,a)),F(0)),sum((aa*bb for aa,bb in zip(Atexact,a)),F(0)))+d*a[-1]]
tu=exact_map(uF);correction=max([F(0)]+[(source[i]+tu[i]-uF[i])/((1-rawq)*vF[i])for i in range(N+1)])+F(1,10**10)
uF=[a+correction*b for a,b in zip(uF,vF)];tu=exact_map(uF);assert all(uF[i]>=source[i]+tu[i]for i in range(N+1))
rootdensity=[F(c['activity'])*tilt**c['length']*c['length']*len(variants(c['cyclic_vertices']))for c in cat]
Rtotal=6*(Gs+Gt)+F(18,5)*(2*Gs*Gs+Gt*Gt);Rtail=Rtotal-sum(rootdensity,F(0));assert Rtail>0
expected=sum((a*b for a,b in zip(rootdensity,uF)),F(0))+Rtail*uF[-1]
amin=min([F(L)*a for L,a in zip(Ls,vF)]+[F(14)])
theta=(1-rawq)/2;timeprefactor=Rtotal/(amin*theta)
resource=dict(expected_distinct_ancestor_count_per_vertex_upper=str(expected),expected_distinct_ancestor_count_per_vertex_decimal=float(expected),count_green_normalized_type_caps=[str(a)for a in uF],minimum_full_weight=str(amin),tilted_root_length_density_upper=str(Rtotal),tilted_root_length_density_decimal=float(Rtotal),tail_root_length_density_upper=str(Rtail),physical_time_exponent=str(theta),physical_time_tail_prefactor_per_vertex_upper=str(timeprefactor),physical_time_tail_prefactor_per_vertex_decimal=float(timeprefactor),interpretation='For all candidate root loops alive at time zero inside an N-vertex finite box, the expected size of the union of ancestors is at most this constant times N. Summing separate root clans overcounts their union. This counts true loop cylinders, not null proposal attempts or cost per oracle call. The probability of any needed birth earlier than -t is at most prefactor times N times exp(-theta t).')
(P/'short_tail_source_resource_certificate.json').write_text(json.dumps(resource,indent=2)+'\n')
print('SOURCE_RESOURCE',json.dumps({k:a for k,a in resource.items()if not isinstance(a,list)},indent=2))
