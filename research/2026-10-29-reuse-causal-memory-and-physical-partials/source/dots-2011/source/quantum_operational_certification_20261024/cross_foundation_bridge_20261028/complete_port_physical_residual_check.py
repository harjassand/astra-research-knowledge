#!/usr/bin/env python3
"""Exact finite author diagnostics of the COMPLETE physical CP-suffix route.
No source samples, random numbers, hardware, generic QE/fit/decoder/compiler.
"""
from pathlib import Path
from hashlib import sha256
from itertools import product, combinations
import json
import sympy as s
HERE=Path(__file__).resolve().parent
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
zero=(I+Z)/2;one=(I-Z)/2;plus=(I+X)/2;yp=(I+Y)/2
states=[(I+sgn*P)/2 for P in [X,Y,Z] for sgn in [1,-1]]
effects=[rho/3 for rho in states]
Din=[I/6+sgn*P/2 for P in [X,Y,Z] for sgn in [1,-1]]
Bout=[3*D for D in Din]
def clean(A):return A.applyfunc(s.expand)
def tr(A):return s.expand(s.trace(A))
def absM(A):return A.applyfunc(abs)
def zeroM(A):return A==s.zeros(A.rows,A.cols)
def entry_norm(A):
    # Exact rational upper bound on nuclear norm: sum |entry| <= sum |Re|+|Im|.
    return sum(abs(s.re(z))+abs(s.im(z)) for z in A)
def ptr_memory(A):
    n=A.rows//2
    return clean(A[:n,:n]+A[n:,n:])
def functional(F,A):
    n=A.rows//2
    return clean(sum((F[b,a]*A[a*n:(a+1)*n,b*n:(b+1)*n]
                     for a,b in product(range(2),repeat=2)),s.zeros(n)))
def units(n):
    for a,b in product(range(n),repeat=2):
        A=s.zeros(n);A[a,b]=1;yield A
for A in units(2):
    assert clean(sum((rho*tr(D*A) for rho,D in zip(states,Din)),s.zeros(2)))==A
    assert clean(sum((B*tr(E*A) for B,E in zip(Bout,effects)),s.zeros(2)))==A
assert sum(effects,s.zeros(2))==I
assert all(max(abs(v) for v in D.eigenvals())==s.Rational(2,3) for D in Din)
assert all(sum(abs(v)*mult for v,mult in B.eigenvals().items())==3 for B in Bout)

SW=s.zeros(4);U=s.zeros(4)
for m,a in product(range(2),repeat=2):
    SW[2*a+m,2*m+a]=1
    U[2*a+(m^a),2*m+a]=1
n=s.Integer(10**7)
phase=((n*n-1)*I+2*n*s.I*Z)/(n*n+1)
Us=s.kronecker_product(phase,I)*U
L0=s.diag(1,s.Rational(4,5));L1=s.Matrix([[0,s.Rational(3,5)],[0,0]])
true_ports={'swap':[SW],'unit':[Us],'damp':[s.kronecker_product(I,L0)*Us,s.kronecker_product(I,L1)*Us]}
fit_ports={'swap':[SW],'unit':[U],'damp':[s.kronecker_product(I,L0)*U,s.kronecker_product(I,L1)*U]}
for ports in [true_ports,fit_ports]:
    for Ks in ports.values():assert clean(sum((K.conjugate().T*K for K in Ks),s.zeros(4)))==s.eye(4)

def induce(K,tau,rho,E):
    W=clean(K*s.kronecker_product(tau,rho)*K.conjugate().T)
    return clean(s.Matrix([[sum(E[c,b]*W[2*m+b,2*z+c] for b,c in product(range(2),repeat=2))
                           for z in range(2)] for m in range(2)]))
eps=s.Rational(1,10**7)
rho0=zero;sig0=(1-eps)*zero+eps*one
Ts=[rho0]+[rho/3 for rho in [one,plus,yp]]
Ss=[sig0]+[(1-eps)*rho/3 for rho in [one,plus,yp]]
# Actual legal prefix: SWAP in rho_j; observe outgoing initial memory with E_Z+.
for j,rho in enumerate([one,plus,yp],start=1):
    assert induce(SW,rho0,rho,zero/3)==Ts[j]
    assert induce(SW,sig0,rho,zero/3)==Ss[j]
