"""Compare two principal outputs; scientific numbers only, not run resources."""
from decimal import Decimal, localcontext, InvalidOperation
import argparse
import json
from pathlib import Path


def compare(a,b):
    maximum=Decimal(0); where=''; count=0
    def walk(x,y,path=''):
        nonlocal maximum,where,count
        if path.endswith('/resources') or path.endswith('/precision_digits'):
            return
        if isinstance(x,dict):
            assert x.keys()==y.keys(),path
            for k in x: walk(x[k],y[k],path+'/'+k)
        elif isinstance(x,list):
            assert len(x)==len(y),path
            for i,(u,v) in enumerate(zip(x,y)): walk(u,v,path+'/'+str(i))
        elif isinstance(x,str):
            try: dx,dy=Decimal(x),Decimal(y)
            except InvalidOperation:
                assert x==y,path
                return
            if not dx.is_finite() or not dy.is_finite():
                assert x==y,path
                return
            diff=abs(dx-dy);count+=1
            if diff>maximum:maximum,where=diff,path
        else:
            assert x==y,(path,x,y)
    with localcontext() as c:
        c.prec=160
        walk(a,b)
        assert maximum < Decimal('1e-60'), (where,maximum)
    return {'status':'PASS','numeric_string_values_compared':count,
            'max_absolute_difference':str(maximum),'max_difference_path':where,
            'integer_counts_crossings_and_budgets_identical':True,
            'meaning':'Precision consistency only; not an interval or trajectory certificate.'}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('first',type=Path);p.add_argument('second',type=Path)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    r=compare(json.loads(a.first.read_text()),json.loads(a.second.read_text()))
    a.output.write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps(r,indent=2))
