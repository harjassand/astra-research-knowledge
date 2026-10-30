"""Exact receiver for shared covariance gluing at all four amplitudes.

Only Python's standard library is required. The receiver rebuilds actual
Fourier moments, all cubic identities, both covariance exchanges, and the
24 positive remainder identities. No numerical optimization is replayed.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import permutations
import importlib.util,json,time,contextlib,io
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('resonant_core',HERE.parent/'resonant_gluing/receive.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
m,b,dot,quadratic,outer,compose,congruence=base.m,base.b,base.dot,base.quadratic,base.outer,base.compose,base.congruence

def psd(H):
    H=[list(row) for row in H];assert H==list(map(list,zip(*H)))
    for k in range(len(H)):
        p=H[k][k];assert p>=0
        if not p:
            assert all(H[k][j]==0 for j in range(k,len(H)));continue
        for i in range(k+1,len(H)):
            for j in range(i,len(H)):
                H[i][j]-=H[i][k]*H[k][j]/p;H[j][i]=H[i][j]
    return True

def network():
    frequencies=[(1,0),(0,1),(1,1),(2,1)]
    phases=[(0,0),(0,0),(-1,0),(-1,-1)]
    original=[[R(1),R(0),R(0),R(0)],[R(0),R(0),R(0),R(1)],[R(1)]*4,[R(4),R(2),R(2),R(1)]]
    images=[{} for _ in range(4)]
    for j,(freq,phase,ray) in enumerate(zip(frequencies,phases,original)):
        amp=tuple(int(i==j) for i in range(4))
        for component in range(4):
            for sign in (-1,1):
                ee=(sign*freq[0],sign*freq[1],sign*phase[0],sign*phase[1])+amp
                images[component]=b.add(images[component],{ee:ray[component]/2})
    return original,images

def moments(poly,images):
    return {ee[2:]:co for ee,co in compose(poly,images,8).items() if ee[:2]==(0,0)}

def from_matrix(mat):
    ans={}
    for i in range(4):
        key=(0,0)+tuple(4*int(j==i) for j in range(4));ans[key]=mat[i][i]
    for i in range(4):
        for j in range(i+1,4):
            key=(0,0)+tuple(2*int(k in (i,j)) for k in range(4));ans[key]=2*mat[i][j]
    return {e:c for e,c in ans.items() if c}

def quartic_data(poly,images,original):
    HF=[[b.diff(b.diff(poly,i),j) for j in range(4)] for i in range(4)]
    H=[[[b.evaluate(p,r) for p in row] for row in HF] for r in original]
    FM=[[R(0) for _ in range(4)] for _ in range(4)]
    for i,r in enumerate(original):FM[i][i]=R(3,8)*b.evaluate(poly,r)
    for i in range(4):
        for j in range(i+1,4):FM[i][j]=FM[j][i]=quadratic(H[i],original[j])/16
    moment=moments(poly,images);ans=from_matrix(FM)
    pplus=(2,1,0,1);pminus=(0,1,2,1)
    u=2*moment.get((1,1)+pplus,R(0));v=2*moment.get((1,-1)+pminus,R(0))
    for phase,powers,co in (((1,1),pplus,u),((1,-1),pminus,v)):
        for sign in (-1,1):
            if co:ans[tuple(sign*x for x in phase)+powers]=co/2
    assert moment==ans
    return FM,u,v

def setup():
    F,_,T=m.acquired();original,images=network()
    gd=json.loads((HERE.parent/'graded_stabilization/certificate.json').read_text())
    powers=gd['cubic_powers'];basis=[list(map(R,v)) for v in gd['cubic_kernel_basis']]
    targets=[]
    for pw in powers:
        moment=moments({tuple(pw):R(1)},images);row=[];ans={}
        for phase,amps in (((1,0),(1,1,1,0)),((0,1),(1,0,1,1))):
            co=2*moment.get(phase+amps,R(0));row.append(co)
            for sign in (-1,1):
                if co:ans[tuple(sign*x for x in phase)+amps]=co/2
        assert moment==ans;targets.append(row)
    aux1=[[R(1),t,t,t*t] for t in (R(-1),R(1,2),R(2))]
    aux2=[[(1+t)**2,t*(1+t),t*(1+t),t*t] for t in (R(-1),R(1,2),R(2))]
    rays=[original[:3]+aux1+[original[3]],[original[i] for i in (0,2,3)]+aux2+[original[1]]]
    HF=[[b.diff(b.diff(F,i),j) for j in range(4)] for i in range(4)]
    H=[[[[b.evaluate(p,r) for p in row] for row in HF] for r in rs] for rs in rays]
    FM,u,v=quartic_data(F,images,original);RM,ru,rv=quartic_data(b.mul(T,T),images,original)
    TU=[row[:] for row in RM]
    for i,co in ((0,abs(ru)),(2,abs(rv))):
        for j in (1,3):TU[i][j]+=co/4;TU[j][i]+=co/4
    return {'F':F,'T':T,'HF':HF,'original':original,'rays':rays,'H':H,'powers':powers,'basis':basis,'targets':targets,'FM':FM,'u':u,'v':v,'RM':RM,'radial_u':ru,'radial_v':rv,'TU':TU,'eta':[R(1,9),R(16,9),R(1,9)]}

def features(data,base_index):
    ans=[]
    for r in data['rays'][base_index]:
        for j in range(4):ans.append([b.evaluate(b.diff({tuple(pw):R(1)},j),r) for pw in data['powers']])
    return [[dot(v,col) for col in ans] for v in data['basis']]

def chart_matrix(order):
    ans=[[R(0) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(i+1):ans[order[i]][j]=R(1)
    return ans

def subtract_pair(D,pair,co):
    i,j=pair;D[i][j]-=co/2;D[j][i]-=co/2

def residual(data,case,profiles):
    order=case['order'];base_index=case['base'];minimum=case['minimum']
    indices=[(0,1,2),(0,2,3)][base_index]
    tau,eps=R(case['tau']),R(case['epsilon']);assert tau>0 and 0<eps<R(1,2)
    assert base_index==(0 if order.index(1)>order.index(3) else 1)
    assert minimum==next(i for i in order if i in indices)
    D=[row[:] for row in data['FM']]
    for i,co,lam in zip((0,2),(abs(data['u']),abs(data['v'])),map(R,case['young_parameters'])):
        assert lam>0
        subtract_pair(D,(i,1),co*lam/2);subtract_pair(D,(i,3),co/(2*lam))
    energies=[]
    for e,X in enumerate(profiles):
        ens=[quadratic(H,x) for H,x in zip(data['H'][base_index],X)];assert all(v>=0 for v in ens);energies.append(ens)
        gamma=1+tau if e==base_index else 1+1/tau
        target_indices=[(0,1,2),(0,2,3)][e]
        for i,global_i in enumerate(indices):
            pair=[z for z in target_indices if z!=global_i] if global_i in target_indices else [0,2]
            subtract_pair(D,pair,gamma*ens[i]/(2*(R(1,2)-eps)))
        pair=[z for z in target_indices if z!=minimum] if minimum in target_indices else [0,2]
        newenergy=sum(ens[i+3]/eta for i,eta in enumerate(data['eta']))
        subtract_pair(D,pair,gamma*newenergy/(2*eps))
        subtract_pair(D,(0,2),ens[6])
    gap=R(1,32)
    return [[D[i][j]-gap*data['TU'][i][j] for j in range(4)] for i in range(4)],energies

def main():
    start=time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):base.main()
    data=setup();cert=json.loads((HERE/'certificate.json').read_text())
    assert cert['uniform_single_block_L4_gap']=='1/32'
    assert [list(map(R,row)) for row in cert['quartic_pair_matrix']]==data['FM']
    assert list(map(R,cert['quartet_coefficients']))==[data['u'],data['v']]
    assert [list(map(R,row)) for row in cert['cubic_targets']]==data['targets']
    assert [list(map(R,row)) for row in cert['radial_upper_matrix']]==data['TU']
    assert [data['radial_u'],data['radial_v']]==[R(1,2),R(11)]
    for base_index,rs in enumerate(data['rays']):
        for r,H in zip(rs,data['H'][base_index]):assert r[0]*r[3]-r[1]*r[2]==0 and psd(H)
        # A SINGLE covariance exchange funds both independent cubic targets.
        assert [[sum(data['eta'][k]*rs[k+3][i]*rs[k+3][j] for k in range(3)) for j in range(4)] for i in range(4)]==[[sum(rs[k][i]*rs[k][j] for k in range(3)) for j in range(4)] for i in range(4)]
        assert b.rank([row[:24] for row in features(data,base_index)])==12
    seen=set()
    for case in cert['charts']:
        order=case['order'];assert tuple(order) not in seen;seen.add(tuple(order));base_index=case['base']
        profiles=[[[R(v) for v in row] for row in X] for X in case['sources']]
        L=features(data,base_index)
        for e,X in enumerate(profiles):
            assert len(X)==7 and all(len(row)==4 for row in X)
            xx=[v for row in X for v in row];target=[dot(v,[row[e] for row in data['targets']]) for v in data['basis']]
            assert all(dot(row,xx)==co for row,co in zip(L,target))
            if e==base_index:assert X[6]==[0,0,0,0]
        D,energies=residual(data,case,profiles);DC=congruence(D,chart_matrix(order))
        P=[list(map(R,row)) for row in case['positive_matrix']];N=[list(map(R,row)) for row in case['nonnegative_matrix']]
        assert P==list(map(list,zip(*P))) and N==list(map(list,zip(*N))) and all(v>=0 for row in N for v in row)
        b.pd(P);assert DC==[[P[i][j]+N[i][j] for j in range(4)] for i in range(4)]
    assert seen==set(permutations(range(4)))
    # The same cross-block estimate applies to arbitrary relative amplitudes.
    spatial=[[R(1),R(0)],[R(0),R(1)],[R(1),R(1)],[R(2),R(1)]];eta=R(3,50)
    for n in spatial:
        H=[[b.evaluate(p,[*n,R(0),R(0)]) for p in row] for row in data['HF']]
        for k in spatial:
            vv=[[k[0],k[1],0,0],[0,0,k[0],k[1]]];den=dot(n,n)*dot(k,k)
            mat=[[quadratic(H,vv[i],vv[j])/den-(eta if i==j else 0) for j in range(2)] for i in range(2)];b.pd(mat)
    result={'prior_triad_proof_replayed':True,'actual_compatible_amplitude_phase_moments_reconstructed':True,'shared_modes':2,'covariance_exchanges_verified':2,'full_cubic_space_dimension':12,'positive_order_cone_certificates':24,'independent_real_relative_amplitudes':4,'all_relative_phases_means_and_common_output_rotations':True,'single_block_L4_gap':'1/32','separated_mixed_block_L4_gap':'1/200','cross_block_positive_matrices':16,'original_full_28_dimensional_face_QC':'NOT_RESOLVED','seconds':time.perf_counter()-start,'scope':'Shared-resource gluing for the stated two-resonance network and arbitrary finite nine-adically separated unions. No unrestricted resonance-network or full-face conclusion.'}
    (HERE/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