Fs=[I,zero/3,plus/3,yp/3]
H=s.Matrix([[tr(F*T) for T in Ts] for F in Fs]);Hf=s.Matrix([[tr(F*T) for T in Ss] for F in Fs])
assert H.det()!=0 and Hf.det()!=0
Hi=H.inv();Hfi=Hf.inv();m=H[0,:];mf=Hf[0,:]
assert list(m)==[1,s.Rational(1,3),s.Rational(1,3),s.Rational(1,3)]

def extract(A,Hi):
    ys=[functional(F,A) for F in Fs]
    return [clean(sum((Hi[j,i]*ys[i] for i in range(4)),s.zeros(ys[0].rows))) for j in range(4)]
def lift(xs,core):
    return clean(sum((s.kronecker_product(T,x) for T,x in zip(core,xs)),s.zeros(2*xs[0].rows)))
for core,inv in [(Ts,Hi),(Ss,Hfi)]:
    for A in units(2):assert lift(extract(A,inv),core)==A

# Source-to-fit algebraic core lift is NOT presumed CP. Find exact negative Choi principal minor.
Jlift=s.zeros(4)
for a,b in product(range(2),repeat=2):
    E=s.zeros(2);E[a,b]=1
    Jlift[2*a:2*a+2,2*b:2*b+2]=lift(extract(E,Hi),Ss)
assert Jlift==Jlift.conjugate().T
negative_minor=None
for k in range(1,5):
    for subset in combinations(range(4),k):
        det=s.factor(Jlift.extract(subset,subset).det())
        if det<0:negative_minor={'indices':subset,'determinant':str(det)};break
    if negative_minor:break
assert negative_minor is not None

# Raw joint tables and exact coordinate matrices; actual full port Kraus operators supplied above.
tables={};coords={};output_blocks={};native_choi_ranks={}
for name,ports,core,inv in [('true',true_ports,Ts,Hi),('fit',fit_ports,Ss,Hfi)]:
    for action,Ks in ports.items():
        for o,K in enumerate(Ks):
            vec=s.Matrix([K[b,a] for a in range(4) for b in range(4)])
            J=vec*vec.conjugate().T
            assert J.rank()==1
            native_choi_ranks[(name,action,o)]=1
            for u,rho in enumerate(states):
                for v,E in enumerate(effects):
                    Hz=s.Matrix([[tr(F*induce(K,T,rho,E)) for T in core] for F in Fs])
                    key=(name,action,u,o,v)
                    tables[key]=Hz;coords[key]=clean(inv*Hz)
            for i,j,u in product(range(4),range(4),range(6)):
                output_blocks[(name,action,o,i,j,u)]=clean(sum(
                    (coords[(name,action,u,o,v)][i,j]*Bout[v] for v in range(6)),s.zeros(2)))
# Full operator reconstruction on a spanning physical set: core 4 x IC6, every native branch.
reconstructions=0
for name,ports,core in [('true',true_ports,Ts),('fit',fit_ports,Ss)]:
    for action,Ks in ports.items():
        for o,K in enumerate(Ks):
            for j,u in product(range(4),range(6)):
                rec=clean(sum((s.kronecker_product(core[i],output_blocks[(name,action,o,i,j,u)])
                               for i in range(4)),s.zeros(4)))
                direct=clean(K*s.kronecker_product(core[j],states[u])*K.conjugate().T)
                assert rec==direct;reconstructions+=1

# Hypothetical rational bands: true exact centers, positive widths; no count/sample claim.
w=s.Rational(1,10**14)
DH=s.ones(4)*w;DH[0,0]=0
A=absM(Hi)*DH
assert max(sum(A[i,j] for j in range(4)) for i in range(4))<1
M=(s.eye(4)-A).inv()*absM(Hi)
assert all(x>=0 for x in M-absM(Hi))
Kcore=max(s.Integer(1),sum(M))
Es={};g_actions={}
for action,Ks in true_ports.items():
    for u,o,v in product(range(6),range(len(Ks)),range(6)):
        Ct=coords[('true',action,u,o,v)];Cf=coords[('fit',action,u,o,v)]
        Hz=tables[('true',action,u,o,v)]
        E=M*(s.ones(4)*w+DH*absM(Cf)+absM(H*Cf-Hz))
        assert all(x>=0 for x in E-absM(Ct-Cf))
        Es[(action,u,o,v)]=E
    g_actions[action]=max(sum(2*Es[(action,u,o,v)][i,j]
        for i,u,o,v in product(range(4),range(6),range(len(Ks)),range(6))) for j in range(4))
