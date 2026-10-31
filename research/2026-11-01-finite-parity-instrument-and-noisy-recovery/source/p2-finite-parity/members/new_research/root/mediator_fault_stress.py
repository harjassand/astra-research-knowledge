"""Full finite-mediator stress test with actual noncommuting data faults.

No thermal, no intrinsic material loss in this diagnostic. Finite pulse,
all main output, and all terminal modes are retained. Unknown fault history
means the nominal controller applies no history-dependent phase recovery.
The visibility quoted discards the record; the inaccessible fraction alone
is also recorded. This is not a universal limit on optimal joint decoding.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp,simpson
from finite_mediator_parity import Model,waveforms

def run(m,q=None,tau=None,du=0.,dw=0.,dg1=0.,dg2=0.,dchi=0.,detune=0.,samples=6001):
    z=np.array([[1,1],[1,-1],[-1,1],[-1,-1]])
    times=np.linspace(0,m.T,samples)
    if tau is not None:times=np.unique(np.r_[times,tau])
    bs=[0,m.T] if tau is None else [0,tau,m.T]
    vals=np.zeros((len(times),4,3),complex);initial=np.zeros((4,3),complex)
    for seg in range(len(bs)-1):
        labels=z.copy()
        if seg:labels[:,q]*=-1
        def rhs(t,a):
            a=a.reshape(4,3);b,c,d=a[:,0],a[:,1],a[:,2];f=waveforms(m,t)
            db=-m.kb*b/2-1j*m.g*(1+dg1)*d-1j*(1+du)*f['u']*labels[:,1]
            dc=-(m.kc/2+1j*(m.chi*(1+dchi)*labels[:,0]+detune))*c-1j*m.g*(1+dg2)*d-1j*(1+dw)*f['w']*labels[:,1]
            dd=-m.Gamma*d/2-1j*m.g*((1+dg1)*b+(1+dg2)*c)
            return np.c_[db,dc,dd].ravel()
        inds=np.where((times>=bs[seg])&(times<=bs[seg+1]))[0]
        sol=solve_ivp(rhs,bs[seg:seg+2],initial.ravel(),t_eval=times[inds],method='DOP853',rtol=1e-10,atol=1e-12)
        if not sol.success:raise RuntimeError(sol.message)
        vals[inds]=sol.y.T.reshape(-1,4,3);initial=vals[inds[-1]]
    main=np.sqrt(m.Gamma)*vals[:,:,2]
    hidden_b=np.sqrt(m.kb)*vals[:,:,0];hidden_c=np.sqrt(m.kc)*vals[:,:,1]
    rows=[]
    for i,j in [(0,3),(1,2)]:
        d=main[:,i]-main[:,j]
        Dmain=float(simpson(abs(d)**2,x=times)/2)
        Dhid=float(simpson(abs(hidden_b[:,i]-hidden_b[:,j])**2+abs(hidden_c[:,i]-hidden_c[:,j])**2,x=times)/2)
        Dterm=float(np.sum(abs(vals[-1,i]-vals[-1,j])**2)/2)
        De=Dmain+Dhid+Dterm
        rows.append({'initial_parity':int(z[i,0]*z[i,1]),'D_main':Dmain,'D_hidden':Dhid,'D_terminal':Dterm,
                     'record_discarded_visibility':float(np.exp(-De)),
                     'record_discarded_equivalent_pZ':float(-np.expm1(-De)/2),
                     'inaccessible_main_visibility':float(np.exp(-(1-m.eta)*Dmain)),
                     'inaccessible_main_equivalent_pZ':float(-np.expm1(-(1-m.eta)*Dmain)/2),
                     'parity_quadrature_difference_energy':float(simpson(d.imag**2,x=times)),
                     'max_final_mode_photons':float(max(np.sum(abs(vals[-1,i])**2),np.sum(abs(vals[-1,j])**2)))})
    return rows

def main():
    m=Model()
    out={'model':m.__dict__,'nominal':run(m),'calibration':[],'X_faults':[]}
    for name,kw in [('source_gain',{'du':.01}),('corrector_gain',{'dw':.01}),('both_gains',{'du':.01,'dw':.01}),
                    ('chi_gain',{'dchi':.01}),('one_beamsplitter',{'dg1':.01}),('both_beamsplitters',{'dg1':.01,'dg2':.01}),
                    ('common_detuning_0.01chi',{'detune':.01*m.chi})]:
        row={'error':name,'parameters':kw,'pairs':run(m,**kw)};out['calibration'].append(row)
        print(name,row['pairs'][0]['record_discarded_equivalent_pZ'],flush=True)
    for q in (0,1):
        for f in (.1,.25,.5,.75,.9):
            row={'physical_qubit':q+1,'time_fraction':f,'pairs':run(m,q=q,tau=m.T*f)};out['X_faults'].append(row)
            print('X',q+1,f,row['pairs'][0]['record_discarded_equivalent_pZ'],row['pairs'][0]['inaccessible_main_equivalent_pZ'],flush=True)
    Path(__file__).with_name('mediator_fault_results.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
