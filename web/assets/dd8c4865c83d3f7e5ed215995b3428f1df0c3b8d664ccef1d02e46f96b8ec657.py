"""Finite-field and deterministic-prefix checks with independent comparators."""
import itertools
import json
import random
import time
from fractions import Fraction
from pathlib import Path
from deterministic_low_sector import BinaryField, small_bias_histogram, DeterministicLowSector, polynomial_mod
from check_low_sector import det, norm, direct_mass

assertions=0

def check(x):
    global assertions
    assertions+=1
    assert x


def main():
    started=time.monotonic();rng=random.Random(60103)
    fields=[]
    for m in range(1,10):
        field=BinaryField(m);q=field.order
        # Direct polynomial-divisor comparator for the acquired modulus.
        for d in range(1,m//2+1):
            for polynomial in range(1<<d,1<<(d+1)):
                check(polynomial_mod(field.modulus,polynomial)!=0)
        for a in range(q):check(field.pow(a,q)==a)
        for _ in range(40):
            a,b,c=[rng.randrange(q) for _ in range(3)]
            check(field.mul(a,b)==field.mul(b,a))
            check(field.mul(a,b^c)==field.mul(a,b)^field.mul(a,c))
            check(field.mul(field.mul(a,b),c)==field.mul(a,field.mul(b,c)))
            if a:check(field.mul(a,field.pow(a,q-2))==1)
        fields.append({'m':m,'q':q,'modulus':field.modulus,'candidates':field.candidates_checked})
    bias_cases=[]
    for f in range(1,8):
        for m in (2,3,4):
            field=BinaryField(m);q=field.order;hist=small_bias_histogram(f,field)
            for subset in range(1,1<<f):
                signed=sum(count*((-1)**((word&subset).bit_count())) for word,count in hist.items())
                roots=0
                for y in range(q):
                    value=0;power=1
                    for i in range(f):
                        if subset>>i&1:value^=power
                        power=field.mul(power,y)
                    if value==0:roots+=1
                check(Fraction(signed,q*q)==Fraction(roots,q))
                check(0<=Fraction(signed,q*q)<=Fraction(f-1,q))
            for size in range(1,min(f,4)+1):
                for selected in itertools.combinations(range(f),size):
                    for bits in itertools.product((0,1),repeat=size):
                        count=sum(weight for word,weight in hist.items()
                                  if all(((word>>i)&1)==b for i,b in zip(selected,bits)))
                        relative_error=abs(Fraction(count*(1<<size),q*q)-1)
                        check(relative_error<=Fraction(((1<<size)-1)*(f-1),q))
            bias_cases.append({'free_bits':f,'q':q,'distinct_words':len(hist)})
    records=[];matrices={}
    for n in range(2,7):
        f=[[(Fraction(rng.randrange(-3,4),5),Fraction(rng.randrange(-3,4),7)) for _ in range(n)] for _ in range(n)]
        matrices[n]=f;engine=DeterministicLowSector(f)
        for k in range(n//2+1):
            true=Fraction(direct_mass(engine,k),engine.denominator**(2*k))
            estimate=engine.deterministic_count(k,Fraction(1,3))
            check(abs(estimate-true)<=true/3)
            check((estimate==0)==(true==0))
            records.append({'n':n,'k':k,'target':str(true),'estimate':str(estimate),'eta':'1/3'})
        k=n//2
        true=Fraction(direct_mass(engine,k,up=(0,),down=(n-1,)),engine.denominator**(2*k))
        estimate=engine.deterministic_count(k,Fraction(1,3),up=(0,),down=(n-1,))
        check(abs(estimate-true)<=true/3)
        check((estimate==0)==(true==0))
    engine=DeterministicLowSector(matrices[4]);prefixes=0
    for length in range(1,5):
        for labels in itertools.product((0,1,-1),repeat=length):
            up=[i for i,label in enumerate(labels) if label==1]
            down=[i for i,label in enumerate(labels) if label==-1]
            empty=[i for i,label in enumerate(labels) if label==0]
            true=Fraction(direct_mass(engine,2,up,down,empty),engine.denominator**4)
            estimate=engine.deterministic_count(2,Fraction(1,3),up,down,empty)
            check(abs(estimate-true)<=true/3)
            check((estimate==0)==(true==0))
            prefixes+=1
    for bits in (8,64,256):
        d=Fraction(1,1<<bits)
        f=[[0,1+d,1,1],[1+d,0,1,2],[1,1,0,1],[1,2,1,0]]
        engine=DeterministicLowSector(f)
        check(engine.deterministic_count(2,Fraction(1,3),up=(0,2),down=(1,3))==d*d)
    zero=DeterministicLowSector([[0 if i==j else 1 for j in range(4)] for i in range(4)])
    check(zero.deterministic_count(2,Fraction(1,3))==0)
    check(zero.born_sample(2,Fraction(3,4),rng=rng)=={'status':'NO_SECTOR'})
    sampler_records=[]
    for n,k,runs in ((3,1,8),(4,2,4),(5,2,1)):
        engine=DeterministicLowSector(matrices[n])
        for seed in range(runs):
            sample=engine.born_sample(k,Fraction(3,4),rng=random.Random(3000+seed))
            check(sample['status']=='OK')
            i,j=sample['I'],sample['J']
            check(len(i)==len(j)==k and not set(i)&set(j))
            check(norm(det([[engine.g[x][y] for y in j] for x in i]))>0)
        check('random_draws' not in engine.stats and 'random_bits' not in engine.stats)
        sampler_records.append({'n':n,'k':k,'successful_runs':runs,'stats':engine.stats})
    # Exact two-site distribution induced by bounded categorical bits.
    class FixedWords:
        def __init__(self,word):self.word=word
        def getrandbits(self,b):return self.word
    engine=DeterministicLowSector([[0,(1,1)],[(2,-1),0]])
    q=64;counts={}
    for word in range(q):
        sample=engine.born_sample(1,Fraction(1,4),rng=FixedWords(word))
        key=(tuple(sample['I']),tuple(sample['J']))
        counts[key]=counts.get(key,0)+1
    target={((0,),(1,)):Fraction(2,7),((1,),(0,)):Fraction(5,7)}
    tv=sum(abs(Fraction(counts.get(key,0),q)-p) for key,p in target.items())/2
    check(tv<=Fraction(1,q))
    result={'status':'PASS','assertions':assertions,'field_fixtures':fields,'bias_cases':bias_cases,
            'exact_prefixes':prefixes,'counts':records,'samplers':sampler_records,'two_site_TV':str(tv),
            'elapsed_seconds':time.monotonic()-started,
            'scope':'Finite exact field/bias/pattern and deterministic relative-prefix checks. No external theorem/priority validation; universal guarantees are in the proof.'}
    Path(__file__).with_name('deterministic_low_sector_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('bias_cases','counts')},indent=2))

if __name__=='__main__':main()
