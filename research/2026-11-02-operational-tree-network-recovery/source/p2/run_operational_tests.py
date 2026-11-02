"""Source-faithful synthetic tests and comparisons; all inputs, source models,
measurements and costs explicit. Test data are not physical observations.
"""
import json, time
import numpy as np
from tree_operational_recovery import RootedTree, Observations, TreeTaskLP, star_quotient


def odd_quad_clamped(z,a,b,cap=.5):
    """Globally valid odd monotone law with bounded derivative: quadratic in
    calibrated |flow|<=cap, tangent-linear outside.
    """
    v=abs(float(z));sgn=1. if z>=0 else -1.
    if v<=cap: return a*z+b*z*abs(z)
    return sgn*(a*cap+b*cap*cap+(a+2*b*cap)*(v-cap))


def original_star_regression():
    # EXACT same conductance-slope [1,5] star as the saved opening:
    # inverse-flow resistance slope [1/5,1].
    C=np.array([[1.,1.],[1.,0.],[0.,1.]])
    t=RootedTree(C,np.array([.2]*3),np.array([1.]*3))
    p_hist=np.array([[.2,.2]]);p_future=np.array([.2,.4]);weight=np.array([1.,0.])
    obs=Observations(ports=[0,1],experiments=[0,0],value=[.3,.3],error=[0.,0.])
    P=TreeTaskLP(t,p_hist,p_future,obs,weight)
    lo,hi,_=P.conditional()
    assert abs(lo-.34)<1e-9 and abs(hi-.50)<1e-9
    return {'lower':lo,'upper':hi,'expected_exact_rationals':['17/50','1/2']}


def model_phi(lo,hi,kind,serial=1):
    # Globally valid inverse law, phi(0)=0; derivative remains in [lo,hi].
    m=(lo+hi)/2; d=(hi-lo)/2
    a=(.37 if kind%2==0 else -.29)*d
    t=(.7+.13*(kind%5))
    return lambda z: m*z + a*np.tanh(t*z)/t


def full_obs(tree, ps, phis,delta=0):
    ys=np.array([tree.actual_voltage(p,phis) for p in ps]);H,ports=ys.shape
    ex=np.repeat(np.arange(H),ports);bp=np.tile(np.arange(ports),H)
    return Observations(bp,ex,ys.flatten(),np.full(H*ports,delta))


def binary_tree(ports=8):
    # Ground-root trunk plus all strict subtrees of a rooted binary tree.
    groups=[]
    def recurse(ids):
        groups.append(ids)
        if len(ids)>1:
            a=len(ids)//2
            recurse(ids[:a]);recurse(ids[a:])
    recurse(list(range(ports)))
    C=np.array([[float(i in grp) for i in range(ports)] for grp in groups])
    lo=.19+.03*(np.arange(len(C))%4)
    hi=lo+.18+.04*(np.arange(len(C))%3)
    return RootedTree(C,lo,hi)


def tree_source_tests():
    tree=binary_tree(8)
    phis=[model_phi(tree.lo[e],tree.hi[e],e) for e in range(tree.edges)]
    rng=np.random.default_rng(377)
    cases=[]
    for case in range(6):
        H=3+case
        p_hist=rng.uniform(-.13,.13,size=(H,tree.ports))
        p_future=rng.uniform(-.2,.2,size=tree.ports)
        weight=np.zeros(tree.ports);weight[case%8]=1.
        if case%3==2: weight[(case+2)%8]=-.5
        ob=full_obs(tree,p_hist,phis,delta=0.00015 if case%2 else 0.)
        # Received readings really are perturbed, with source-preserving,
        # deterministic bounded sensor error, not a fictitious exact record.
        if case%2:
            ob.value += rng.uniform(-ob.error,ob.error)
        P=TreeTaskLP(tree,p_hist,p_future,ob,weight)
        start=time.perf_counter();lower,upper,extrema=P.conditional();p_time=time.perf_counter()-start
        # Strong, equally informed FULL-LAW IDENTIFICATION comparator:
        # construct two different globally valid piecewise-affine original
        # edge-law families attaining the exact source sharp task endpoints.
        reconstructed=[]
        for val,res in extrema:
            laws=P.construct_source(res)
            tval=float(weight@tree.actual_voltage(p_future,laws))
            assert abs(tval-val)<3e-7
            for z in range(len(ob.value)):
                h=int(ob.experiments[z]);port=int(ob.ports[z])
                yy=tree.actual_voltage(p_hist[h],laws)[port]
                assert abs(yy-ob.value[z])<=ob.error[z]+3e-7
            reconstructed.append(tval)
        du,_,_=P.dual_certificate(1.)
        dl,_,_=P.dual_certificate(-1.)
        rho,_,_=P.dual_certificate(minimax=True)
        base_lo,base_hi=P.no_history()
        truth=weight@tree.actual_voltage(p_future,phis)
        assert lower-1e-8<=truth<=upper+1e-8
        assert abs(upper-du)<2e-7 and abs(lower+dl)<2e-7
        assert (upper-lower)/2<=rho+2e-7 # conditioned radius <= global minimax
        cases.append({'case':case,'edge_count':tree.edges,'ports':tree.ports,'old_episodes':H,
            'observed_scalars':len(ob.value),'measurement_halfwidth':float(ob.error[0]),
            'true':float(truth),'conditional_low':lower,'conditional_high':upper,
            'conditional_width':upper-lower,'no_history_width':base_hi-base_lo,
            'global_minimax_halfwidth':rho,'constructed_full_law_extrema':reconstructed,
            'primal_time_s':p_time,'dual_gap':max(abs(upper-du),abs(lower+dl))})
    return cases


