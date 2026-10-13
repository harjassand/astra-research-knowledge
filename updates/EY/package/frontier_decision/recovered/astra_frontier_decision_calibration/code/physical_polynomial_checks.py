"""Check multivariate physical polynomials against directly evaluated trial fields.
This uses the saved small quantum packet, rather than a model response oracle.
"""
from pathlib import Path
from fractions import Fraction as F
import math,json,time
import numpy as np
from fast_algebra import build
from jet_solver import align
from prior_exact import integer_matrix,safe_dot
from multi_certificate import exact_dot,weighted_gram,compile_exact
from multi_poly import load,evalpoly
ROOT=Path(__file__).resolve().parent.parent

def run():
 start=time.perf_counter();path=ROOT/'results/anchors/V1p0_exact';rec=json.loads(path.with_suffix('.json').read_text())
 with np.load(path.with_suffix('.npz'),allow_pickle=False) as data:
  fw=[tuple(map(int,w)) for w in data['fw']];gw=[tuple(map(int,w)) for w in data['gw']];inds=[tuple(map(int,a)) for a in data['indices']];FN=data['FN'].copy();GN=data['GN'].copy();den=int(data['den'][0]);params=dict(zip(['t','U','V','d'],map(str,data['params'])))
 tests=[]
 for dv,du,dd in [(F(1,16),F(-1,16),F(1,16)),(F(-1,16),F(1,16),F(-1,16)),(F(0),F(-1,16),F(1,16))]:
  point=(dv,du,dd);w=[math.prod(x**k for x,k in zip(point,a))/math.prod(math.factorial(k) for k in a) for a in inds];L=math.lcm(*(x.denominator for x in w));coeff=np.array([int(x*L) for x in w],dtype=object)
  ff=coeff@FN.astype(object);gg=coeff@GN.astype(object);assert max(map(abs,ff))+max(map(abs,gg))<2**60
  ff=np.asarray(ff,dtype=np.int64);gg=np.asarray(gg,dtype=np.int64);den2=den*L
  U=4+du;V=1+dv;d=2+dd;scale=2*math.lcm(U.denominator,V.denominator,d.denominator)
  er,af=build(fw,float(scale),float(scale*U),float(scale*V));orr,ag=build(gw,float(scale),float(scale*U),float(scale*V))
  er2=sorted(set(er)|set(gw));or2=sorted(set(orr)|set(fw)|{(3,1)});AF=align(er,integer_matrix(af,1),er2);AG=align(orr,integer_matrix(ag,1),or2)
  ei={w:i for i,w in enumerate(er2)};oi={w:i for i,w in enumerate(or2)};qe=np.array([a.bit_count() for a,z in er2]);qo=np.array([a.bit_count() for a,z in or2]);qf=np.array([a.bit_count() for a,z in fw]);qg=np.array([a.bit_count() for a,z in gw]);gidx=np.array([ei[x] for x in gw]);fidx=np.array([oi[x] for x in fw])
  afn=safe_dot(AF,ff);agn=safe_dot(AG,gg);assert not np.any(afn[qe==0])
  sf=sum((F(2*int(q)*int(x)**2,den2**2) for q,x in zip(qf,ff)),F());sg=sum((F(2*int(q)*int(x)**2,den2**2) for q,x in zip(qg,gg)),F());cross=F(2*int(exact_dot(afn[gidx][None,:],gg[None,:])[0,0]),scale*den2**2);jf=F(-int(ff[fw.index((3,1))]),den2)
  ph=4*(2*jf-d/2*sf+d/2*sg+2*cross)
  assert ph==evalpoly(load(rec['corrected_D_poly']),point)
  so=agn.copy();se=afn.copy();ds=int(scale*d/2);assert F(ds)==scale*d/2
  so[fidx]+=ds*qf*ff;se[gidx]+=ds*qg*gg;so[oi[(3,1)]]+=scale*den2//2
  for typ,arr,q in [('odd',so,qo),('even',se,qe)]:
   value=weighted_gram(arr[None,:],q,(scale*den2)**2)[0,0]
   assert value==evalpoly(load(rec[f'residual_{typ}_norm_poly']),point)
  tests.append({'point':list(map(str,point)),'corrected_output_and_both_residual_norms_match_exactly':True})
 # Inject a defect in a hopping-visible coefficient. The mathematical checker,
 # not just the file hash, must reject it.
 er0,af0=build(fw,1.,0.,0.);mask=np.array([w[0]==0 for w in er0]);P=af0[mask,:].tocsc();col=int(np.flatnonzero(np.asarray(P.getnnz(axis=0)))[0]);bad=FN.copy();bad[0,col]+=1
 rejected=False
 try:compile_exact(fw,gw,bad,GN,den,inds,params)
 except AssertionError as exc:
  assert 'population imbalance' in str(exc);rejected=True
 assert rejected
 out={'tests':tests,'exact_scalar_comparisons':9,'corrupted_population_defect_rejected':True,'seconds':time.perf_counter()-start,'scope':'Independent contraction path using actual quantum trial coefficients; shares finite Pauli compiler, not independent mathematical review.'}
 (ROOT/'results/physical_polynomial_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':run()
