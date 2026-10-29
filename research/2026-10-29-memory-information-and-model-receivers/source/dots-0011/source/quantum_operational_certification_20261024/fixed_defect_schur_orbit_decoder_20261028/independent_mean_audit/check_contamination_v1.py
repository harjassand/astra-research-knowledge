"""Exact small Schur-Weyl spectral-law check of binomial defect domination."""
from pathlib import Path
import sympy as s,math,json,hashlib
D=Path(__file__).parent

def partitions(n,top=None):
 if n==0:yield ();return
 for z in range(min(n,top or n),0,-1):
  for tail in partitions(n-z,z):yield (z,)+tail

def fdim(nu):
 den=1
 for i,row in enumerate(nu):
  for j in range(row):den*=row-j+sum(t>j for t in nu[i+1:])
 return math.factorial(sum(nu))//den
rows=[]
for k in range(3,9):
 for c in [s.Rational(1,2),s.Rational(1),s.Rational(2)]:
  p=c/k;spec=[1-p,p/3,2*p/3]
  # If p large, chosen first eigenvalue may not be the largest; domination by its
  # count is nevertheless valid. The claim assumes only a dominant weight≥1-c/k.
  h=[s.Rational(1)]+[s.Rational(0)]*k
  for x in spec:
   for n in range(1,k+1):h[n]+=x*h[n-1]
  law=[]
  for nu in partitions(k):
   if len(nu)>3:continue
   ell=len(nu);J=s.Matrix(ell,ell,lambda i,j:h[nu[i]-i+j] if 0<=nu[i]-i+j<=k else 0);prob=s.factor(fdim(nu)*J.det());assert prob>=0;law.append((nu,prob))
  assert sum(p for nu,p in law)==1
  for j in range(min(k,4)):
   tail=sum(prob for nu,prob in law if k-nu[0]>j);binomial=sum(math.comb(k,r)*p**r*(1-p)**(k-r) for r in range(j+1,k+1));assert tail<=binomial
   rows.append({'k':k,'c':str(c),'j':j,'Schur_defect_tail':str(tail),'binomial_tail':str(binomial)})
out={'status':'PASS_EXACT_SMALL_SCHUR_LAW_CONTAMINATION_CHECK','spectra':18,'tail_cases':len(rows),'rows':rows,'scope':'Exact spectral-law check supplements subgroup-invariance proof; no source promise acquisition.','sha256':{Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
(D/'check_contamination_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['tail_cases'])
