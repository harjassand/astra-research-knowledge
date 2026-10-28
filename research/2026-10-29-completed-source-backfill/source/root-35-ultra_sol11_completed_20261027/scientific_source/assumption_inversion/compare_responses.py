"""Exact supplied-model response construction versus strong ordinary methods.

All propagation and Poisson certificates use Python integers/Fractions.
The candidate is a scaled block exponential; the ordinary comparator includes
the SAME fused block kernel plus prior differentiated-uniformization jets.
No stable-vs-unstable-subtraction result is promoted to a new capability.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import time

OUT=Path(__file__).resolve().parent
MU=F(8)
TIME=F(4)
BMAX=F(7,4)
TOL=F(1,10**12)


def exp_negative_interval(mu):
    total=F(1)
    term=F(1)
    k=0
    while True:
        k+=1
        term*=mu/k
        total+=term
        if k+2>mu:
            next_term=term*mu/(k+1)
            tail=next_term/(1-mu/(k+2))
            if tail<F(1,10**90):
                return 1/(total+tail),1/total,k


ELO,EHI,EXP_TERMS=exp_negative_interval(MU)


def poisson_tail(after):
    assert after+2>MU
    first=MU**(after+1)/math.factorial(after+1)
    return EHI*first/(1-MU/(after+2))


def choose_m(kind,eta,K=1):
    m=max(10,K+9)
    while True:
        if kind=='direct':
            bound=2*BMAX*poisson_tail(m)/eta
        elif kind=='block':
            bound=BMAX*TIME*poisson_tail(m-1)
        else:
            bound=sum((eta**(j-1)*BMAX*TIME**j/F(math.factorial(j))
                       *poisson_tail(m-j) for j in range(1,K+1)),F(0))
        if bound<=TOL/4:
            return m
        m+=1


def make_input(n):
    start=time.monotonic()
    rows=[[[i,1],[(i+1)%n,4],[(i-1)%n,2],[(i+11)%n,1]] for i in range(n)]
    killing=sorted(set([0,1,n//3,n//2]))
    data={'n':n,'P_denominator':8,'P_numerator_rows':rows,'lambda':'2','t':'4',
          'b_numerators':[8+i%7 for i in range(n)],'b_denominator':8,
          'D_nonzero_unit_diagonal':killing,'c_coordinate':0}
    path=OUT/'inputs'/f'chain_{n}.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data,separators=(',',':'))+'\n')
    return {'path':str(path.relative_to(OUT)),'bytes':path.stat().st_size,
            'generate_write_seconds':time.monotonic()-start}


def load_input(path):
    start=time.monotonic()
    inp=json.loads((OUT/path).read_text())
    n=inp['n']
    assert inp['P_denominator']==8 and inp['lambda']=='2' and inp['t']=='4'
    assert len(inp['P_numerator_rows'])==len(inp['b_numerators'])==n
    for row in inp['P_numerator_rows']:
        assert sum(w for _,w in row)==8
        assert all(0<=j<n and w>=0 for j,w in row)
    assert max(inp['b_numerators'])==14
    assert inp['b_denominator']==8 and inp['c_coordinate']==0
    inp['input_read_validate_seconds']=time.monotonic()-start
    return inp


def scalar_bounds(partial,tail):
    return ELO*partial,EHI*partial+tail


def fused_block(inp,eta):
    """Candidate AND ordinary structure-exploiting block action: same kernel."""
    start=time.monotonic()
    n=inp['n']
    rows=inp['P_numerator_rows']
    kills=set(inp['D_nonzero_unit_diagonal'])
    m=choose_m('block',eta)
    den=eta.denominator
    num=eta.numerator
    L=8*den
    diag=[den-4*num*(i in kills) for i in range(n)]
    assert min(diag)>=0
    source=[4*den*(i in kills) for i in range(n)]
    # Full row input is consumed. Factoring common den is ordinary algebra.
    z=[0]*n
    u=inp['b_numerators'][:]
    coeff=F(1,8)
    total=F(0)
    for k in range(m+1):
        total+=coeff*z[0]
        if k==m:
            break
        unext=[den*sum(w*u[j] for j,w in row) for row in rows]
        znext=[den*sum(w*z[j] for j,w in row)-4*num*(i in kills)*z[i]+source[i]*u[i]
               for i,row in enumerate(rows)]
        u,z=unext,znext
        coeff*=MU/F((k+1)*L)
    low,high=scalar_bounds(total,BMAX*TIME*poisson_tail(m-1))
    assert high-low<=TOL
    return {'method':'candidate_fused_and_ordinary_fused_block','m':m,'K':1,
            'lower':str(low),'upper':str(high),'partial_sum':str(total),
            'recurrence_denominator':L,'exact_matvec_rows':2*n*m,
            'max_final_integer_bits':max(max(u).bit_length(),max(z).bit_length()),
            'compute_seconds':time.monotonic()-start}


def ordinary_generic_block(inp,eta):
    """Independent generic sparse block-matrix action, same prior formula."""
    start=time.monotonic()
    n=inp['n']
    den,num=eta.denominator,eta.numerator
    L=8*den
    killing=set(inp['D_nonzero_unit_diagonal'])
    rows=[]
    for i,row in enumerate(inp['P_numerator_rows']):
        rr={j:den*w for j,w in row}
        if i in killing:
            rr[i]-=4*num
            rr[n+i]=4*den
        assert all(w>=0 for w in rr.values())
        rows.append(list(rr.items()))
    rows += [[(n+j,den*w) for j,w in row] for row in inp['P_numerator_rows']]
    state=[0]*n+inp['b_numerators'][:]
    m=choose_m('block',eta)
    coeff=F(1,8)
    total=F(0)
    for k in range(m+1):
        total+=coeff*state[0]
        if k==m:
            break
        state=[sum(w*state[j] for j,w in row) for row in rows]
        coeff*=MU/F((k+1)*L)
    low,high=scalar_bounds(total,BMAX*TIME*poisson_tail(m-1))
    assert high-low<=TOL
    return {'method':'ordinary_generic_Van_Loan_block','m':m,'K':1,
            'lower':str(low),'upper':str(high),'partial_sum':str(total),
            'exact_matvec_rows':2*n*m,'max_final_integer_bits':max(state).bit_length(),
            'compute_seconds':time.monotonic()-start}


def ordinary_jets(inp,eta):
    """Prior differentiated uniformization, with exact Taylor remainder."""
    start=time.monotonic()
    K=1
    while eta**K*BMAX*TIME**(K+1)/math.factorial(K+1)>TOL/4:
        K+=1
    rem=eta**K*BMAX*TIME**(K+1)/math.factorial(K+1)
    m=choose_m('jets',eta,K)
    n=inp['n']
    rows=inp['P_numerator_rows']
    killing=set(inp['D_nonzero_unit_diagonal'])
    jet=[inp['b_numerators'][:]]+[[0]*n for _ in range(K)]
    total=[F(0)]*(K+1)
    coeff=F(1,8)
    for k in range(m+1):
        for j in range(1,K+1):
            total[j]+=coeff*jet[j][0]
        if k==m:
            break
        new=[]
        for j in range(K+1):
            vec=jet[j]
            nxt=[sum(w*vec[ii] for ii,w in row) for row in rows]
            if j:
                for ii in killing:
                    nxt[ii]+=4*jet[j-1][ii]
            new.append(nxt)
        jet=new
        coeff*=F(1,k+1)  # MU/P_denominator=1 for this declared input.
    low,high=F(0),F(0)
    for j in range(1,K+1):
        jl,jh=scalar_bounds(total[j],BMAX*TIME**j/F(math.factorial(j))*poisson_tail(m-j))
        factor=eta**(j-1)
        if j%2:
            low+=factor*jl
            high+=factor*jh
        else:
            low-=factor*jh
            high-=factor*jl
    if K%2:
        low-=rem
    else:
        high+=rem
    assert high-low<=TOL
    return {'method':'ordinary_positive_derivative_jets_with_remainder','m':m,'K':K,
            'lower':str(low),'upper':str(high),
            'partial_sums':[str(x) for x in total],
            'remainder_bound':str(rem),'exact_matvec_rows':(K+1)*n*m,
            'max_final_integer_bits':max(max(v).bit_length() for v in jet),
            'compute_seconds':time.monotonic()-start}


def independent_responses(inp,eta):
    start=time.monotonic()
    den,num=eta.denominator,eta.numerator
    L=8*den
    n=inp['n']
    rows=inp['P_numerator_rows']
    killing=set(inp['D_nonzero_unit_diagonal'])
    m=choose_m('direct',eta)
    u=inp['b_numerators'][:]
    v=u[:]
    coeff=F(1,8)
    su,sv=F(0),F(0)
    for k in range(m+1):
        su+=coeff*u[0]
        sv+=coeff*v[0]
        if k==m:
            break
        u=[den*sum(w*u[j] for j,w in row) for row in rows]
        v=[den*sum(w*v[j] for j,w in row)-4*num*(i in killing)*v[i]
           for i,row in enumerate(rows)]
        coeff*=MU/F((k+1)*L)
    ul,uh=scalar_bounds(su,BMAX*poisson_tail(m))
    vl,vh=scalar_bounds(sv,BMAX*poisson_tail(m))
    low,high=(ul-vh)/eta,(uh-vl)/eta
    assert high-low<=TOL
    return {'method':'separate_exact_responses','m':m,'K':0,'lower':str(low),
            'upper':str(high),'partial_sums':[str(su),str(sv)],
            'exact_matvec_rows':2*n*m,'max_final_integer_bits':max(max(u).bit_length(),max(v).bit_length()),
            'compute_seconds':time.monotonic()-start}


def run_method(method,path,eta):
    start=time.monotonic()
    inp=load_input(path)
    ans=method(inp,eta)
    ans['read_validate_seconds']=inp['input_read_validate_seconds']
    ans['full_query_seconds']=time.monotonic()-start
    ans['display_lower']=float(F(ans['lower']))
    ans['display_upper']=float(F(ans['upper']))
    ans['display_width']=float(F(ans['upper'])-F(ans['lower']))
    return ans


def main():
    start=time.monotonic()
    rows=[]
    generated=[]
    for n in [64,512,4096]:
        inf=make_input(n)
        generated.append(inf)
        for eta in [F(1,100),F(1,10**8),F(1,10**14),F(1,10**20)]:
            by_method=[]
            for method in [fused_block,ordinary_generic_block,ordinary_jets,independent_responses]:
                by_method.append(run_method(method,inf['path'],eta))
            block,generic,jets,direct=by_method
            assert block['partial_sum']==generic['partial_sum']
            assert block['lower']==generic['lower'] and block['upper']==generic['upper']
            # The independently derived jet and independent-response intervals
            # must meet the exact block bracket; a common intersection is required.
            assert max(F(r['lower']) for r in by_method)<=min(F(r['upper']) for r in by_method)
            # A strong ordinary implementation can use the IDENTICAL fused kernel.
            # Its best measured choice is therefore never slower than the candidate.
            ordinary_best=min(block['full_query_seconds'],generic['full_query_seconds'],
                              jets['full_query_seconds'])
            row={'n':n,'eta':str(eta),'tolerance':str(TOL),'input':inf,
                 'methods':by_method,'ordinary_fused_algorithmically_identical':True,
                 'ordinary_best_seconds':ordinary_best,
                 'candidate_to_best_ordinary_ratio':block['full_query_seconds']/ordinary_best}
            rows.append(row)
            partial={'status':'PARTIAL_EXACT_COMPARISON','rows':rows}
            (OUT/'EXACT_COMPARISON.json').write_text(json.dumps(partial,indent=2)+'\n')
            print(json.dumps({'n':n,'eta':str(eta),'value':block['display_lower'],
                  'block_m':block['m'],'direct_m':direct['m'],'jet_K':jets['K'],
                  'block_seconds':block['full_query_seconds'],
                  'generic_seconds':generic['full_query_seconds'],
                  'jets_seconds':jets['full_query_seconds'],
                  'separate_seconds':direct['full_query_seconds'],
                  'candidate_to_best_ordinary_ratio':row['candidate_to_best_ordinary_ratio']}),flush=True)
    result={'status':'EXACT_SCOPED_ORDINARY_COMPARATOR_FAILURE','cases':len(rows),
            'exp_negative_interval':[str(ELO),str(EHI)],'exp_positive_series_terms':EXP_TERMS,
            'rows':rows,'input_generation':generated,
            'full_declared_query_wave_seconds':time.monotonic()-start,
            'scope':'Candidate is the established block-triangular exponential operation. '
                    'A strong ordinary method can execute its identical fused kernel; '
                    'small-perturbation derivative jets can additionally reduce exact bit cost. '
                    'All values certified for explicit supplied rational model, no physical acquisition, '
                    'no novelty or consequential new capability established. Import/setup before main excluded.'}
    (OUT/'EXACT_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    main()
