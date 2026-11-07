"""Restricted, causal no-dark refit. No source solver replay or mechanism proof.

Run `python3 refit_lif_null.py fit`, then `python3 refit_lif_null.py evaluate`.
The fit stage never opens polarization scans other than scan000. Evaluation
does not optimize calibration/model parameters. Local measurement_search
dependencies and source data are read-only inputs.
"""
from pathlib import Path
import hashlib, json, os, sys, time
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
ROOT = Path(__file__).resolve().parent
MEAS = ROOT.parent / 'measurement_search'
sys.path.insert(0, str(MEAS / 'deps'))
import h5py
import numpy as np
from scipy.special import erf, voigt_profile
from scipy.optimize import least_squares
from scipy.interpolate import RegularGridInterpolator

HBAR = 0.6582119569  # eV fs
SCAN0 = 'transient_LiF_nirlinpol_run6_scan_000_2024_05_07_16_29_09.hdf5'
TIME = -(np.arange(100) * .1 + 3 - 11.1) * 6.6
PIX_TRANS = [577,635,655,666,1035.5,1119,1137.5]
PIX_STATIC = [404,465,486,497,867,950,968]
LAMBDA = [27.2,26.31,25.99,25.85,20.7,19.5,19.2]

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for x in iter(lambda: f.read(1 << 20), b''): h.update(x)
    return h.hexdigest()

def energy(pixels):
    return 1239.843 / np.polyval(np.polyfit(pixels, LAMBDA, 1), np.arange(1340))

ENERGY = energy(PIX_TRANS)
TARGET = (ENERGY >= 60) & (ENERGY <= 64)
TSEL = (TIME >= -10) & (TIME <= 18)
BASE = TIME >= 30
E = ENERGY[TARGET]
TAU = TIME[TSEL]
X = (E - 62) / 2

def load_raw(name):
    with h5py.File(MEAS/'data'/name, 'r') as f:
        return {k: f['data/'+k][()].astype(float) for k in
                ['res0/on','res0/off','bg0/on','bg0/off']}

def static_fit():
    p = MEAS/'data'/'static_LiF_2023_11_07_14_55_18.hdf5'
    with h5py.File(p, 'r') as f:
        bg = f['data/bg0/off'][()].mean(0)
        sample = f['data/res0/sample'][()].mean(0) - bg
        membrane = f['data/res0/membrane'][()].mean(0) - bg
    ee = energy(PIX_STATIC)
    selected = (ee >= 60) & (ee <= 64)
    xx, yy = ee[selected], -np.log10(sample[selected]/membrane[selected])
    mu0 = np.array([60.75,61.46,61.76,62.60])
    def model(z, x=xx):
        mu, sig, amp = z[:4], z[4:8], z[8:12]
        return (voigt_profile(x[:,None]-mu, sig, .04)
                /voigt_profile(np.zeros(4),sig,.04)) @ amp + z[12]+z[13]*(x-62)
    z0 = np.r_[mu0, [.12,.12,.22,.35], [.10,.30,.70,.15], yy.min(), .02]
    lo = np.r_[mu0-[.15,.15,.15,.25], [.04]*4, [0]*4, -1, -.5]
    hi = np.r_[mu0+[.15,.15,.15,.25], [.5,.5,.65,.8], [3]*4, 2, .5]
    fit = least_squares(lambda z: model(z)-yy, z0, bounds=(lo,hi),
                        max_nfev=1000, ftol=1e-11, xtol=1e-11, gtol=1e-11)
    return {'parameters': fit.x.tolist(), 'mu_eV': fit.x[:4].tolist(),
            'sigma_eV':fit.x[4:8].tolist(),'height_OD':fit.x[8:12].tolist(),
            'fixed_Lorentzian_HWHM_eV':.04,
            'fit_rmse_OD':float(np.sqrt(np.mean((model(fit.x)-yy)**2))),
            'n_static_pixels':len(xx),'n_free_parameters':14,
            'success':bool(fit.success),'source_sha256':sha(p)}

