"""Exact 15-state five-port CP obstruction and attained entropy minimum."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
import json
import hashlib
from check_thermodynamic_completion import zero,gen,mul,tr,inv,block,entropy,dec,convert


def main():
    m=5; n=15; a=zero(n); w=[F(1)]*m+[F(16,15)]*10
    alpha=[]; beta=[]
    for edge in range(5):
        i,j=edge,(edge+1)%5
        for orient in [0,1]:
            x=5+2*edge+orient
            p=F(5,8) if orient==0 else F(3,8)
            al=[F(0)]*m; be=[F(0)]*m
            al[i]=p; al[j]=1-p; be[i]=1-p; be[j]=p
            alpha.append(al); beta.append(be)
            for k in range(m):
                a[k][x]=w[x]*al[k]
                a[x][k]=w[x]*be[k]
    q=gen(a,w)
    assert [-q[i][i] for i in range(m)]==[F(32,15)]*m
    assert [-q[i][i] for i in range(m,n)]==[F(1)]*10
    assert all(q[i][j]==0 for i in range(m,n) for j in range(m,n) if i!=j)
    B=list(range(m)); I=list(range(m,n))
    L=[[-w[i]*q[i][j] for j in range(n)] for i in range(n)]
    A=block(a,B,I); Bout=block(a,I,B)
    Di=[[1/w[i] if i==j else F(0) for j in I] for i in I]
    M=mul(mul(A,Di),Bout)
    C=[[F(1) if (i-j)%5 in [1,4] else F(0) for j in B] for i in B]
    expected=[[F(i==j)+F(17,30)*C[i][j] for j in B] for i in B]
    assert M==expected
    Ginv=inv(block(L,I,I)); Lbi=block(L,B,I); Lib=block(L,I,B)
    product=mul(mul(Lbi,Ginv),Lib)
    S=[[L[i][j]-product[i][j] for j in B] for i in B]
    assert S==[[F(17,15) if i==j else -F(17,30)*C[i][j] for j in B] for i in B]
    wi=[[w[i]] for i in I]
    br=[w[i]-x[0] for i,x in enumerate(mul(mul(Lbi,Ginv),wi))]
    bl=[w[i]-x[0] for i,x in enumerate(mul(mul(tr(Lib),tr(Ginv)),wi))]
    c=mul(mul(tr(wi),Ginv),wi)[0][0]
    assert br==bl==[F(47,15)]*m and c==F(32,3)
    assert [sum(r) for r in M]==[F(32,15)]*m
    # Every row's nonnegative-entry upper bounds sum to its exact margin.
    upper=[[F(1) if i==j else F(17,30)*C[i][j] for j in B] for i in B]
    assert upper==M and [sum(r) for r in upper]==[F(32,15)]*m
    # Exact positive-definiteness certificate by an LDL^T decomposition.
    low=zero(m); diag=[]
    for i in B:
        low[i][i]=1
        di=M[i][i]-sum(low[i][k]**2*diag[k] for k in range(i))
        assert di>0; diag.append(di)
        for j in range(i+1,m):
            low[j][i]=(M[j][i]-sum(low[j][k]*low[i][k]*diag[k] for k in range(i)))/di
    assert mul(mul(low,[[diag[i] if i==j else F(0) for j in B] for i in B]),tr(low))==M
    H=[[1-2*C[i][j] for j in B] for i in B]
    horn=sum(H[i][j]*M[i][j] for i in B for j in B)
    assert horn==F(-2,3)
    # Verify copositivity on nonnegative-grid controls only; the ordinary
    # proof for all real nonnegative vectors is in the companion note.
    grid_count=0
    from itertools import product as cartesian
    for z in cartesian(range(4),repeat=m):
        assert sum(z[i]*H[i][j]*z[j] for i in B for j in B)>=0
        grid_count+=1
    with localcontext() as ctx:
        ctx.prec=85
        E=entropy(a); target=dec(F(16,3))*dec(F(5,3)).ln()
        assert abs(E-target)<Decimal('1e-70')
        normalized=E/dec(sum(w))
    # Laplace-bin-independent kernel identity from actual generator:
    # Q_II=-I, so K(t)=exp(-t) M at every t, not just sample points.
    assert block(q,I,I)==[[-F(i==j) for j in I] for i in I]
    P=[[x/F(32,15) for x in row] for row in M]
    assert P==tr(P) and all(sum(row)==1 for row in P)
    score=horn/F(32,3)*F(1,2) # h=log2, 5*rho=32/3
    assert score==F(-1,32)
    data=dict(status='PASS',kind='supplied exact rational generator, no observations',
              total_states=n,ports=m,hidden_states=10,total_mass=sum(w),hidden_mass=c,
              source_observations=0,source_preparations=0,random_draws=0,
              S=S,b_R=br,b_L=bl,c=c,forced_residence_matrix=M,
              native_rates=[-q[i][i] for i in range(n)],
              psd_ldl_diagonal=diag,Horn_witness=H,Horn_inner_product=horn,
              copositive_grid_controls=grid_count,
              equilibrium_completion='IMPOSSIBLE; exact Horn certificate',
              entropy_unnormalized=E,exact_optimum='(16/3)*log(5/3)',
              entropy_normalized=normalized,
              boundary_kernel='K(t)=exp(-t)*M; exact generator identity',
              reversible_event_chain=P,bounded_score_mean_at_log2=score,
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    Path(__file__).with_name('COMPLETE_POSITIVITY_CHECKS.json').write_text(json.dumps(convert(data),indent=2)+'\n')
    print(json.dumps(convert({k:data[k] for k in ['status','total_states','hidden_states','Horn_inner_product','entropy_unnormalized','entropy_normalized','bounded_score_mean_at_log2','source_observations']}),indent=2))


if __name__=='__main__': main()
