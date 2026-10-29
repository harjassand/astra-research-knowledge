import itertools,json,random,hashlib,time,importlib.util
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parent;start=time.time()
spec=importlib.util.spec_from_file_location('author',R/'grs_wrapper_v1.py');author=importlib.util.module_from_spec(spec);spec.loader.exec_module(author)
saved=json.loads((R/'exact_wrapper_checks_v1.json').read_text());rng=random.Random(943210)
def pmul(a,b):
 p=0
 while b:
  if b&1:p^=a
  a<<=1;b>>=1
 return p
def rem(a,f):
 while a.bit_length()>=f.bit_length():a^=f<<(a.bit_length()-f.bit_length())
 return a
def xor(xs):
 z=0
 for x in xs:z^=x
 return z
def binmat_inv(rows,n):
 work=[row|(1<<(n+i)) for i,row in enumerate(rows)]
 for j in range(n):
  p=next(i for i in range(j,n) if work[i]>>j&1);work[j],work[p]=work[p],work[j]
  for i in range(n):
   if i!=j and work[i]>>j&1:work[i]^=work[j]
 assert [x&((1<<n)-1) for x in work]==[1<<i for i in range(n)]
 return [x>>n for x in work]
def compile_binary(rows):
 n=len(rows);w=rows[:];ops=[]
 for j in range(n):
  p=next(i for i in range(j,n) if w[i]>>j&1)
  if p!=j:w[j],w[p]=w[p],w[j];ops.append(('S',j,p))
  for i in range(n):
   if i!=j and w[i]>>j&1:w[i]^=w[j];ops.append(('C',j,i))
 assert w==[1<<i for i in range(n)]
 return ops[::-1]
def act_bits(v,ops):
 for typ,a,b in ops:
  if typ=='C':v^=((v>>a)&1)<<b
  elif typ=='S':
   u=((v>>a)^(v>>b))&1;v^=(u<<a)|(u<<b)
 return v
def act_pauli(x,z,ops):
 for typ,a,b in ops:
  if typ=='C':x^=((x>>a)&1)<<b;z^=((z>>b)&1)<<a
  elif typ=='S':
   u=((x>>a)^(x>>b))&1;x^=(u<<a)|(u<<b);u=((z>>a)^(z>>b))&1;z^=(u<<a)|(u<<b)
  else:
   u=((x>>a)^(z>>a))&1;x^=u<<a;z^=u<<a
 return x,z
