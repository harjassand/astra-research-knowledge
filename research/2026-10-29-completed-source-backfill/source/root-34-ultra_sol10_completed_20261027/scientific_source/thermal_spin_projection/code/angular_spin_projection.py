"""All-state p6 twisted traces and full integer-spin Fourier projection.

This is a numerical preview. No certified trace/angle/roundoff enclosure is
claimed. The direct physical builder is independent of the sol9 cycle code.
The prior accepted first connected input is read-only.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import pathlib,itertools,json,time,math,hashlib,argparse
import numpy as np
import scipy.sparse as ss
import scipy.linalg as la

ROOT=pathlib.Path(__file__).resolve().parents[1]
WORK=ROOT.parents[1]
PRIOR=WORK/'sol9_frontier_20261028/thermal'

def sector_parts(n,mag):
    """H_M(phi)=D0+sqrt6 D1+e^iphi(E0+sqrt6 E1)+h.c.

    D has all open bonds and the closing SzSz term. E raises the LAST
    spin and lowers the FIRST. Every coefficient is integer or sqrt6.
    """
    states=[w for w in itertools.product(range(-2,3),repeat=n)if sum(w)==mag]
    lookup={w:i for i,w in enumerate(states)};rows=[[],[],[],[]];cols=[[],[],[],[]];vals=[[],[],[],[]]
    def insert(kind,row,col,value):
        if value:rows[kind].append(row);cols[kind].append(col);vals[kind].append(value)
    for col,w in enumerate(states):
        diag=sum(w[j]*w[j+1]for j in range(n-1))+w[-1]*w[0]
        insert(0,col,col,diag)
        for edge in range(n-1):
            for step in [-1,1]:
                a=w[edge];b=w[edge+1]
                if not(-2<=a+step<=2 and -2<=b-step<=2):continue
                v=list(w);v[edge]+=step;v[edge+1]-=step;row=lookup[tuple(v)]
                product=(6-a*(a+step))*(6-b*(b-step))//4
                if product==6:insert(1,row,col,1)
                else:
                    coefficient=math.isqrt(product);assert coefficient**2==product
                    insert(0,row,col,coefficient)
        a=w[-1];b=w[0]
        if a<2 and b>-2:
            v=list(w);v[-1]+=1;v[0]-=1;row=lookup[tuple(v)]
            product=(6-a*(a+1))*(6-b*(b-1))//4
            if product==6:insert(3,row,col,1)
            else:
                coefficient=math.isqrt(product);assert coefficient**2==product
                insert(2,row,col,coefficient)
    matrices=[ss.csr_matrix((np.array(vals[k],dtype=np.int64),(rows[k],cols[k])),shape=(len(states),len(states)))for k in range(4)]
    assert (matrices[0]-matrices[0].T).nnz==0 and (matrices[1]-matrices[1].T).nnz==0
    return states,matrices

def build(n=6):
    blocks=[];arrays={};dimensions=[]
    for mag in range(2*n+1):
        states,parts=sector_parts(n,mag);d=len(states);dimensions.append({'M':mag,'dimension':d,'multiplicity':1 if mag==0 else 2})
        if not d:continue
        for label,matrix in zip(['D0','D1','E0','E1'],parts):
            prefix=f'M{mag}_{label}'
            arrays[prefix+'_data']=matrix.data;arrays[prefix+'_indices']=matrix.indices;arrays[prefix+'_indptr']=matrix.indptr
        arrays[f'M{mag}_states']=np.array(states,dtype=np.int8)
        d0,d1,e0,e1=parts
        dmat=(d0+np.sqrt(6)*d1).toarray();emat=(e0+np.sqrt(6)*e1).toarray()
        blocks.append((mag,dmat,emat))
    assert sum(x['dimension']*x['multiplicity']for x in dimensions)==5**n
    np.savez_compressed(ROOT/'results/physical_sector_parts.npz',**arrays)
    return blocks,dimensions

def reference_moments():
    data=json.loads((PRIOR/'results/cycle6_moments_exact_degree192.json').read_text())
    return {r['twist']:list(map(int,r['trace_2H_powers']))for r in data['records']}

def physical_spectra(grid=64):
    start=time.monotonic();blocks,dimensions=build();ref=reference_moments();all_spectra=[];controls=[]
    for k in range(grid//2+1):
        phi=2*np.pi*k/grid;z=np.exp(1j*phi);values=[];hermiticity=0.
        for mag,d,e in blocks:
            h=d+z*e+z.conjugate()*e.T
            hermiticity=max(hermiticity,float(np.max(abs(h-h.conjugate().T))))
            es=la.eigvalsh(h,check_finite=False,overwrite_a=True)
            values.extend(es.tolist()*(1 if mag==0 else 2))
        values=np.array(values);assert len(values)==15625
        assert values.min()>-36-1e-8 and values.max()<24+1e-8
        checks=[]
        for p in range(7):
            expected=(ref['I'][p]+ref['P'][p]+(ref['I'][p]-ref['P'][p])*np.cos(phi))/(2*2**p)
            measured=float(np.sum(values**p))
            checks.append({'power_H':p,'expected':expected,'observed':measured,
                           'scaled_error':abs(measured-expected)/max(1.,abs(expected))})
        all_spectra.append(values)
        controls.append({'angle_index':k,'angle_float':phi,'Hermiticity_max_entry_error':hermiticity,'low_moment_controls':checks})
        print('angle',k,'of',grid//2,'seconds',round(time.monotonic()-start,3),flush=True)
        np.savez_compressed(ROOT/'results/angular_spectra_partial.npz',eigenvalues=np.array(all_spectra),grid=np.array(grid),completed_half_angles=np.array(k+1))
    spectral=np.array(all_spectra)
    np.savez_compressed(ROOT/f'results/angular_spectra_grid{grid}.npz',eigenvalues=spectral,grid=np.array(grid))
    return spectral,dimensions,controls,time.monotonic()-start

def a5_vector_multiplicity(spin):
    def character(phi):return 1+2*sum(np.cos(m*phi)for m in range(1,spin+1))
    golden=(1+np.sqrt(5))/2;conjugate=(1-np.sqrt(5))/2
    value=(3*(2*spin+1)-15*character(np.pi)+12*golden*character(2*np.pi/5)+12*conjugate*character(4*np.pi/5))/60
    integer=round(value);assert abs(integer-value)<1e-8 and integer>=0
    return integer

def project(eigenvalues,grid,beta,samples):
    assert grid%samples==0;stride=grid//samples
    half=np.array([np.sum(np.exp(-beta*eigenvalues[k*stride]))/15625 for k in range(samples//2+1)])
    values=np.r_[half,half[-2:0:-1]];assert len(values)==samples
    fourier=np.fft.fft(values)/samples
    spins=fourier.real[:-1]-fourier.real[1:]
    return values,fourier,spins

def preview(spectral,grid):
    prior=json.loads((PRIOR/'results/a5_preview.json').read_text());out=[]
    for beta in [1.5,3.,6.]:
        old=next(r for r in prior['rows']if r['beta']==beta);theta=old['scalar_theta'];M=old['moments']['6']['3']
        for samples in [32,64]:
            if grid%samples:continue
            values,fourier,spins=project(spectral,grid,beta,samples)
            m1=float(spins[1]);complement=M-m1
            assert m1>0 and complement>0
            r1=m1**(1/6);rc=complement**(1/6)
            tau=sum(dim*old['radius_over_theta'][ir]**256 for ir,dim in [('1',1),('3prime',3),('4',4),('5',5)])
            tau+=3*((r1/theta)**256+(rc/theta)**256)
            count=min(samples//2-1,24)
            reconstruct=sum(a5_vector_multiplicity(s)*float(spins[s])for s in range(count))
            item={'beta':beta,'angle_samples':samples,'scalar_theta':theta,
                  'physical_trace_at_zero_normalized':float(values[0]),
                  'Fourier_coefficients_real':fourier.real[:samples//2+1].tolist(),
                  'Fourier_max_imaginary_abs':float(np.max(abs(fourier.imag))),
                  'spin_list_sixth_moments_preview':spins[:samples//2-1].tolist(),
                  'spin1_M6':m1,'A5_M3_6':M,'A5_triplet_complement_M6':complement,
                  'fraction_A5_triplet_mass_outside_spin1':complement/M,
                  'spin1_radius':r1,'spin1_radius_over_scalar_lower':r1/theta,
                  'complement_radius':rc,'complement_radius_over_scalar_lower':rc/theta,
                  'all_mode_relative_loop_tail_proposal':tau,
                  'A5_M3_reconstructed_from_spin_prefix':reconstruct,
                  'spin_prefix_reconstruction_relative_difference':(reconstruct-M)/M,
                  'scope':'NUMERICAL_FULL_SPIN_PROJECTION_ONLY_NO_CERTIFIED_NEXT_INPUT'}
            out.append(item)
            print('projection',beta,samples,'spin1 ratio',r1/theta,'complement ratio',rc/theta,'loop',tau,flush=True)
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--grid',type=int,default=64);args=parser.parse_args()
    assert args.grid>=64 and args.grid%64==0
    spectral,dimensions,controls,seconds=physical_spectra(args.grid);rows=preview(spectral,args.grid)
    source_paths=[PRIOR/'results/a5_preview.json',PRIOR/'results/cycle6_moments_exact_degree192.json']
    result={'status':'FULL_SPIN_FOURIER_NUMERICAL_PREVIEW','grid':args.grid,'rows':rows,
            'sector_dimensions':dimensions,'controls':controls,'spectral_acquisition_seconds':seconds,
            'physical_dimension_every_angle':15625,
            'input_receipts':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in source_paths],
            'new_exact_or_cyclotomic_acquisition':False,'next_connected_input_acquired':False,
            'arithmetic_scope':'float64 all-state Hermitian eigvalsh and uniform angular DFT; no verified eigenpair/angle/roundoff enclosure.'}
    (ROOT/'results/spin_projection_preview.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
