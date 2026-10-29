import sympy as s,json,sys,time,math,hashlib
from pathlib import Path
from fractions import Fraction
sys.set_int_max_str_digits(0);PTH=Path(__file__).parent;SRC=PTH/'received';st=time.time()
x,y,z=s.symbols('x y z');sh=json.loads((SRC/'shape.json').read_text());inp=json.loads((SRC/'input.json').read_text());bs=[s.sympify(a) for a in sh['lex_basis']]
def asc(f):
 p=s.Poly(f,z);return [int(p.nth(i)) for i in range(p.degree()+1)]
U=asc(bs[2]);cx=int(s.Poly(bs[0],x,y,z).coeff_monomial(x));cy=int(s.Poly(bs[1],x,y,z).coeff_monomial(y));X=asc(-bs[0].subs(x,0));Y=asc(-bs[1].subs(y,0));n=len(U)-1;assert n==40
terms=[]
for e,c in zip(inp['exponents'],inp['perturbed']):
 if e[0]:terms.append((e[1:],Fraction(c)*e[0]))
data={'U':list(map(str,U)),'Xnum':list(map(str,X)),'Xden':str(cx),'Ynum':list(map(str,Y)),'Yden':str(cy),'F0':[[e,str(c)] for e,c in terms],'source_sha256':{f:hashlib.sha256((SRC/f).read_bytes()).hexdigest() for f in ['input.json','shape.json','boundary.json','fixed_good_direction_modp.json']}}
(PTH/'quotient_input.json').write_text(json.dumps(data,indent=2)+'\n')
lines=[str(n)]+list(map(str,U))+[str(cx)]+[str(X[i] if i<len(X) else 0) for i in range(n)]+[str(cy)]+[str(Y[i] if i<len(Y) else 0) for i in range(n)]+[str(len(terms))]
for e,c in terms:lines.append(' '.join(map(str,[*e,c.numerator,c.denominator])))
(PTH/'quotient_input.txt').write_text('\n'.join(lines)+'\n')
def trim(a):
 while a and not a[-1]:a.pop()
 return a
def division(a,b,p):
 a=a.copy();q=[0]*max(0,len(a)-len(b)+1);iv=pow(b[-1],-1,p)
 while len(a)>=len(b):
  k=len(a)-len(b);v=a[-1]*iv%p;q[k]=v
  for j in range(len(b)):a[k+j]=(a[k+j]-v*b[j])%p
  trim(a)
 return trim(q),a
def mulraw(a,b,p):
 out=[0]*(len(a)+len(b)-1)
 for i,aa in enumerate(a):
  for j,bb in enumerate(b):out[i+j]=(out[i+j]+aa*bb)%p
 return trim(out)
def add(a,b,p,fac=1):
 out=a.copy()+[0]*max(0,len(b)-len(a))
 for i,v in enumerate(b):out[i]=(out[i]+fac*v)%p
 return trim(out)
def inverse(a,u,p):
 r0,r1=u,a;t0,t1=[],[1]
 while r1:
  q,r=division(r0,r1,p);r0,r1=r1,r;t0,t1=t1,add(t0,mulraw(q,t1,p),p,-1)
 if len(r0)!=1:raise ValueError('noninvertible norm')
 return division([c*pow(r0[0],-1,p)%p for c in t0],u,p)[1]
def charpoly(pr):
 if (cx*cy*U[-1])%pr==0:raise ValueError('denominator')
 u=[a*pow(U[-1]%pr,-1,pr)%pr for a in U]
 def mul(a,b):return division(mulraw(a,b,pr),u,pr)[1]
 pp=[a*pow(cx%pr,-1,pr)%pr for a in X];qq=[a*pow(cy%pr,-1,pr)%pr for a in Y];zz=[0,1]
 norm=add(add(add([1],mul(pp,pp),pr),mul(qq,qq),pr),[0,0,1],pr)
 powers=[]
 for a in [pp,qq,zz]:powers.append([[1],a,mul(a,a),mul(mul(a,a),a)])
 num=[]
 for e,c in terms:
  v=[c.numerator*pow(c.denominator%pr,-1,pr)%pr]
  for j,k in enumerate(e):v=mul(v,powers[j][k])
  num=add(num,v,pr)
 lam=[a*pow(4,-1,pr)%pr for a in mul(num,inverse(norm,u,pr))]
 cols=[];v=[1]
 for k in range(n+1):cols.append(v+[0]*(n-len(v)));v=mul(v,lam)
 A=[[cols[j][i] for j in range(n)]+[-cols[n][i]%pr] for i in range(n)]
 for col in range(n):
  row=next((i for i in range(col,n) if A[i][col]),None)
  if row is None:raise ValueError('nonprimitive modular value')
  A[col],A[row]=A[row],A[col];iv=pow(A[col][col],-1,pr);A[col]=[a*iv%pr for a in A[col]]
  for i in range(n):
   if i!=col and A[i][col]:
    factor=A[i][col];A[i]=[(a-factor*b)%pr for a,b in zip(A[i],A[col])]
 return [A[i][-1] for i in range(n)]+[1]
def rr(a,M):
 lim=math.isqrt(M//2);r0,r1=M,a;t0,t1=0,1
 while r1>lim:
  q=r0//r1;r0,r1=r1,r0-q*r1;t0,t1=t1,t0-q*t1
 if t1==0 or abs(t1)>lim or math.gcd(r1,t1)!=1:return None
 if t1<0:r1=-r1;t1=-t1
 if (r1-a*t1)%M:return None
 return Fraction(r1,t1)
mod=1;res=[0]*n;prime=1000000007;records=[]
for attempt in range(512):
 try:cp=charpoly(prime)
 except ValueError as e:prime=int(s.nextprime(prime));continue
 inv=pow(mod%prime,-1,prime)
 for j in range(n):res[j]+=mod*((cp[j]-res[j])%prime*inv%prime)
 mod*=prime;records.append(prime)
 if len(records)%8==0:
  rec=[rr(a,mod) for a in res];ok=all(a is not None for a in rec);print(len(records),mod.bit_length(),'all_reconstruct',ok,'seconds',time.time()-st,flush=True)
  if ok:
   testpr=int(s.nextprime(prime));test=charpoly(testpr);match=all(c.denominator%testpr and c.numerator*pow(c.denominator%testpr,-1,testpr)%testpr==test[j] for j,c in enumerate(rec))
   if match:
    rec+=[Fraction(1)];den=math.lcm(*(c.denominator for c in rec));ints=[int(c*den) for c in rec];gg=math.gcd(*ints);ints=[a//gg for a in ints]
    out={'status':'MODULAR_CANDIDATE_REQUIRES_EXACT_VERIFICATION','degree':n,'monic_coefficients_low_to_high':[str(c) for c in rec],'integer_coefficients_low_to_high':list(map(str,ints)),'prime_count':len(records),'CRT_modulus_bits':mod.bit_length(),'extra_test_prime':testpr,'max_integer_coefficient_bits':max(abs(a).bit_length() for a in ints),'seconds':time.time()-st,'primes':records}
    (PTH/'candidate_value_polynomial.json').write_text(json.dumps(out,indent=2)+'\n');(PTH/'candidate_value_polynomial.txt').write_text('\n'.join([str(n)]+list(map(str,ints)))+'\n');print('CANDIDATE',out['max_integer_coefficient_bits'],out['seconds'],flush=True);break
 prime=int(s.nextprime(prime))
else:raise RuntimeError('512-prime budget exhausted without candidate')