rowsout=[]
for record in saved['cases']:
 m=record['m'];q=1<<m;mod=int(record['irreducible_polynomial_bits'],2);c=record['construction'];B=c['B'];t=c['t'];s=c['s'];ell=c['ell']
 table=[[rem(pmul(a,b),mod) for b in range(q)] for a in range(q)];inverse=[0]+[next(b for b in range(1,q) if table[a][b]==1) for a in range(1,q)]
 mul=lambda a,b:table[a][b]
 def pw(a,k):
  z=1
  for _ in range(k):z=mul(z,a)
  return z
 def dot(a,b):return xor(mul(x,y) for x,y in zip(a,b))
 def rowmul(a,T):return [dot(a,col) for col in zip(*T)]
 def trace(a):
  vals=[]
  for _ in range(m):vals.append(a);a=mul(a,a)
  out=xor(vals);assert out in (0,1);return out
 # Independently reconstruct GRS weights and both dual orthogonality conditions.
 aa=list(range(B));v=[]
 for a in aa:
  prod=1
  for b in aa:
   if a!=b:prod=mul(prod,a^b)
  u=inverse[prod];roots=[b for b in range(q) if mul(b,b)==u];assert len(roots)==1;v.append(roots[0])
 C=[[mul(v[i],pw(aa[i],h)) for i in range(B)] for h in range(B-2*t)];assert C==c['C'] and C[:s]==c['H']
 assert all(dot(h,row)==0 for h in C[:s] for row in C)
 assert all(dot(row,col)==int(i==j) for i,row in enumerate(c['T']) for j,col in enumerate(zip(*c['Ti'])))
 # Author BW control flow checked against independently generated low-weight syndrome oracle.
 # Replace arithmetic by independently constructed complete finite-field tables only.
 g=author.GF(m,mod);g.mul=mul;g.inv=lambda a:inverse[a] if a else (_ for _ in ()).throw(ZeroDivisionError())
 expected={}
 if B<=9:
  for w in range(t+1):
   for pos in itertools.combinations(range(B),w):
    for vals in itertools.product(range(1,q),repeat=w):
     e=[0]*B
     for i,a in zip(pos,vals):e[i]=a
     synd=tuple(dot(h,e) for h in C[:s]);assert synd not in expected;expected[synd]=e
  selected=list(expected.items()) if B<=8 else rng.sample(list(expected.items()),min(1000,len(expected)))
 else:
  selected=[]
  for _ in range(1000):
   e=[0]*B
   for i in rng.sample(range(B),rng.randrange(t+1)):e[i]=rng.randrange(1,q)
   selected.append((tuple(dot(h,e) for h in C[:s]),e))
 for sy,e in selected:
  actual,ok=author.decode_syndrome(g,c,list(sy));assert ok and actual==e
 totality=0
 syndromes=list(itertools.product(range(q),repeat=s)) if B<=8 else [tuple(rng.randrange(q) for _ in range(s)) for _ in range(200)]
 for sy in syndromes:
  actual,ok=author.decode_syndrome(g,c,list(sy));assert len(actual)==B
  if ok:
   assert sum(a!=0 for a in actual)<=t and tuple(dot(h,actual) for h in C[:s])==sy
  if expected:assert ok==(sy in expected)
  totality+=1
 # Construct actual binary CNOT/SWAP network for row-coordinate decoder Lin(T^-1).
 def pack(es):return sum(e<<(m*i) for i,e in enumerate(es))
 def unpack(v):return [(v>>(m*i))&(q-1) for i in range(B)]
 n=m*B;columns=[]
 for j in range(n):columns.append(pack(rowmul(unpack(1<<j),c['Ti'])))
 mat=[sum(((columns[j]>>i)&1)<<j for j in range(n)) for i in range(n)];gates=compile_binary(mat)
 for j in range(n):assert act_bits(1<<j,gates)==columns[j]
 # Trace Fourier = H^m after the binary trace-Gram linear map.
 J=[sum(trace(mul(1<<i,1<<j))<<j for j in range(m)) for i in range(m)];binmat_inv(J,m)
 jgates=compile_binary(J)
 for block in range(s):
  gates += [(typ,a+m*block,b+m*block) for typ,a,b in jgates]
  gates += [('H',m*block+i,0) for i in range(m)]
 def phasepack(fs):return pack([sum((row&f).bit_count()%2<<i for i,row in enumerate(J)) for f in fs])
 tests=[]
 for site in range(B):
  for a,b in itertools.product(range(q),repeat=2):
   if a==b==0:continue
   e=[0]*B;f=[0]*B;e[site]=a;f[site]=b;tests.append((e,f))
 tests=tests if B<=8 else rng.sample(tests,500)
 for _ in range(100):
  e=[0]*B;f=[0]*B
  for i in rng.sample(range(B),rng.randrange(t+1)):e[i]=rng.randrange(q);f[i]=rng.randrange(q)
  tests.append((e,f))
 for e,f in tests:
  x,z=act_pauli(pack(e),phasepack(f),gates);xfield=unpack(x)
  se=[dot(row,xfield[s+ell:]) for row in c['HRt']];sf=xfield[:s]
  eh,o1=author.decode_syndrome(g,c,se);fh,o2=author.decode_syndrome(g,c,sf);assert o1 and o2 and eh==e and fh==f
  xc,zc=act_pauli(pack(eh),phasepack(fh),gates)
  mask=((1<<(ell*m))-1)<<(s*m);assert ((x^xc)&mask)==0 and ((z^zc)&mask)==0
  # Independent bit-gate propagation must match the author's declared field formulas.
  xx,zz=author.decoded_error(g,c,e,f);assert x==pack(xx) and z==phasepack(zz)
 rowsout.append({'B':B,'q':q,'t':t,'independent_low_weight_syndrome_table_size':len(expected),'BW_correctable_tests':len(selected),'BW_totality_tests':totality,'actual_binary_gate_count':len(gates),'binary_Pauli_pattern_tests':len(tests),'all_pass':True})
 print(rowsout[-1],flush=True)
out={'status':'INDEPENDENT_EXACT_GRS_DUAL_BW_AND_BINARY_BILATERAL_ORIENTATION_CHECKS_PASS','cases':rowsout,'elapsed_seconds':time.time()-start,'author_import_scope':'Only BW/declared field transformation algorithms under test; arithmetic tables, syndrome truth tables, binary gate compiler/Pauli propagation independently implemented','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'grs_wrapper_v1.py',R/'exact_wrapper_checks_v1.json',R/'GOVERNING_WRAPPER_v1.md']}}
(D/'results_v1.json').write_text(json.dumps(out,indent=2)+'\n')
