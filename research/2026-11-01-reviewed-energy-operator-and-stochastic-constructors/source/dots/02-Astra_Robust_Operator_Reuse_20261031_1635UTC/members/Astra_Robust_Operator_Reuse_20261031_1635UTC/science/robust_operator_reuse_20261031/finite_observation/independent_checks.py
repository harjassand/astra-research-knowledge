from robust_replay import *
import itertools,random,copy,json
rng=random.Random(917); checks=0
for case in range(8):
 n=4;m=2
 C=[]
 for _ in range(m):
  rows=[[rng.randrange(1,8) for j in range(n)] for i in range(n)]
  C.append(sp.Matrix([[sp.Rational(v,sum(row)) for v in row] for row in rows]))
 raw=[rng.randrange(1,10) for _ in range(n)];h=sp.Matrix(raw)/sum(raw)
 b=sp.Matrix([rng.randrange(-2,3) for _ in range(n)]);ell=sp.Matrix([rng.randrange(-2,3) for _ in range(n)])
 if case==0:b=sp.zeros(n,1)
 if case==1:ell=sp.zeros(n,1)
 basis=[]
 for x in (sp.ones(n,1),b,sp.diag(*h).inv()*ell):append_basis(x,basis,h)
 V=sp.Matrix.hstack(*basis);blocks,_=stable_blocks(C,V,h,12)
 boxes=[(A,A) for A in C];cert=certificate(boxes,b,ell,V,h,blocks,4,15)
 model={'basis':V,'metric':h,'operators':blocks,'boxes':boxes,'certificate':cert,'tolerance':cert['bound']+1,'ledger':{}}
 enc=encode_model(model);assert verify(boxes,b,ell,enc,expected_length=4,expected_tolerance=cert['bound']+1);checks+=1
 comp=compile_integer_replay(blocks,cert['right'],cert['output'],15)
 for l in range(5):
  for word in itertools.product(range(m),repeat=l):
   state=comp['initial_grid_state'];truth=b
   for a in word:state,_=integer_step(comp['operators'][a],state);truth=C[a]*truth
   ans=integer_output(comp,state);assert ans==replay(model,word)[0]
   assert abs(ans-(ell.T*truth)[0])<=cert['bound'];checks+=1
 for f,val in [('length',True),('query_bits',False),('bound','0'),('tolerance',1.0)]:
  bad=copy.deepcopy(enc);bad[f]=val
  if f=='bound' and cert['bound']==0:continue
  assert not verify(boxes,b,ell,bad,expected_length=4,expected_tolerance=cert['bound']+1);checks+=1
for p in [1,3,10]:
 for num in range(-20,21):
  x=sp.Rational(num,2**(p+1));r=rounded(x,p)
  assert abs(r-x)<=sp.Rational(1,2**(p+1));checks+=1
# Independent PSD cases including singular non-leading support.
for A,ok in [(sp.Matrix([[0,1],[1,0]]),False),(sp.diag(0,1),True),(sp.Matrix([[1,2],[2,4]]),True),(sp.Matrix([[1,2],[2,3]]),False)]:
 assert psd(A)==ok;checks+=1
print(json.dumps({'checks':checks,'scope':'Exact small signed-task/random-H and integer replay challenges; not proof or sample provenance.'},indent=2))
