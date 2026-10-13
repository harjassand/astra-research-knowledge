"""Exact multivariate response certificate, including physical d uncertainty.
Uses checked integer limbs with BLAS: every product and absolute partial sum <2**52.
Axes V,U,d; trial coefficients are partial derivatives at the recorded centre.
"""
from __future__ import annotations
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import math,json,time,hashlib,argparse,resource
import numpy as np
import scipy.sparse as sp
from fast_algebra import build
from local_solver import nullspace_columns,reflect
from prior_exact import integer_matrix,safe_dot
from multi_solver import indices,predecessor
from jet_solver import align

def fac(a):return math.prod(math.factorial(int(x)) for x in a)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def inc(a,i):
 b=list(a);b[i]+=1;return tuple(b)
def objzero(m,n):return np.zeros((m,n),dtype=object)

def exact_dot(A,B):
 """Return A @ B.T as arbitrary-precision integers, A,B int64.
 Each limb matrix product is provably exact under IEEE binary64 arithmetic.
 """
 A=np.asarray(A,dtype=np.int64);B=np.asarray(B,dtype=np.int64)
 if A.shape[1]!=B.shape[1]:raise ValueError('shape')
 n=A.shape[1];out=objzero(len(A),len(B))
 if not n:return out
 vmax=max(int(np.max(np.abs(A),initial=0)),int(np.max(np.abs(B),initial=0)))
 if vmax>=2**62:raise OverflowError('input limb range')
 k=max(1,(vmax.bit_length()+13)//14);base=1<<14
 assert n*(base-1)**2<2**52
 sa=np.sign(A);sb=np.sign(B);aa=np.abs(A);bb=np.abs(B)
 al=[np.asarray(((aa>>(14*i))&(base-1))*sa,dtype=np.float64) for i in range(k)]
 bl=[np.asarray(((bb>>(14*i))&(base-1))*sb,dtype=np.float64) for i in range(k)]
 for i,x in enumerate(al):
  if not np.any(x):continue
  for j,y in enumerate(bl):
   if not np.any(y):continue
   v=x@y.T
   assert np.max(np.abs(v),initial=0)<2**52 and np.all(v==np.rint(v))
   out+=v.astype(np.int64).astype(object)*(1<<(14*(i+j)))
 return out

def weighted_gram(A,weights,den=1,B=None,inverse=True,factor=2):
 if B is None:B=A
 out=objzero(len(A),len(B));weights=np.asarray(weights,dtype=int)
 for q in sorted(set(weights)):
  if not q:
   assert not np.any(A[:,weights==0]),'undamped contribution'
   continue
  mask=weights==q;X=exact_dot(A[:,mask],B[:,mask]);mult=F(factor,den*int(q)) if inverse else F(factor*int(q),den)
  for i in range(len(A)):
   for j in range(len(B)):out[i,j]+=mult*int(X[i,j])
 return out

def polydump(p):return [[list(a),str(c)] for a,c in sorted(p.items(),key=lambda z:(sum(z[0]),z[0])) if c]
def polyload(p):return {tuple(a):F(c) for a,c in p}

def compile_exact(fw,gw,FN,GN,den,inds,params):
 start=time.perf_counter();t,U,V,d=[F(str(params[k])) for k in ['t','U','V','d']]
 if t!=1 or d!=2:raise ValueError('implemented centre requires t=1,d0=2')
 if len(fw)!=len(set(fw)) or len(gw)!=len(set(gw)):raise ValueError('duplicate')
 for parity,words in [(1,fw),(0,gw)]:
  for x,z in words:
   assert (x|z)&1 and (x,z)<reflect((x,z))
   assert x.bit_count()%2==0 and z.bit_count()%2==1 and (x&z).bit_count()%2==parity
   if (x|z).bit_length()>18:raise ValueError('span')
 scale=2*math.lcm(t.denominator,U.denominator,V.denominator)
 if 3000*max(abs(int(x*scale)) for x in [t,U,V,F(1)])>=2**50:raise ValueError('assembly')
 mats=[];rows=[]
 for words in [fw,gw]:
  item=[];rws=[]
  for pars in [(t,U,V),(0,0,1),(0,1,0)]:
   rr,aa=build(words,*[float(F(x)*scale) for x in pars]);rws.append(rr);item.append(integer_matrix(aa,1))
  rows.append(rws);mats.append(item)
 er=sorted(set(gw).union(*map(set,rows[0])));orr=sorted(set(fw)|{(3,1)}|set().union(*map(set,rows[1])))
 AF,BF,UF=[align(rr,aa,er).astype(np.int64) for rr,aa in zip(rows[0],mats[0])]
 AG,BG,UG=[align(rr,aa,orr).astype(np.int64) for rr,aa in zip(rows[1],mats[1])]
 ei={w:i for i,w in enumerate(er)};oi={w:i for i,w in enumerate(orr)};gidx=np.array([ei[w] for w in gw]);fidx=np.array([oi[w] for w in fw])
 qf=np.array([w[0].bit_count() for w in fw]);qg=np.array([w[0].bit_count() for w in gw]);qe=np.array([w[0].bit_count() for w in er]);qo=np.array([w[0].bit_count() for w in orr])
 Fa=[np.array([safe_dot(M,a) for a in FN]) for M in [AF,BF,UF]]
 Ga=[np.array([safe_dot(M,a) for a in GN]) for M in [AG,BG,UG]]
 assert not np.any(Fa[0][:,qe==0]),'exact population imbalance'
 assert not np.any(Fa[1][:,qe==0]) and not np.any(Fa[2][:,qe==0])
 assert max(int(np.max(np.abs(x),initial=0)) for x in Fa+Ga)<2**58
 order=max(map(sum,inds));rinds=indices(order+1);ip={a:i for i,a in enumerate(inds)}
 RO=np.zeros((len(rinds),len(orr)),dtype=np.int64);RE=np.zeros((len(rinds),len(er)),dtype=np.int64)
 for k,a in enumerate(rinds):
  if a in ip:
   ix=ip[a];RO[k]=Ga[0][ix];RE[k]=Fa[0][ix]
   RO[k,fidx]+=scale*qf*FN[ix];RE[k,gidx]+=scale*qg*GN[ix]
  if not any(a):RO[k,oi[(3,1)]]+=scale*den//2
  for ax,num in enumerate(a):
   if not num:continue
   b=predecessor(a,ax)
   if b not in ip:continue
   ix=ip[b]
   if ax<2:RO[k]+=num*Ga[ax+1][ix];RE[k]+=num*Fa[ax+1][ix]
   else:
    assert scale%2==0
    RO[k,fidx]+=num*(scale//2)*qf*FN[ix];RE[k,gidx]+=num*(scale//2)*qg*GN[ix]
 assert not np.any(RE[:,qe==0]),'residual population defect'
 # Checked limb bounds include all sums and degree factors.
 assert max(int(np.max(np.abs(RO),initial=0)),int(np.max(np.abs(RE),initial=0)))<2**60
 print('assembled exact residuals',RO.shape,RE.shape,flush=True)
 rd=(scale*den)**2
 GO=weighted_gram(RO,qo,rd);GE=weighted_gram(RE,qe,rd)
 print('exact residual Grams',time.perf_counter()-start,flush=True)
 SF=weighted_gram(FN,qf,den*den,inverse=False)
 # g may have undamped coefficients; don't require zeros for direct S norm.
 SG=objzero(len(GN),len(GN))
 for q in sorted(set(qg)):
  if q:
   X=exact_dot(GN[:,qg==q],GN[:,qg==q])
   for i in range(len(GN)):
    for j in range(len(GN)):SG[i,j]+=F(2*int(q)*int(X[i,j]),den*den)
 crosses=[]
 for X in Fa:
  Y=exact_dot(X[:,gidx],GN);crosses.append([[F(2*int(c),scale*den*den) for c in row] for row in Y])
 ph=defaultdict(F);jix=fw.index((3,1))
 for i,a in enumerate(inds):
  ph[a]+=F(-8*int(FN[i,jix]),den*fac(a))
  for j,b in enumerate(inds):
   ab=add(a,b);ff=fac(a)*fac(b)
   ph[ab]+=F(4,ff)*(-SF[i,j]+SG[i,j]+2*crosses[0][i][j])
   ph[inc(ab,2)]+=F(2,ff)*(-SF[i,j]+SG[i,j])
   ph[inc(ab,0)]+=F(8,ff)*crosses[1][i][j]
   ph[inc(ab,1)]+=F(8,ff)*crosses[2][i][j]
 def normpoly(G):
  p=defaultdict(F)
  for i,a in enumerate(rinds):
   for j,b in enumerate(rinds):p[add(a,b)]+=G[i,j]/(fac(a)*fac(b))
  return p
 po,pe=normpoly(GO),normpoly(GE)
 zero=(0,0,0);low=ph[zero]-4*pe[zero];up=ph[zero]+4*po[zero]
 # Independent zeroth lower expression in original normalization.
 jf=F(-int(FN[0,jix]),den)
 na=weighted_gram(Fa[0][0:1],qe,rd)[0,0]
 independentlow=4*(2*jf-SF[0,0]-na)
 assert low==independentlow,(low,independentlow)
 W=max((x|z).bit_length() for x,z in er+orr)
 out=dict(parameters={k:str(F(str(params[k]))) for k in params},axes=['V','U','d'],order=order,trial_indices=[list(a) for a in inds],residual_indices=[list(a) for a in rinds],denominator=str(den),assembly_scale=scale,f_basis=len(fw),g_basis=len(gw),commutator_nnz=sum(x.nnz for x in [AF,AG,BF,BG,UF,UG]),full_output_span=W,min_ring_size=2*W+1,balance_exact=True,residual_odd_gram_exact=[[str(c) for c in row] for row in GO],residual_even_gram_exact=[[str(c) for c in row] for row in GE],corrected_D_poly=polydump(ph),residual_odd_norm_poly=polydump(po),residual_even_norm_poly=polydump(pe),D_interval_exact=[str(low),str(up)],D_interval_float=[float(low),float(up)],residual_norm_squared_at_centre=[float(GO[k,k]+GE[k,k]) for k in range(len(rinds))],verification_seconds=time.perf_counter()-start,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 return out

def round_file(path,out,bits=34):
 p=Path(path);data=np.load(p);pars=json.loads(p.with_suffix('.json').read_text())['parameters'];fw=[tuple(map(int,w)) for w in data['fw']];gw=[tuple(map(int,w)) for w in data['gw']];inds=[tuple(map(int,a)) for a in data['indices']]
 er,A=build(fw,1.,0.,0.);N,ent,free,rank=nullspace_columns(A[[w[0]==0 for w in er],:].tocsc())
 lcm=math.lcm(*(x.denominator for i,j,x in ent));den=(1<<bits)*lcm
 FN=[]
 for u in data['us']:
  vals=np.rint(u*(1<<bits)).astype(np.int64);nums=[0]*len(fw)
  for i,j,x in ent:nums[i]+=int(x*lcm)*int(vals[j])
  FN.append(np.array(nums,dtype=np.int64))
 GN=np.rint(data['gs']*den).astype(np.int64);FN=np.array(FN)
 rec=compile_exact(fw,gw,FN,GN,den,inds,pars)
 out=Path(out);out.parent.mkdir(exist_ok=True,parents=True)
 np.savez_compressed(str(out)+'.npz',fw=np.array(fw),gw=np.array(gw),FN=FN,GN=GN,den=np.array([den],dtype=np.int64),indices=np.array(inds,dtype=np.int64),params=np.array([str(F(str(pars[k]))) for k in ['t','U','V','d']]))
 rec.update(rounding_bits=bits,witness_sha256=hashlib.sha256(out.with_suffix('.npz').read_bytes()).hexdigest(),witness_file=out.with_suffix('.npz').name)
 out.with_suffix('.json').write_text(json.dumps(rec,indent=2));print('certificate',rec['D_interval_float'],rec['verification_seconds'],flush=True);return rec
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('path');p.add_argument('out');p.add_argument('--bits',type=int,default=34);a=p.parse_args();round_file(a.path,a.out,a.bits)
