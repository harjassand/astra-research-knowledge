"""Exact-rational check of unmarked native calibration cells for HB+3-cycles."""
from fractions import Fraction as F
from pathlib import Path
import json, random

OUT=Path(__file__).resolve().parent
rng=random.Random(708113)
checks=0
models=[]

for n in range(1,9):
    for style in ('forward','reverse','alternating','random'):
        a=[F(rng.randrange(90,111),100) for _ in range(n)]
        b=[F(rng.randrange(90,111),100) for _ in range(n-1)]
        alpha=[F(rng.randrange(50,101),100) for _ in range(n-1)]
        forward=[style=='forward' or (style=='alternating' and i%2==0)
                 or (style=='random' and bool(rng.randrange(2))) for i in range(n-1)]
        # Also verify the extension with unknown positive HB attempt rates.
        lam=[F(rng.randrange(80,121),100) for _ in range(n)]
        cells={}
        def record(key,value,expected):
            global checks
            assert value==expected,(n,style,key,value,expected)
            if key in cells:
                assert cells[key]==value
            cells[key]=value
            checks+=1
        for x in range(2**n):
            bits=[(x>>i)&1 for i in range(n)]
            rates={}
            for i in range(n):
                odds=a[i]
                if i and bits[i-1]: odds*=b[i-1]
                if i+1<n and bits[i+1]: odds*=b[i]
                rates[1<<i]=lam[i]*(odds if not bits[i] else 1)/(1+odds)
            for i in range(n-1):
                code=bits[i]+2*bits[i+1]
                newcode=([1,3,2,0] if forward[i] else [3,0,2,1])[code]
                if code==newcode: continue
                v=a[i]**bits[i]*a[i+1]**bits[i+1]
                for j in range(max(0,i-1),min(n-1,i+2)):
                    v*=b[j]**(bits[j]*bits[j+1])
                mask=(code^newcode)<<i
                rates[mask]=rates.get(mask,F(0))+alpha[i]/v
            for i in range(n):
                left_zero=(i==0 or bits[i-1]==0)
                if not left_zero: continue
                if i+1<n and bits[i+1]==1:
                    odds=a[i]*b[i]
                    record(('hb01',i,bits[i]),rates[1<<i],
                           lam[i]*(odds if not bits[i] else 1)/(1+odds))
                if i==n-1:
                    record(('last',i,bits[i]),rates[1<<i],
                           lam[i]*(a[i] if not bits[i] else 1)/(1+a[i]))
                elif bits[i+1]==0 and bits[i]==int(forward[i]):
                    record(('hb00',i),rates[1<<i],
                           lam[i]*(1 if forward[i] else a[i])/(1+a[i]))
            for i in range(n-1):
                if forward[i]:
                    if not(bits[i]==bits[i+1]==1): continue
                    if i and bits[i-1]: continue
                    if i+2<n and bits[i+2]: continue
                    record(('cycle',i),rates[3<<i],alpha[i]/(a[i]*a[i+1]*b[i]))
                elif bits[i]==bits[i+1]==0:
                    record(('cycle',i),rates[3<<i],alpha[i])
        ahat=[]; bhat=[]; lhat=[]
        for i in range(n):
            if i==n-1:
                up=cells['last',i,0]; down=cells['last',i,1]
                li=up+down; ai=up/down
            else:
                up=cells['hb01',i,0]; down=cells['hb01',i,1]
                li=up+down
                q=cells['hb00',i]
                ai=(li-q)/q if forward[i] else q/(li-q)
                bhat.append((up/down)/ai)
            lhat.append(li); ahat.append(ai)
        alhat=[]
        for i in range(n-1):
            val=cells['cycle',i]
            alhat.append(val*ahat[i]*ahat[i+1]*bhat[i] if forward[i] else val)
        assert ahat==a and bhat==b and lhat==lam and alhat==alpha
        models.append({'n':n,'orientation':style,'distinct_rate_cells':len(cells)})

result={'exact_native_rate_checks':checks,'models':models,
        'all_parameters_recovered_exactly':True,
        'scope':'Checks all global states in each listed rational model; proof is in PASSIVE_IDENTIFIABILITY.txt.'}
(OUT/'native_clean_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'exact_native_rate_checks':checks,'model_count':len(models),
                  'all_parameters_recovered_exactly':True}))
