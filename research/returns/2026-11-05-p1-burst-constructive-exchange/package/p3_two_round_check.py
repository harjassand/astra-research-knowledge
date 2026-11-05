"""Independent exact check: one normalization plus logical identity suffices.
This checks only the semantic island abstraction, not full physical routing.
"""
from itertools import product
from pathlib import Path
import json

def majority(x): return x.bit_count()>=3

def regular(x): return x.bit_count()<=1 or x.bit_count()>=4

def setbit(x,i,b): return (x & ~(1<<i)) | (b<<i)

def run(initial,fr,fp,site,new_info,held_values,spoiled):
    x=initial
    for r in range(2):
        held=[0,0,0]
        for p in range(3):
            if (r,p)==(fr,fp):
                x=setbit(x,site,new_info)
                for h in range(3):held[h]=setbit(held[h],site,(held_values>>h)&1)
                held[p]=spoiled
            else:held[p]=31 if majority(x) else 0
        x=(held[0]&held[1])|(held[0]&held[2])|(held[1]&held[2])
    return x

def main():
    count=0
    for args in product(range(32),range(2),range(3),range(5),range(2),range(8),range(32)):
        out=run(*args)
        assert regular(out)
        assert not regular(args[0]) or majority(out)==majority(args[0])
        count+=1
    result={'rounds':2,'normalizing_rounds_before_gate':1,'cases':count,
            'all_exact_checks_passed':True,'scope':'identity semantic core only'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
