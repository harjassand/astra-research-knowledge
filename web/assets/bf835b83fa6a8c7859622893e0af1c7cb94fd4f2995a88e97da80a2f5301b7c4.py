"""Fixed exact weighted-metric/channel-convention checks; no scans or floats."""
from pathlib import Path
import json
import sympy as s


def same(left, right):
    assert left.shape == right.shape
    assert all(s.simplify(x)==0 for x in left-right)


def partial_trace_output(matrix, input_dim, output_dim):
    return s.Matrix(input_dim,input_dim,lambda i,j:sum(
        matrix[i*output_dim+k,j*output_dim+k] for k in range(output_dim)))


def partial_trace_input(matrix, input_dim, output_dim):
    return s.Matrix(output_dim,output_dim,lambda i,j:sum(
        matrix[k*output_dim+i,k*output_dim+j] for k in range(input_dim)))


def main():
    I=s.eye(2)
    X=s.Matrix([[0,1],[1,0]])
    Y=s.Matrix([[0,-s.I],[s.I,0]])
    Z=s.diag(1,-1)
    sigma=s.diag(s.Rational(9,10),s.Rational(1,10))
    root=s.diag(3/s.sqrt(10),1/s.sqrt(10))
    inverse_root=s.diag(s.sqrt(10)/3,s.sqrt(10))
    gamma=lambda A:root*A*root
    kms=lambda A,B:s.simplify(s.trace(A.conjugate().T*gamma(B)))
    mean=lambda A:s.simplify(s.trace(sigma*A))

    # A noncommuting input POVM tests the weighted Petz normalization.
    effects=[(I+X)/2,(I-X)/2]
    probabilities=[mean(F) for F in effects]
    posteriors=[s.simplify(gamma(F)/p) for F,p in zip(effects,probabilities)]
    assert probabilities==[s.Rational(1,2),s.Rational(1,2)]
    expected=[s.Matrix([[s.Rational(9,10),s.Rational(3,10)],
                        [s.Rational(3,10),s.Rational(1,10)]]),
              s.Matrix([[s.Rational(9,10),-s.Rational(3,10)],
                        [-s.Rational(3,10),s.Rational(1,10)]])]
    for state,target in zip(posteriors,expected):
        same(state,target)
        assert s.trace(state)==1 and s.det(state)==0
        assert state[0,0]>0 and state[1,1]>0
    same(sum((p*pi for p,pi in zip(probabilities,posteriors)),s.zeros(2)),sigma)
    psi=lambda A:sum((pi*s.trace(F*A) for pi,F in zip(posteriors,effects)),s.zeros(2))
    P=lambda A:sum((F*s.trace(pi*A) for pi,F in zip(posteriors,effects)),s.zeros(2))
    same(psi(sigma),sigma)
    same(psi(I),2*sigma)
    same(P(I),I)
    same(P(X),s.Rational(3,5)*X)
    same(P(Y),s.zeros(2))
    same(P(Z),s.Rational(4,5)*I)
    for A in [I,X,Y,Z]:same(gamma(P(A)),psi(gamma(A)))
    choi=sum((s.kronecker_product(F.T,pi)
              for F,pi in zip(effects,posteriors)),s.zeros(4))
    same(partial_trace_output(choi,2,2),I)
    same(partial_trace_input(choi,2,2),2*sigma)
    assert all(ev>=0 for ev in choi.eigenvals())
    basis=[I,X,Y,Z]
    gram=s.Matrix(4,4,lambda a,b:kms(basis[a],basis[b]))
    matrix_P=s.Matrix(4,4,lambda a,b:s.simplify(s.trace(basis[a]*P(basis[b]))/2))
    same(gram*matrix_P,matrix_P.T*gram)
    assert all(0<=ev<=1 for ev in matrix_P.eigenvals())

    # Full Petz score/estimator crossmoment and its exact Schur equality.
    centered=[X/s.sqrt(s.Rational(3,5)),Y/s.sqrt(s.Rational(3,5)),
              (Z-s.Rational(4,5)*I)/s.Rational(3,5)]
    same(s.Matrix(3,3,lambda a,b:kms(centered[a],centered[b])),s.eye(3))
    scores=[s.Matrix([s.simplify(s.trace(pi*A)) for A in centered]) for pi in posteriors]
    estimator=[1/s.sqrt(s.Rational(3,5)),-1/s.sqrt(s.Rational(3,5))]
    same(sum((x*F for x,F in zip(estimator,effects)),s.zeros(2)),centered[0])
    covariance=sum((p*a*a.T for p,a in zip(probabilities,scores)),s.zeros(3))
    cross=sum((p*a*x for p,a,x in zip(probabilities,scores,estimator)),s.zeros(3,1))
    noise=s.simplify(sum(p*x*x for p,x in zip(probabilities,estimator)))
    same(covariance,s.diag(s.Rational(3,5),0,0))
    same(cross,s.Matrix([1,0,0]))
    assert noise==s.Rational(5,3)
    same(covariance-cross*cross.T/noise,s.zeros(3))

    # Pure stationary coupling: auxiliary channel is exactly id; transpose signs matter.
    purification=s.Matrix([3/s.sqrt(10),0,0,1/s.sqrt(10)])
    omega=purification*purification.T
    same(partial_trace_output(omega,2,2),sigma)
    same(partial_trace_input(omega,2,2),sigma)
    scaling=s.kronecker_product(inverse_root,I)
    auxiliary_choi=s.simplify(scaling*omega*scaling)
    maximally_entangled=s.Matrix([1,0,0,1])
    same(auxiliary_choi,maximally_entangled*maximally_entangled.T)
    for A in basis:
        for B in basis:
            assert s.simplify(s.trace(omega*s.kronecker_product(A,B))-kms(A.T,B))==0
    sibling_covariance=s.Matrix(3,3,lambda a,b:s.simplify(
        s.trace(omega*s.kronecker_product(centered[a],centered[b]))))
    same(sibling_covariance,s.diag(1,-1,1))
    assert kms(X,X)==s.Rational(3,5) and mean(X*X)==1

    # The pure coupling is output by an actual legal compatible replacer broadcaster.
    broadcaster_choi=s.kronecker_product(I,omega)
    same(partial_trace_output(broadcaster_choi,2,4),I)
    assert all(ev>=0 for ev in broadcaster_choi.eigenvals())
    R=lambda A:mean(A)*I
    matrix_R=s.Matrix(4,4,lambda a,b:s.simplify(s.trace(basis[a]*R(basis[b]))/2))
    same(gram*matrix_R,matrix_R.T*gram)

    # Exact stationary dephasing broadcaster exercises the selected +1 mode.
    V0=s.zeros(4,2);V1=s.zeros(4,2)
    V0[0,0]=1;V1[3,1]=1
    same(V0.T*V0+V1.T*V1,I)
    broadcast=lambda A:V0*A*V0.T+V1*A*V1.T
    dephase=lambda A:s.diag(A[0,0],A[1,1])
    for A in basis:
        same(partial_trace_output(broadcast(A),2,2),dephase(A))
        same(partial_trace_input(broadcast(A),2,2),dephase(A))
        same(gamma(dephase(A)),dephase(gamma(A)))
    same(partial_trace_output(broadcast(sigma),2,2),sigma)
    assert s.trace(broadcast(sigma)*s.kronecker_product(centered[2],centered[2]))==1
    assert mean(centered[2]*centered[2])==1

    # Symbolic geometric recursion and the final C4 spectral polynomial.
    r=s.symbols('r',positive=True)
    n0=s.symbols('n0',positive=True)
    m=s.symbols('m',integer=True,nonnegative=True)
    D=n0*r**m+r*(1-r**m)/(1-r)
    assert s.simplify(D.subs(m,m+1)-r*(D+1))==0
    lam=s.symbols('lambda',real=True)
    scalar_difference=s.factor((2*lam**2-1)-(4*lam-3))
    assert scalar_difference==2*(lam-1)**2

    result={
      'status':'all exact assertions passed',
      'scope':'Fixed channel/metric conventions and scalar identities, not a formal proof or parameter scan.',
      'faithful_reference':[['9/10','0'],['0','1/10']],
      'noncommuting_Petz_POVM':{
        'probabilities':['1/2','1/2'],'posterior_states':[str(pi) for pi in posteriors],
        'Heisenberg_images':{'I':'I','X':'3X/5','Y':'0','Z':'4I/5'},
        'Schrodinger_identity_image':'2 sigma',
        'KMS_positive_spectrum':{str(k):v for k,v in matrix_P.eigenvals().items()},
        'full_centered_covariance':str(covariance),'unbiased_crossmoment':str(cross),
        'physical_estimator_variance':str(noise),'Schur_equality':'exact'},
      'pure_sibling_coupling':{
        'both_marginals':'sigma','auxiliary_channel':'identity',
        'normalized_KMS_covariance':str(sibling_covariance),
        'legal_broadcaster':'B(rho)=Tr(rho) |Omega_sigma><Omega_sigma|',
        'marginal_channel':'Phi(rho)=Tr(rho) sigma',
        'transpose_identity':'all 16 Pauli-basis pairs passed'},
      'metric_distinction':{'Pauli_X_GNS_Jordan_norm_squared':'1',
                           'Pauli_X_KMS_norm_squared':'3/5'},
      'selected_mode_control':{'broadcaster':'V0=|00><0|, V1=|11><1|',
                               'marginal':'sigma-eigenbasis dephasing',
                               'selected_centered_Z_eigenvalue':'1',
                               'normalized_sibling_covariance':'1'},
      'scalar_checks':{'geometric_recursion':'D_(m+1)=r(D_m+1)',
                       'C4_polynomial_difference':str(scalar_difference)}}
    Path(__file__).with_name('EXACT_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
