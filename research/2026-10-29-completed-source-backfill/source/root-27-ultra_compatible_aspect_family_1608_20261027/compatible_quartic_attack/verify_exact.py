"""Independent exact replay of the retained continuum construction.

The family producer expands affine atoms in t. This verifier instead
substitutes rational t first, reacquires integer atom moments, uses SymPy
for Euclidean divisions/Sturm root counting, and replays the source's
literal acoustic certificate. No floating optimizer output is trusted.
"""
import hashlib,importlib.util,json,math,time
from fractions import Fraction as Q
import sympy as s
from exact_profile import ROOT,polynomial,diff,solve_ldl

def ev(p,t):
 z=Q(0)
 for c in reversed(p):z=z*t+Q(c)
 return z

def aspoly(p):
 return s.Poly.from_list([s.Rational(Q(x).numerator,Q(x).denominator)for x in reversed(p)],s.Symbol('t'),domain=s.QQ)

def verify_sturm(p,sequence):
 p=aspoly(p);seq=list(map(aspoly,sequence));assert seq[0].monic()==p.monic()
 assert seq[0].LC()/p.LC()>0
 derivative=seq[0].diff();assert seq[1].monic()==derivative.monic()and seq[1].LC()/derivative.LC()>0
 for a,b,c in zip(seq,seq[1:],seq[2:]):
  r=-a.rem(b);assert r.monic()==c.monic()and c.LC()/r.LC()>0
 assert seq[-1].degree()==0
 count=p.count_roots(0,s.oo);assert count==0 and p.eval(0)>0
 return {'positive_roots':int(count),'degree':p.degree(),'positive_at_zero':True,'Euclidean_recurrences_checked':len(seq)-2}

def direct_moments(nodes,D,t):
 n=len(nodes);den=D*t.denominator;num=t.numerator;qt=t.denominator
 f,_=polynomial();df=[diff(f,i)for i in range(4)];hh=[[diff(df[i],j)for j in range(4)]for i in range(4)]
 needed=set(f)
 for p in df:needed.update(p)
 for row in hh:
  for p in row:needed.update(p)
 pairs={}
 for i in range(4):
  for j in range(4):
   e=[0]*4;e[i]+=1;e[j]+=1;pairs[i,j]=tuple(e);needed.add(tuple(e))
 sums={e:0 for e in needed};mean=[0]*4;det=0
 for i in range(n):
  bar=[sum(nodes[(i+1)%n][j][o]-nodes[i][j][o]for j in range(n))for o in range(2)]
  for j in range(n):
   v0=nodes[i][j];v1=nodes[(i+1)%n][j];v2=nodes[(i+1)%n][(j+1)%n];v3=nodes[i][(j+1)%n]
   for edges in [[(v1[o]-v0[o],v2[o]-v1[o])for o in range(2)],[(v2[o]-v3[o],v3[o]-v0[o])for o in range(2)]]:
    x=[]
    for o,(dx,dy)in enumerate(edges):x.extend([qt*bar[o]+num*(n*dx-bar[o]),qt*n*dy])
    mean=[a+b for a,b in zip(mean,x)];det+=x[0]*x[3]-x[1]*x[2]
    powers=[[1,z,z*z,z**3,z**4]for z in x]
    for e in needed:sums[e]+=math.prod(powers[k][e[k]]for k in range(4))
 assert not any(mean)and det==0
 moments={e:Q(v,2*n*n*den**sum(e))for e,v in sums.items()}
 def avg(p):return sum(c*moments[e]for e,c in p.items())
 c=avg(f);b=[avg(p)for p in df];H=[[avg(p)for p in row]for row in hh]
 z,pivots=solve_ldl(H,b);gap=c-sum(x*y for x,y in zip(b,z))/2
 covariance=[[moments[pairs[i,j]]for j in range(4)]for i in range(4)]
 _,covariance_pivots=solve_ldl(covariance,[Q(0)]*4)
 return c,b,H,gap,covariance_pivots

def run():
 start=time.monotonic();profile=json.loads((ROOT/'data/EXACT_COMPATIBLE_PROFILE.json').read_text());family=json.loads((ROOT/'data/EXACT_ASPECT_FAMILY.json').read_text());target=json.loads((ROOT/'TARGET.json').read_text())
 source=ROOT.parent/'quartic_alternative/combined_full_cone';source_path=source/'heat_normal_extreme_ROC.json'
 assert hashlib.sha256(source_path.read_bytes()).hexdigest()==target['source_sha256']
 spec=importlib.util.spec_from_file_location('source_exact_acoustic',source/'exact_acoustic.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 acoustic=module.verify(source_path);assert acoustic['status']=='EXACT_STRICT_ROC_LITERAL_ACOUSTIC_CERTIFICATE_PASS'
 A,B,C,E,G,Hc,L,M,N=map(Q,target['coefficients'])
 assert A==B and G==Hc==N==0 and C+E-2*A>0 and E<0
 ell=(abs(L+M)+abs(L-M))/2;kappa=A-ell**2/(-4*E)
 assert kappa>0 and kappa==Q(profile['pointwise_coercivity_kappa'])
 samples=[]
 for t in [Q(1,2),Q(1),Q(2)]:
  c,b,H,gap,covariance_pivots=direct_moments(profile['integer_nodes'],profile['node_denominator'],t)
  assert c==ev(family['c_coefficients'],t)
  assert b==[ev(p,t)for p in family['b_coefficients']]
  assert H==[[ev(p,t)for p in row]for row in family['H_coefficients']]
  determinant=Q(s.det(s.Matrix([[s.Rational(x.numerator,x.denominator)for x in row]for row in H])))
  assert determinant==ev(family['detH_coefficients'],t)
  assert 2*determinant*gap==ev(family['cleared_gap_polynomial'],t)
  assert gap>Q(family['uniform_relative_gap_lower'])*c
  samples.append({'t':str(t),'Delta_over_c':str(gap/c),'integer_gradient_mean_and_determinant_zero':True,
   'positive_covariance_exact_LDL_pivots':list(map(str,covariance_pivots))})
 primary=verify_sturm(family['cleared_gap_polynomial'],family['Sturm_sequence'])
 guard=verify_sturm(family['relative_guard_polynomial'],family['relative_guard_Sturm_sequence'])
 det=aspoly(family['detH_coefficients']);c=aspoly(family['c_coefficients']);P=aspoly(family['cleared_gap_polynomial']);guard_p=aspoly(family['relative_guard_polynomial']);epsilon=s.Rational(family['uniform_relative_gap_lower'])
 assert guard_p==P-2*epsilon*det*c
 r=Q(profile['Schur_loss_over_c']);assert Q(2,3)<r<1
 result={'status':'EXACT_CONTINUUM_COMPATIBLE_FAMILY_REPLAY_PASS','source_acoustic_replay':acoustic,
 'substitute_then_reacquire_samples':samples,'primary_Sturm':primary,'relative_guard_Sturm':guard,
 'uniform_relative_gap_lower':family['uniform_relative_gap_lower'],'pointwise_coercivity_kappa':str(kappa),
 'exact_amplitude_curve_nonconvex_but_nonnegative':True,
 'seconds':time.monotonic()-start,'scope':'One declared exact P1 profile and its compatible aspect-ratio family, all affine backgrounds; no global quasiconvexity assertion.'}
 (ROOT/'data/EXACT_REPLAY.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return result
if __name__=='__main__':run()
