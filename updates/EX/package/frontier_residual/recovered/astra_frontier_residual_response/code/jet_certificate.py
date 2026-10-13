"""Exact, a-posteriori infinite-chain response-jet certificate.
No optimizer residual is trusted. All Pauli output rows are regenerated and included.
The fast exact compiler is restricted to real ZZ/ZIZ parameters, t=1, d=2 and span<=18.
"""
from __future__ import annotations
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json,math,time,argparse,hashlib,resource
import numpy as np
import scipy.sparse as sp
from fast_algebra import build
from local_solver import nullspace_columns,canon,reflect
from prior_exact import integer_matrix,safe_dot,weighted_squares

def sqrt_upper(x:F,bits=48)->F:
    if x<0:raise ValueError('negative squared norm')
    scale=1<<bits
    n=(x.numerator*scale*scale+x.denominator-1)//x.denominator
    k=math.isqrt(n)
    if k*k<n:k+=1
    out=F(k,scale)
    assert out*out>=x
    return out

def idot(a,b,q=None):
    if q is None:return sum(int(x)*int(y) for x,y in zip(a,b))
    return sum(int(x)*int(y)*int(z) for x,y,z in zip(a,b,q))

def compile_exact(fw,gw,FN,GN,den,parameters):
    tt,uu,vv,dd=[F(str(parameters[k])) for k in ['t','U','V','d']]
    if tt!=1 or dd!=2:raise ValueError('checked fixture requires t=1,d=2')
    L=max((x|z).bit_length() for x,z in fw+gw)
    if L>18:raise ValueError('fast encoding supports span<=18')
    for pp,ww in [(1,fw),(0,gw)]:
      if len(ww)!=len(set(ww)):raise ValueError('duplicate word')
      for x,z in ww:
        assert (x|z)&1 and (x,z)<reflect((x,z))
        assert x.bit_count()%2==0 and z.bit_count()%2==1 and (x&z).bit_count()%2==pp
    scale=2*math.lcm(tt.denominator,uu.denominator,vv.denominator)
    if 100*(L+4)*max(abs((q*scale).numerator) for q in (tt,uu,vv,F(1)))>=2**50:
        raise ValueError('coefficient assembly exceeds exact binary64 range')
    er,AF=build(fw,float(tt*scale),float(uu*scale),float(vv*scale))
    orr,AG=build(gw,float(tt*scale),float(uu*scale),float(vv*scale))
    be,BF=build(fw,0.,0.,float(scale));bo,BG=build(gw,0.,0.,float(scale))
    AF,AG,BF,BG=[integer_matrix(a,1) for a in [AF,AG,BF,BG]]
    aff=[safe_dot(AF,a) for a in FN];agg=[safe_dot(AG,a) for a in GN]
    bff=[safe_dot(BF,a) for a in FN];bgg=[safe_dot(BG,a) for a in GN]
    for av in aff:
      assert all(int(c)==0 for w,c in zip(er,av) if w[0]==0),'population imbalance'
    assert all(w[0] for w in be+bo), 'diagonal perturbation created population'
    qf=[w[0].bit_count() for w in fw];qg=[w[0].bit_count() for w in gw]
    er_i={w:i for i,w in enumerate(er)};be_i={w:i for i,w in enumerate(be)}
    matchA=[(i,er_i[w]) for i,w in enumerate(gw) if w in er_i]
    matchB=[(i,be_i[w]) for i,w in enumerate(gw) if w in be_i]
    def ag_cross(a,b):return sum(int(aff[a][j])*int(GN[b][i]) for i,j in matchA)
    def bg_cross(a,b):return sum(int(bff[a][j])*int(GN[b][i]) for i,j in matchB)
    M=len(FN)-1;dden=den*den
    # Polynomial derivative coefficients for the corrected physical D(s)=4F(s).
    Fder=[]
    for k in range(2*M+2):
      ans=-2*tt*F(int(FN[k][fw.index((3,1))]),den) if k<=M else F(0)
      for a in range(max(0,k-M),min(M,k)+1):
        b=k-a;cc=math.comb(k,a)
        ans+=cc*(F(-2*idot(FN[a],FN[b],qf)+2*idot(GN[a],GN[b],qg),dden)+F(4*ag_cross(a,b),scale*dden))
      if k:
       for a in range(max(0,k-1-M),min(M,k-1)+1):
        b=k-1-a;cc=k*math.comb(k-1,a)
        ans+=cc*F(4*bg_cross(a,b),scale*dden)
      Fder.append(4*ans)
    # Complete residual coefficient polynomials, never restricted to discovery dictionaries.
    rO=[];rE=[];q2=[]
    for k in range(M+2):
      p=defaultdict(int);q=defaultdict(int)
      if k<=M:
        for w,c,s in zip(fw,FN[k],qf):p[w]+=scale*int(c)*s
        for w,c in zip(orr,agg[k]):p[w]+=int(c)
        for w,c,s in zip(gw,GN[k],qg):q[w]+=scale*int(c)*s
        for w,c in zip(er,aff[k]):q[w]+=int(c)
      if k==0:
        jn=-tt*F(scale*den,2);assert jn.denominator==1;p[(3,1)]-=int(jn)
      else:
        for w,c in zip(bo,bgg[k-1]):p[w]+=k*int(c)
        for w,c in zip(be,bff[k-1]):q[w]+=k*int(c)
      p={w:c for w,c in p.items() if c};q={w:c for w,c in q.items() if c}
      assert all(w[0] for w in p.keys()|q.keys()),'residual population defect'
      def norm(v):return 2*weighted_squares(list(v.values()),[w[0].bit_count() for w in v],True)/((scale*den)**2)
      q2.append(norm(p)+norm(q));rO.append(p);rE.append(q)
    Q=[sqrt_upper(v) for v in q2]
    errs=[];w=F(1) # 4 Jstar(V1)/d=4*(1/2)/2
    for k in range(M+1):
      ans=F()
      for a in range(k+1):
       for b in range(k-a+1):
        c=k-a-b
        ans+=F(math.factorial(k),math.factorial(a)*math.factorial(b))*Q[a]*Q[b]*w**c
      errs.append(4*ans)
    # Classical value interval from the identical zeroth jets, independently expanded.
    low=-2*tt*F(int(FN[0][fw.index((3,1))]),den)-2*F(idot(FN[0],FN[0],qf),dden)-2*weighted_squares(aff[0],[w[0].bit_count() for w in er],True)/(scale*den)**2
    res=defaultdict(int)
    for w,c in zip(orr,agg[0]):res[w]-=int(c)
    res[(3,1)]-=scale*den//2
    res={w:c for w,c in res.items() if c}
    up=2*weighted_squares(list(res.values()),[w[0].bit_count() for w in res],True)/(scale*den)**2+F(2*idot(GN[0],GN[0],qg),dden)
    assert up-low==q2[0],('zero jet gap mismatch',up-low,q2[0])
    def normdict(v):return 2*weighted_squares(list(v.values()),[w[0].bit_count() for w in v],True)/(scale*den)**2
    assert Fder[0]/4==low+normdict(rE[0])==up-normdict(rO[0]),'corrected-value identity'
    def gram(fields):
      size=len(fields);out=[[F() for _ in range(size)] for _ in range(size)]
      for i in range(size):
       for j in range(i,size):
        aa,bb=fields[i],fields[j]
        if len(aa)>len(bb):aa,bb=bb,aa
        sums=defaultdict(int)
        for word,c in aa.items():
          cc=bb.get(word,0)
          if cc:sums[word[0].bit_count()]+=int(c)*int(cc)
        val=2*sum((F(a,q) for q,a in sums.items()),F())/((scale*den)**2)
        out[i][j]=val;out[j][i]=val
      return out
    GO=gram(rO);GE=gram(rE)
    assert all(GO[i][i]+GE[i][i]==q2[i] for i in range(M+2))
    def normpoly(mat):
      out=[F() for _ in range(2*M+3)]
      for i in range(M+2):
       for j in range(M+2):out[i+j]+=mat[i][j]/(math.factorial(i)*math.factorial(j))
      return out
    NO=normpoly(GO);NE=normpoly(GE)
    fc=[a/F(math.factorial(i)) for i,a in enumerate(Fder)]+[F(0)]
    lowpoly=[a-4*b for a,b in zip(fc,NE)];uppoly=[a+4*b for a,b in zip(fc,NO)]
    assert lowpoly[0]==4*low and uppoly[0]==4*up
    W=max((w[0]|w[1]).bit_length() for v in rO+rE for w in v)
    return dict(residual_odd_gram_exact=[[str(x) for x in row] for row in GO],residual_even_gram_exact=[[str(x) for x in row] for row in GE],lower_D_polynomial_exact=list(map(str,lowpoly)),upper_D_polynomial_exact=list(map(str,uppoly)),parameters={k:str(F(str(v))) for k,v in parameters.items()},order=M,denominator=str(den),scale=scale,full_output_span=W,min_finite_ring_size=2*W+1,f_basis=len(fw),g_basis=len(gw),commutator_nnz=sum(a.nnz for a in [AF,AG,BF,BG]),balance_exact=True,zero_jet_gap_exact=True,corrected_value_identity_exact=True,D_interval_exact=[str(4*low),str(4*up)],D_interval_float=[float(4*low),float(4*up)],D_width_float=float(4*(up-low)),residual_norms_squared_exact=list(map(str,q2)),residual_norm_upper_exact=list(map(str,Q)),corrected_D_derivatives_exact=list(map(str,Fder)),corrected_D_polynomial_exact=[str(a/F(math.factorial(i))) for i,a in enumerate(Fder)],D_jet_radii_exact=list(map(str,errs)),D_jet_intervals_float=[[float(Fder[k]-errs[k]),float(Fder[k]+errs[k])] for k in range(M+1)],full_residual_terms=[len(p)+len(q) for p,q in zip(rO,rE)])

