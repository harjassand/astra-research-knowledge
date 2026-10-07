"""Exact finite control comparisons; owned output only."""
import itertools
import json
import math
import random
import time
from fractions import Fraction
from pathlib import Path
from color_sector_control import ColorSector
from low_sector_sampler import LowSector
from check_low_sector import det, norm, direct_mass

assertions=0

def check(value):
    global assertions
    assertions+=1
    assert value


def direct_draw(engine,k,signs,up=(),down=(),empty=()):
    up,down,empty=set(up),set(down),set(empty)
    if len(up)>k or len(down)>k or 2*k>engine.n-len(empty): return 0
    if k==0:return 1
    free=set(range(engine.n))-up-down-empty
    left=up|{i for i in free if signs[i]==1}
    right=down|{i for i in free if signs[i]==-1}
    directions=[(left,right)]
    if not up and not down: directions.append((right,left))
    value=0
    for rows,cols in directions:
        for ii in itertools.combinations(sorted(rows),k):
            if not up<=set(ii): continue
            for jj in itertools.combinations(sorted(cols),k):
                if not down<=set(jj):continue
                value+=norm(det([[engine.g[i][j] for j in jj] for i in ii]))
    return engine.range_multiplier(k,len(up),len(down))*value


def audit(f,k,up=(),down=(),empty=(),name=''):
    engine=ColorSector(f);pfengine=LowSector(f)
    free=sorted(set(range(engine.n))-set(up)-set(down)-set(empty))
    true=direct_mass(engine,k,up,down,empty)
    bad=len(up)>k or len(down)>k or 2*k>engine.n-len(empty)
    c=0 if bad else engine.range_multiplier(k,len(up),len(down))
    values=[];pvalues=[]
    for word in itertools.product((-1,1),repeat=len(free)):
        signs=[1]*engine.n
        for i,s in zip(free,word): signs[i]=s
        value=engine.prefix_draw_integer(k,signs,up,down,empty)
        check(value==direct_draw(engine,k,signs,up,down,empty))
        check(0<=value<=c*true)
        values.append(value)
        pvalues.append(pfengine.prefix_draw_integer(k,signs,up,down,empty))
    mean=Fraction(sum(values),len(values));second=Fraction(sum(x*x for x in values),len(values))
    check(mean==true)
    check(second<=c*true*true)
    psecond=Fraction(sum(x*x for x in pvalues),len(pvalues))
    return {'name':name,'n':engine.n,'k':k,'up':list(up),'down':list(down),'empty':list(empty),
            'sign_words':len(values),'target':str(Fraction(true,engine.denominator**(2*k))),
            'color_C':c,'color_relative_second_moment':str(second/(true*true)) if true else 'ZERO',
            'pfaffian_relative_second_moment':str(psecond/(true*true)) if true else 'ZERO'}


def main():
    started=time.monotonic();rng=random.Random(712244);cases=[];matrices={}
    for n in range(2,7):
        f=[[(Fraction(rng.randrange(-4,5),3),Fraction(rng.randrange(-4,5),5)) for _ in range(n)] for _ in range(n)]
        matrices[n]=f
        for k in range(n//2+1):cases.append(audit(f,k,name='generic_rational_root'))
        cases.append(audit(f,n//2,up=(0,),down=(n-1,),name='up_down'))
        cases.append(audit(f,1,down=(0,),empty=(1,),name='down_empty'))
    for length in range(1,5):
        for labels in itertools.product((0,1,-1),repeat=length):
            up=[i for i,label in enumerate(labels) if label==1]
            down=[i for i,label in enumerate(labels) if label==-1]
            empty=[i for i,label in enumerate(labels) if label==0]
            cases.append(audit(matrices[4],2,up,down,empty,name='all_four_site_prefixes'))
    f=[[0]*4 for _ in range(4)];f[0][2]=f[1][3]=1
    unique=audit(f,2,name='unique_supported_word')
    check(unique['color_relative_second_moment']=='8')
    check(unique['pfaffian_relative_second_moment']=='1')
    cases.append(unique)
    cases.append(audit([[0 if i==j else 1 for j in range(4)] for i in range(4)],2,name='exact_zero'))
    sampler_runs=[]
    for n,k,runs in ((3,1,8),(4,2,8),(5,2,4)):
        engine=ColorSector(matrices[n])
        for seed in range(runs):
            sample=engine.born_sample(k,Fraction(3,4),rng=random.Random(2000+seed),enumerate_if_cheaper=False)
            check(sample['status']=='OK')
            i,j=sample['I'],sample['J']
            check(len(i)==len(j)==k and not set(i)&set(j))
            check(norm(det([[engine.g[x][y] for y in j] for x in i]))>0)
        sampler_runs.append({'n':n,'k':k,'runs':runs,'stats':engine.stats})
    result={'status':'PASS','assertions':assertions,'cases':len(cases),'sign_words':sum(x['sign_words'] for x in cases),
            'elapsed_seconds':time.monotonic()-started,'fixtures':cases,'samplers':sampler_runs,
            'scope':'Independent exact color-coding/prefix comparisons and 20 full-cap sampler runs. No universal variance advantage or unrestricted FPRAS claim.'}
    Path(__file__).with_name('color_sector_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='fixtures'},indent=2))

if __name__=='__main__':main()
