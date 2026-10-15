if not __debug__:
    raise RuntimeError("Run without -O / PYTHONOPTIMIZE; validation assertions are required")
from fractions import Fraction as Q
import sys,json,time,subprocess,math,os
sys.path.insert(0,os.path.dirname(__file__))
import exact_intervals as c
D=os.path.dirname(__file__)
def prepare(kind):
 start=time.time(); n=400;K=128
 if kind=='two':a=Q('0.7385658319646086');p=Q('0.7821972683346718');ls=[Q(1,2)]*200+[Q(3,2)]*200
 else:a=Q('0.9076164362901215');p=Q('0.7370771264577279');ls=[Q(399+2*i,798) for i in range(400)]
 F=1-(K+2)*p**(K+1)+(K+1)*p**(K+2)
 norm=(c.I.q(1/(1-p)-1)+c.logpoint(1-p))*a
 C=(norm*Q(1,5)).sqrt()*(2*n);logF=c.logpoint(F)
 logM=C-logF*n; cdfs=[];qmax=Q(0);cache={}
 for lam in ls:
  if lam not in cache:
   weights=[(m+1)*p**m*lam/(lam+a*m) for m in range(K+1)];total=sum(weights);Z=(1-p)**2*total
   acc=Q(0);cdf=[]
   for w in weights[:-1]:
    acc+=w;cdf.append((acc/total*(1<<64)).__floor__())
   cache[lam]=(cdf,c.logpoint(Z),F*lam/Z)
  cdf,lz,q=cache[lam];cdfs.append(cdf);logM=logM+lz;qmax=max(qmax,q)
 M=c.expneg(logM); base=logF*n-C-c.logpoint(1-p)*(2*n)
 # base conversion error checked against exact interval.
 basefloat=float(Q(base.l+base.h,2*c.S));assert max(abs(Q(basefloat)-Q(base.l,c.S)),abs(Q(basefloat)-Q(base.h,c.S)))<Q(1,10**12)
 bias_parts={'finite_mixture':1-F**n,'categorical_grid':Q(n*K,2**64),'exceptional_uniform':Q(n,2**40),'classification_band':Q(8,10**13)*n*n*qmax,'weight_numerics':Q(1,10**7),'output_quantization':Q(1,2**24)}
 bias=Q(c.ceildiv(sum(bias_parts.values()).numerator*(1<<160),sum(bias_parts.values()).denominator),1<<160);prep={'kind':kind,'a':str(a),'p':str(p),'qmax':str(qmax),'qmax_float':float(qmax),'M':c.encode(M),'logM':c.encode(logM),'bias_parts':{k:float(v) for k,v in bias_parts.items()},'bias_exact':str(bias),'bias_upper':float(bias),'prep_seconds':time.time()-start}
 with open(D+'/'+kind+'.in','w') as f:
  f.write(f'{float(a).hex()} {float(p).hex()} {basefloat.hex()}\n')
  for lam,cdf in zip(ls,cdfs):f.write(float(lam).hex()+' '+' '.join(map(str,cdf))+'\n')
 json.dump(prep,open(D+'/'+kind+'_prep.json','w'),indent=2)
 return prep

def finish(kind,N,seed):
 prep=json.load(open(D+'/'+kind+'_prep.json'));start=time.time()
 proc=subprocess.run([D+'/sampler',D+'/'+kind+'.in',str(N),str(seed)],capture_output=True,text=True,check=True)
 rows=[list(map(int,r.split())) for r in proc.stdout.splitlines()];s=sum(r[0] for r in rows);ss=sum(r[1] for r in rows);events=sum(r[2] for r in rows);exceptions=sum(r[3] for r in rows)
 S=1<<24;mean=Q(s,N*S);var=Q(ss*N-s*s,N*(N-1)*S*S);x=Q(4383,1000)
 term=Q(1);ex=term
 for j in range(1,40):term=term*x/j;ex+=term
 assert ex>80
 rad=c.I.q(2*var*x/N).sqrt()+7*x/(3*(N-1));r=Q(rad.h,c.S);bias=Q(prep['bias_exact']);lo=max(Q(0),mean-r-bias);hi=min(Q(1),mean+r+bias)
 ml=Q(prep['M']['lo']);mh=Q(prep['M']['hi']);res={**prep,'N':N,'seed':seed,'sample_seconds':time.time()-start,'events':events,'exceptions':exceptions,'sum_units':str(s),'sum_squared_units':str(ss),'scale_bits':24,'mean':float(mean),'variance':float(var),'radius_upper':float(r),'relative_halfwidth':float((r+bias)/mean),'probability_interval':{'lo':str(ml*lo),'hi':str(mh*hi),'approx_lo':float(ml*lo),'approx_hi':float(mh*hi)},'assumption':'iid independent fair random bits; mt19937_64 seeded run is only reproducibility, not a proof of randomness'}
 out=D+f'/{kind}_{N}_{seed}.json';json.dump(res,open(out,'w'),indent=2);print(json.dumps({k:v for k,v in res.items() if k not in ['qmax','bias_exact','M','logM']},indent=2))
if __name__=='__main__':
 kind=sys.argv[1];N=int(sys.argv[2]);seed=int(sys.argv[3]) if len(sys.argv)>3 else 187492
 if not os.path.exists(D+'/'+kind+'_prep.json'):prepare(kind)
 finish(kind,N,seed)