def make_edge(raw, reference):
    # Only scan000 repeats 0,...,4 and backgrounds 0,...,4 train all transforms.
    bgon = raw['bg0/on'][:5].mean(0)
    bgoff = raw['bg0/off'][:5].mean(0)
    off = raw['res0/off'][:,:,:5,:] - bgoff
    if np.any(off[:,:, :,reference] <= 0): raise ValueError('Nonpositive reference counts')
    edge_maps, ranks = [], []
    rank_options = [0,2,5,10,20]
    for pol in range(2):
        logoff = np.log10(off[:,pol])
        # Paired off-only repeat differences, not pumped data. First pair trains
        # inner rank selection; second pair validates it, then both refit.
        cal = np.concatenate([logoff[:,0]-logoff[:,1],
                              logoff[:,2]-logoff[:,3]], axis=0)
        def mapper(rows, rank):
            xx, yy = cal[rows][:,reference], cal[rows][:,TARGET]
            if rank == 0: return np.zeros((int(reference.sum()),int(TARGET.sum())))
            u,s,vt = np.linalg.svd(xx, full_matrices=False)
            return (vt[:rank].T/s[:rank]) @ (u[:,:rank].T @ yy)
        losses = []
        for rank in rank_options:
            bb = mapper(np.arange(100),rank)
            loss = np.mean((cal[100:][:,reference]@bb-cal[100:][:,TARGET])**2)
            losses.append(float(loss))
        rank = rank_options[int(np.argmin(losses))]
        edge_maps.append(mapper(np.arange(200),rank))
        ranks.append({'selected_rank':rank,'candidate_ranks':rank_options,
                      'off_only_inner_validation_MSE_OD2':losses})
    return bgon,bgoff,np.array(edge_maps),ranks

def processed(raw, reps, bgon, bgoff, maps, reference, baseline=None):
    on = raw['res0/on'][:,:,reps,:]-bgon
    off = raw['res0/off'][:,:,reps,:]-bgoff
    relevant = TARGET | reference
    if np.any(on[:,:,:,relevant] <= 0) or np.any(off[:,:,:,relevant] <= 0):
        raise ValueError('Nonpositive target/reference counts; censor model required')
    # Average repeat-wise logarithms, deliberately not source log-of-means.
    dod = -np.log10(on/off)
    out = np.stack([dod[:,p][:,:,TARGET] - dod[:,p][:,:,reference]@maps[p]
                    for p in range(2)])  # [pol,time,repeat,energy]
    if baseline is None: baseline = out[:,BASE].mean(axis=(1,2))
    return out-baseline[:,None,None,:],baseline

def qgauss(tt, tau, center, width):
    # Integral of a nonnegative Gaussian field intensity from 0 to tt.
    k = 2*np.sqrt(np.log(2))
    x0 = -tau[:,None]+center
    x1 = tt[None,:]+x0
    h0 = np.exp(-(k*x0/width)**2)
    h1 = np.exp(-(k*x1/width)**2)
    q = width*np.sqrt(np.pi)/(2*k)*(erf(k*x1/width)-erf(k*x0/width))
    dc = h1-h0
    dw = (q-x1*h1+x0*h0)/width
    return q,dc,dw

