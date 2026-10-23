from fractions import Fraction as F
R, M, n = F(3,2), 2, 16
qp, qr = F(1,2*M), R/(2*M)
assert qp*M + qr + F(M,1)/(2*M)-R/(2*M) == 1
for label,kappa in [('expansion',5),('coalescence',0)]:
    if label=='expansion':
        native_q_ratio=R**(-2*kappa)
        ratio=R
        target_ratio=F(n*n,M)
        forward=M*qp
        native_reverse=qr/(target_ratio*ratio)
        aggregate_reverse=native_reverse
    else:
        native_q_ratio=R**(2*kappa)
        ratio=1/R
        target_ratio=F(n*n*M)
        forward=qr
        native_reverse=qp/(target_ratio*ratio)
        aggregate_reverse=M*native_reverse
    screen_squared=native_q_ratio*ratio**(2*kappa)
    assert screen_squared==1
    assert target_ratio*ratio>1
    assert aggregate_reverse==forward/(n*n)
    assert 1-forward-aggregate_reverse>=0
    print(label, {'S_squared':str(screen_squared),'t_forward':str(target_ratio*ratio),'forward_total':str(forward),'reverse_total':str(aggregate_reverse),'actual_internal_L_diagonal':str(1-forward-aggregate_reverse)})
print('Exact rational identity spot checks passed; no mixing or asymptotic assertion is inferred.')
