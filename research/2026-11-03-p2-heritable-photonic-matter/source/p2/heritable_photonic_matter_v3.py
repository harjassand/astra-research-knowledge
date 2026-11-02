#!/usr/bin/env python3
"""Research execution v3: count ALL genome-template copies in the optical reference.
NOT a wet-laboratory result, NOT a new physical genotype->material demonstration.
Primary source: https://doi.org/10.1021/acs.nanolett.5b05139 (2016).
Only the Förster radius 5.4 nm, representative distances 5.2/5.6 nm,
and linear antenna fit alpha=0.606, intercept=0.006 come from that source.
Everything about binding/folding, PCR expression, photons in the sorter,
and genotype-dependent distances is an explicit *model assumption*.
Genotype is a 6-bit variable-domain origami-scaffold allele; each position is
occupied by exactly one of two shared staples, labelled Cy3 vs unlabelled.
A common fixed Cy5 staple occupies the central acceptor position.
Physical mapping of genotype variable domains into caDNAno remains unmade.

Outputs /mnt/data/heritable_photonic_matter_v3_results.json and
/mnt/data/heritable_photonic_matter_v3_variants.csv when run with --save.
"""
import csv
import itertools
import json
from dataclasses import dataclass
from pathlib import Path
import argparse
import math
import numpy as np

R0=5.4                 # nm, experimental Cy3->Cy5
DIST=np.array([5.2,5.6,5.2,5.6,5.2,5.6]) # illustrative category assignment, NOT paper's site map
ALPHA=0.606            # fitted excitation/cross-section factor
Q=0.006                # fitted intercept AFTER experimental direct-excitation correction


def fret_eff(r_nm):
    return 1.0/(1.0+(np.asarray(r_nm)/R0)**6)


def ae(bits, distances=DIST):
    """Low flux, linear antenna effect for a complete Cy5-active origami."""
    return float(Q+ALPHA*np.dot(np.asarray(bits),fret_eff(distances)))


def genotypes(weight=4):
    return [tuple(g) for g in itertools.product((0,1),repeat=6) if sum(g)==weight]


def rising(x,k):
    y=1.0
    for j in range(k):y*=x+j
    return y


def beta_bernoulli_pattern_prob(n_occupied,n_unoccupied,p,kappa):
    """Exact exchangeable Beta-Bernoulli occupancy for one specific bit pattern.
    P~Beta(p*kappa,(1-p)*kappa); conditional site Bernoullis iid(P).
    """
    a,b=p*kappa,(1-p)*kappa
    return rising(a,n_occupied)*rising(b,n_unoccupied)/rising(a+b,n_occupied+n_unoccupied)


def tail_probability(bits, threshold=1.0, p=0.85, kappa=12.0,
                     fold=0.94, acceptor=0.96, correlated=True):
    """Probability a *single physical object* meets AE threshold;
    folded + acceptor active required.  Site probabilities are *unmeasured*.
    A nonfunctional object is counted as failure, not hidden by normalization.
    """
    occupied=[i for i,x in enumerate(bits) if x]
    n=len(occupied)
    out=0.
    for states in itertools.product((0,1),repeat=n):
        k=sum(states)
        if correlated:
            pr=beta_bernoulli_pattern_prob(k,n-k,p,kappa)
        else:
            pr=p**k*(1-p)**(n-k)
        physical=np.zeros(6,dtype=int)
        for idx,state in zip(occupied,states):physical[idx]=state
        if ae(physical)>=threshold:
            out+=pr
    return float(out*fold*acceptor)


@dataclass
class Scenario:
    name:str
    p_site:float
    kappa_batch:float
    kappa_clone:float
    fold_p:float
    acceptor_p:float
    geom_batch_sigma_nm:float
    geom_gb_sigma_nm:float
    photons_per_acceptor:float
    mean_copies:float
    cv_copies:float
    background_counts:float
    clones_training:int
    clones_test:int

OPT=Scenario('optimistic_model_UNMEASURED', 0.94,150.,75.,0.96,0.96,0.035,0.030,12.,140.,0.9,10.,4,16)
STRESS=Scenario('stress_model_UNMEASURED',0.79,12.,9.,0.85,0.90,0.13,0.15,4.,100.,1.6,20.,4,16)


def draw_batch(rng,sc, gs):
    """Clones in same batch share fold/binding/Mg geometry deviations,
    while genotype-by-batch shifts are shared within a given clone family."""
    pb=float(rng.beta(sc.p_site*sc.kappa_batch,(1-sc.p_site)*sc.kappa_batch))
    pf=float(rng.beta(sc.fold_p*sc.kappa_batch,(1-sc.fold_p)*sc.kappa_batch))
    global_shift=rng.normal(0,sc.geom_batch_sigma_nm)
    gb={g:rng.normal(0,sc.geom_gb_sigma_nm,size=6) for g in gs}
    return pb,pf,global_shift,gb


