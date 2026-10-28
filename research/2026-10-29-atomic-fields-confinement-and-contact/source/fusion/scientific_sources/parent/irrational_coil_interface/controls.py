"""Independent segment-field and source-coordinate controls, modest runtime."""
from pathlib import Path
import json,time
import construct as c
import numpy as np
from scipy.signal import resample
s=c.s
ROOT=Path(__file__).resolve().parent


def segment_field(targets,nodes):
    # Increasing-theta polygon orientation uses negative current. This exact
    # finite-segment formula does not reuse construct.coil_field or tangents.
    M,N=nodes.shape[:2]
    starts=nodes.reshape(-1,3)
    ends=np.roll(nodes,-1,axis=0).reshape(-1,3)
    current=-(4*np.pi/(s.KAPPA*s.KMOD))/N
    out=[]
    for target in targets:
        r1=target-starts;r2=target-ends
        a=np.linalg.norm(r1,axis=-1);b=np.linalg.norm(r2,axis=-1)
        dot=np.einsum('ij,ij->i',r1,r2)
        value=np.cross(r1,r2)*((1/a+1/b)/(a*b+dot))[:,None]
        out.append(value.sum(axis=0)*current/(4*np.pi))
    return np.array(out)


def main():
    start=time.monotonic()
    data=np.load(ROOT/'finite_coils.npz')
    indices=np.arange(0,len(data['target_coordinates']),11)
    q=data['target_coordinates'][indices];exact=data['exact_field'][indices]
    norm=np.linalg.norm(exact,axis=-1)
    targets=s.embedding(q);reference=data['finite_field'][indices]
    rows=[]
    for M in (512,1024,2048):
        nodes=resample(data['nodes'],M,axis=0)
        b=segment_field(targets,nodes)
        rows.append({'polygon_nodes_per_coil':M,
          'max_relative_difference_from_smooth_quadrature':float(np.max(np.linalg.norm(b-reference,axis=-1)/norm)),
          'max_sample_relative_error_to_source':float(np.max(np.linalg.norm(b-exact,axis=-1)/norm))})
    # Independent analytical gradient pullback: Phi_u=Im sn(z1),
    # Phi_v=Im sn(z2), Phi_zeta=Re(sn(z1)+sn(z2)).
    u,v,z=q.T
    p1,_,_=s.complex_jacobi(s.K+s.KAPPA*(u-s.U0)+1j*s.KAPPA*z)
    p2,_,_=s.complex_jacobi(s.K+s.KAPPA*v+1j*(s.KP+s.KAPPA*z))
    partial=np.stack((p1.imag,p2.imag,(p1+p2).real),axis=-1)
    pullback=np.einsum('...ji,...j->...i',s.jacobian(q),exact)
    pullback_error=float(np.max(abs(pullback-partial)))
    # A toroidal circulation evaluated on the axis, independently of loops.
    z=2*np.pi*np.arange(4096)/4096
    axis=np.stack((np.full(len(z),s.U0),np.zeros(len(z)),z),axis=-1)
    vals=s.data(axis)
    measured=2*np.pi*np.einsum('ij,ij->i',vals['B'],vals['J'][:,:,2]).mean()
    predicted=4*np.pi/(s.KAPPA*s.KMOD)
    assert abs(measured-predicted)<1e-10
    assert pullback_error<1e-10
    # The same Fourier curves, not new optimized shapes, are represented by
    # successively finer polygons. Polygon error is finite shape error.
    out={'status':'INDEPENDENT_FINITE_SEGMENT_CONTROL_PASS',
      'control_target_count':len(indices),'rows':rows,
      'source_gradient_pullback_max_absolute_error':pullback_error,
      'circulation_direct_integral':float(measured),'circulation_formula':float(predicted),
      'seconds':time.monotonic()-start,
      'scope':'Independent exact-segment evaluation on refined polygons of the same sampled Fourier curves; numerical convergence, not uniform/certified quadrature or engineering.'}
    (ROOT/'CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