class CausalDiagonal:
    def __init__(self, static, common=False, dt=.06):
        self.common = common
        self.nj = 1 if common else 4
        self.n = 4*self.nj+8
        tt = np.arange(0,24+dt/2,dt)
        self.tt = tt
        mu,sig,amp = (np.array(static[k]) for k in ['mu_eV','sigma_eV','height_OD'])
        wt = np.full(len(tt),dt); wt[[0,-1]] *= .5
        self.kernels = []
        for j in range(4):
            env = np.exp(-.04*tt/HBAR-.5*(sig[j]*tt/HBAR)**2)
            norm = np.sum(env*wt)
            self.kernels.append(amp[j]*(env*wt/norm)[None,:]
                                *np.exp(1j*(E[:,None]-mu[j])*tt[None,:]/HBAR))

    def unpack(self,z):
        k = 2*self.nj
        delta = z[:k].reshape(2,self.nj)
        gamma = z[k:2*k].reshape(2,self.nj)
        center,width,rleft,rright = z[2*k:2*k+4]
        nuisance = z[2*k+4:].reshape(2,2)
        return delta,gamma,center,width,rleft,rright,nuisance

    def predict(self,z,jac=False):
        delta,gamma,c,w,rl,rr,nu = self.unpack(z)
        qm,cm,wm = qgauss(self.tt,TAU,c,w)
        ql,cl,_ = qgauss(self.tt,TAU,c-9,3)
        qr,cr,_ = qgauss(self.tt,TAU,c+12,8)
        q = qm+rl*ql+rr*qr
        dq = [cm+rl*cl+rr*cr,wm,ql,qr]
        h = lambda x,width: np.exp(-4*np.log(2)*(x/width)**2)
        xx = c-TAU
        g = h(xx,w)+rl*h(xx-9,3)+rr*h(xx+12,8)
        dg = [-8*np.log(2)*xx/w**2*h(xx,w)
              -rl*8*np.log(2)*(xx-9)/9*h(xx-9,3)
              -rr*8*np.log(2)*(xx+12)/64*h(xx+12,8),
              8*np.log(2)*xx**2/w**3*h(xx,w),h(xx-9,3),h(xx+12,8)]
        pred = np.zeros((2,len(TAU),len(E)))
        jj = np.zeros(pred.shape+(self.n,)) if jac else None
        k = 2*self.nj
        for p in range(2):
            for j,F in enumerate(self.kernels):
                a = 0 if self.common else j
                zeta = gamma[p,a]+1j*delta[p,a]
                ex = np.exp(-zeta*q/HBAR)
                pred[p] += np.real((ex-1)@F.T)
                if jac:
                    ji = p*self.nj+a
                    jj[p,:,:,ji] += np.real((-1j*q/HBAR*ex)@F.T)
                    jj[p,:,:,k+ji] += np.real((-q/HBAR*ex)@F.T)
                    for r in range(4):
                        jj[p,:,:,2*k+r] += np.real((-zeta/HBAR*ex*dq[r])@F.T)
            spectral = nu[p,0]+nu[p,1]*X
            pred[p] += g[:,None]*spectral
            if jac:
                for r in range(4): jj[p,:,:,2*k+r] += dg[r][:,None]*spectral
                jj[p,:,:,2*k+4+2*p] = g[:,None]
                jj[p,:,:,2*k+5+2*p] = g[:,None]*X
        return (pred,jj.reshape(-1,self.n)) if jac else pred

    def fit(self,y,initial=None):
        n = self.nj
        z0 = np.r_[[.15]*(2*n), [.015]*(2*n), 0,6,.08,.08, [0]*4]
        if initial is not None: z0 = initial
        lo = np.r_[[-1]*(2*n), [0]*(2*n), -3,2.5,0,0, [-.15]*4]
        hi = np.r_[[1]*(2*n), [1]*(2*n), 3,12,.5,.5, [.15]*4]
        cached = [None,None,None]
        def get(z):
            if cached[0] is None or not np.array_equal(z,cached[0]):
                pp,jj = self.predict(z,True); cached[:] = [z.copy(),pp,jj]
            return cached[1:]
        start = time.perf_counter()
        fit = least_squares(lambda z:(get(z)[0]-y).ravel(), z0,
                            jac=lambda z:get(z)[1],bounds=(lo,hi),
                            max_nfev=180,ftol=1e-8,xtol=1e-8,gtol=1e-8)
        return fit,{'wall_seconds':time.perf_counter()-start,
                    'n_free_parameters':len(z0),'success':bool(fit.success),
                    'message':fit.message,'nfev':fit.nfev,'njev':fit.njev,
                    'parameter_values':fit.x.tolist(),'lower_bounds':lo.tolist(),
                    'upper_bounds':hi.tolist(),'gradient_infinity_norm':float(fit.optimality)}

def template_fit(y,kind):
    aa = np.load(MEAS/'data'/('DeltaOD_'+kind+'.npy'))
    ww = np.load(MEAS/'data'/'w.npy')
    interp = RegularGridInterpolator((np.linspace(-10,10,101),ww),aa,
                                     bounds_error=False,fill_value=0)
    def pred(z):
        amp,c,scale,eshift = z[:2],z[2],z[3],z[4]
        nu = z[5:].reshape(2,2)
        tt,ee = np.meshgrid((TAU-c)/scale,E-eshift,indexing='ij')
        base = interp(np.stack([tt,ee],axis=-1))
        g = np.exp(-4*np.log(2)*((TAU-c)/(6*scale))**2)
        return np.stack([amp[p]*base+g[:,None]*(nu[p,0]+nu[p,1]*X) for p in range(2)])
    z0 = np.r_[10,3,0,1,0,[0]*4]
    lo = np.r_[0,0,-3,.5,-.5,[-.15]*4]
    hi = np.r_[100,100,3,2,.5,[.15]*4]
    start=time.perf_counter()
    fit=least_squares(lambda z:(pred(z)-y).ravel(),z0,bounds=(lo,hi),
                      max_nfev=300,ftol=1e-9,xtol=1e-9,gtol=1e-9)
    return fit.x,pred(fit.x),{'wall_seconds':time.perf_counter()-start,
                           'n_free_parameters':9,'parameter_values':fit.x.tolist(),
                           'success':bool(fit.success),'nfev':fit.nfev,
                           'array_sha256':sha(MEAS/'data'/('DeltaOD_'+kind+'.npy')),
                           'caution':'Template normalization/axes recalibration; not full TDSE refit.'}

