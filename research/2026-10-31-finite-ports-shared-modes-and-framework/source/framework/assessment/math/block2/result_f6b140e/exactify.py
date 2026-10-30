"""Recover a rational certificate from diagnostic Gram matrices."""
from sos_search import *
extra=[]
extra.extend(mats[0]*s.Matrix([-2,1,-2,1,0]))
extra.extend(mats[1][:,1]);extra.extend(mats[1]*s.Matrix([-1,0,2,0]))
extra.extend(mats[2]*s.Matrix([-2,1,0]))
extra.extend(mats[3]*s.Matrix([-2,1]));extra.append(mats[4][0,0])
eqs=list(Am*s.Matrix(unknown)-bm.subs(nu,s.Rational(1,5)))+extra
solx=list(s.linsolve(eqs,unknown))[0]
free=sorted(set().union(*(z.free_symbols for z in solx)) & set(unknown),key=str)
print('exact free coordinates',free,flush=True)
print('symbolic parameters',solx[-5:],flush=True)
for mat in mats:print('SYMBOLIC',mat.subs(dict(zip(unknown,solx))),flush=True)
# Rounding only independent coordinates preserves every identity and forced kernel.
for denom in [100,1000,10000,100000,1000000]:
    vals={v:s.Rational(round(float(out[unknown.index(v)])*denom),denom) for v in free}
    rat=[s.factor(z.subs(vals)) for z in solx]
    ratmap=dict(zip(unknown,rat));ratmats=[ma.subs(ratmap) for ma in mats]
    allmin=[]
    for ma in ratmats:
        for k in range(1,ma.rows+1):
            allmin.extend(ma.extract(ids,ids).det() for ids in combinations(range(ma.rows),k))
    if all(v>=0 for v in allmin):break
else:raise RuntimeError('no exact PSD rationalization')
assert all(s.expand(e.subs(ratmap))==0 for e in eqs)
print('EXACT PSD at denominator',denom,'parameters',rat[-5:],flush=True)
for mat in ratmats:print(mat,flush=True)
data={str(k):str(val) for k,val in zip(unknown,rat)}
open(__file__.replace('.py','_certificate.json'),'w').write(json.dumps(dict(nu='1/5',values=data),indent=2))