def star_information_floor():
    tree=star_quotient(4,calibration=True)
    def f0(z):return odd_quad_clamped(z,.12,.09)
    def phie(e):return lambda z:odd_quad_clamped(z,.35+.01*(e%4),.07)
    phis=[f0]+[phie(e) for e in range(1,tree.edges)]
    future=np.array([.12,.12,.12,.12,0.])
    base=np.eye(tree.ports)[:4]*.12
    c=np.zeros(tree.ports);c[0]=1
    old=full_obs(tree,base,phis,delta=0.)
    P=TreeTaskLP(tree,base,future,old,c)
    low,hi,_=P.conditional()
    du,_,_=P.dual_certificate(1.)
    dl,_,_=P.dual_certificate(-1.)
    assert abs(hi-du)<1e-7 and abs(low+dl)<1e-7
    # one high-flow reference probe in dedicated calibration port
    ref=np.zeros(tree.ports);ref[-1]=.48
    augmented=np.vstack([base,ref])
    aug=full_obs(tree,augmented,phis,delta=0.)
    PA=TreeTaskLP(tree,augmented,future,aug,c)
    auglo,aughi,_=PA.conditional()
    # Analytic info lower bound on unseen high trunk flow from <=.12 tests
    floor=(tree.hi[0]-tree.lo[0])*(.48-.12)
    assert hi-low>=floor-1e-7
    assert aughi-auglo<1e-7
    return {'safe_single_port_limit':.12,'target_trunk_flow':.48,
            'unavoidable_trunk_interval_width':floor,
            'without_reference':[low,hi],'without_width':hi-low,
            'with_calibration_reference':[auglo,aughi],'with_width':aughi-auglo,
            'no_history':P.no_history(),'true':float(c@tree.actual_voltage(future,phis))}


