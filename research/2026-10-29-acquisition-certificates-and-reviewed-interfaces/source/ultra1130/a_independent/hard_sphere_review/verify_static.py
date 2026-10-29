"""Independent small read-only intake, not a kinetic/grid reproduction.

Checks saved exact interval coverage, declared hashes, source moments and
scalar Gaussian/factory/finite-cell inequalities. Never imports the producer
programs, runs their LP/row integration grid, or generates kinetic samples.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,time
from flint import arb,fmpq,ctx

ctx.prec=192
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent.parent/'t_near_equilibrium'

def b(q):
    q=F(q);return arb(fmpq(q.numerator,q.denominator))

def scalar_record(x):
    return str(x)

def cdf(s,beta):
    s=b(s)
    return (s*(beta/2).sqrt()).erf()-s*(2*beta/arb.pi()).sqrt()*(-beta*s*s/2).exp()

def main():
    start=time.perf_counter()
    rec=json.loads((SOURCE/'FINAL_RECEIPT.json').read_text())
    hashes=[]
    for item in rec['manifest']:
        p=SOURCE/item['path'];raw=p.read_bytes();digest=hashlib.sha256(raw).hexdigest()
        hashes.append({'path':item['path'],'sha256':digest,'matches_producer_receipt':digest==item['sha256']})
    rows=json.loads((SOURCE/'RADIAL_ROW_CERTIFICATE.json').read_text())
    ordered=sorted(rows['head_admission'],key=lambda x:F(*x['v_interval'][0]))
    last=F(0)
    for row in ordered:
        lo,hi=(F(*x) for x in row['v_interval'])
        assert lo==last and hi>lo and F(*row['row_bound_upper'])<F(99,100)
        last=hi
    assert last==8 and not rows['failures'] and not rows['pending']
    assert F(*rows['v_tail_bound_upper'])<F(99,100)
    aa=max(abs(F(*row['controls'][0])) for row in ordered)
    cc=max(abs(F(*row['controls'][1])) for row in ordered)
    assert F(41,189)*F(12,5)+F(148,189)*F(2343,740)==3
    assert F(41,189)*F(3,32)+F(148,189)*F(6,37)==F(33,224)

    beta=b(F(3,4));D=b(F(1,3200));nu0=2*(2/arb.pi()).sqrt()
    Z=(2*arb.pi())**F(3,8)*beta**F(-3,2)
    C=Z/beta.sqrt()
    assert C.upper()<4 and Z.upper()<b(F(16,5))
    offspring=b(F(99,100))+4*D*C
    assert offspring.upper()<b(F(199,200))
    E=16+b(F(8,3))+4+beta**F(-3,2)/nu0*(b(aa)+4*b(cc))
    assert E.upper()<48
    assert 2+F(48)/(1-F(1,400))<51
    assert F(19,2)*51/F(3,400)==64600

    am=[cdf(1,b(1)),cdf(2,b(1))-cdf(1,b(1)),1-cdf(2,b(1))]
    bm=[Z*cdf(1,beta),Z*(cdf(2,beta)-cdf(1,beta)),Z*(1-cdf(2,beta))]
    margins=[a-D*c for a,c in zip(am,bm)]
    assert all(x.lower()>b(F(1,10)) for x in margins)
    cube_ratio=(2*arb.pi())**F(-3,8)*(-b(6)).exp()
    overflow_a=1-(b(4)/b(2).sqrt()).erf()**3
    overflow_b=Z*(1-(b(4)*(beta/2).sqrt()).erf()**3)
    assert cube_ratio.lower()>D and (overflow_a-D*overflow_b).lower()>0
    assert F(48)*34/F(200000)<F(1,100)
    assert F(1,40)+F(40,3200)<F(1,16)

    result={'scope':'Independent exact manifest/cover/source checks and outward scalar inequalities only; no operator-row-grid or kinetic rerun.',
       'all_producer_manifest_hashes_match':all(x['matches_producer_receipt'] for x in hashes),
       'hashes':hashes,'head_intervals':len(ordered),'head_cover':['0','8'],
       'largest_row_upper':str(max(F(*r['row_bound_upper']) for r in ordered)),
       'speed_tail_upper':str(F(*rows['v_tail_bound_upper'])),
       'Z_beta':str(Z),'C_beta':str(C),'offspring_upper_expression':str(offspring),
       'envelope_uniform_expression':str(E),'factory_base_coin_upper':64600,
       'three_cell_positive_margins':list(map(str,margins)),
       'cube_inside_ratio':str(cube_ratio),'cube_overflow_margin':str(overflow_a-D*overflow_b),
       'seconds_after_imports':time.perf_counter()-start,'new_kinetic_samples':0,'row_grid_rerun':False}
    (HERE/'STATIC_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='hashes'},indent=2))

if __name__=='__main__':main()
