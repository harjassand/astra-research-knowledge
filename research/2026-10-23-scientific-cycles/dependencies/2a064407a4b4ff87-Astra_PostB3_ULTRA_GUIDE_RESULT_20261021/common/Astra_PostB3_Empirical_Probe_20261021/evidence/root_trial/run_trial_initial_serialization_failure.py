"""Bounded sampling diagnostic, not biological replication or new prediction."""
from pathlib import Path
import argparse, hashlib, json, resource, sys, time
import numpy as np
from scipy import sparse

HERE = Path(__file__).resolve().parent
LOCAL_DEPS = HERE.parent / 'opportunities/perturbation/deps'
if LOCAL_DEPS.exists():
    sys.path.insert(0, str(LOCAL_DEPS))
import h5py

EXPECTED = '5da0485aed81b23bda57b4a7b4510a394682d54911416db89b4846ff6dd34732'

def column(obj):
    if isinstance(obj, h5py.Dataset):
        vals = obj[:]
    else:
        cats = obj['categories'][:]
        codes = obj['codes'][:]
        if np.any(codes < 0):
            raise ValueError('Missing labels')
        vals = cats[codes]
    return np.array([v.decode() if isinstance(v, bytes) else str(v) for v in vals])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, default=HERE.parent/'opportunities/perturbation/data/WesselsSatija2023.h5ad')
    ap.add_argument('--output', type=Path, default=HERE/'RESULT.json')
    args = ap.parse_args()
    started = time.perf_counter()
    cpu = time.process_time()
    h = hashlib.sha256()
    with args.input.open('rb') as handle:
        for buf in iter(lambda: handle.read(8*1024*1024), b''):
            h.update(buf)
    if h.hexdigest() != EXPECTED:
        raise ValueError('Input digest mismatch')
    rng = np.random.default_rng(20261021)
    with h5py.File(args.input, 'r') as f:
        labels = column(f['obs/perturbation'])
        names = sorted(set(labels))
        index = {n:i for i,n in enumerate(names)}
        shape = tuple(f['X'].attrs['shape'])
        assert shape == (30707,21052)
        group = np.empty(len(labels), dtype=int)
        for name in names:
            ix = np.flatnonzero(labels == name)
            rng.shuffle(ix)
            mid = len(ix)//2
            group[ix[:mid]] = 2*index[name]
            group[ix[mid:]] = 2*index[name]+1
        counts = np.bincount(group, minlength=2*len(names))
        assert np.min(counts) >= 7
        sums = np.zeros((2*len(names),shape[1]), dtype=np.float64)
        indptr = f['X/indptr'][:]
        nnz = len(f['X/data'])
        for first in range(0,shape[0],1024):
            last = min(shape[0], first+1024)
            lo,hi = int(indptr[first]),int(indptr[last])
            X = sparse.csr_matrix((f['X/data'][lo:hi].astype(np.float64),
                                   f['X/indices'][lo:hi],
                                   indptr[first:last+1]-lo),shape=(last-first,shape[1]))
            totals = np.asarray(X.sum(axis=1)).ravel()
            if np.any(totals <= 0):
                raise ValueError('Zero-total cell')
            X.data *= np.repeat(10000./totals, np.diff(X.indptr))
            np.log1p(X.data, out=X.data)
            W = sparse.csr_matrix((np.ones(last-first),
                                   (group[first:last],np.arange(last-first))),
                                  shape=(2*len(names),last-first))
            sums += (W@X).toarray()
    means = (sums/counts[:,None]).reshape((len(names),2,shape[1]))
    del sums
    pairs = [n for n in names if '_' in n]
    assert len(pairs) == 158 and 'control' in index
    pair_index = np.array([index[n] for n in pairs])
    a = np.array([index[n.split('_')[0]] for n in pairs])
    b = np.array([index[n.split('_')[1]] for n in pairs])
    c = index['control']
    observed = means[pair_index]
    single_sum = means[a]+means[b]
    residual = observed-single_sum+means[c][None,:,:]
    dot = np.einsum('ij,ij->i',residual[:,0,:],residual[:,1,:])/shape[1]
    norm = np.einsum('ihj,ihj->ih',residual,residual)/shape[1]
    cosine = dot/np.sqrt(norm[:,0]*norm[:,1])
    pooled = (means*counts.reshape((-1,2,1))).sum(axis=1)/counts.reshape((-1,2)).sum(axis=1)[:,None]
    shared = observed-pooled[a,None,:]-pooled[b,None,:]+pooled[c,None,:]
    shared_dot = np.einsum('ij,ij->i',shared[:,0,:],shared[:,1,:])/shape[1]
    shared_norm = np.einsum('ihj,ihj->ih',shared,shared)/shape[1]
    shared_cosine = shared_dot/np.sqrt(shared_norm[:,0]*shared_norm[:,1])
    train = np.array([hashlib.sha256(n.encode()).digest()[0]<128 for n in pairs])
    tests=[]
    for source in (0,1):
        target = 1-source
        feature = single_sum[:,source,:]-2*means[c,source,:]
        center = means[c,source,:]
        y = observed[:,source,:]-center
        lam = float(np.clip(np.einsum('ij,ij->',feature[train],y[train])/
                            np.einsum('ij,ij->',feature[train],feature[train]),0,2))
        errors={}
        for name,value in [('control',0.),('additive',1.),('shrunken_additive',lam)]:
            prediction = center+value*feature
            errors[name]=float(np.mean((prediction[~train]-observed[~train,target,:])**2))
        tests.append({'source_half':source,'target_half':target,'lambda_fit_on_development_pairs':lam,
                      'mean_squared_test_error_all_genes':errors})
    result={
        'status':'COMPLETED_SAMPLING_DIAGNOSTIC_ONLY',
        'input_sha256':EXPECTED,'input_shape':list(shape),'input_nnz':nnz,
        'normalization':'per-cell counts/total*10000, then natural log1p; all genes',
        'random_seed':20261021,'pair_count':len(pairs),
        'half_counts_min':int(counts.min()),
        'development_pairs':int(train.sum()),'test_pairs':int((~train).sum()),
        'independent_arm_sampling':{
            'mean_cross_inner_product_per_gene':float(dot.mean()),
            'median_cross_inner_product_per_gene':float(np.median(dot)),
            'positive_pairs':int((dot>0).sum()),
            'median_cosine':float(np.median(cosine)),
            'mean_squared_residual_by_half':norm.mean(axis=0).tolist()},
        'intentionally_shared_reference_diagnostic_NOT_independent':{
            'mean_cross_inner_product_per_gene':float(shared_dot.mean()),
            'positive_pairs':int((shared_dot>0).sum()),
            'median_cosine':float(np.median(shared_cosine))},
        'ordinary_shrinkage_diagnostic':tests,
        'per_pair':[{'pair':n,'development':bool(train[i]),
                     'half_cell_counts':{arm:counts[2*index[arm]:2*index[arm]+2].tolist()
                                        for arm in [n,*n.split('_'),'control']},
                     'cross_inner_product_per_gene':float(dot[i]),'cosine':float(cosine[i]),
                     'shared_reference_cross_inner_product_per_gene':float(shared_dot[i])}
                    for i,n in enumerate(pairs)],
        'limitations':[
            'Disjoint cells are not independent biological experiments.',
            'Fixed-seed repeatability is not a significance test or an uncertainty bound.',
            'Pairs share single/control estimates; pair-wise observations are dependent.',
            'Raw interaction signal does not establish signal beyond PRESAGE or predictability.',
            'The log-normalized scale can itself introduce or modify nonadditivity.',
            'No gene selection, new predictor, clinical inference or novelty claim.'],
        'wall_s':time.perf_counter()-started,'cpu_s':time.process_time()-cpu,
        'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'versions':{'numpy':np.__version__,'h5py':h5py.__version__}}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='per_pair'},indent=2))

if __name__=='__main__':
    main()