def large_serial_experiment(n_service=64,serial=40):
    """All physical edges are distinct (per-edge law unidentifiable on chains),
    but known *series-equivalent* uncertainty bands reduce exactly to a star
    quotient. 1 robust calibration source and n low-flow service probes.
    """
    tree=star_quotient(n_service,series_length=serial,calibration=True)
    ports=tree.ports
    weights=np.array([.8+.4*((i*23)%31)/30 for i in range(n_service)],float)
    q=.48*weights/np.sum(weights)
    pstar=np.r_[q,0.]
    def trunk(j): return odd_quad_clamped(j,.12,.09)
    def branch(i,j):return odd_quad_clamped(j,.33+.06*((i*7)%13)/12,.07)
    # Heterogeneous distinct constituent laws per serial chain. Because sine
    # and cosine coefficients sum to zero around a full period, the SUM of
    # each branch's 40 laws is the intended nonlinear aggregate EXACTLY in
    # real arithmetic, not an assumption of identical microscopic edges.
    def components(a,b,offset):
        laws=[]
        for k in range(serial):
            angle=2*np.pi*(k+offset)/serial
            ak=a/serial*(1+.04*np.sin(angle))
            bk=b/serial*(1+.10*np.cos(angle))
            laws.append(lambda z, a=ak, b=bk:odd_quad_clamped(z,a,b))
        return laws
    phis=components(.12,.09,0)
    for i in range(ports):
        phis.extend(components(.33+.06*((i*7)%13)/12,.07,i%17))
    truth=np.array([trunk(.48)+branch(i,q[i]) for i in range(n_service)])
    # Source-faithful equality to original 2640-edge model on target state.
    full=tree.actual_voltage(pstar,phis)
    assert np.allclose(full[:n_service],truth,atol=1e-12)
    ref=np.zeros(ports);ref[-1]=.48
    ref_y=tree.actual_voltage(ref,phis)
    # reference inactive port 0, even if a measurement port is driven, choose a different one.
    yref=ref_y[0]
    pred=np.zeros(n_service);rows=[]
    for i in range(n_service):
        p=np.zeros(ports);p[i]=q[i]
        y=tree.actual_voltage(p,phis)
        inactive=0 if i!=0 else 1
        pred[i]=yref+y[i]-y[inactive]
        rows.append({'port':i,'demand':q[i],'true_voltage':truth[i],
                     'stitched_voltage':pred[i],'ordinary_no_history_low':.10*.48+.30*q[i],
                     'ordinary_no_history_high':.50*.48+.80*q[i]})
    assert np.allclose(truth,pred,atol=1e-12)
    # The reference probe necessarily incurs its actual paid stationary input power.
    pref=ref[-1]*ref_y[-1]
    ptarget=sum(q*truth)
    # Also solve the original physical 2640-edge LP for one terminal using only
    # three scalar readings and all the unknown series-edge values retained.
    p_probe=np.zeros(ports);p_probe[0]=q[0]
    y_probe=tree.actual_voltage(p_probe,phis)
    p_hist=np.array([ref,p_probe])
    obs=Observations(ports=[1,0,1],experiments=[0,1,1],
                     value=[ref_y[1],y_probe[0],y_probe[1]],error=[2e-5]*3)
    c=np.zeros(ports);c[0]=1.
    P=TreeTaskLP(tree,p_hist,pstar,obs,c)
    tic=time.perf_counter();low,high,_=P.conditional();lp_seconds=time.perf_counter()-tic
    assert low-1e-7<=truth[0]<=high+1e-7
    assert (high-low)<0.000125
    return {'physical_edges':tree.edges,'service_ports':n_service,'serial_edges_per_branch':serial,
            'terminal_observations':1+2*n_service,'controlled_episodes':1+n_service,
            'reference_total_flow':.48,'reference_steady_power':pref,'target_total_power':ptarget,
            'max_source_true':max(truth),'max_service_no_history_upper':max(r['ordinary_no_history_high'] for r in rows),
            'reference_port_voltage':ref_y[-1], 'original_edge_lp_first_terminal_interval':[low,high],
            'original_edge_lp_seconds':lp_seconds, 'original_edge_lp_variables':P.n,
            'original_edge_lp_inequalities':P.A.shape[0], 'maximum_equality_error':max(abs(pred-truth)),
            'measurement_error_assumed_each':2e-5,
            'with_exact_currents_observation_error_bound':6e-5,
            'with_input_current_error_budget':(6e-5+.50*2e-4+.80*1e-5+.50*n_service*5e-6+.80*5e-6),
            'rated_service_voltage_threshold':.09,
            'service_outcomes_certified':bool(max(truth)+6e-5+.50*2e-4+.80*1e-5+.50*n_service*5e-6+.80*5e-6<.09),
            'details':rows}


if __name__=='__main__':
    r={'original_star_regression':original_star_regression(),
       'tree_negative_and_positive_flow_cases':tree_source_tests(),
       'info_floor_fixture':star_information_floor(),
       'large_serial_counterfactual':large_serial_experiment()}
    file='producer-workspace/operational_recovery_results.json'
    with open(file,'w') as f:json.dump(r,f,indent=2)
    print('WROTE',file)
    for x in r['tree_negative_and_positive_flow_cases']:
        print('tree',x['case'],'history',x['old_episodes'],'true',round(x['true'],8),
          'sharp width',round(x['conditional_width'],8),'no history',round(x['no_history_width'],8),
          'dualgap',x['dual_gap'])
    print('information floor',r['info_floor_fixture'])
    print('large physical star summary:',{k:v for k,v in r['large_serial_counterfactual'].items() if k!='details'})
