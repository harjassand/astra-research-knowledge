"""Exhaustive integral face checks; positive weights bound the search box."""
from pathlib import Path
import json


def below(weight,bound,total=None):
    return [(i,j) for i in range(bound//weight[0]+1)
            for j in range(bound//weight[1]+1)
            if i*weight[0]+j*weight[1]<=bound
            and (total is None or i+j<=total)]


def face(weight,bound):
    return [(i,j) for i,j in below(weight,bound)
            if i*weight[0]+j*weight[1]==bound]


assert below((1,2),4,3)==[(0,0),(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)]
assert face((1,2),4)==[(0,2),(2,1),(4,0)]
assert face((2,3),6)==[(0,2),(3,0)]
assert face((2,3),5)==[(1,1)]
assert face((1,2),3)==[(1,1),(3,0)]
assert face((1,3),3)==[(0,1),(3,0)]
out={'IIb_21_products_including_self':below((1,2),4,3),
     'IIb_top_tangent_products':face((1,2),4),
     'IIc_top_tangent_products':face((2,3),6),
     'IIc_weight5_only_product':face((2,3),5),
     'IId_weight3_products_u12':face((1,2),3),
     'IId_weight3_products_u13':face((1,3),3)}
Path(__file__).with_name('exact_faces.json').write_text(json.dumps(out,indent=2)+'\n')
print('All six integral face enumerations passed.')