g=max(g_actions.values())
delta_m=max(DH[0,j]+abs(m[j]-mf[j]) for j in range(4))
eta=Kcore*(3*g+delta_m)/2
assert 0<eta<1

# Full quantum coordinate action including retained R, with direct comparison.
def step_coords(xs,name,action):
    out=[]
    partials={(j,u):functional(Din[u],xs[j]) for j,u in product(range(4),range(6))}
    for o in range(len(true_ports[action])):
        ys=[]
        for i in range(4):
            val=sum((s.kronecker_product(output_blocks[(name,action,o,i,j,u)],partials[(j,u)])
                     for j,u in product(range(4),range(6))),s.zeros(xs[0].rows))
            ys.append(clean(val))
        out.append(ys)
    return out
bell=s.Matrix([1,0,0,1]);Bell=bell*bell.T/2
Omega=s.kronecker_product(zero,Bell)
Omega_after=clean(s.kronecker_product(Us,I)*Omega*s.kronecker_product(Us.conjugate().T,I))
xc=extract(Omega_after,Hi)
assert lift(xc,Ts)==Omega_after
assert sum(entry_norm(x) for x in xc)<=Kcore
negative_coordinate=next(({'block':j,'diagonal':a,'value':str(x[a,a])}
    for j,x in enumerate(xc) for a in range(4) if x[a,a].is_real and x[a,a]<0),None)
if negative_coordinate is None:
    for j,x in enumerate(xc):
        for k in range(1,5):
            for subset in combinations(range(4),k):
                det=s.factor(x.extract(subset,subset).det())
                if det<0:negative_coordinate={'block':j,'minor_indices':subset,'minor_determinant':str(det)};break
            if negative_coordinate:break
        if negative_coordinate:break
assert negative_coordinate is not None
complete_reference_checks=0
for name,ports,core,inv in [('true',true_ports,Ts,Hi),('fit',fit_ports,Ss,Hfi)]:
    xs=extract(Omega_after,inv)
    for action,Ks in ports.items():
        for ys,K in zip(step_coords(xs,name,action),Ks):
            direct=clean(s.kronecker_product(K,I)*Omega_after*s.kronecker_product(K.conjugate().T,I))
            assert lift(ys,core)==direct;complete_reference_checks+=1

# Finite adaptive controller, all native/local records retained, coherent output recycling.
Q=s.Matrix([[s.Rational(3,5),-4*s.I/5],[s.Rational(4,5),3*s.I/5]])
assert Q.conjugate().T*Q==I
local_instrument=[L0*Q,L1*Q]
assert clean(sum((L.conjugate().T*L for L in local_instrument),s.zeros(2)))==I

def caller_coord(xs,L):
    LR=s.kronecker_product(L,I)
    return [clean(LR*x*LR.conjugate().T) for x in xs]
def caller_physical(A,L):
    big=s.kronecker_product(I,L,I)
    return clean(big*A*big.conjugate().T)
def native_physical(A,K):
    big=s.kronecker_product(K,I)
    return clean(big*A*big.conjugate().T)
def action_at(depth,history):
    if depth==0:return 'unit'
    if depth==1:return 'unit' if history[1]==0 else 'damp'
    return 'damp' if history[1]==0 else 'swap'
def evolve_coordinate(schedule):
    branches={():[Bell]+[s.zeros(4) for _ in range(3)]}
    prefix_norm_tests=0
    for depth,name in enumerate(schedule):
        nb={}
        for history,xs in branches.items():
            for o,ys in enumerate(step_coords(xs,name,action_at(depth,history))):
                nh=history+(o,)
                if depth==0:
                    for r,L in enumerate(local_instrument):nb[nh+(r,)]=caller_coord(ys,L)
                elif depth==1:nb[nh]=caller_coord(ys,Q)
                else:nb[nh]=ys
        branches=nb
    return branches

def evolve_physical(name):
    initial=rho0 if name=='true' else sig0;ports=true_ports if name=='true' else fit_ports
    branches={():s.kronecker_product(initial,Bell)}
    for depth in range(3):
        nb={}
        for history,omega in branches.items():
            for o,K in enumerate(ports[action_at(depth,history)]):
                yy=native_physical(omega,K);nh=history+(o,)
                if depth==0:
                    for r,L in enumerate(local_instrument):nb[nh+(r,)]=caller_physical(yy,L)
                elif depth==1:nb[nh]=caller_physical(yy,Q)
                else:nb[nh]=yy
        branches=nb
    assert sum(tr(A) for A in branches.values())==1
    return branches

