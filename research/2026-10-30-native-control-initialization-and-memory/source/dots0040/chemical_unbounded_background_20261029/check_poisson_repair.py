from fractions import Fraction as F
import json,math
d=F(1,1000)
def h(a): return 1+1/(a+d)
def defect(a,b):
    R=a*b*(b-1)*(h(a+1)-h(a))
    if a>=2: R+=a*(a-1)*b*(h(a-1)-h(a))
    T=100*h(a+1)-(1+a)*h(a)
    if a: T+=F(a,100)*h(a-1)
    return R+T
count=0
for a in range(301):
    for b in [0,1,2,10,100,399,400,401,1000,10000]:
        z=defect(a,b)
        if a==0 or a>=138 or b>=400: assert z<0,(a,b,z)
        count+=1
assert 100*h(1)-h(0)==-F(801901,1001)
assert F(100635,1000)-F(74,100)*138 < -1
assert -F(400**2,141)+F(3*400,2)+149 < -1
assert 160-F(400*399,6)<-1
def affinity_log(a,p):
    f=lambda n: math.prod(range(n-p+1,n+1))
    # stable sqrt difference
    u,v=f(a+p),f(a)
    delta=(u-v)/(math.sqrt(u)+math.sqrt(v))
    return -delta*delta/2
out={'exact_rational_defect_checks':count,'analytic_exterior_rectangle':{'A_min':1,'A_max':137,'B_min':0,'B_max':399},'boundary_A0_defect':str(100*h(1)-h(0)),'fiber_affinity_log_examples':[{'p':p,'A':a,'log_affinity':affinity_log(a,p)} for p in [1,2,3,4] for a in [100,1000]],'scope':'Finite regression of a separately written all-size proof; not a universal chemical recurrence theorem.'}
print(json.dumps(out,indent=2))
