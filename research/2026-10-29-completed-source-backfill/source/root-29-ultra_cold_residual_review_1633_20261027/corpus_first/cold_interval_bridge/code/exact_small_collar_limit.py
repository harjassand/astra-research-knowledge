"""Exact source witness for the actual block4/collar1 residual criterion."""
import sys
sys.dont_write_bytecode=True
import sympy as S
import mpmath as mp
import json,math
from seam_residual import BASE


def run():
    t=S.symbols('t',positive=True)
    # One-magnon sector of four spin2 sites; central bond12 is cut, while
    # the outside Hamiltonian consists of01 and23. All entries are rational.
    def hbond(i,j):
        H=4*S.eye(4)
        H[i,i]=H[j,j]=2;H[i,j]=H[j,i]=2
        return H
    V=hbond(1,2);hout=hbond(0,1)+hbond(2,3)
    # t=exp(s): eigenvalues of the central bond are0 and4 in this sector.
    P0=S.eye(4)-V/4;P4=V/4
    E=P0+t**(-2)*P4;inverse=P0+t**2*P4
    assert S.simplify(E*inverse)==S.eye(4)
    R=S.simplify((hout-E*hout*inverse)/2)
    hermitian=S.simplify((R+R.T)/2)
    witness=S.simplify(hermitian[1,0])
    assert S.simplify(witness+(t**2+t**(-2)-2)/4)==0
    # Hence ||Herm R|| >=(cosh(2s)-1)/2. Distinct block4 seam cells are
    # disjoint and identical, so their Hermitian extreme eigenvalues add.
    mp.iv.dps=80;iv=mp.iv;beta=iv.mpf(3)/4
    sinh=(iv.exp(2*beta)-iv.exp(-2*beta))/2
    rows=[]
    for n in (256,512):
        m=n//4;lower=m*(sinh/4-beta/2)
        rows.append(dict(n=n,beta=.75,seams=m,
            true_integrated_operator_residual_lower=math.nextafter(float(lower.a),-math.inf),
            required_global_integrated_residual_upper=9.300594805589878e-8,
            all_Schatten_residual_certificate_acquired=False))
    result=dict(status='EXACT_SOURCE_WITNESS_EXCLUDES_THIS_SMALL_COLLAR_CERTIFICATE',
        one_magnon_basis='The spin lowered from2to1 is at positions0,1,2,3 respectively.',
        central_V=[[str(x)for x in V.row(i)]for i in range(4)],
        Hermitian_residual_entry=str(witness),
        pointwise_lower='||E_total(s)|| >= (n/8)(cosh(2s)-1)',
        integral_lower='integral_0^beta||E_total(s)||ds >= (n/4)(sinh(2beta)/4-beta/2)',
        rows=rows,
        scope='An obstruction to this exact block4/collar1 multiplicative-residual certificate. It is not a lower bound on the actual Gibbs-to-ansatz purity error, and not a no-go for larger/entangled boundary methods.')
    (BASE/'results/EXACT_SMALL_COLLAR_LIMIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
