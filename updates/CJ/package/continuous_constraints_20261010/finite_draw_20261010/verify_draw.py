#!/usr/bin/env python3
"""Replay saved integer/rational certificates; never trust reported floats.

Uses the same integer normal-CDF primitive (so this is not an independent proof
of that primitive). All matrix, acceptance, solve and residual checks are
recomputed directly from saved raw input and saved factor/output arrays.
"""
import hashlib, json, math, sys, time
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from certified_draw import normal_cdf_interval, IV_SCALE, N, M, D, SCALE, normal_constant, precision_factor

sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent

def rat(x): return Q(int(x['num']),int(x['den']))

def verify_report(report=None, raw_path=None):
    report=report or json.loads((HERE/'CERTIFIED_DRAW.json').read_text())
    raw_path=raw_path or HERE/'RAW_INPUT.npz'
    assert hashlib.sha256(raw_path.read_bytes()).hexdigest()==report['raw_input_sha256']
    raw=np.load(raw_path,allow_pickle=False)
    d=int(raw['denominator'])
    b=[raw['B1'].astype(object),raw['B2'].astype(object)]
    assert d==D and all(a.shape==(N,N) for a in b)
    g=[[sum(int(x)*int(y) for x,y in zip(a.flat,c.flat)) for c in b] for a in b]
    nc=report['native_certificate']
    assert g==nc['G_integer']
    detg=g[0][0]*g[1][1]-g[0][1]**2
    assert detg==int(nc['det_G']) and detg>0
    h=[[Q(x,d*d) for x in row] for row in g]
    assert h==[[rat(x) for x in row] for row in nc['H']]
    mp=(g[1][1]*(b[0]@b[0].T)-g[0][1]*(b[0]@b[1].T+b[1]@b[0].T)+g[0][0]*(b[1]@b[1].T))
    assert np.array_equal(mp,mp.T)
    rows=[int(mp[i,i])+sum(abs(int(mp[i,j])) for j in range(N) if i!=j) for i in range(N)]
    assert rows==[int(x) for x in nc['Mp_Gershgorin_row_numerators']]
    r=nc['r']; assert r*max(rows)<=detg and r>=4*(M+1)**2
    assert max(rows)* (r+1)>detg # r is largest passing this Gershgorin bound.
    assert nc['ideal_acceptance_lower_bound']=={'num':str(r-2),'den':str(r),'float':float(Q(r-2,r))} or rat(nc['ideal_acceptance_lower_bound'])==Q(r-2,r)
    comm=b[0]@b[1]-b[1]@b[0]
    assert sum(int(x)**2 for x in comm.flat)==int(nc['commutator_integer_squared_Frobenius'])>0
    assert all(np.count_nonzero(a)==N*N for a in b)

    witness=report['nonradial_witness']
    lams=[[rat(x) for x in witness[key]] for key in ['lambda_1','lambda_2']]
    radii=[sum((v[i]*h[i][j]*v[j] for i in range(M) for j in range(M)),Q(0)) for v in lams]
    assert radii[0]==radii[1]==rat(witness['equal_H_radius_squared'])
    db=[precision_factor(b,v)[3] for v in lams]
    assert db[0][1]<db[1][0] or db[1][1]<db[0][0]
    assert witness['intervals_disjoint'] is True

    draw=report['draw']; seeds=draw['seed_generation']['seeds']
    assert len(seeds)==r+2*N
    assert draw['seed_generation']['normal_constant_certificate']==normal_constant()[1]
    z=[]; total_seed_error=Q(0)
    for c in seeds:
        k=c['uniform_cell_index']; ub=c['uniform_bits']; qb=c['fraction_bits']
        lo,hi=map(int,c['normal_interval_integer']); zi=int(c['rounded_normal_integer'])
        assert 0<k<(1<<ub)-1 and lo<=zi<=hi and qb==48
        cl=normal_cdf_interval(Q(lo,1<<qb)); ch=normal_cdf_interval(Q(hi,1<<qb))
        assert cl[1]==int(c['cdf_upper_at_lower']) and ch[0]==int(c['cdf_lower_at_upper'])
        assert Q(cl[1],IV_SCALE)<=Q(k,1<<ub)
        assert Q(ch[0],IV_SCALE)>=Q(k+1,1<<ub)
        e=Q(max(zi-lo,hi-zi),1<<qb)
        assert e==rat(c['coordinate_error_bound'])
        total_seed_error+=e*e
        z.append(Q(zi,1<<qb))
    assert total_seed_error==rat(draw['seed_generation']['sum_coordinate_coupling_error_squared'])

    lam=[rat(x) for x in draw['proposal']['lambda']]
    lden=math.lcm(*(x.denominator for x in lam))
    anum=sum((a*int(x*lden) for a,x in zip(b,lam)),np.zeros((N,N),dtype=object))
    aden=d*lden
    knum=anum@anum.T+np.eye(N,dtype=object)*(aden*aden)
    lint=np.array([[int(x) for x in row] for row in draw['precision_factor']['rounded_factor_integer']],dtype=object)
    assert all(lint[i,i]>0 for i in range(N))
    assert all(lint[i,j]==0 for i in range(N) for j in range(i+1,N))
    pp=lint@lint.T
    en=knum*SCALE*SCALE-pp*aden*aden
    delta=Q(max(sum(abs(int(x)) for x in row) for row in en),aden*aden*SCALE*SCALE)
    assert delta==rat(draw['precision_factor']['residual_norm_bound_delta'])<1
    detp=Q(math.prod(int(lint[i,i]) for i in range(N)),SCALE**N)**2
    assert detp==rat(draw['precision_factor']['det_P'])
    detlo,detup=detp/(1+delta)**N,detp/(1-delta)**N
    assert detlo==rat(draw['precision_factor']['det_K_lower'])
    assert detup==rat(draw['precision_factor']['det_K_upper'])
    ss=sum((lam[i]*h[i][j]*lam[j] for i in range(M) for j in range(M)),Q(0))
    ac=draw['acceptance']; alo,ahi=(1+ss/r)**r/detup,(1+ss/r)**r/detlo
    assert ss==rat(ac['s'])
    assert alo==rat(ac['squared_acceptance_lower']) and ahi==rat(ac['squared_acceptance_upper'])
    assert 0<alo<=ahi<=1
    uhi=Q(ac['uniform_cell_index']+1,1<<ac['uniform_bits'])
    assert uhi*uhi<alo and ac['decision']=='accept'
    assert alo-uhi*uhi==rat(ac['exact_positive_comparison_margin'])

    out=draw['output']; xx=list(map(int,out['x_integer'])); yy=list(map(int,out['y_integer']))
    rr=[sum((Q(int(lint[j,i])*xx[j],SCALE*SCALE) for j in range(i,N)),Q(0))-z[r+i] for i in range(N)]
    rr2=sum((x*x for x in rr),Q(0))
    assert rr2==rat(out['covariance_solve_residual_squared'])
    assert rr2/(1-delta)==rat(out['squared_distance_to_L_inverse_transpose_rounded_seed_upper'])
    ff=[[sum(xx[k]*int(b[i][k,j]) for k in range(N)) for j in range(N)] for i in range(M)]
    fden=d*SCALE
    ss=[[sum(ff[i][k]*ff[j][k] for k in range(N)) for j in range(M)] for i in range(M)]
    dets=ss[0][0]*ss[1][1]-ss[0][1]**2
    assert dets>0
    assert Q(dets,(ss[0][0]+ss[1][1])*fden*fden)==rat(out['fiber_Gram_min_eigenvalue_lower'])
    zz=[int(x*SCALE) for x in z[r+N:]]
    fz=[sum(ff[i][j]*zz[j] for j in range(N)) for i in range(M)]
    coeff=[ss[1][1]*fz[0]-ss[0][1]*fz[1],ss[0][0]*fz[1]-ss[0][1]*fz[0]]
    ystar=[Q(zz[j]*dets-sum(ff[i][j]*coeff[i] for i in range(M)),SCALE*dets) for j in range(N)]
    assert all(sum((Q(ff[i][j],fden)*ystar[j] for j in range(N)),Q(0))==0 for i in range(M))
    yerr=sum(((Q(yy[j],SCALE)-ystar[j])**2 for j in range(N)),Q(0))
    assert yerr==rat(out['fiber_rounding_error_squared'])<=Q(N,4*SCALE*SCALE)
    fr=[Q(sum(ff[i][j]*yy[j] for j in range(N)),fden*SCALE) for i in range(M)]
    fr2=sum((x*x for x in fr),Q(0))
    assert fr==[rat(x) for x in out['final_residual']]
    assert fr2==rat(out['final_residual_squared'])<=rat(out['requested_residual_tolerance'])**2
    return {'all_saved_exact_certificates_verified':True,'normal_cells_verified':len(seeds),
        'r':r,'full_W1_algorithm_verified':False,
        'shared_code_limit':'CDF verifier reuses the same directed integer CDF implementation; this is a replay consistency check, not a separate proof audit.'}


def main():
    t=time.perf_counter(); result=verify_report()
    result['verification_wall_seconds']=time.perf_counter()-t
    (HERE/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