def summary(y,pred):
    err = y-pred
    feature_e = (E >= 62.4)&(E <= 62.6)
    feature_t = (TAU >= -.7)&(TAU <= .7)
    return {'RMSE_mOD':float(1000*np.sqrt(np.mean(err**2))),
            'by_polarization_RMSE_mOD':(1000*np.sqrt(np.mean(err**2,axis=(1,2)))).tolist(),
            'flagship_62p5_near_zero_mean_mOD':(1000*y[:,feature_t][:,:,feature_e].mean(axis=(1,2))).tolist(),
            'flagship_prediction_mean_mOD':(1000*pred[:,feature_t][:,:,feature_e].mean(axis=(1,2))).tolist(),
            'n_pixels':len(E),'n_time_points':len(TAU),
            'uncertainty':'No calibrated hypothesis-test p value; camera counts correlated.'}

def fit_stage():
    start = time.perf_counter()
    raw = load_raw(SCAN0)
    static = static_fit()
    report = {'stage':'FROZEN_TRAINING_FIT','scientific_target':'Discrete dark-exciton coupling required by observations',
              'scope':'Restricted causal diagonal null vs calibrated output templates; no target proof.',
              'training_scan':SCAN0,'training_repeats':[0,1,2,3,4],
              'within_scan_holdout_repeats':[5,6,7,8,9],
              'fit_time_fs':[-10,18],'fit_energy_eV':[60,64],
              'static_fit':static,'protocols':{},
              'source_input_sha256':{SCAN0:sha(MEAS/'data'/SCAN0)},
              'selection_leakage':['Energy/time windows and peak count inherited from source analysis.',
                                  'Source model arrays already fitted to another stabilized experiment.',
                                  'Delay/energy axis line positions inherited without acquired covariance.',
                                  'Same-scan repeats are not independent specimens.'],
              'unavailable':['Source TDSE fitting solver','same-scan independent NIR pulse field',
                             'calibration confidence set','count gain/read-noise law','inference token/cost/energy telemetry']}
    for protocol in ['paper_35_55_eV','script_first_1025_pixels']:
        reference = ((ENERGY>=35)&(ENERGY<=55)) if protocol.startswith('paper') else np.arange(1340)<1025
        bgon,bgoff,maps,ranks = make_edge(raw,reference)
        arr,baseline = processed(raw,np.arange(5),bgon,bgoff,maps,reference)
        y = arr[:,TSEL].mean(2)
        predictions,params = {},{}
        common = CausalDiagonal(static,common=True)
        ff,meta = common.fit(y)
        predictions['common_shift_and_rate'] = common.predict(ff.x)
        params['common_shift_and_rate'] = meta
        independent = CausalDiagonal(static)
        dc,gc,c,w,rl,rr,nu = common.unpack(ff.x)
        initial = np.r_[np.repeat(dc,4,axis=1).ravel(),
                        np.repeat(gc,4,axis=1).ravel(),c,w,rl,rr,nu.ravel()]
        fi,meta = independent.fit(y,initial)
        predictions['state_specific_shift_and_rate'] = independent.predict(fi.x)
        params['state_specific_shift_and_rate'] = meta
        # One more deterministic initialisation limits local-optimisation claims.
        alternate = initial.copy(); alternate[:8] *= -.5
        fa,ma = independent.fit(y,alternate)
        if np.sum((independent.predict(fa.x)-y)**2) < np.sum((predictions['state_specific_shift_and_rate']-y)**2):
            fi,meta = fa,ma
            predictions['state_specific_shift_and_rate'] = independent.predict(fi.x)
            params['state_specific_shift_and_rate'] = meta
        params['state_specific_shift_and_rate']['number_of_starts']=2
        fine = CausalDiagonal(static,dt=.03).predict(fi.x)
        numerical = float(1000*np.sqrt(np.mean((fine-predictions['state_specific_shift_and_rate'])**2)))
        for kind in ['starkshift','fullmodel']:
            z,pred,meta = template_fit(y,kind)
            predictions['refitted_'+kind+'_template'] = pred
            params['refitted_'+kind+'_template'] = meta
        np.savez_compressed(ROOT/(protocol+'_FROZEN.npz'),bgon=bgon,bgoff=bgoff,maps=maps,
                            reference=reference,baseline=baseline,
                            **{'prediction_'+k:v for k,v in predictions.items()})
        report['protocols'][protocol]={'reference_pixel_count':int(reference.sum()),
                    'reference_energy_endpoints_eV':[float(ENERGY[reference].min()),float(ENERGY[reference].max())],
                    'edge_rank_fit':ranks,'model_fits':params,
                    'training_errors':{k:summary(y,v) for k,v in predictions.items()},
                    'forward_quadrature_halved_step_difference_RMSE_mOD':numerical}
        (ROOT/'FROZEN_TRAINING.json').write_text(json.dumps(report,indent=2)+'\n')
        print(protocol,{k:v['RMSE_mOD'] for k,v in report['protocols'][protocol]['training_errors'].items()},flush=True)
    report['total_fit_wall_seconds']=time.perf_counter()-start
    report['fitting_code_sha256']=sha(__file__)
    (ROOT/'FROZEN_TRAINING.json').write_text(json.dumps(report,indent=2)+'\n')
    freeze={'file':'FROZEN_TRAINING.json','sha256':sha(ROOT/'FROZEN_TRAINING.json'),
            'created_unix_seconds':time.time(),'holdout_files_opened':[]}
    (ROOT/'FIT_FREEZE_RECEIPT.json').write_text(json.dumps(freeze,indent=2)+'\n')
    print('FIT FREEZE',freeze,flush=True)

