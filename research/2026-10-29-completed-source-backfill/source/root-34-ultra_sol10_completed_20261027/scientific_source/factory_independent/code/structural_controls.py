"""Independent exact local controls for spectral closure and fusion loss."""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import json
from model import Chain, beamsplitter, EFF

ROOT=Path(__file__).resolve().parents[1]

def falling(k,s):
    return factorial(k)//factorial(k-s) if k>=s else 0

def run():
    records=[]
    for lam in (F(999,1000),F(99999,100000),F(1)):
        chain=Chain(lam); kernel_components=0; spectral_components=0
        for i in range(5):
            for j in range(5):
                before=[F(0)]*9
                for a,pa in enumerate(chain.loss(i)):
                    for b,pb in enumerate(chain.loss(j)):
                        for r,pbs in enumerate(beamsplitter(a,b)):
                            before[r]+=pa*pb*pbs*(1-EFF)**(a+b-r)
                after=[sum(pbs*(1-EFF*lam)**(i+j-k)*comb(k,r)*lam**r*(1-lam)**(k-r)
                       for k,pbs in enumerate(beamsplitter(i,j)) if k>=r)
                       for r in range(9)]
                assert before==after
                kernel_components+=len(before)
        for i in range(9):
            for s in range(9):
                assert sum(p*falling(k,s) for k,p in enumerate(chain.loss(i)))==lam**s*falling(i,s)
                spectral_components+=1
        records.append({'lambda':str(lam),'loss_before_vs_after_BS_exact_components':kernel_components,
                        'pure_death_falling_factorial_exact_components':spectral_components})
    counts={1:1}
    for n in (2,4,8,16,32):counts[n]=(n+1)**2+(n+2)*counts[n//2]
    output={'status':'PASS_EXACT_LOCAL_AND_SPECTRAL_CONTROLS','cases':records,
            'literal_transient_state_count_recurrence':counts,
            'scope':'Input photon counts 0..4 and pure-death support 0..8; exact identities have separate general proof.'}
    (ROOT/'results/structural_controls.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))

if __name__=='__main__':run()
