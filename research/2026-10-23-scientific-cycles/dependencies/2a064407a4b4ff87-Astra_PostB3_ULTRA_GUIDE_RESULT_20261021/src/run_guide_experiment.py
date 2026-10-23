"""One frozen guide-distinct experiment. No closed cell-half diagnostic.
Actual input identities, design eligibility and source-only fitting enforced.
"""
import argparse,hashlib,json,os,resource,sys,time,datetime
from pathlib import Path
import h5py,numpy as np
from scipy import sparse,stats
from map_design import column
ROOT=Path(__file__).resolve().parents[1]
BASE='5da0485aed81b23bda57b4a7b4510a394682d54911416db89b4846ff6dd34732'
LAMBDAS=np.array([.01,.1,1.,10.,100.]);UPPER=np.log(10001.)

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def scalarize(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    raise TypeError(str(type(x)))
def guard(x,scale):return np.clip(x,0,UPPER if scale=='log' else np.inf)
def normrows(x):return np.einsum('ij,ij->i',x,x)

def cell_norms(x):
    out=np.empty(x.shape[0],dtype=np.float64)
    for start in range(0,x.shape[0],256):
        stop=min(start+256,x.shape[0]);a,b=x.indptr[start],x.indptr[stop]
        squared=x.data[a:b].astype(np.float64)**2
        out[start:stop]=np.add.reduceat(np.r_[squared,0.],x.indptr[start:stop]-a)
    return out

class Data:
    def __init__(self,path,design):
        start=time.perf_counter();require(digest(path)==BASE,'unexpected scientific input')
        with h5py.File(path) as f:
            self.obs={k:column(f['obs'],k) for k in ['CRISPRcas13_Array','Guide.Class','10X_lane','HTO','cell_barcode']}
            self.genes=column(f['var'],'gene_symbol')
            shape=tuple(map(int,f['X'].attrs['shape']));data=f['X/data'][:];indices=f['X/indices'][:];indptr=f['X/indptr'][:]
        require(shape==(30707,21052),'wrong matrix shape');require(np.all(np.isfinite(data)) and np.all(data>=0) and np.all(data==np.floor(data)),'X not finite raw counts')
        require(data.max()<2**24,'float32 count exactness would be lost')
        self.x=sparse.csr_matrix((data.astype(np.float32,copy=False),indices,indptr),shape=shape,copy=False);del data
        self.lib=np.asarray(self.x.sum(axis=1,dtype=np.float64)).ravel();require(np.all(self.lib>0),'zero library')
        self.arrays=sorted(set(self.obs['CRISPRcas13_Array']));self.ai={a:i for i,a in enumerate(self.arrays)}
        self.arm=np.array([self.ai[a] for a in self.obs['CRISPRcas13_Array']],dtype=np.int32);self.na=len(self.arrays);self.nc=shape[0];self.ng=shape[1]
        self.cells=[np.flatnonzero(self.arm==h) for h in range(self.na)];self.n=np.array([len(a) for a in self.cells],dtype=float)
        self.reference=np.array([c in ('Single','NT') for c in self.obs['Guide.Class']]);self.refarms=np.array([bool(np.all(self.reference[a])) for a in self.cells]);require(all(np.all(self.reference[a]) or np.all(~self.reference[a]) for a in self.cells),'mixed reference arm')
        levels=[sorted(set(self.obs[k])) for k in ('10X_lane','HTO')];self.levels=levels;self.z=np.zeros((self.nc,sum(map(len,levels))),dtype=np.float64)
        offset=0
        for key,lev in zip(('10X_lane','HTO'),levels):
            lookup={v:i for i,v in enumerate(lev)};self.z[np.arange(self.nc),offset+np.array([lookup[v] for v in self.obs[key]])]=1;offset+=len(lev)
        logdata=self.x.data.copy();self.log=sparse.csr_matrix((logdata,self.x.indices,self.x.indptr),shape=shape,copy=False)
        for lo in range(0,self.nc,256):
            hi=min(lo+256,self.nc);a,b=self.x.indptr[lo],self.x.indptr[hi]
            factor=np.repeat((10000/self.lib[lo:hi]).astype(np.float32),np.diff(self.x.indptr[lo:hi+1]));logdata[a:b]*=factor;np.log1p(logdata[a:b],out=logdata[a:b])
        self.log=self.log.astype(np.float64,copy=False) if False else self.log
        self.z0={'log':self.z[self.reference].mean(0),'rate':np.average(self.z[self.reference],axis=0,weights=self.lib[self.reference])}
        fam=[a for a in design['families'] if a['eligible']];self.fam=fam;self.N=len(fam);self.pairs=[a['pair'] for a in fam]
        self.idx=np.array([[self.ai[a] for a in f['arms']] for f in fam],dtype=np.int32);self.c=self.ai[design['matching_control']]
        targets=sorted(set([f['a'] for f in fam]+[f['b'] for f in fam]));ti={v:i for i,v in enumerate(targets)};self.inc=np.zeros((self.N,len(targets)))
        for i,f in enumerate(fam):self.inc[i,ti[f['a']]]=1;self.inc[i,ti[f['b']]]=1
        self.targets=targets;self.hats=[self.ridge_hats(self.n[self.idx[:,d]]) for d in (0,1)]
        self.point,self.raw,self.tech=self.summaries(np.ones(self.nc))
        self.noise=self.noise_traces();self.load_s=time.perf_counter()-start
    def ridge_hats(self,w):
        w=w/w.mean();sw=np.sqrt(w);mean=np.average(self.inc,axis=0,weights=w);z=self.inc-mean;scale=np.sqrt(np.sum(w[:,None]*z*z,axis=0));scale=np.maximum(scale,1e-15);z=z/scale
        u,s,v=np.linalg.svd(sw[:,None]*z,full_matrices=False);base=np.outer(sw,sw)/np.sum(w);out=[]
        for lam in LAMBDAS:
            ht=base+(u*(s*s/(s*s+lam)))@u.T;h=ht/sw[:,None]*sw[None,:];den=1-np.diag(h);require(np.all(den>1e-10),'LOO ridge rank failure')
            loo=h/den[:,None];np.fill_diagonal(loo,0);out.append((h,loo,w,den))
        return out
    def summaries(self,w,allow_changed_n=False):
        rows=self.arm;cols=np.arange(self.nc);wm=sparse.csr_matrix((w,(rows,cols)),shape=(self.na,self.nc));total=np.asarray(wm@np.ones(self.nc)).ravel();exposure=np.asarray(wm@self.lib).ravel();require(np.all(total>0),'empty resampled arm');require(allow_changed_n or np.allclose(total,self.n,rtol=0,atol=1e-10),'bootstrap arm count changed')
        sum_log=(wm@self.log).toarray();sum_raw=(wm@self.x).toarray();mraw={'log':sum_log/total[:,None],'rate':10000*sum_raw/exposure[:,None]};adjusted={};tech={}
        wr=w*self.reference;zb=sparse.csr_matrix((self.z*wr[:,None]).T)
        for kind in ('log','rate'):
            weights=w if kind=='log' else w*self.lib;den=total if kind=='log' else exposure;zs=np.asarray(wm@(self.z if kind=='log' else self.z*self.lib[:,None]));composition=zs/den[:,None]
            cross=self.z.T@((weights*self.reference)[:,None]*self.z);zr=zs[self.refarms];dr=den[self.refarms]
            k=cross-zr.T@(zr/dr[:,None]);eig,vec=np.linalg.eigh(k);tol=max(eig.max(),1)*1e-10;keep=eig>tol;ki=(vec[:,keep]/eig[keep])@vec[:,keep].T
            b=(zb@(self.log if kind=='log' else self.x)).toarray()*(1 if kind=='log' else 10000.)
            rhs=b-zr.T@mraw[kind][self.refarms];coef=ki@rhs;adjusted[kind]=mraw[kind]-(composition-self.z0[kind])@coef
            tech[kind]={'rank':int(keep.sum()),'nonzero_condition':float(eig[keep].max()/eig[keep].min()) if keep.any() else None,'coeff_norm':float(np.linalg.norm(coef))}
        return adjusted,mraw,tech
    def noise_traces(self):
        # Observed plug-in trace penalties, held fixed in resampling. No claim of
        # known population variance; global mean/bootstrap sharing remains coupled.
        w=sparse.csr_matrix((np.ones(self.nc),(self.arm,np.arange(self.nc))),shape=(self.na,self.nc));n=self.n
        ss=np.asarray(w@cell_norms(self.log)).ravel();trlog=np.maximum(0,ss-n*normrows(self.raw['log']))/(n*np.maximum(n-1,1))
        norms=cell_norms(self.x);psi=np.empty(self.nc)
        for h,inds in enumerate(self.cells):
            m=self.raw['rate'][h];dot=np.asarray(self.x[inds]@m).ravel();psi[inds]=1e8*norms[inds]-20000*self.lib[inds]*dot+self.lib[inds]**2*np.dot(m,m)
        sl=np.asarray(w@self.lib).ravel();rate=np.maximum(0,np.asarray(w@psi).ravel())*(n/np.maximum(n-1,1))/(sl*sl)
        return {'log':trlog,'rate':rate}
    def weights(self,rng):
        w=np.empty(self.nc)
        for inds in self.cells:w[inds]=np.bincount(rng.integers(len(inds),size=len(inds)),minlength=len(inds))
        return w

def fit_nonnegative(a,b,t,va,vb):
    aa=normrows(a);bb=normrows(b);ab=np.einsum('ij,ij->i',a,b);at=np.einsum('ij,ij->i',a,t);bt=np.einsum('ij,ij->i',b,t)
    floor=1e-8*np.maximum(aa+bb,1e-12);d0=aa+va+floor;d1=bb+vb+floor;r0=at+va+floor;r1=bt+vb+floor;det=d0*d1-ab*ab;require(np.all(det>0),'potency normal matrix singular')
    interior=np.stack([(r0*d1-r1*ab)/det,(r1*d0-r0*ab)/det],1)
    candidates=np.stack([np.maximum(interior,0),np.stack([np.maximum(r0/d0,0),np.zeros_like(r0)],1),np.stack([np.zeros_like(r1),np.maximum(r1/d1,0)],1),np.zeros_like(interior)],1)
    # A clipped interior is not a stationary point, but both valid boundary
    # minimizers and zero are enumerated, so taking minimum remains correct.
    obj=d0[:,None]*candidates[:,:,0]**2+d1[:,None]*candidates[:,:,1]**2+2*ab[:,None]*candidates[:,:,0]*candidates[:,:,1]-2*r0[:,None]*candidates[:,:,0]-2*r1[:,None]*candidates[:,:,1]
    beta=candidates[np.arange(len(a)),np.argmin(obj,axis=1)];g=np.stack([np.stack([aa,ab],1),np.stack([ab,bb],1)],1);ev=np.linalg.eigvalsh(g)
    return beta,ev

def project(v,refs):
    # refs N x4 xG; all-four-single span, no pair response sets its basis.
    gram=refs@refs.transpose(0,2,1);eig,vec=np.linalg.eigh(gram);keep=eig>np.maximum(eig[:,-1:],1e-30)*1e-10
    inv=(vec*np.where(keep,1/np.maximum(eig,1e-300),0)[:,None,:])@vec.transpose(0,2,1);dot=np.einsum('nkg,ng->nk',refs,v);coef=np.einsum('nkl,nl->nk',inv,dot)
    return v-np.einsum('nk,nkg->ng',coef,refs),keep.sum(1)

def fit_direction(d,m,kind,direction,need_null=False):
    idx=d.idx;src=idx[:,direction];target=idx[:,1-direction]
    sa=idx[:,2] if direction==0 else idx[:,5];sb=idx[:,3] if direction==0 else idx[:,4]
    ta=idx[:,5] if direction==0 else idx[:,2];tb=idx[:,4] if direction==0 else idx[:,3];c=m[d.c];a=m[sa]-c;b=m[sb]-c;t=m[src]-c
    noise=d.noise[kind];beta,ev=fit_nonnegative(a,b,t,noise[sa]+noise[d.c],noise[sb]+noise[d.c])
    base_src0=guard(c+beta[:,0,None]*a+beta[:,1,None]*b,kind);res=m[src]-base_src0;gram=res@res.T;cv=[]
    for h,loo,w,den in d.hats[direction]:
        r=np.eye(d.N)-h;diag=np.einsum('ij,jk,ik->i',r,gram,r,optimize=True);cv.append(float(np.sum(w*diag/(den*den))/np.sum(w)/d.ng))
    choice=int(np.argmin(cv));offset=d.hats[direction][choice][1]@res
    unguard_src=c+beta[:,0,None]*a+beta[:,1,None]*b+offset;unguard_tgt=c+beta[:,0,None]*(m[ta]-c)+beta[:,1,None]*(m[tb]-c)+offset
    pred_src=guard(unguard_src,kind);pred=guard(unguard_tgt,kind)
    refs=np.stack([m[idx[:,2]]-c,m[idx[:,3]]-c,m[idx[:,5]]-c,m[idx[:,4]]-c],1);u,rank=project(m[src]-pred_src,refs);transfer=guard(pred+.5*u,kind)
    ordinary=normrows(m[target]-pred)/d.ng;transfer_error=normrows(m[target]-transfer)/d.ng;gain=ordinary-transfer_error
    additive=guard(m[ta]+m[tb]-c,kind);add_error=normrows(m[target]-additive)/d.ng
    out={'gain':gain,'ordinary_mse':ordinary,'transfer_mse':transfer_error,'additive_mse':add_error,'beta':beta,'lambda_index':choice,'cv':np.array(cv),'rank':rank,'single_gram_eigenvalues':ev,'clipped_ordinary_entries':int(np.count_nonzero(pred!=unguard_tgt)),'clipped_transfer_entries':int(np.count_nonzero(transfer!=pred+.5*u))}
    if need_null:
        null=m.copy();null[src]=pred_src;null[target]=pred;out['null_means']=null
    return out

def raw_contrast(d,m,kind):
    ix=d.idx;c=m[d.c];r1=m[ix[:,0]]-m[ix[:,2]]-m[ix[:,3]]+c;r2=m[ix[:,1]]-m[ix[:,4]]-m[ix[:,5]]+c
    product=np.einsum('ij,ij->i',r1,r2);den=np.sqrt(normrows(r1)*normrows(r2));return {'cross_product':product,'shared_control_trace_correction':float(d.noise[kind][d.c]),'corrected_cross_product':product-d.noise[kind][d.c],'cosine':np.divide(product,den,out=np.full_like(product,np.nan),where=den>0)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--draws',type=int,default=399);ap.add_argument('--output',type=Path,default=ROOT/'results');args=ap.parse_args();require(args.draws==399,'frozen draw count must be399')
    start=time.perf_counter();cpu=time.process_time();out=args.output;out.mkdir(parents=True,exist_ok=True);design=json.loads((ROOT/'results/DESIGN_MAP.json').read_text());freeze=json.loads((ROOT/'FREEZE.json').read_text());require(digest(ROOT/'FROZEN_CONTRACT.txt')==freeze['contract_sha256'],'frozen contract changed');require(digest(ROOT/'results/DESIGN_MAP.json')==freeze['design_map_sha256'],'design changed')
    d=Data(args.input,design);print(json.dumps({'phase':'input_and_reference_preparation','load_s':d.load_s,'rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'reference_technical_design':d.tech}),flush=True)
    kinds=['log','rate'];point={k:[fit_direction(d,d.point[k],k,z,True) for z in (0,1)] for k in kinds};raw={k:raw_contrast(d,d.raw[k],k) for k in kinds}
    point_file={'input_sha256':BASE,'contract_sha256':freeze['contract_sha256'],'point':{k:[{a:b for a,b in v.items() if a!='null_means'} for v in point[k]] for k in kinds},'raw':raw,'families':d.pairs,'technical':d.tech};(out/'POINT_RESULT.json').write_text(json.dumps(point_file,default=scalarize,indent=2)+'\n')
    print(json.dumps({'phase':'frozen_point_complete','mean_gain':{k:[float(v['gain'].mean()) for v in point[k]] for k in kinds},'elapsed_s':time.perf_counter()-start}),flush=True)
    rng=np.random.default_rng(20261021);b=args.draws;gains=np.empty((b,2,2,d.N));nullgain=np.empty((b,2,2));lambdas=np.empty((b,2,2),dtype=np.int8);null_lam=np.empty_like(lambdas);control_weights=[];technical_ranks=[];completed=0
    try:
        for j in range(b):
            if time.perf_counter()-start>1200:raise RuntimeError('frozen20minute body resource cap')
            if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>3*2**30:raise RuntimeError('frozen3GiB RSS resource cap')
            weights=d.weights(rng);control_weights.append(weights[d.cells[d.c]].astype(int));mb,unused,tech=d.summaries(weights);technical_ranks.append([tech[k]['rank'] for k in kinds])
            for ki,k in enumerate(kinds):
                delta=mb[k]-d.point[k]
                for direction in (0,1):
                    v=fit_direction(d,mb[k],k,direction);gains[j,ki,direction]=v['gain'];lambdas[j,ki,direction]=v['lambda_index']
                    vn=fit_direction(d,point[k][direction]['null_means']+delta,k,direction);nullgain[j,ki,direction]=vn['gain'].mean();null_lam[j,ki,direction]=vn['lambda_index']
            completed=j+1
            if completed%25==0:print(json.dumps({'phase':'joint_arm_bootstrap','completed':completed,'elapsed_s':time.perf_counter()-start,'rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}),flush=True)
    finally:
        np.savez_compressed(out/'BOOTSTRAP_DRAWS.npz',gains=gains[:completed],null_gain=nullgain[:completed],lambda_index=lambdas[:completed],null_lambda_index=null_lam[:completed],control_weights=np.array(control_weights[:completed]),technical_ranks=np.array(technical_ranks[:completed]))
        (out/'RESOURCE_RECEIPT.json').write_text(json.dumps({'completed':completed,'requested':b,'wall_s':time.perf_counter()-start,'self_cpu_s':time.process_time()-cpu,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'python':sys.version,'numpy':np.__version__,'input_sha256':BASE,'source_sha256':digest(__file__),'freeze_contract_sha256':freeze['contract_sha256'],'scope':'actual analysis body; dependency setup and reasoning costs separate'},indent=2)+'\n')
    summary={};all_pass=True
    for ki,k in enumerate(kinds):
        summary[k]=[]
        for direction in (0,1):
            obs=float(point[k][direction]['gain'].mean());boot=gains[:,ki,direction].mean(1);lo,hi=2*obs-np.quantile(boot,[.99375,.00625]);exceed=int(np.sum(nullgain[:,ki,direction]>=obs));p=(exceed+1)/(b+1);upper=float(stats.beta.ppf(.95,exceed+1,b-exceed)) if exceed<b else 1.
            passed=bool(obs>0 and lo>0 and upper<=.0125);all_pass&=passed;summary[k].append({'direction':f'{direction+1}->{2-direction}','mean_gain':obs,'familywise98p75_basic_interval':[float(lo),float(hi)],'ordinary_null_exceedances':exceed,'simulated_p':p,'MC95_upper_exceedance_probability':upper,'conditional_gate_pass':passed,'positive_family_gains':int(np.sum(point[k][direction]['gain']>0)),'lambda':float(LAMBDAS[point[k][direction]['lambda_index']])})
    # All seven matched-control omissions, no alternative choice or replication.
    loco=[]
    for cell in d.cells[d.c]:
        w=np.ones(d.nc);w[cell]=0
        mb,_,tech=d.summaries(w,allow_changed_n=True)
        loco.append({'omitted_cell_barcode':d.obs['cell_barcode'][cell],'mean_gains':{k:[float(fit_direction(d,mb[k],k,z)['gain'].mean()) for z in (0,1)] for k in kinds},'note':'six distinct control cells; recomputed means/technical adjustment, frozen plug-in variance penalty retained; fragility only, not independent replication'})
    result={'status':'CONDITIONAL_TECHNICAL_GATE_PASS' if all_pass else 'CONDITIONAL_TECHNICAL_GATE_NOT_PASSED','intrinsic_biological_interaction':'NOT_IDENTIFIED_WITHOUT_IMPLEMENTATION_EXCLUSIONS','summary':summary,'eligible_families':d.N,'excluded_families':len(design['excluded_pairs']),'reference_control_n':7,'inference_scope':'conditional nonparametric and source-only plug-in ordinary-null checks; not finite-sample guaranteed with7controls; no culture variance','remaining_current_method_boundary':'October2026 calibrated/PRESAGE compatible execution NOT_PERFORMED; no predictive headroom or superiority claim','leave_one_control_out':loco,'continuation':'STOP_THIS_ALLOCATION; preserve exact design ambiguity and frozen assay-conditional evidence; evaluator owns any new measurement/allocation','resource':json.loads((out/'RESOURCE_RECEIPT.json').read_text())};(out/'RESULT.json').write_text(json.dumps(result,default=scalarize,indent=2)+'\n');print(json.dumps({'phase':'complete','status':result['status'],'summary':summary},indent=2),flush=True)
if __name__=='__main__':main()
