"""Independent ordinary route: balanced binaryization of fixed proposals.

Four exact corners per artificial binary node; upward moment rounding.
No direct many-way secant relaxation is used.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time
START=time.monotonic();OUT=Path(__file__).resolve().parent
def roundup(x,bits=48):
    exponent=x.numerator.bit_length()-x.denominator.bit_length()
    power=F(2)**exponent
    if x<power:exponent-=1
    step=F(2)**(exponent-bits+1);scaled=x/step
    return ((scaled.numerator+scaled.denominator-1)//scaled.denominator)*step
def join(left,right):
    pl,ql,ll,ul,bl,dl=left;pr,qr,lr,ur,br,dr=right
    pm,qm=pl+pr,ql+qr;p,q=pl/(pl+pr),ql/(ql+qr)
    costs=[]
    for x in [ll,ul]:
        for y in [lr,ur]:
            costs.append((p*p*bl*x*x/q+(1-p)**2*br*y*y/(1-q))/(p*x+(1-p)*y)**2)
    return pm,qm,(pl*ll+pr*lr)/pm,(pl*ul+pr*ur)/pm,roundup(max(costs)),max(dl,dr)+1
rows=[]
for name in ['16_narrow','16_heterogeneous_width','4096_heterogeneous_width']:
    start=time.monotonic();data=json.loads((OUT/f'INPUT_{name}.json').read_text())['branch']
    P,q,B,lo,hi=([F(z) for z in data[k]] for k in ['P','q','B','ell','up'])
    load_time=time.monotonic()-start
    start=time.monotonic();layer=[(p,qq,l,u,b,0) for p,qq,l,u,b in zip(P,q,lo,hi,B)];nodes=0
    while len(layer)>1:
        nxt=[]
        for i in range(0,len(layer)-1,2):nxt.append(join(layer[i],layer[i+1]));nodes+=1
        if len(layer)%2:nxt.append(layer[-1])
        layer=nxt
    cert=layer[0];seconds=time.monotonic()-start
    exact=json.loads((OUT/f'CERT_{name}.json').read_text());upper=F(exact['upper'])
    row={'name':name,'k':len(P),'binary_upper':str(cert[4]),'display_binary_upper':float(cert[4]),
         'secant_upper':str(upper),'binary_relative_to_secant':float(cert[4]/upper),
         'artificial_depth':cert[5],'binary_nodes':nodes,'corner_checks':4*nodes,
         'moment_rounding_bits':48,'input_loading_seconds':load_time,'binary_seconds':seconds}
    rows.append(row);print(json.dumps(row),flush=True)
result={'status':'BINARY_ALTERNATIVE_ACQUIRED','cases':rows,'module_seconds':time.monotonic()-START,
        'scope':'Same fixed proposal via balanced binary tree. Safe upper bounds, not exact many-way box maxima. Input interval acquisition remains separate.'}
(OUT/'BINARY_ALTERNATIVE.json').write_text(json.dumps(result,indent=2)+'\n')