def evaluate_stage():
    start=time.perf_counter()
    freeze=json.loads((ROOT/'FIT_FREEZE_RECEIPT.json').read_text())
    if sha(ROOT/'FROZEN_TRAINING.json')!=freeze['sha256']: raise ValueError('Training freeze mutated')
    metadata=json.loads((MEAS/'sources'/'zenodo_14783448_metadata.json').read_text())
    heldout=[v['key'] for v in metadata['files'] if v['key'].startswith('transient_LiF_nirlinpol_run6_scan_')
             and not v['key'].startswith('transient_LiF_nirlinpol_run6_scan_000')]
    existing=[x for x in sorted(heldout) if (MEAS/'data'/x).exists()]
    report={'stage':'FROZEN_MODELS_EVALUATED_WITHOUT_TEST_REFIT',
            'training_freeze':freeze,'protocols':{},'cross_scan_files':[{'name':x,'sha256':sha(MEAS/'data'/x)} for x in existing],
            'scope':'Finite acquired camera data prediction; no target-mechanism p value or model-independent state inference.'}
    raw0=load_raw(SCAN0)
    for protocol in ['paper_35_55_eV','script_first_1025_pixels']:
        pp=np.load(ROOT/(protocol+'_FROZEN.npz'))
        maps,reference,baseline,bgon,bgoff=(pp[k] for k in ['maps','reference','baseline','bgon','bgoff'])
        preds={k[len('prediction_'):]:pp[k] for k in pp.files if k.startswith('prediction_')}
        test,_=processed(raw0,np.arange(5,10),bgon,bgoff,maps,reference,baseline)
        yy=test[:,TSEL].mean(2)
        evaluations={'within_scan_repeat_holdout':{k:summary(yy,v) for k,v in preds.items()},'cross_scan_holdouts':{}}
        for name in existing:
            raw=load_raw(name)
            # Main transfer uses fixed training background/reference/baseline;
            # test backgrounds are intentionally not fitted or used.
            yy,_=processed(raw,np.arange(10),bgon,bgoff,maps,reference,baseline)
            yy=yy[:,TSEL].mean(2)
            evaluations['cross_scan_holdouts'][name]={k:summary(yy,v) for k,v in preds.items()}
        report['protocols'][protocol]=evaluations
    report['evaluation_wall_seconds']=time.perf_counter()-start
    report['no_test_parameter_or_hyperparameter_fit']=True
    (ROOT/'HELDOUT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    for p,v in report['protocols'].items():
        print(p,'within',{k:round(x['RMSE_mOD'],3) for k,x in v['within_scan_repeat_holdout'].items()})
        for name,w in v['cross_scan_holdouts'].items(): print(name,{k:round(x['RMSE_mOD'],3) for k,x in w.items()})

if __name__=='__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in ['fit','evaluate']: raise SystemExit(__doc__)
    fit_stage() if sys.argv[1]=='fit' else evaluate_stage()
