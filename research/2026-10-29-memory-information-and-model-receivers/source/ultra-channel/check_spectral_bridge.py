"""All-moduli integer affine identities; no finite-modulus extrapolation."""
from pathlib import Path
from time import perf_counter
import hashlib,json

HERE=Path(__file__).resolve().parent
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

def main():
    start=perf_counter()
    R=[[-1,0,0],[0,1,0],[0,0,1]]
    primary=[[[1,2,0],[0,1,0],[0,0,1]],[[1,2,1],[0,1,0],[0,0,1]],
             [[1,0,0],[2,1,0],[0,0,1]],[[1,0,0],[2,1,-1],[0,0,1]]]
    ours=[[[1,2,0],[0,1,0],[0,0,1]],[[1,2,1],[0,1,0],[0,0,1]],
          [[1,0,0],[2,1,0],[0,0,1]],[[1,0,0],[2,1,1],[0,0,1]]]
    inv=[[[1,-2,0],[0,1,0],[0,0,1]],[[1,-2,-1],[0,1,0],[0,0,1]],
         [[1,0,0],[-2,1,0],[0,0,1]],[[1,0,0],[-2,1,-1],[0,0,1]]]
    I=[[int(i==j) for j in range(3)] for i in range(3)]
    assert mul(R,R)==I
    for a,b,c in zip(primary,ours,inv):
        assert mul(mul(R,a),R)==c and mul(b,c)==mul(c,b)==I
    assert 1250<1296  # (5 sqrt2)^2 < (36/5)^2, so8-5sqrt2>4/5.
    out={'status':'PASS','integer_identities':4,'primary_generators':primary,'our_generators':ours,
         'reflection':R,'primary_conjugated_to_our_inverses':inv,
         'scope':'all positive integer moduli; no oddness or modular test sample',
         'primary_pdf_sha256':hashlib.sha256((HERE/'source_entry/gross_eisert.pdf').read_bytes()).hexdigest(),
         'source_scope':'acquired primary research statement of named standard classical bound; original GG/JM proof not read',
         'seconds':perf_counter()-start}
    (HERE/'SPECTRAL_BRIDGE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