def copy_count(rng,sc):
    """Poisson-lognormal number of origamis in a clonal aliquot."""
    sdlog=math.sqrt(math.log1p(sc.cv_copies**2))
    meanlog=math.log(sc.mean_copies)-sdlog**2/2
    intensity=rng.lognormal(meanlog,sdlog)
    return max(1,int(rng.poisson(intensity)))


def expression(rng,sc,g,batch):
    """Complete in-silico genotype -> physical defects -> two optical signals.
    Simulates individual particles; no perfect genotype-to-phenotype oracle.
    """
    pb,pf,global_shift,gb=batch
    pclone=rng.beta(pb*sc.kappa_clone,(1-pb)*sc.kappa_clone)
    count=copy_count(rng,sc)
    folded=rng.random(count)<pf
    acceptor=rng.random(count)<sc.acceptor_p
    actual=folded & acceptor
    occupancy=rng.random((count,6))<pclone
    occupancy=occupancy & np.array(g,dtype=bool)[None,:]
    dist=np.maximum(.5,DIST+global_shift+gb[g])
    coeff=ALPHA*fret_eff(dist)
    optical=Q*actual.astype(float)+actual*(occupancy@coeff)
    # v3: dedicated reference bound to the genome, NOT Cy5-direct reference.
    # This conservative material-per-input metric counts nonfolded / missing-Cy5
    # genomes as functionless instead of conditioning them out. The added
    # fixed remote reference dye, optical cross-talk, and its survival are
    # physically UNVALIDATED. ALEX direct Cy5 from 2016 is NOT such a count.
    ref_unit=int(count)
    physical=float(optical.sum())
    signal=rng.poisson(sc.photons_per_acceptor*physical+sc.background_counts)
    reference=rng.poisson(sc.photons_per_acceptor*ref_unit+sc.background_counts)
    # Both backgrounds are assumed estimable from matched blank measurements.
    raw=float(signal)
    r=reference-sc.background_counts
    s=signal-sc.background_counts
    norm=float(s/r) if r>10 else float('nan')
    return {'raw':raw,'corrected_ae':norm,'copy_count':count,
            'active_acceptor_count':int(actual.sum()),'latent_ae':physical/ref_unit if ref_unit else float('nan')}


def screen_population(rng,sc, gs, num_clones):
    batch=draw_batch(rng,sc,gs)
    out={}
    for g in gs:
        records=[expression(rng,sc,g,batch) for i in range(num_clones)]
        out[g]={name:float(np.nanmean([v[name] for v in records]))
                for name in ('raw','corrected_ae','copy_count','active_acceptor_count','latent_ae')}
    return out


def selection_campaign(rng,sc, gs):
    train=screen_population(rng,sc,gs,sc.clones_training)
    # Physical selection: actually measured donor-excited red / acceptor-excited red.
    winner=max(gs,key=lambda g:train[g]['corrected_ae'])
    raw_winner=max(gs,key=lambda g:train[g]['raw'])
    # Strong incumbent on the SAME known physics, without noisy experimental search:
    incumbent=max(gs,key=ae)
    random_winner=gs[int(rng.integers(len(gs)))]
    selected=(winner,raw_winner,incumbent,random_winner)
    test=screen_population(rng,sc,selected,sc.clones_test)
    return dict(winner=''.join(map(str,winner)),raw_winner=''.join(map(str,raw_winner)),
                best_geometry=''.join(map(str,incumbent)),
                nominal=[ae(g) for g in selected],
                train=[train[g]['corrected_ae'] for g in selected],
                fresh=[test[g]['corrected_ae'] for g in selected],
                fresh_physical=[test[g]['latent_ae'] for g in selected])


def mean_ci(samples):
    a=np.array(samples,dtype=float)
    return {'mean':float(np.nanmean(a)),
            'p05':float(np.nanquantile(a,.05)),
            'p95':float(np.nanquantile(a,.95))}


def repeatability_across_fresh_batches(rng,sc,gs,n_clones=8):
    a=screen_population(rng,sc,gs,n_clones)
    b=screen_population(rng,sc,gs,n_clones)
    x=np.array([a[g]['corrected_ae'] for g in gs])
    y=np.array([b[g]['corrected_ae'] for g in gs])
    return float(np.corrcoef(x,y)[0,1]) if np.std(x)>0 and np.std(y)>0 else float('nan')


