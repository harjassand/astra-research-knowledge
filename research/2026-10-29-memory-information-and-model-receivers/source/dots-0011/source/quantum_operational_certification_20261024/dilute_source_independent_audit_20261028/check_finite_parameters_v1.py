import math,json
from pathlib import Path

def partitions(n,b,cap=None):
    if b==0:
        if n==0: yield ()
        return
    for t in range(min(n,n if cap is None else cap),-1,-1):
        for rest in partitions(n-t,b-1,t): yield (t,)+rest

def h(p): return -sum(x*math.log2(x) for x in p if x)
def f(b,x): return x*math.log2(b-1)+h((x,1-x))
rows=[]
for b in range(2,6):
    worst=1e9; count=0
    for k in range(1,31):
        b0=(b-1)*(b+2)/2
        for mu in partitions(k,b):
            num=math.factorial(k)*math.prod(mu[i]-mu[j]+j-i for i in range(b) for j in range(i+1,b))
            den=math.prod(math.factorial(mu[i]+b-i-1) for i in range(b))
            assert num%den==0
            dim=num//den
            margin=math.log2(dim)-k*h([x/k for x in mu])+b0*math.log2(k+b)
            assert margin>=-1e-10
            worst=min(worst,margin);count+=1
    rows.append(dict(b=b,cases=count,min_hook_lower_bound_margin_bits=worst))
c=1;eps=.1;R=.25;Delta=.25;b=2;A0=20/9
j=0
while c**(j+1)/math.factorial(j+1)>eps/6:j+=1
for k in range(j+1,1000000):
    b0=(b-1)*(b+2)/2;u=math.sqrt(2/k*math.log(6*(k+1)**b0/eps))
    if c/k>.5 or u>1:continue
    logL=sum(math.log2(k-i) for i in range(j))
    left=k*(Delta-f(b,c/k)-f(b,u/2))-b0*math.log2(k+b)
    right=3*logL+math.log2(6*A0/eps)
    if left>=right:break
else:raise AssertionError('finite example missing')
result={'hook_checks':rows,'illustrative_not_practical_parameters':dict(c=c,epsilon=eps,R=R,Delta=Delta,b=b,j=j,k=k,u=u,left=left,right=right,log2_alpha0=2*logL,log2_M0=3*logL,payload_ebits=math.floor(k*R))}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
