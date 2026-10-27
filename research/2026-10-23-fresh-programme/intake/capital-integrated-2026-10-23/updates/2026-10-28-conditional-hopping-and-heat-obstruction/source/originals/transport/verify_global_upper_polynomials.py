from robust_decision import *
import hashlib

def cross(a,b,den):
 sums=defaultdict(int)
 for w,c in a.items():
  cc=b.get(w,0)
  if cc:sums[w[0].bit_count()]+=c*cc
 assert not sums.get(0,0)
 return sum((F(v,q) for q,v in sums.items() if q),F())/(den*den)

if __name__=='__main__':
 rows=[]
 for name in ['V0','Vhalf','V1','V1half','V2','V2half','V3']:
  f,g,den,rec=load(name);V=F(rec['parameters']['V']);Ag=act(g,hnom(V));A1g=act(g,[(0,5,2)]);r={w:-v for w,v in Ag.items()};r[(3,1)]=r.get((3,1),0)-2*den;r[(3,2)]=r.get((3,2),0)+2*den;r=clean(r)
  pp=[4*(norm2(r,4*den,'inverse')+norm2(g,den,'S')),-8*cross(r,A1g,4*den),4*norm2(A1g,4*den,'inverse')]
  assert pp==[F(x) for x in rec['upper_D_polynomial_exact']]
  rows.append({'anchor':name,'all_three_coefficients_exact':list(map(str,pp)),'source_npz_sha256':hashlib.sha256((SRC/'results/anchors'/f'{name}.npz').read_bytes()).hexdigest(),'status':'EXACT_PASS'})
  print(name,'EXACT_PASS',flush=True)
 (OUT/'GLOBAL_UPPER_POLYNOMIAL_REPLAY.json').write_text(json.dumps(rows,indent=2)+'\n')
