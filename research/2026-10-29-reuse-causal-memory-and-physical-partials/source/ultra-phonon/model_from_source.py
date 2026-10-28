"""Exact symmetry-fitted harmonic INTERPOLANT of the public Si example.
This does not identify a unique infinite-crystal Hessian from a finite supercell.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,itertools,json,re,time,xml.etree.ElementTree as ET
import numpy as np
import sympy as sy
BASE=Path(__file__).parent

def main():
    start=time.perf_counter();c=BASE/'source_cache'
    y=(c/'phonopy_disp.yaml').read_text()
    section=y.split('supercell:\n',1)[1].split('displacements:',1)[0]
    coords=[sy.Matrix([sy.Rational(z.strip()) for z in s.split(',')]) for s in re.findall(r'coordinates:\s*\[([^]]+)\]',section)]
    assert len(coords)==16
    pos=[2*v for v in coords];basis=[pos[0],pos[8]]
    def key(v):return tuple(x%2 for x in v)
    keys={key(v):i for i,v in enumerate(pos)}
    root=ET.parse(c/'vasprun.xml').getroot();vf=root.findall('.//varray[@name="forces"]')
    assert len(vf)==1
    forces=[sy.Matrix([sy.Rational(z) for z in v.text.split()]) for v in vf[0]]
    assert len(forces)==16
    # Anchor the YAML key: create_displacements is a different configuration key.
    s=y.split('\ndisplacements:\n',1)[1];disp=sy.Matrix([sy.Rational(z.strip()) for z in re.search(r'\[([^]]+)\]',s).group(1).split(',')])
    assert sy.Rational(999,10**7)<(disp.T*disp)[0]<sy.Rational(1001,10**7)
    P=sy.Matrix([[0,1,1],[1,0,1],[1,1,0]]);rot=[]
    for perm in itertools.permutations(range(3)):
      for signs in itertools.product([-1,1],repeat=3):
        Q=sy.zeros(3)
        for i,j in enumerate(perm):Q[i,j]=signs[i]
        U=P.inv()*Q*P
        mapped=[key(basis[0]+U*(v-basis[0])) for v in pos]
        if all(v in keys for v in mapped):rot.append((Q,[keys[v] for v in mapped]))
    assert len(rot)==24
    K=[sy.zeros(3) for _ in pos];gram=sy.zeros(3)
    for Q,mapping in rot:
        d=Q*disp;gram+=d*d.T
        for j,idx in enumerate(mapping):K[idx]-=(Q*forces[j])*d.T
    K=[v*gram.inv() for v in K]
    invmap=[keys[key(basis[0]+basis[1]-v)] for v in pos]
    KB=[None]*16
    for i,j in enumerate(invmap):KB[j]=K[i]
    raw={};multiplicity=[]
    for a,column in enumerate([K,KB]):
      for i,v in enumerate(pos):
        b=0 if i<8 else 1;R=v-basis[b];assert all(z.q==1 for z in R)
        # Finite-range minimum-image interpolation, an explicit model choice.
        choices=[];best=None
        for z in itertools.product(range(-2,3),repeat=3):
            shift=R+2*sy.Matrix(z);d=P*(basis[b]+shift-basis[a]);norm=(d.T*d)[0]
            if best is None or norm<best:best=norm;choices=[shift]
            elif norm==best:choices.append(shift)
        multiplicity.append(len(choices))
        for shift in choices:
            r=tuple(-int(z) for z in shift)
            raw.setdefault(r,sy.zeros(6));raw[r][3*b:3*b+3,3*a:3*a+3]+=column[i]/len(choices)
    support=set(raw)|{tuple(-v for v in r) for r in raw};zero=sy.zeros(6)
    coeff={r:(raw.get(r,zero)+raw.get(tuple(-v for v in r),zero).T)/2 for r in support}
    repairs=[]
    for a in range(2):
        G=sum((A[3*a:3*a+3,3*b:3*b+3] for A in coeff.values() for b in range(2)),sy.zeros(3))
        assert G==G.T
        repairs.append(G)
        coeff[(0,0,0)][3*a:3*a+3,3*a:3*a+3]-=G
    T=sy.Matrix.vstack(sy.eye(3),sy.eye(3));D0=sum(coeff.values(),sy.zeros(6))
    assert D0*T==sy.zeros(6,3)
    assert all(A==coeff[tuple(-v for v in r)].T for r,A in coeff.items())
    assert all(T.T*sum((r[j]*A for r,A in coeff.items()),sy.zeros(6))*T==sy.zeros(3) for j in range(3))
    rows=[]
    for r,A in sorted(coeff.items()):
        if A==zero:continue
        rows.append(dict(R=r,matrix=[[str(v) for v in row] for row in A.tolist()]))
    data=dict(status='EXACT_RATIONAL_FINITE_RANGE_SYMMETRY_FITTED_MODEL_NOT_PHYSICAL_HESSIAN_CERTIFICATE',
        source_repository_commit='ea3c269be8502f4fde4db31870725d8dcb3f27d3',atoms_per_primitive_cell=2,supercell_atoms=16,
        displacement=[str(v) for v in disp],site_symmetries=len(rot),cell_gauge=True,masses_omitted_for_stability=True,
        minimum_image_multiplicities=sorted(set(multiplicity)),support_size=len(rows),
        acoustic_sum_rule_repair=[[[str(v) for v in row] for row in G.tolist()] for G in repairs],
        coefficients=rows,source_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in c.iterdir() if f.is_file()},
        seconds=time.perf_counter()-start,
        unpaid=['finite-displacement truncation error','supercell aliases and unobserved range','DFT and specimen model discrepancy','physical force-constant uncertainty'])
    (BASE/'MODEL.json').write_text(json.dumps(data,indent=2)+'\n')
    numeric=[(np.array(r['R']),np.array(r['matrix'],dtype=str).astype(object)) for r in rows]
    cnum=np.array([np.array(A,dtype=float) for A in coeff.values()]);rr=np.array(list(coeff))
    rng=np.random.default_rng(20261029);q=rng.uniform(-np.pi,np.pi,(4096,3))
    D=np.einsum('pr,rij->pij',np.exp(1j*q@rr.T),cnum)
    eig=np.linalg.eigvalsh(D)
    out=dict(status=data['status'],support_size=len(rows),site_symmetries=24,seconds=data['seconds'],
        random_preview_points=4096,smallest_preview_eigenvalue=float(eig[:,0].min()),max_input_ASR_repair=float(max(abs(v) for G in repairs for v in G)),
        exact_acoustic_zero=True,exact_linear_acoustic_block_zero=True,coefficient_R_max=np.max(abs(rr),axis=0).tolist())
    (BASE/'MODEL_PREVIEW.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