def round_file(path,bits=36,output=None):
 start=time.perf_counter();path=Path(path);data=np.load(path)
 pars=json.loads(path.with_suffix('.json').read_text())['parameters']
 fw=[tuple(map(int,w)) for w in data['fw']];gw=[tuple(map(int,w)) for w in data['gw']]
 er,A=build(fw,1.,0.,0.);N,ent,free,rank=nullspace_columns(A[[w[0]==0 for w in er],:].tocsc())
 lcm=math.lcm(*(x.denominator for i,j,x in ent));den=(1<<bits)*lcm
 FN=[]
 for u in data['us']:
  v=np.rint(u*(1<<bits)).astype(np.int64);nums=[0]*len(fw)
  for i,j,x in ent:
   t=x*lcm;assert t.denominator==1;nums[i]+=t.numerator*int(v[j])
  FN.append(np.array(nums,dtype=np.int64))
 GN=np.rint(data['gs']*den).astype(np.int64)
 rec=compile_exact(fw,gw,np.array(FN),GN,den,pars)
 target=Path(output) if output else path.with_name(path.stem+'_jet_exact.npz')
 np.savez_compressed(target,fw=np.array(fw),gw=np.array(gw),FN=np.array(FN),GN=GN,den=np.array([den],dtype=np.int64),params=np.array([str(F(str(pars[k]))) for k in ['t','U','V','d']]))
 rec.update(witness_file=target.name,witness_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),rounding_bits=bits,verification_seconds=time.perf_counter()-start,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 target.with_suffix('.json').write_text(json.dumps(rec,indent=2));print(json.dumps(rec,indent=2),flush=True);return rec

def verify(path):
 start=time.perf_counter();p=Path(path);q=np.load(p);fw=[tuple(map(int,w)) for w in q['fw']];gw=[tuple(map(int,w)) for w in q['gw']]
 pars=dict(zip(['t','U','V','d'],q['params']));rec=compile_exact(fw,gw,q['FN'],q['GN'],int(q['den'][0]),pars)
 rec.update(verification_seconds=time.perf_counter()-start,witness_sha256=hashlib.sha256(p.read_bytes()).hexdigest());print(json.dumps(rec,indent=2));return rec
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('path');p.add_argument('--bits',type=int,default=36);p.add_argument('--verify',action='store_true');p.add_argument('--output');a=p.parse_args()
 if a.verify:verify(a.path)
 else:round_file(a.path,a.bits,a.output)
