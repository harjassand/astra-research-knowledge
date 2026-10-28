#!/usr/bin/env python3
"""Replayable independent local consistency checks for the two source fields.

These checks validate implementation identities and numerical differentiation;
they do not certify a complete volume, orbit error, or physical performance.
"""
from pathlib import Path
import json
import numpy as np
import lopez_native as l
import sengupta_paraboloid as s
import mpmath as mp
ROOT=Path(__file__).resolve().parent


def lopez():
    rng=np.random.default_rng(261029921)
    r=np.sqrt(rng.uniform(0,.8**2,32));theta=rng.uniform(0,2*np.pi,32)
    q=np.column_stack((.15+r*np.cos(theta)/30,.02+r*np.sin(theta)/10,rng.uniform(0,2*np.pi,32)))
    J=l.jacobian(*q.T);B,dB=l.field_labels(*q.T,gradient=True);h=l.h_analytic(*q.T)
    coordinate=J[:,:,2]/h[:,None]**2
    inverse=np.linalg.inv(J);clebsch=np.cross(inverse[:,0],inverse[:,1])
    derivative=[];x=l.embedding(*q.T);z=np.sqrt(q[:,0])*np.exp(1j*q[:,2])
    for i in range(3):
        e=np.zeros(3);e[i]=1e-6
        zp,_=l.root_continue(x+e,z);zm,_=l.root_continue(x-e,z)
        derivative.append((l.field_known_root(x+e,zp)-l.field_known_root(x-e,zm))/(2e-6))
    fd=np.stack(derivative,axis=-1)
    v=rng.uniform(-.9,.9,len(q));mu=rng.uniform(0,.05,len(q))
    qa,va=l.gc_rhs(q,v,mu,.004);qb,vb=l.gc_label_rhs(q,v,mu,.004)
    return {'point_count':len(q),'maximum_relative_B_chart_cartesian_difference':float(np.max(np.linalg.norm(B-coordinate,axis=1)/np.linalg.norm(B,axis=1))),
        'maximum_h_chart_formula_difference':float(np.max(abs(h-np.linalg.norm(J[:,:,2],axis=1)))),
        'maximum_relative_clebsch_difference':float(np.max(np.linalg.norm(clebsch-2*q[:,0,None]*B,axis=1)/np.linalg.norm(clebsch,axis=1))),
        'maximum_relative_cartesian_gradient_FD_difference':float(np.max(np.linalg.norm(fd-dB,axis=(1,2))/np.linalg.norm(dB,axis=(1,2)))),
        'maximum_divergence_residual':float(np.max(abs(np.trace(dB,axis1=1,axis2=2)))),
        'maximum_curl_jacobian_antisymmetry':float(np.max(abs(dB-np.swapaxes(dB,-1,-2)))),
        'maximum_label_GC_vs_Cartesian_GC_difference':float(abs(qa-qb).max()),'maximum_mirror_force_difference':float(abs(va-vb).max())}


def sengupta():
    rng=np.random.default_rng(147);q=np.column_stack((s.U0+rng.uniform(-.1,.1,20),rng.uniform(-.04,.04,20),rng.uniform(0,2*np.pi,20)))
    mp.mp.dps=40;errs=[]
    for u,v,z in q:
        for zz in [s.K+s.KAPPA*(u-s.U0)+1j*s.KAPPA*z,s.K+s.KAPPA*v+1j*(s.KP+s.KAPPA*z)]:
            for name,val in zip(['sn','cn','dn'],s.complex_jacobi(zz)):
                exact=complex(mp.ellipfun(name,complex(zz),s.M));errs.append(abs(val-exact)/max(1,abs(exact)))
    a=s.data(q,True);J=a['J'];u,v,z=q.T;P=np.cosh(u)*np.cosh(v);E=np.sinh(u)*np.sinh(v)-np.sin(2*z);D=P*P-E*E
    metric=np.zeros((len(q),3,3));metric[:,0,0]=metric[:,1,1]=P*P;metric[:,0,1]=metric[:,1,0]=P*E;metric[:,2,2]=D
    partials=[]
    for i in range(3):
        d=np.zeros(3);d[i]=1e-6
        partials.append((s.data(q+d)['strength']-s.data(q-d)['strength'])/(2e-6))
    fd=np.linalg.solve(np.swapaxes(J,-1,-2),np.stack(partials,axis=-1)[...,None])[...,0]
    psip=s.label_partials(q);pdot=np.einsum('ij,ij->i',psip,a['contravariant'])
    axis=np.column_stack((np.full(101,s.U0),np.zeros(101),np.linspace(0,2*np.pi,101)))
    return {'point_count':len(q),'M':s.M,'K':s.K,'KP':s.KP,'KAPPA':s.KAPPA,'U0':s.U0,'PSI0':s.PSI0,
        'maximum_relative_complex_Jacobi_difference_vs_mpmath40':float(max(errs)),
        'maximum_metric_identity_difference':float(abs(np.einsum('...ji,...jk->...ik',J,J)-metric).max()),
        'maximum_relative_strength_gradient_FD_difference':float(np.max(np.linalg.norm(fd-a['grad_strength'],axis=1)/np.linalg.norm(a['grad_strength'],axis=1))),
        'maximum_absolute_analytic_B_dot_grad_psi':float(abs(pdot).max()),
        'maximum_relative_analytic_label_invariance_residual':float(np.max(abs(pdot)/(np.linalg.norm(psip,axis=1)*np.linalg.norm(a['contravariant'],axis=1)))),
        'maximum_axis_label_difference':float(abs(s.surface_label(axis)-s.PSI0).max()),
        'maximum_strength_formula_difference':float(abs(np.linalg.norm(a['B'],axis=1)-a['strength']).max()),
        'all_checked_points_regular':bool(s.regular(q).all())}


def main():
    result={'status':'FINITE_IMPLEMENTATION_CONSISTENCY_CHECKS','lopez':lopez(),'sengupta':sengupta(),
            'scope':'Random seed and point counts declared in this verifier. Numerical identity checks, not directed enclosures; only verify_passing_action.py supplies a directed volume enclosure.'}
    assert result['lopez']['maximum_relative_B_chart_cartesian_difference']<1e-12
    assert result['lopez']['maximum_relative_cartesian_gradient_FD_difference']<1e-6
    assert result['lopez']['maximum_label_GC_vs_Cartesian_GC_difference']<1e-10
    assert result['sengupta']['maximum_relative_complex_Jacobi_difference_vs_mpmath40']<1e-11
    assert result['sengupta']['maximum_relative_strength_gradient_FD_difference']<1e-6
    assert result['sengupta']['maximum_relative_analytic_label_invariance_residual']<1e-10
    (ROOT/'verification_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))


if __name__=='__main__':main()
