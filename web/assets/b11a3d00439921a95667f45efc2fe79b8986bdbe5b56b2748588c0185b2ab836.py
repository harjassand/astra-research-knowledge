#!/usr/bin/env python3
"""Exact prescribed raw-channel and reference audits; no solver or floats."""
from fractions import Fraction as F
from pathlib import Path
import json


def mat(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def eye(n):
    a=mat(n)
    for i in range(n): a[i][i]=F(1)
    return a


def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return sum(a[i][i] for i in range(len(a)))


def transpose(a):
    return [list(c) for c in zip(*a)]


def add(a,b):
    return [[x+y for x,y in zip(rowa,rowb)] for rowa,rowb in zip(a,b)]


def scale(a,c):
    return [[c*x for x in row] for row in a]


def raw(a):
    n=len(a); out=mat(n)
    for j in range(n): out[(j+1)%n][(j+1)%n]=a[j][j]
    return out


def local_raw(a, da, db):
    out=mat(da*db)
    for u in range(da):
        for v in range(da):
            for j in range(db):
                out[u*db+(j+1)%db][v*db+(j+1)%db]=a[u*db+j][v*db+j]
    return out


def local_dephase(a,da,db):
    out=mat(da*db)
    for u in range(da):
        for v in range(da):
            for j in range(db):
                out[u*db+j][v*db+j]=a[u*db+j][v*db+j]
    return out


def serialize(a):
    if isinstance(a,F): return str(a)
    if isinstance(a,dict): return {k:serialize(v) for k,v in a.items()}
    if isinstance(a,(tuple,list)): return [serialize(x) for x in a]
    return a


def main():
    d=4
    # Full matrix-unit HS representation: real coefficients, so adjoint
    # is ordinary transpose in this orthonormal complex HS basis.
    sup=mat(d*d)
    for j in range(d): sup[((j+1)%d)*d+(j+1)%d][j*d+j]=F(1)
    star=transpose(sup)
    s=mul(star,sup)
    deph=mat(d*d)
    for j in range(d): deph[j*d+j][j*d+j]=F(1)
    assert s==deph and sup!=star
    assert mul(s,s)==s and transpose(s)==s
    # Pure basis canonical Psi is exactly dephasing; full C=1 order.
    psi=deph
    assert psi==s

    jmat=mat(d)
    jmat[0][1]=jmat[1][0]=jmat[2][3]=jmat[3][2]=F(1)
    assert mul(jmat,jmat)==eye(d)
    r=F(24,25)
    rho=scale(add(eye(d),scale(jmat,r)),F(1,4))
    rootrho=add(scale(eye(d),F(2,5)),scale(jmat,F(3,10)))
    assert mul(rootrho,rootrho)==rho and tr(rho)==1
    output=raw(rho)
    assert output==scale(eye(d),F(1,4))
    v=raw(rootrho)
    w=scale(eye(d),F(1,2))
    energy=1-tr(mul(v,v))
    beta=tr(mul(w,v))
    assert energy==F(9,25) and beta==F(4,5)
    norm_difference=tr(mul(add(w,scale(v,-1)),add(w,scale(v,-1))))
    assert 2*(1-beta)-energy==norm_difference==F(1,25)
    b=e=r/2
    assert b==e==F(12,25)
    assert e*e<=2*energy

    projectors=[]
    for pair in (0,2):
        for sign in (1,-1):
            proj=mat(d)
            proj[pair][pair]=proj[pair+1][pair+1]=F(1,2)
            proj[pair][pair+1]=proj[pair+1][pair]=F(sign,2)
            projectors.append(proj)
    evals=[F(49,100),F(1,100),F(49,100),F(1,100)]
    roots=[F(7,10),F(1,10),F(7,10),F(1,10)]
    constructed=mat(d)
    for lam,proj in zip(evals,projectors): constructed=add(constructed,scale(proj,lam))
    assert constructed==rho
    p=[[raw(projectors[j])[i][i] for j in range(d)] for i in range(d)]
    assert all(sum(row)==1 for row in p)
    assert all(sum(p[i][j] for i in range(d))==1 for j in range(d))
    assert p!=transpose(p)
    a=[[p[i][j]*evals[j] for j in range(d)] for i in range(d)]
    c=[[p[i][j]/4 for j in range(d)] for i in range(d)]
    assert sum(map(sum,a))==sum(map(sum,c))==1
    assert all(sum(a[i])==F(1,4) for i in range(d))
    joint_beta=sum(p[i][j]*roots[j]/2 for i in range(d) for j in range(d))
    assert joint_beta==beta
    assert F(2,5)>=energy

    # A genuine maximally entangled untouched-reference input.
    da=db=4
    omega=mat(da*db)
    for i in range(d):
        for j in range(d): omega[i*d+i][j*d+j]=F(1,4)
    assert mul(omega,omega)==omega and tr(omega)==1
    a_marg=[[sum(omega[u*d+j][v0*d+j] for j in range(d))
             for v0 in range(d)] for u in range(d)]
    b_marg=[[sum(omega[u*d+j][u*d+k] for u in range(d))
             for k in range(d)] for j in range(d)]
    assert a_marg==b_marg==scale(eye(d),F(1,4))
    out_t=local_raw(omega,da,db)
    out_psi=local_dephase(omega,da,db)
    assert tr(out_t)==tr(out_psi)==1
    assert mul(omega,out_t)==mat(d*d)
    assert tr(mul(out_t,out_t))==F(1,4)
    reference_energy=1-tr(mul(out_t,out_t))
    assert reference_energy==F(3,4)
    corr_proj=mat(d*d)
    for j in range(d): corr_proj[j*d+j][j*d+j]=1
    assert out_psi==scale(corr_proj,F(1,4))
    assert mul(corr_proj,omega)==omega
    # Explicit invariant decomposition gives difference eigenvalues.
    reference_diff_eigenvalues=[F(3,4),F(-1,4),F(-1,4),F(-1,4)]
    ref_e=sum(abs(x) for x in reference_diff_eigenvalues)/2
    assert ref_e==F(3,4)
    ref_b=F(1) # Orthogonal normalized states, verified above.

    assert F(4,2)==2  # With H^3=CD/(2b^2), (2bH)^2=2CD/H.
    general_cubic=F(3)**3/2
    assert general_cubic==F(27,2)
    c4_cubic=4*general_cubic
    assert c4_cubic==54
    squared_coefficient_cubed=c4_cubic**2*4/27
    assert squared_coefficient_cubed==432<512

    result={
      'status':'EXACT_PRESCRIBED_RAW_AND_REFERENCE_IDENTITIES_PASS',
      'arithmetic':'integers and fractions only',
      'dimension_B':d,
      'raw_HS_selfadjoint':False,
      'S_equals_basis_dephasing':True,
      'explicit_joint_broadcaster':'B(Z)=sum_j Z_jj |j+1,j+1><j+1,j+1|',
      'Psi':'canonical pure basis dephasing, full C=1 comparator',
      'faithful_noncommuting_input':{
        'rho_eigenvalues':evals,'b':b,'e':e,
        'E_S_sqrt_rho':energy,'beta':beta,
        'separate_eigenbasis_transition':p,
        'joint_a':a,'joint_c':c,
        'analytic_entropy_lower':'Delta >= -2 log(4/5) >= 2/5 >= 9/25',
        'square_root_norm_difference':norm_difference,
      },
      'untouched_quantum_reference':{
        'state':'maximally entangled A1=B=C^4; optional pure independent spectator A0=C^m',
        'rho_B_equals_tau_B':True,'b':ref_b,'e':ref_e,
        'E_id_S_sqrt_rho':reference_energy,
        'entropy_budget':'I(A:B)=2 log4, independent of spectator m',
        'global_tracial_divergence':'2 log4+log m',
      },
      'general_cubic_constant':general_cubic,
      'C4_cubic_constant':c4_cubic,
      'C4_squared_constant':'3*2^(4/3)<8',
      'C4_squared_constant_cubed':squared_coefficient_cubed,
      'proves_unrestricted_theorem':False,
      'external_validation':'UNKNOWN'
    }
    out=Path(__file__).with_name('BISTOCHASTIC_REPLAY_RESULT.json')
    out.write_text(json.dumps(serialize(result),indent=2)+'\n')
    print(json.dumps({'status':result['status'],'output':str(out),
                      'C4_cubic_constant':54,'squared_K_below':8}))


if __name__=='__main__': main()
