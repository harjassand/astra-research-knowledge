from check_adjugate_coordinates import *
import math
st=time.time();res=[0]*120;mod=1;pr=10000019;records=[]
for attempt in range(768):
 a=check(pr);cs=sum(a['coordinate_numerators_low_to_high'],[]);iv=pow(mod%pr,-1,pr)
 for j in range(120):res[j]+=mod*((cs[j]-res[j])%pr*iv%pr)
 mod*=pr;records.append(pr)
 if len(records)%16==0:
  recon=[rr(x,mod) for x in res];ok=all(x is not None for x in recon);print(len(records),mod.bit_length(),ok,time.time()-st,flush=True)
  if ok:
   testpr=int(sp.nextprime(pr));test=sum(check(testpr)['coordinate_numerators_low_to_high'],[])
   if all(x.denominator%testpr and cv==v for x,cv,v in [(x,x.numerator*pow(x.denominator%testpr,-1,testpr)%testpr,v) for x,v in zip(recon,test)]):
    out={'status':'RATIONAL_CANDIDATES_REQUIRE_EXACT_COORDINATE_IDENTITY','seconds':time.time()-st,'primes':records,'modulus_bits':mod.bit_length(),'coefficients':[list(map(str,recon[k*40:(k+1)*40])) for k in range(3)],'max_numerator_bits':max(abs(x.numerator).bit_length() for x in recon),'max_denominator_bits':max(x.denominator.bit_length() for x in recon)};(OUT/'coordinate_candidates.json').write_text(json.dumps(out,indent=2)+'\n');break
 pr=int(sp.nextprime(pr))
else:print('BUDGET_EXHAUSTED',flush=True)
