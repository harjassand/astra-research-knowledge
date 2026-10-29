from fractions import Fraction as F
import json
out=[]
for n in range(4,202,2):
 a=F(n-4,2*(n-1)); q=F(3*(n-2),4*(n-1)); e=1-a*a
 assert e/q==F(n+2,n-1)
 out.append({'n':n,'a':str(a),'q_coefficient':str(q),'e_coefficient':str(e),'ratio':str(e/q)})
print(json.dumps(out,indent=2))