def run(seed=20261103, campaigns=150):
    rng=np.random.default_rng(seed)
    gs=genotypes(4)
    all6=(1,)*6
    res={'metadata':{
        'source':'https://doi.org/10.1021/acs.nanolett.5b05139',
        'reference_convention':'ALL scaffold input copies; dedicated inert DNA reporter UNDEMONSTRATED. Not ALEX Cy5 reference',
        'source_physics':{'R0_nm':R0,'near_nm':5.2,'far_nm':5.6,'alpha':ALPHA,'q':Q},
        'unmeasured':['variable-genotype origami interface','site geometry assignment',
                      'site occupancy','fold/acceptor yield','correlated batch effects',
                      'genotype-by-batch geometry','photons per object','object copy-number'],
        'seed':seed,'campaigns':campaigns,
        'n_genotypes':len(gs), 'all_six_nominal_AE':ae(all6)},
        'exact_single_object_probabilities':{},'campaign_results':{},'variants':[]}
    for p,kappa in ((0.85,12.),(0.95,12.)):
        for corr in (False,True):
            key=f'P_AE_ge_1_for_all_six_p{p}_'+('beta_correlated' if corr else 'independent')
            res['exact_single_object_probabilities'][key]=tail_probability(all6,1,p,kappa,.94,.96,corr)
    for g in gs:
        res['variants'].append(dict(genome=''.join(map(str,g)),near_sites=sum(x for i,x in enumerate(g) if DIST[i]==5.2),
                                    donor_sites=sum(g),nominal_AE=ae(g),
                                    P_single_AE_ge_1_p085_independent=tail_probability(g,1,.85,12.,.94,.96,False),
                                    P_single_AE_ge_1_p085_beta_correlated=tail_probability(g,1,.85,12.,.94,.96,True)))
    for sc in (OPT,STRESS):
        campaigns_results=[selection_campaign(rng,sc,gs) for _ in range(campaigns)]
        fresh=np.array([r['fresh'] for r in campaigns_results]);nom=np.array([r['nominal'] for r in campaigns_results])
        physical=np.array([r['fresh_physical'] for r in campaigns_results]);
        repeat=[repeatability_across_fresh_batches(rng,sc,gs,8) for i in range(max(20,campaigns//4))]
        result={'scenario':vars(sc),
                'source_nominal_selected':mean_ci(nom[:,0]),
                'source_nominal_raw_selected':mean_ci(nom[:,1]),
                'source_nominal_incumbent':mean_ci(nom[:,2]),
                'source_nominal_random':mean_ci(nom[:,3]),
                'fresh_corrected_AE_selected':mean_ci(fresh[:,0]),
                'fresh_corrected_AE_raw_selected':mean_ci(fresh[:,1]),
                'fresh_corrected_AE_incumbent':mean_ci(fresh[:,2]),
                'fresh_corrected_AE_random':mean_ci(fresh[:,3]),
                'fresh_latent_AE_selected':mean_ci(physical[:,0]),
                'fresh_latent_AE_raw_selected':mean_ci(physical[:,1]),
                'fresh_latent_AE_incumbent':mean_ci(physical[:,2]),
                'fresh_latent_AE_random':mean_ci(physical[:,3]),
                'repeatability_2_fresh_batches_r':mean_ci(repeat),
                'prob_geometric_optimum_selected':float(np.mean(np.isclose(nom[:,0],nom[:,2]))),
                'example_campaign':campaigns_results[0]}
        res['campaign_results'][sc.name]=result
    return res


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--save',action='store_true')
    parser.add_argument('--campaigns',type=int,default=150)
    args=parser.parse_args()
    res=run(campaigns=args.campaigns)
    print('Six-donor ring source-calibrated nominal AE:',round(res['metadata']['all_six_nominal_AE'],4))
    print('Individual six-donor optical threshold probabilities:',res['exact_single_object_probabilities'])
    for name,r in res['campaign_results'].items():
        print(name,'best selected nominal:',r['source_nominal_selected'],'incumbent:',r['source_nominal_incumbent'])
        print(' fresh measured corrected AE:',r['fresh_corrected_AE_selected'],
              'directly programmed:',r['fresh_corrected_AE_incumbent'],
              'raw-brightness selection:',r['fresh_corrected_AE_raw_selected'])
        print(' repeatability:',r['repeatability_2_fresh_batches_r'],
              'optimal genome probability:',r['prob_geometric_optimum_selected'])
    if args.save:
        base=Path('/mnt/data')
        (base/'heritable_photonic_matter_v3_results.json').write_text(json.dumps(res,indent=2))
        with (base/'heritable_photonic_matter_v3_variants.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(res['variants'][0]));w.writeheader();w.writerows(res['variants'])

if __name__=='__main__':main()
