"""Direct symbolic homogenization of the source scalar formula."""
import math, json
from pathlib import Path
import sympy as s

X=s.symbols('X0:4'); w=sum(X)
x=(X[0]+X[1]+X[2]/3,X[0]+X[2]/3,X[0]-X[2]/3)
A=sum(v*v for v in x);B=s.prod(x);C=sum(x[i]**2*x[j]**2 for i in range(3) for j in range(i))
terms=(s.Integer(1),A,B,A*A,C,A*B,A**3,A*C,B**2)
degrees=(0,2,3,4,4,5,6,6,6)
Hs=(0,0,1000,-100,-150,300,-20,70,-510)
Fs=(0,4000,-3000,700,-4000,-800,0,0,0)
Gs=(1000,-1610,-3100,773,4000,-3980,0,0,0)

def homogeneous(cs,r):
    return s.Poly(sum(s.Rational(c,1000)*v*w**(r-d) for c,v,d in zip(cs,terms,degrees) if c),*X)

def summary(poly,r):
    d=poly.as_dict();coeffs=[];norm=[]
    for a in range(r+1):
      for b in range(r-a+1):
       for c in range(r-a-b+1):
        I=(a,b,c,r-a-b-c);v=d.get(I,s.Integer(0));coef=math.factorial(r)//math.prod(math.factorial(i) for i in I)
        coeffs.append((v,I));norm.append((v/coef,I))
    m,I=min(coeffs);n,J=min(norm)
    return {'degree':r,'coefficients':len(coeffs),'minimum':str(m),'argmin':I,'min_Bernstein':str(n),'min_Bernstein_argmin':J,'nonnegative':m>=0}

result={}; certificates={}
for name,cs,r in [('H_plus_half',tuple(c+(500 if i==0 else 0) for i,c in enumerate(Hs)),6),('F',Fs,5),('G',Gs,14),('Euler_scaling',tuple((3-d)*c for c,d in zip(Hs,degrees)),6),('H_plus_3_25',tuple(c+(120 if i==0 else 0) for i,c in enumerate(Hs)),6),('F_minus_3_10_A',tuple(c-(300 if i==1 else 0) for i,c in enumerate(Fs)),5),('G_minus_87_1000',tuple(c-(87 if i==0 else 0) for i,c in enumerate(Gs)),14),('Euler_minus_A2_20',tuple((3-d)*c-(50 if i==3 else 0) for i,(c,d) in enumerate(zip(Hs,degrees))),6)]:
    poly=homogeneous(cs,r)
    result[name]=summary(poly,r)
    result[name]['nonnegative']=bool(result[name]['nonnegative'])
    if name in ('H_plus_3_25','F_minus_3_10_A','Euler_minus_A2_20'):
        certificates[name]={','.join(map(str,I)):str(v) for I,v in poly.as_dict().items()}
    if name=='G':
        Gc=poly-s.Poly(s.Rational(613,71500)*w**14,*X)
        assert all(v>=0 for v in Gc.coeffs())
        certificates['G_minus_613_71500']={','.join(map(str,I)):str(v) for I,v in Gc.as_dict().items()}
Path(__file__).with_name('scalar_exact_results.json').write_text(json.dumps(result,indent=2))
Path(__file__).with_name('scalar_exact_certificates.json').write_text(json.dumps(certificates,indent=2))
print(json.dumps(result,indent=2))
