"""Finite-time compatible-bar polarity transfer; declared synthetic model only.

Includes material order parameter, displacement, inertia, viscosity, segmented
piezo charge, two electrical work ports, and an actual final passive RC short.
No material fit, acquired observation, thermal-noise trajectory, or efficiency
claim. The static global theorem is in ../mechanical/COMPATIBLE_PIEZO_GATE.txt.

Run: python matter_operations_20261023/coupled_dynamics/coupled_cycle.py
"""
from pathlib import Path
import argparse
import json
import time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import lil_matrix, csr_matrix, diags, bmat, vstack, hstack, eye

OUT = Path(__file__).resolve().parent


class Bar:
    def __init__(self, cells=12, subdivisions=8, pitch=.2):
        # One fixed, passive, small-strain-compatible, dimensionless model.
        self.C = 40000.
        self.KE = 20000.
        self.Cp = 1.
        self.theta = 200.
        self.alpha = .01
        self.b = self.c = 1.
        self.a = 3/16
        self.kappa = .05
        self.rho = 40000.
        self.eta = 2000.
        self.zeta = .05
        self.Rz = .02
        # Background field capacitance and series loss, per sample volume.
        self.Ch = .1
        self.Rh = .01
        self.cells = cells
        self.sub = subdivisions
        self.ell = pitch
        self.n = cells*subdivisions
        self.nn = self.n+1
        self.dx = pitch/subdivisions
        self.length = cells*pitch
        self.KD = self.KE+self.theta**2/self.Cp
        self.u0 = 2*self.alpha**2*self.C*self.KE/(self.C+self.KE)
        self.bm = self.b+self.u0
        self.Ceff = self.Cp+self.theta**2/(self.C+self.KE)
        self.Theta = self.theta*self.C*self.alpha/(self.C+self.KE)
        self.U = 2*self.Theta**2/self.Ceff
        self.B = np.sqrt(3*self.b/(4*self.c))
        self.zB = self.Theta*self.B**2
        self.lam = 9*self.bm**2/(20*self.c)-self.a
        self.mass = np.full(self.nn, self.rho*self.dx)
        self.mass[[0,-1]] *= .5
        self.left = np.arange(cells)*subdivisions
        self.right = self.left+subdivisions
        n, nn = self.n, self.nn
        self.qs = slice(0,n)
        self.us = slice(n,n+nn)
        self.vs = slice(n+nn,n+2*nn)
        self.zs = slice(n+2*nn,n+2*nn+cells)
        self.hi = n+2*nn+cells
        self.is0 = self.hi+1
        # Integrals: field-source work, piezo-source work, and four losses.
        self.size = self.is0+6
        self.integral_names = ['field_source_work','piezo_source_work',
                               'order_parameter_heat','viscous_heat',
                               'piezo_resistor_heat','field_resistor_heat']
        d=lil_matrix((self.n,self.nn))
        for i in range(self.n): d[i,i]=-1;d[i,i+1]=1
        self.D=d.tocsr()
        j=lil_matrix((self.cells,self.nn))
        for k,(l,r) in enumerate(zip(self.left,self.right)): j[k,l]=-1;j[k,r]=1
        self.J=j.tocsr()
        g=lil_matrix((self.n-1,self.n))
        for i in range(self.n-1):g[i,i]=-1;g[i,i+1]=1
        self.G=g.tocsr()

    def unpack(self,y):
        return y[self.qs],y[self.us],y[self.vs],y[self.zs]

    def initial(self):
        y = np.zeros(self.size)
        y[self.qs] = -self.B
        e = self.C*self.alpha*self.B**2/(self.C+self.KE)
        x = np.linspace(-self.length/2,self.length/2,self.nn)
        y[self.us] = e*x
        y[self.zs] = self.zB
        return y

    @staticmethod
    def ramp(s):
        s = min(1.,max(0.,s))
        return s**3*(10-15*s+6*s*s),30*s*s*(1-s)**2

    def controls(self,t,T):
        """Charge current command, smooth conjugate field, its derivative."""
        if t < T/4:
            r,dr = self.ramp(t/(T/4)); dr /= T/4
            return (-self.U*self.B**3*r,
                    -self.U*self.B**3*dr,-self.zB*dr,-self.B,'engage')
        if t < 3*T/4:
            r,dr = self.ramp((t-T/4)/(T/2)); dr /= T/2
            p = self.B*(2*r-1); pdot = 2*self.B*dr
            h = self.a*p+(self.U-self.b)*p**3+self.c*p**5
            hd = (self.a+3*(self.U-self.b)*p*p+5*self.c*p**4)*pdot
            return h,hd,0.,p,'traverse'
        if t < T:
            r,dr = self.ramp((t-3*T/4)/(T/4)); dr /= T/4
            return (self.U*self.B**3*(1-r),
                    -self.U*self.B**3*dr,self.zB*dr,self.B,'release')
        return 0.,0.,None,self.B,'passive_short'

    def rates(self,t,y,T):
        q,u,v,z = self.unpack(y)
        hcmd,hd_cmd,zd_cmd,_,stage = self.controls(t,T)
        h=y[self.hi]
        e = np.diff(u)/self.dx
        ed = np.diff(v)/self.dx
        ec = (u[self.right]-u[self.left])/self.ell
        vc = (z-self.theta*ec)/self.Cp
        zd = -vc/self.Rz if zd_cmd is None else np.full(self.cells,zd_cmd)
        # Natural zero-flux q boundary conditions from the discrete energy.
        gl = np.zeros(self.n)
        dq = np.diff(q)
        gl[:-1] += dq
        gl[1:] -= dq
        fmprime = self.a*q-self.bm*q**3+self.c*q**5
        qd = (h-fmprime+2*self.C*self.alpha*q*(e-self.alpha*q*q)
              +self.kappa*gl/self.dx**2)/self.zeta
        stress = self.C*(e-self.alpha*q*q)+self.eta*ed
        force = np.zeros(self.nn)
        force[:-1] += stress
        force[1:] -= stress
        shunt_stress = self.KE*ec-self.theta*vc
        np.add.at(force,self.left,shunt_stress)
        np.add.at(force,self.right,-shunt_stress)
        vd = force/self.mass
        hd=hd_cmd if t<T else (-h/self.Rh-np.mean(qd))/self.Ch
        vz = np.zeros(self.cells) if zd_cmd is None else vc+self.Rz*zd
        dh = np.mean(qd)+self.Ch*hd
        # Source voltage h+Rh*Ddot sustains the commanded internal field h.
        wh = self.length*(h+self.Rh*dh)*dh if t<T else 0.
        wz = self.ell*np.dot(vz,zd)
        heats = [self.zeta*self.dx*np.dot(qd,qd),
                 self.eta*self.dx*np.dot(ed,ed),
                 self.Rz*self.ell*np.dot(zd,zd),
                 self.Rh*self.length*dh*dh]
        dy = np.zeros_like(y)
        dy[self.qs]=qd; dy[self.us]=v; dy[self.vs]=vd; dy[self.zs]=zd
        dy[self.hi]=hd
        dy[self.is0:]=[wh,wz,*heats]
        return dy

    def energy(self,t,y,T):
        q,u,v,z = self.unpack(y)
        e=np.diff(u)/self.dx
        ec=(u[self.right]-u[self.left])/self.ell
        h=y[self.hi]
        fm=self.a*q*q/2-self.bm*q**4/4+self.c*q**6/6
        return float(self.dx*np.sum(fm+self.C*(e-self.alpha*q*q)**2/2)
                     +self.kappa*np.dot(np.diff(q),np.diff(q))/(2*self.dx)
                     +self.ell*np.sum(self.KE*ec*ec/2+(z-self.theta*ec)**2/(2*self.Cp))
                     +np.dot(self.mass,v*v)/2+self.length*self.Ch*h*h/2)

    def sparsity(self):
        """Conservative state-dependency mask for driven and passive stages."""
        s=lil_matrix((self.size,self.size),dtype=int)
        n,nn=self.n,self.nn
        for i in range(n):
            s[i,max(0,i-1):min(n,i+2)]=1
            s[i,n+i:n+i+2]=1
            s[i,self.hi]=1
        for i in range(nn):
            s[n+i,n+nn+i]=1
            row=n+nn+i
            s[row,max(0,i-1):min(n,i+1)]=1
            s[row,n+max(0,i-1):n+min(nn,i+2)]=1
            s[row,n+nn+max(0,i-1):n+nn+min(nn,i+2)]=1
        for j,(l,r) in enumerate(zip(self.left,self.right)):
            iz=n+2*nn+j
            for node in [l,r]:
                s[n+nn+node,n+l]=1; s[n+nn+node,n+r]=1
                s[n+nn+node,iz]=1
            s[iz,n+l]=1;s[iz,n+r]=1;s[iz,iz]=1
        # The passive bias equation contains mean(qdot) and the internal h.
        s[self.hi,self.qs]=1
        s[self.hi,self.us]=1
        s[self.hi,self.hi]=1
        s[self.is0:,:self.is0]=1
        return s.tocsr()

    def jacobian(self,t,y,T):
        """Analytical Jacobian, including source-work/heat integrals.

        Removes numerical-Jacobian overflow in zero-current terminal stages.
        Verified independently against directional finite differences.
        """
        q,u,v,z=self.unpack(y)
        _,hd_cmd,zd_cmd,_,_=self.controls(t,T)
        h=y[self.hi]
        n,nn,nz=self.n,self.nn,self.cells
        e=np.diff(u)/self.dx
        ed=np.diff(v)/self.dx
        ec=(u[self.right]-u[self.left])/self.ell
        vc=(z-self.theta*ec)/self.Cp
        zd=-vc/self.Rz if zd_cmd is None else np.full(nz,zd_cmd)
        dy=self.rates(t,y,T);qd=dy[self.qs]
        zmat=lambda a,b:csr_matrix((a,b))
        jq=diags((-self.a+3*self.bm*q*q-5*self.c*q**4
                  +2*self.C*self.alpha*e-6*self.C*self.alpha**2*q*q)/self.zeta)
        jq-=self.kappa/(self.zeta*self.dx**2)*(self.G.T@self.G)
        ju=diags(2*self.C*self.alpha*q/self.zeta)@self.D/self.dx
        im=diags(1/self.mass)
        fq=im@self.D.T@diags(2*self.C*self.alpha*q)
        fu=-im@(self.C/self.dx*(self.D.T@self.D)
                 +self.KD/self.ell*(self.J.T@self.J))
        fv=-im@(self.eta/self.dx*(self.D.T@self.D))
        fz=im@self.J.T*(self.theta/self.Cp)
        zu=self.theta/(self.Rz*self.Cp*self.ell)*self.J if zd_cmd is None else zmat(nz,nn)
        zz=-eye(nz)/(self.Rz*self.Cp) if zd_cmd is None else zmat(nz,nz)
        olddyn=bmat([[jq,ju,zmat(n,nn),zmat(n,nz)],
                  [zmat(nn,n),zmat(nn,nn),eye(nn),zmat(nn,nz)],
                  [fq,fu,fv,fz],
                  [zmat(nz,n),zu,zmat(nz,nn),zz]],format='csr')
        hc=np.zeros((self.hi,1));hc[self.qs,0]=1/self.zeta
        top=hstack([olddyn,csr_matrix(hc)],format='csr')
        hr=np.zeros(self.is0)
        if t>=T:
            hr=-np.asarray(top[self.qs,:].sum(axis=0)).ravel()/(n*self.Ch)
            hr[self.hi]-=1/(self.Rh*self.Ch)
        dyn=vstack([top,csr_matrix(hr[None,:])],format='csr')
        ji=np.asarray(dyn[self.qs,:].sum(axis=0)).ravel()/n+self.Ch*hr
        ih=np.mean(qd)+self.Ch*dy[self.hi]
        rows=np.zeros((6,self.is0))
        if t<T:
            rows[0]=self.length*(h+2*self.Rh*ih)*ji
            rows[0,self.hi]+=self.length*ih
        if zd_cmd is not None:
            rows[1,self.us]=-self.theta/self.Cp*np.asarray(zd@self.J).ravel()
            rows[1,self.zs]=self.ell*zd/self.Cp
        rows[2]=2*self.zeta*self.dx*np.asarray(qd@dyn[self.qs,:]).ravel()
        rows[3,self.vs]=2*self.eta*np.asarray(ed@self.D).ravel()
        rows[4]=2*self.Rz*self.ell*np.asarray(zd@dyn[self.zs,:]).ravel()
        rows[5]=2*self.Rh*self.length*ih*ji
        return hstack([vstack([dyn,csr_matrix(rows)]),zmat(self.size,6)],format='csr')

    def run(self,T,hold,rtol=2e-7,atol=2e-9,samples=401):
        started=time.perf_counter()
        y=self.initial(); e0=self.energy(0,y,T)
        ts=[]; ys=[]; nfev=njev=nlu=0
        # Break exactly at the controlled-current/passive-short transition.
        for a,b in [(0,T/4),(T/4,3*T/4),(3*T/4,T),(T,T+hold)]:
            if b<=a: continue
            sol=solve_ivp(lambda t,st:self.rates(t,st,T),(a,b),y,
                          method='BDF',rtol=rtol,atol=atol,
                          jac=lambda t,st:self.jacobian(t,st,T),dense_output=True,
                          max_step=min((b-a)/40,.1))
            if not sol.success: raise RuntimeError(sol.message)
            tt=np.linspace(a,b,max(25,int(samples*(b-a)/(T+hold))),endpoint=False)
            ts.extend(tt.tolist()); ys.extend(sol.sol(tt).T)
            y=sol.y[:,-1];nfev+=sol.nfev;njev+=sol.njev;nlu+=sol.nlu
        ts.append(T+hold);ys.append(y)
        ts=np.array(ts);ys=np.array(ys)
        en=np.array([self.energy(t,st,T) for t,st in zip(ts,ys)])
        wi=ys[:,self.is0]+ys[:,self.is0+1]
        di=ys[:,self.is0+2:].sum(axis=1)
        residual=en-e0-wi+di
        qs=ys[:,self.qs]
        us=ys[:,self.us]
        zz=ys[:,self.zs]
        targets=np.array([self.controls(t,T)[3] for t in ts])
        emax=np.max(np.abs(np.diff(us,axis=1)/self.dx))
        ec=(us[:,self.right]-us[:,self.left])/self.ell
        vmax=np.max(np.abs((zz-self.theta*ec)/self.Cp))
        final_q=y[self.qs]
        scale=max(1e-12,np.max(np.abs(wi)),np.max(di),self.length*self.U*self.B**4/4)
        report={
            'status':'SYNTHETIC_FINITE_TIME_COUPLED_MODEL_NOT_AN_EXPERIMENT',
            'cycle_duration':T,'zero_source_voltage_hold':hold,
            'grid_segments':self.n,'actuator_cells':self.cells,'dx':self.dx,
            'pitch':self.ell,'sample_length':self.length,
            'rtol':rtol,'atol':atol,'solver':'scipy.solve_ivp BDF',
            'solver_nfev':nfev,'solver_njev':njev,'solver_nlu':nlu,
            'elapsed_seconds':time.perf_counter()-started,
            'initial_energy':e0,'final_energy':float(en[-1]),
            'maximum_absolute_energy_identity_residual':float(np.max(np.abs(residual))),
            'maximum_scaled_energy_identity_residual':float(np.max(np.abs(residual))/scale),
            **{key:float(val) for key,val in zip(self.integral_names,y[self.is0:])},
            'total_source_work':float(wi[-1]),'total_dissipated_heat':float(di[-1]),
            'peak_strain_magnitude':float(emax),'peak_piezo_capacitor_voltage_magnitude':float(vmax),
            'maximum_spatial_order_parameter_std':float(np.max(np.std(qs,axis=1))),
            'maximum_reference_tracking_rms':float(np.max(np.sqrt(np.mean((qs-targets[:,None])**2,axis=1)))),
            'final_q_mean':float(np.mean(final_q)),'final_q_min':float(np.min(final_q)),
            'final_q_max':float(np.max(final_q)),'target_B':self.B,
            'final_fraction_q_positive':float(np.mean(final_q>0)),
            'final_fraction_above_bare_polar_basin_saddle':float(np.mean(final_q>np.sqrt(self.b/(4*self.c)))),
            'final_rms_q_error':float(np.sqrt(np.mean((final_q-self.B)**2))),
            'final_rms_charge_error':float(np.sqrt(np.mean((y[self.zs]-self.zB)**2))),
            'final_passive_rc_voltage_rms':float(np.sqrt(np.mean(((y[self.zs]-self.theta*(y[self.us][self.right]-y[self.us][self.left])/self.ell)/self.Cp)**2))),
            'final_bias_capacitor_field':float(y[self.hi]),
            'terminal_source_condition':'Both external source voltages zero; internal bias field and piezo voltages relax dynamically.',
            'temperature_noise':'NOT INCLUDED; deterministic persistence is not a lifetime certificate',
            'practical_advantage':'UNKNOWN',
        }
        return report,dict(t=ts,q=qs,u=us,z=zz,h=ys[:,self.hi],energy=en,energy_residual=residual,
                           accumulated=ys[:,self.is0:],reference=targets)

    def parameters(self):
        keys=['C','KE','KD','Cp','theta','alpha','b','bm','c','a','kappa','rho',
              'eta','zeta','Rz','Ch','Rh','u0','U','Ceff','Theta','B','zB','lam']
        return {**{k:float(getattr(self,k)) for k in keys},
                'coupling_squared':(self.KD-self.KE)/self.KD,
                'sufficient_pitch_bound':float(np.pi*np.sqrt(self.kappa/self.lam)),
                'continuum_variance_margin':float(self.kappa*np.pi**2/self.ell**2-self.lam),
                'circulated_gate_work_per_volume':self.U*self.B**4/4,
                'units':'declared dimensionless; not an identified material fit'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--quick',action='store_true')
    args=p.parse_args()
    cases=[('slow',20.,100.,8,2e-7,2e-9),('fast',2.,100.,8,2e-7,2e-9),
           ('adiabatic',100.,100.,8,2e-7,2e-9)]
    if not args.quick:
        cases.extend([('slow_refined',20.,100.,16,7e-8,7e-10),
                      ('fast_refined',2.,100.,16,7e-8,7e-10),
                      ('adiabatic_refined',100.,100.,16,7e-8,7e-10)])
    results=[]
    for name,T,hold,sub,rtol,atol in cases:
        bar=Bar(subdivisions=sub)
        result,data=bar.run(T,hold,rtol,atol)
        result['case']=name
        results.append(result)
        np.savez_compressed(OUT/f'{name}_trajectory.npz',**data)
        (OUT/f'{name}_results.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result),flush=True)
    payload={'model_status':'compatible synthetic continuum/discretized dynamics',
             'parameters':Bar().parameters(),'cases':results,
             'immutable_prior_work':'No conversion, pump/reset, or original completed-package file modified.'}
    (OUT/'coupled_cycle_results.json').write_text(json.dumps(payload,indent=2)+'\n')


if __name__=='__main__':
    main()
