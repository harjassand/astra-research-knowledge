from fractions import Fraction
import random,math,json
rng=random.Random(20261029);M=4;T=240;p=Fraction(1,3);eta=Fraction(1,32);alpha=Fraction(1,20);weights=[1]*M
avg=Fraction();comp=Fraction();sq=Fraction();path=[];prev=0
for t in range(T):
 # Predictable path chosen only from records preceding this round.
 j=(t//60+prev)%M if t%60==0 else path[-1];path.append(j)
 learn=rng.randrange(3)==0
 nums=[rng.randrange(21) for _ in range(M)]
 ell=[Fraction(3*x,20) if learn else Fraction(0) for x in nums]
 avg+=sum(Fraction(weights[k],sum(weights))*ell[k] for k in range(M));comp+=ell[j];sq+=ell[j]**2
 factors=[640-3*x if learn else 640 for x in nums]
 tmp=[weights[k]*factors[k] for k in range(M)];total=sum(tmp)
 weights=[76*v+total for v in tmp]
 assert min(weights)>0
 prev=nums[0]%M
S=sum(path[t]!=path[t-1] for t in range(1,T))
K=math.log(M)+S*math.log(M/float(alpha))+(T-1-S)*math.log(1/(1-float(alpha)))
lhs=float(avg-comp);rhs=K/float(eta)+float(eta*sq)
assert lhs<=rhs+1e-10
# Exhaust all binary words for a two-attempt cap on uniform integers0..6.
counts=[0]*7;fail=0
for a in range(8):
 for b in range(8):
  v=a if a<7 else b
  if v<7:counts[v]+=1
  else:fail+=1
assert counts==[9]*7 and fail==1
result=dict(M=M,T=T,switches=S,estimated_regret=lhs,pathwise_upper_bound=rhs,exact_integer_updates=M*T,max_weight_bits=max(w.bit_length() for w in weights),capped_sampler_uniform_counts=counts,capped_sampler_failures=fail,scope='Exact integer fixed-share updates and exhaustive cap neutrality; logarithmic potential diagnostic uses floating evaluation. Synthetic records, not acquired physical data.')
print(json.dumps(result,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(result,indent=2)+'\n')
