"""Exact SU2 contact algebra and literal finite-history controls.

The small physical finite-separation limit is a numerical control of the
shared-edge contact formula. It is not a thermal precision acquisition.
"""
from pathlib import Path
import json,time
import numpy as np
import sympy as sy
from bilocal_time_preview import Physical,ROOT

def epsilon(a,b,c):return (a-b)*(b-c)*(c-a)//2 if len({a,b,c})==3 else 0
def comm(a,b):return a*b-b*a
def anti(a,b):return a*b+b*a

def main():
    begin=time.monotonic();I=sy.I;eye=sy.eye(5);sp=sy.zeros(5)
    for m in range(-2,2):sp[m+3,m+2]=sy.sqrt(6-m*(m+1))
    sm=sp.T;spin=[(sp+sm)/2,(sp-sm)/(2*I),sy.diag(-2,-1,0,1,2)]
    g=[I*s for s in spin];z=sy.zeros(5)
    for a in range(3):
        for d in range(3):
            expression=-sum((epsilon(a,b,c)*g[b]*g[d]*g[c]for b in range(3)for c in range(3)),z)-anti(g[a],g[d])-6*(a==d)*eye
            assert expression==z
    left=[sy.kronecker_product(s,eye)for s in spin];right=[sy.kronecker_product(eye,s)for s in spin]
    h=sum((a*b for a,b in zip(left,right)),sy.zeros(25));H=3*h
    dl=18*right[2]-anti(left[2],H)/2;dr=18*left[2]-anti(right[2],H)/2
    x=sum((epsilon(2,b,c)*comm(H,left[b])*left[c]for b in range(3)for c in range(3)),sy.zeros(25))
    assert x-I*dl-comm(H,I*left[2])/2==sy.zeros(25)
    contact=I*sum((epsilon(2,b,c)*right[b]*dl*right[c]for b in range(3)for c in range(3)),sy.zeros(25))+anti(dl,right[2])/2
    symmetric=3*(36*sy.eye(25)-6*(left[2]**2+right[2]**2)+anti(left[2],anti(right[2],h))/4)
    assert contact==symmetric and sy.trace(contact)==1200
    ng=[np.array(a,dtype=complex)for a in g];rng=np.random.default_rng(20261028)
    def trace_word(events):
        w=np.eye(5,dtype=complex)
        for _,a in sorted(events,key=lambda x:-x[0]):w=w@a
        return np.trace(w)
    def avg(history,delta=None):
        cuts={0.,1.}
        for t,_ in history:
            cuts.add(t)
            if delta is not None:cuts.add((t-delta)%1)
        cuts=sorted(cuts);out=0j
        for a,b in zip(cuts,cuts[1:]):
            t=(a+b)/2
            if delta is None:value=trace_word(history+[(t,ng[2])])
            else:value=-trace_word(history+[((t+delta)%1,ng[0]),(t,ng[1])])+trace_word(history+[((t+delta)%1,ng[1]),(t,ng[0])])
            out+=(b-a)*value
        return out
    history_controls=[]
    for k in range(1,9):
        times=np.sort(rng.random(k));labels=rng.integers(0,3,k);history=list(zip(times,[ng[a]for a in labels]))
        jet=0j
        for j,d in enumerate(labels):
            word=np.eye(5,dtype=complex)
            for index in list(range(j-1,-1,-1))+list(range(k-1,j,-1)):word=word@ng[labels[index]]
            jet+=np.trace((ng[2]@ng[d]+6*(d==2)*np.eye(5))@word)
        base=avg(history);finite=(avg(history,1e-6)-base)/1e-6
        jeterror=abs(finite-jet)/max(1.,abs(jet));assert jeterror<2e-7,(k,finite,jet)
        parity=abs(avg(history,.125)+avg(history,.875))/max(1.,abs(avg(history,.125)))
        half=abs(avg(history,.5));assert parity<2e-12 and half<1e-11
        shifted=[((t+.371)%1,a)for t,a in history]
        shift=abs(avg(history,.125)-avg(shifted,.125))/max(1.,abs(avg(history,.125)));assert shift<2e-12
        history_controls.append({'events':k,'labels':labels.tolist(),'one_sided_jet_relative_error':jeterror,
                                 'relative_time_parity_error':parity,'half_period_absolute':half,'global_translation_error':shift})
    model=Physical(2);c00,_=model.source_integral(None,None,24)
    dl_np=np.array(dl,dtype=float);dr_np=np.array(dr,dtype=float);contact_np=np.array(contact,dtype=float)
    H_np=np.array(H,dtype=float);e,u=np.linalg.eigh(H_np);aa=u.T@dl_np@u;bb=u.T@dr_np@u
    gaps=abs(e[:,None]-e[None,:]);psi=np.ones_like(gaps);mask=gaps>1e-9
    psi[mask]=-np.expm1(-gaps[mask])/gaps[mask]
    kernel=np.exp(-np.minimum(e[:,None],e[None,:]))*psi
    c11=float(np.sum(aa*bb.T*kernel));kmean=float(np.dot(np.diag(u.T@contact_np@u),np.exp(-e)))
    jet_norm=-c11+kmean;controls=[]
    c01=float(np.sum((u.T@np.array(left[2],dtype=float)@u)*bb.T*kernel))
    for delta in (.002,.001,.0005):
        c0d,_=model.source_integral(None,delta,24);cdd,_=model.source_integral(delta,delta,24)
        estimate=(-cdd+2*c0d-c00)/delta**2
        controls.append({'delta':delta,'jet_norm_finite_separation':estimate,'jet_norm_relative_error':abs(estimate/jet_norm-1),
                         'cross_jet_estimate':(c0d-c00)/delta,'cross_jet_relative_error':abs(((c0d-c00)/delta)/c01-1)})
    assert controls[-1]['jet_norm_relative_error']<.03 and controls[-1]['cross_jet_relative_error']<.03
    output={'status':'PASS_EXACT_SPIN_ALGEBRA_AND_LITERAL_HISTORY_CONTACT_CONTROLS',
      'exact_triple_generator_identities':9,'exact_endpoint_operator_identity':True,
      'exact_shared_edge_contact_identity':True,'trace_contact_beta3':1200,
      'literal_histories':history_controls,'physical_dimer_controls':controls,
      'dimer_source_jet_norm_formula':jet_norm,'dimer_naive_without_contact':-c11,
      'dimer_contact_expectation':kmean,'seconds':time.monotonic()-begin,
      'scope':'Small exact algebra plus numerical finite-history and dimer limits. Not a certified source moment family.'}
    (ROOT/'results/contact_identity_controls.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
