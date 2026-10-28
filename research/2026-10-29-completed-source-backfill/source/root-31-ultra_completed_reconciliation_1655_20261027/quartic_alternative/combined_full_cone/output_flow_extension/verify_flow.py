"""Read-only exact replay using the frozen standard-library polynomial helper.

No producer, numeric arrays, solver or symbolic package is imported. The
parent's separate SymPy implementation uses no author code at all.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement as cwr
import json,hashlib,time,argparse,math
ROOT=Path(__file__).resolve().parent
import literal_polynomials as P


def evaluate(poly,values):
    return sum((c*math.prod(x**n for x,n in zip(values,e)) for e,c in poly.items()),F(0))
def substitute(poly,values):
    return P.add(*(P.scale(P.product(values[i] for i in range(4) for j in range(e[i])),c) for e,c in poly.items()))
def mean(A,B):return [[(A[i][j]+B[i][j])/2 for j in range(2)] for i in range(2)]
def conjugate(A,O):return [[sum(O[i][k]*A[k][l]*O[j][l] for k in range(2) for l in range(2)) for j in range(2)] for i in range(2)]
def normal_form():
    J=[[F(0),F(-1)],[F(1),F(0)]];D=[[F(1),F(0)],[F(0),F(-1)]]
    for basis in range(12):
        blocks=[[[F(0)]*2 for i in range(2)] for k in range(3)]
        blocks[basis//4][(basis%4)//2][basis%2]=F(1);original=blocks
        blocks=[mean(M,conjugate(M,J)) for M in blocks]
        diag=mean(blocks[0],blocks[2]);blocks=[diag,blocks[1],diag]
        blocks=[mean(M,conjugate(M,D) if k!=1 else [[-x for x in row] for row in conjugate(M,D)]) for k,M in enumerate(blocks)]
        aa=sum(original[k][i][i] for k in [0,2] for i in range(2))/4
        bb=(original[1][1][0]-original[1][0][1])/2
        assert blocks==[[[aa,F(0)],[F(0),aa]],[[F(0),-bb],[bb,F(0)]],[[aa,F(0)],[F(0),aa]]]


def main(write=False):
    start=time.monotonic();path=ROOT/'EXACT_FLOW_FAMILY.json';raw=path.read_bytes();r=json.loads(raw)
    target_raw=(ROOT/'SYMMETRIC_TARGET.json').read_bytes();target=json.loads(target_raw)
    p=list(map(F,target['coefficients']));assert p==list(map(F,r['target_coefficients']))
    a=[P.var(i) for i in range(4)];z=[P.var(i+4) for i in range(6)]
    f=P.add(*(P.scale(poly,c) for poly,c in zip(P.bases(a),p)));q=P.invariants(a)[3];q2=P.mul(q,q)
    transformations=[[P.scale(a[2],-1),P.scale(a[3],-1),a[0],a[1]],
                     [a[1],a[0],a[3],a[2]],[a[0],P.scale(a[1],-1),P.scale(a[2],-1),a[3]]]
    for t in transformations:assert substitute(f,t)==f and substitute(q2,t)==q2
    normal_form()
    J1=[z[0],z[1],z[3],z[4]];J2=[z[1],z[2],z[4],z[5]]
    rotate=lambda v:[P.scale(v[2],-1),P.scale(v[3],-1),v[0],v[1]]
    JB1,JB2=rotate(J1),rotate(J2)
    def diss(poly,mixed=False):
        return P.add(*(P.mul((P.add(P.mul(J1[i],JB2[j]),P.mul(J2[i],JB1[j])) if mixed else P.add(P.mul(J1[i],J1[j]),P.mul(J2[i],J2[j]))),P.diff(P.diff(poly,i),j)) for i in range(4) for j in range(4)))
    ef,ejf,ed,ejd=diss(f),diss(f,True),diss(q2),diss(q2,True)
    monoms=[next(iter(P.product([a[i],a[j],z[k],z[l]]))) for i,j in cwr(range(4),2) for k,l in cwr(range(6),2)]
    assert len(monoms)==len(set(monoms))==210
    l0,l1=list(map(F,r['L0'])),list(map(F,r['L1']));assert len(l0)==len(l1)==210
    def functional(values):
        lookup=dict(zip(monoms,values))
        def apply(poly):
            assert set(poly)<=set(lookup)
            return sum((c*lookup[e] for e,c in poly.items()),F(0))
        return apply
    L0,L1=functional(l0),functional(l1);Le=functional([x+y for x,y in zip(l0,l1)])
    features=[P.mul(ai,zz) for ai in a for zz in z];pivots=[]
    for apply,key in [(L0,'moment0_LDL_pivots'),(Le,'moment_end_LDL_pivots')]:
        M=[[apply(P.mul(v,w)) for w in features] for v in features]
        pivots+=P.positive_matrix(M,r[key])
    pairs=list(combinations(range(4),2));triples=list(combinations(range(4),3))
    for apply,key in [(L0,'closedness_eta0'),(L1,'closedness_eta1')]:
        eta=list(map(F,r[key]));assert len(eta)==16
        for i,j in pairs:
            for k,l in cwr(range(4),2):
                mono=P.mul(a[k],a[l]);pull=P.mul(mono,P.add(P.mul(J1[i],J2[j]),P.scale(P.mul(J1[j],J2[i]),-1)))
                def omega(s,t):return mono if (s,t)==(i,j) else P.scale(mono,-1) if (t,s)==(i,j) else {}
                expected=F(0)
                for h,(s,t,u) in enumerate(triples):
                    derivative=P.add(P.diff(omega(t,u),s),P.scale(P.diff(omega(s,u),t),-1),P.diff(omega(s,t),u))
                    for index in range(4):
                        e=[0]*10;e[index]=1;expected+=eta[4*h+index]*derivative.get(tuple(e),F(0))
                assert apply(pull)==expected
    G=F(r['gamma_upper']);bound=json.loads((ROOT/'GAMMA_BOUND.json').read_text());assert G==F(bound['used_rational_upper_bound'])>0
    AA=list(map(F,bound['A']));eta=list(map(F,bound['eta']));assert eta[0]==1
    zz=eta[1];curve=P.add(P.diff(P.diff(f,0),0),P.scale(P.diff(P.diff(f,0),1),2*zz),P.scale(P.diff(P.diff(f,1),1),zz*zz))
    curvature=evaluate(curve,AA+[F(0)]*6);detprime=AA[3]-zz*AA[2]
    assert curvature==F(bound['F_curvature'])>0 and detprime==F(bound['det_derivative'])!=0
    assert curvature/(2*detprime*detprime)==F(bound['exact_gamma_upper_bound'])<=G
    assert L0(ejf)==0 and L1(ejf)-G*L0(ejd)==0 and L1(ejd)==0
    coeff=[L0(ef),L1(ef)-G*L0(ed),-G*L1(ed)];bern=[coeff[0],coeff[0]+coeff[1]/2,sum(coeff)]
    assert coeff==list(map(F,r['energy_power_coefficients']))
    assert bern==list(map(F,r['energy_Bernstein_coefficients'])) and all(x<0 for x in bern)
    s,t=z[0],z[1];features8=[P.mul(s,ai) for ai in a]+[P.mul(t,ai) for ai in a]
    Q=[[F(c) for c in row] for row in target['ROC_matrix']];rho=F(target['ROC_shift']);assert rho==F(1,400000)
    ac=P.add(P.mul(P.mul(s,s),P.diff(P.diff(f,0),0)),P.scale(P.mul(P.mul(s,t),P.diff(P.diff(f,0),1)),2),P.mul(P.mul(t,t),P.diff(P.diff(f,1),1)))
    assert ac==P.add(*(P.scale(P.mul(features8[i],features8[j]),Q[i][j]*(1 if i==j else 2)) for i in range(8) for j in range(i,8)))
    dr=P.positive_matrix([[Q[i][j]-(rho if i==j else 0) for j in range(8)] for i in range(8)],target['shifted_LDL_pivots'])
    out={'status':'EXACT_LITERAL_ALL_B_GAMMA_PURE_FLOW_OBSTRUCTION_PASS',
         'family_sha256':hashlib.sha256(raw).hexdigest(),'symmetric_target_sha256':hashlib.sha256(target_raw).hexdigest(),
         'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'frozen_literal_helper_sha256':hashlib.sha256(Path(P.__file__).read_bytes()).hexdigest(),
         'endpoint_positive_pivots':len(pivots),'ROC_shifted_positive_pivots':len(dr),
         'closedness':'ALL60_LITERAL_COLUMNS_FOR_BOTH_AFFINE_PARTS',
         'operator_normal_form':'ALL12_REAL_COEFFICIENT_BASIS_IMAGES_CHECKED',
         'target_symmetries':'OUTPUT_QUARTER_TURN_COLUMN_SWAP_PAIRED_REFLECTION_EXACT',
         'mixed_polynomial_identically_zero':True,'gamma_upper':str(G),'energy_Bernstein_coefficients':list(map(str,bern)),
         'maximum_pivot_integer_bits':max(max(abs(x.numerator).bit_length(),x.denominator.bit_length()) for x in pivots+dr),
         'seconds':time.monotonic()-start,'imports':'PYTHON_STDLIB_AND_FROZEN_LITERAL_POLYNOMIAL_HELPER',
         'scope':'With the analytic symmetry/parabolic/QC argument, excludes uniformlycoercive constant real outputcoupled puretarget flows, all gamma>=0, in the closedquadratic/bilinearSOS class. No arbitrary combined-component theorem.'}
    if write:(ROOT/'VERIFY_FLOW.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write-receipt',action='store_true')
    main(parser.parse_args().write_receipt)
