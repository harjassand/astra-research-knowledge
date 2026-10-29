from fractions import Fraction as F
import itertools,math,random,json
rng=random.Random(20261029);m=1;net=[]
for k in itertools.product(range(-m,m+1),repeat=3):
 D=m*m+sum(a*a for a in k);q=[F(m*m-sum(a*a for a in k),D)]+[F(2*m*a,D) for a in k]
 assert sum(x*x for x in q)==1
 w,x,y,z=q
 C=[[1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y)], [2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x)], [2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)]]
 assert all(sum(C[a][j]*C[b][j] for j in range(3))==int(a==b) for a in range(3) for b in range(3))
 det=sum(C[0][j]*(C[1][(j+1)%3]*C[2][(j+2)%3]-C[1][(j+2)%3]*C[2][(j+1)%3]) for j in range(3))
 assert det==1
 net.append(C)
L=20*math.factorial(4*m*m)**4;eta=F(1,128);p=F(1,2);G=64*L
weights=[1]*len(net); cum=[0.]*len(net); alg=0.;sq=[0.]*len(net);maxbits=0;maxattempts=0
for t in range(256):
 a,b,c,d=[rng.randrange(3) for _ in range(4)];yz=rng.choice([-1,1]);uv=rng.choice([-1,1]);probe=rng.randrange(2)==0
 f=[F(10-yz*C[a][b]*(1+9*uv*C[c][d]),20) for C in net]
 assert all(0<=x<=1 and (L*x).denominator==1 for x in f)
 total=sum(weights);bits=total.bit_length();tries=0
 for tries in range(1,33):
  r=rng.getrandbits(bits)
  if r<total:break
 else:
  raise RuntimeError("declared sampler cap exhausted")
 maxattempts=max(maxattempts,tries)
 idx=0
 while r>=weights[idx]:r-=weights[idx];idx+=1
 assert 0<=idx<len(net)
 loss=[float(x/p) if probe else 0. for x in f]
 alg+=sum((w/total)*l for w,l in zip(weights,loss))
 for j in range(len(net)):cum[j]+=loss[j];sq[j]+=loss[j]**2
 if probe:
  factors=[G-int(L*x) for x in f]
  assert all(F(z,G)==1-eta*x/p and z>0 for z,x in zip(factors,f))
  weights=[w*z for w,z in zip(weights,factors)]
 maxbits=max(maxbits,max(w.bit_length() for w in weights))
 # Actual deterministic potential inequality; floating only for log evaluation.
 assert all(alg-cum[j]<=math.log(len(net))/float(eta)+float(eta)*sq[j]+1e-8 for j in range(len(net)))
# Forced rejection fixture: cap is checked before any 33rd draw.
def capped_draw(total, cap, draw):
 for _ in range(cap):
  value=draw(total.bit_length())
  if value<total:return value
 return None
calls=[0]
def reject(bits):
 calls[0]+=1;return (1<<bits)-1
assert capped_draw(5,32,reject) is None and calls[0]==32
print(json.dumps(dict(forced_rejection_draws=calls[0],net_size=len(net),rounds=256,common_loss_denominator=L,update_denominator=G,max_weight_bits=maxbits,max_rejection_attempts=maxattempts,exact_unit_and_SO3_checks=len(net),exact_update_checks=256*len(net),scope='Exact Fraction/integer net and update/sampler construction; log-potential diagnostic uses ordinary float. Synthetic signed records exercise arithmetic, not an acquired physical bank.'),indent=2))