def readout(xs,row):return clean(sum((row[j]*xs[j] for j in range(4)),s.zeros(4)))
true_x=evolve_coordinate(['true']*3);fit_x=evolve_coordinate(['fit']*3)
true_phys=evolve_physical('true');fit_phys=evolve_physical('fit')
for h in true_phys:
    assert lift(true_x[h],Ts)==true_phys[h]
    assert lift(fit_x[h],Ss)==fit_phys[h]
    assert readout(true_x[h],m)==ptr_memory(true_phys[h])
    assert readout(fit_x[h],mf)==ptr_memory(fit_phys[h])
# Check each algebraic hybrid and exact CP-suffix telescoping identity at complete endpoints.
hybrids=[evolve_coordinate(['true']*k+['fit']*(3-k)) for k in range(4)]
for h in true_x:
    native_sum=sum((readout(hybrids[k][h],mf)-readout(hybrids[k-1][h],mf)
                    for k in range(1,4)),s.zeros(4))
    mass=readout(true_x[h],m-mf)
    assert clean(native_sum+mass)==clean(ptr_memory(true_phys[h])-ptr_memory(fit_phys[h]))
actual_upper=sum(entry_norm(ptr_memory(true_phys[h])-ptr_memory(fit_phys[h])) for h in true_phys)/2
assert 0<actual_upper<eta
terminal_upper=sum(entry_norm(readout(true_x[h],m-mf)) for h in true_x)/2
assert terminal_upper<=Kcore*delta_m/2

# Failure control: every scalar IC causal-break branch of transpose is CP and TP on sum,
# but the putative full qubit port is not CP on a Bell input.
transpose_probs=[[tr(E*rho.T) for E in effects] for rho in states]
assert all(p>=0 for row in transpose_probs for p in row)
assert all(sum(row)==1 for row in transpose_probs)
Jtranspose=SW
assert Jtranspose.eigenvals()=={1:3,-1:1}
assert min((Jtranspose/2).eigenvals())==-s.Rational(1,2)

out={'status':'PASS exact author complete-port physical-residual diagnostics',
 'source_sha256':sha256((HERE/'COMPLETE_PORT_PHYSICAL_RESIDUAL_SIMULATOR.md').read_bytes()).hexdigest(),
 'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'memory_dimension':2,'full_core_rank':4,'H_determinant':str(H.det()),'Hfit_determinant':str(Hf.det()),
 'raw_true_masses':[str(x) for x in m],'raw_fit_masses':[str(x) for x in mf],
 'source_and_candidate_full_port_Kraus_TP_checks':6,'rank_one_native_Chois':len(native_choi_ranks),
 'full_port_spanning_reconstructions':reconstructions,'complete_entangled_reference_checks':complete_reference_checks,
 'IC_input_output_pairs':36,'IC_pair_weight':'2','IC_total_pair_weight':'72',
 'synthetic_probability_width':str(w),'actual_count_acquisition':False,
 'candidate_required_to_lie_in_bands_in_this_fixture':False,
 'K_core_exact':str(Kcore),'K_core_decimal':str(s.N(Kcore,18)),
 'epsilon_exact':str(g),'epsilon_decimal':str(s.N(g,18)),
 'mass_row_debit_exact':str(delta_m),'eta_horizon3_exact':str(eta),'eta_horizon3_decimal':str(s.N(eta,18)),
 'retained_record_branches':len(true_phys),'exact_hybrid_telescope_checks':len(true_phys),
 'complete_endpoint_half_trace_norm_certified_upper_exact':str(actual_upper),
 'complete_endpoint_half_trace_norm_certified_upper_decimal':str(s.N(actual_upper,18)),
 'terminal_mass_half_trace_norm_certified_upper_exact':str(terminal_upper),
 'negative_operator_coordinate_witness':negative_coordinate,'non_CP_core_lift_witness':negative_minor,
 'transpose_failure_control':{'positive_scalar_branches':36,'TP_branch_sums':6,'full_Choi_spectrum':{'1':3,'-1':1},'Bell_output_minimum_eigenvalue':'-1/2'},
 'source_calls':0,'episode_starts':0,'RNG_calls':0,'hardware_executions':0,
 'generic_physical_feasibility_executed':False,'generic_QE_executed':False,'decoder_SDP_executed':False,
 'compiler_executed':False,'floating_point_used_for_proof_or_comparison':False}
(HERE/'complete_port_physical_residual_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
