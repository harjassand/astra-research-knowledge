#!/usr/bin/env python3
"""Compare scientific certificate outputs at two arithmetic precisions."""
import argparse
import json
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path

getcontext().prec=160
SKIP={'started_utc','finished_utc','wall_seconds','dps','python','source_sha256',
      'identity_absolute_error'}


def compare(a,b,path='',stats=None):
    if stats is None: stats={'numeric_comparisons':0,'max_scaled_difference':Decimal(0)}
    if isinstance(a,dict):
        assert set(a)==set(b),(path,'keys')
        for key in a:
            if key not in SKIP: compare(a[key],b[key],path+'/'+key,stats)
    elif isinstance(a,list):
        assert len(a)==len(b),(path,'length')
        for i,(x,y) in enumerate(zip(a,b)): compare(x,y,path+f'/{i}',stats)
    elif isinstance(a,str):
        try: x,y=Decimal(a),Decimal(b)
        except InvalidOperation:
            assert a==b,(path,a,b)
        else:
            diff=abs(x-y)/max(Decimal(1),abs(x),abs(y))
            stats['numeric_comparisons']+=1
            stats['max_scaled_difference']=max(stats['max_scaled_difference'],diff)
            assert diff<Decimal('1e-45'),(path,diff)
    else:
        assert a==b,(path,a,b)
    return stats


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('left',type=Path);p.add_argument('right',type=Path)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    result=compare(json.loads(args.left.read_text()),json.loads(args.right.read_text()))
    result['max_scaled_difference']=str(result['max_scaled_difference'])
    result.update(status='passed',threshold='1e-45',
                  qualification='Precision consistency of numerical values, not an interval proof.')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
