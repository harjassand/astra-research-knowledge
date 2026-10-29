import math,json
out=[]
for C in [1.5,2,3,6,100]:
 for J in [155,1000,10000,100000]:
  t=J//8; delta=1/128
  eta=math.expm1(math.log(1/delta)/(t+1));s=1/(1+C*eta)
  R=C*s/(1-s);bound=math.exp((t+1)*math.log(R/(1+R)))
  assert abs(bound-delta)<1e-11
  out.append(dict(C=C,J=J,t=t,s=s,bound=bound,expected_tests=J*C*eta,limit_tests=8*C*math.log(1/delta)))
print(json.dumps(out,indent=2))
