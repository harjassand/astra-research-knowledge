"""One predeclared receiver execution and same-output ordinary Wild control."""
from pathlib import Path
from fractions import Fraction as F
import json,random,time,hashlib
from dataclasses import asdict
from quantized import (Counts,Bits,Real,Normal,Uniform,Receiver,const,less,
                       quantize,ROTATIONS,transpose_apply,run)

def initial(bits):
    z = [Normal(bits) for _ in range(3)]
    if bits.bit() == 0:
        return [z[0],const(F(21,20),bits.counts).sqrt()*z[1],
                const(F(11,10),bits.counts).sqrt()*z[2]]
    # Cholesky of [[26/25,1/25,0],[1/25,26/25,0],[0,0,21/20]].
    l = const(F(26,25),bits.counts).sqrt()
    off = F(1,25)/l
    return [l*z[0],off*z[0]+(F(26,25)-off**2).sqrt()*z[1],
            const(F(21,20),bits.counts).sqrt()*z[2]]

def ordinary_wild(t,bits):
    stack,values,leaves = [('node',const(t,bits.counts))],[],0
    while stack:
        kind,left = stack.pop()
        if kind == 'combine':
            a,b = values.pop(),values.pop()
            delta = [x-y for x,y in zip(a,b)]
            # transpose vs forward law is immaterial for this symmetric R catalog.
            rotated = transpose_apply(ROTATIONS[bits.integer(4)],delta)
            values.append([(x+y+r)/2 for x,y,r in zip(a,b,rotated)])
        else:
            wait = -Uniform(bits).log()
            if not less(wait,left,bits.counts):
                values.append(initial(bits));leaves += 1
            else:
                rest = left-wait
                stack.extend([('combine',None),('node',rest),('node',rest)])
    assert len(values) == 1
    return values[0],leaves

def main():
    root = Path(__file__).resolve().parent
    first = root/'EXECUTION.json'
    saved = root/'FIRST_EXECUTION.json'
    if first.exists() and not saved.exists():
        saved.write_bytes(first.read_bytes())
    result = run([F(0),F(3),F(1000000)],200,2026102991)
    ordinary = []
    rng = random.Random(2026102993)
    for t in [F(0),F(3)]:
        counts = Counts();bits = Bits(lambda:rng.getrandbits(1),counts)
        outputs,leaves = [],0
        tick = time.perf_counter()
        for _ in range(200):
            v,n = ordinary_wild(t,bits);leaves += n
            outputs.append([quantize(x,F(1,4),counts) for x in v])
        ordinary.append(dict(t=str(t),n=200,quantization_width='1/4',integer_bins=outputs,
                             leaves=leaves,counts=asdict(counts),seconds=time.perf_counter()-tick))
    result['ordinary_same_bin_control'] = dict(seed=2026102993,rows=ordinary,
        contract='same rational initial covariance catalog and finite collision kernel, same exact bin law under iid bits',
        excluded='no ordinary Wild execution at t=1e6; expected genealogical leaves exp(t), not an all-solver lower bound')
    result['source_sha256'] = {p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in [root/'quantized.py',root/'consume.py']}
    (root/'EXECUTION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(receiver=[{k:x[k] for k in ['t','n','counts','seconds']} for x in result['rows']],
        ordinary=[{k:x[k] for k in ['t','n','leaves','counts','seconds']} for x in ordinary]),indent=2))

if __name__ == '__main__':
    main()
