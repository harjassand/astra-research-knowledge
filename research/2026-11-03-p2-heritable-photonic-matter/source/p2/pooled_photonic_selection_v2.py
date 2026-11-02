#!/usr/bin/env python3
"""Two-round *synthetic* pooled selection with Poisson template mixing and photon readout.
This is model evidence only: enzymatic amplification, folding, droplet-compatible
Cy3/Cy5 assay, FADS, and physical genome recovery have NOT been jointly demonstrated.
Source-calibrated FRET physics: Hemmig 2016 DOI 10.1021/acs.nanolett.5b05139.
All sorter, folding, copy, background, and DNA loading assumptions are model inputs.

Each droplet contains N~Poisson(lam) (including empty drops). Its genomes
are i.i.d. from the current pool, each copies to a random number of origamis.
Each replica experiences correlated clone-level folding/occupation and shared batch.
Green and red signals are independent Poisson counts conditional on actual
photons, with direct-acceptor excitation as the internal copy-number reference.
Selected droplets are destroyed for genome recovery; when mixed, the recovered
genome is sampled uniformly among input templates. Fresh clones are physically
resimulated in an independent batch, not read from genotype truth.
"""
import numpy as np, json, argparse, math
from pathlib import Path
import heritable_photonic_matter_v3 as optics


def truncated_pois(rng, lam):
    n=0
    while n==0: n=int(rng.poisson(lam))
    return n


def make_batch(rng,sc,gs):return optics.draw_batch(rng,sc,gs)


def simulate_positive_droplets(rng,sc,gs,prior, positive,lam,select_fraction=0.1, ref_gate=100):
    batch=make_batch(rng,sc,gs)
    score=[];genomes=[];multiplicities=[];k_total=[];n_valid=0
    for j in range(positive):
        ng=truncated_pois(rng,lam)
        dna_ids=rng.choice(len(gs), size=ng, p=prior)
        latent_sum=0.0; active_sum=0; total_copies=0
        for idx in dna_ids:
            r=optics.expression(rng,sc,gs[idx],batch)
            if np.isfinite(r['latent_ae']):
                latent_sum+=r['latent_ae']*r['copy_count']
            active_sum+=r['copy_count'];total_copies+=r['copy_count']
        green=rng.poisson(sc.photons_per_acceptor*latent_sum+sc.background_counts)
        red=rng.poisson(sc.photons_per_acceptor*active_sum+sc.background_counts)
        if red-sc.background_counts>=ref_gate:
            score.append(float((green-sc.background_counts)/(red-sc.background_counts)))
            genomes.append(dna_ids)
            multiplicities.append(ng)
            k_total.append(total_copies)
    n_valid=len(score)
    if n_valid<2:return None
    n_selected=max(1,int(round(select_fraction*n_valid)))
    winners=np.argpartition(np.asarray(score),-n_selected)[-n_selected:]
    selected_dna=[int(rng.choice(genomes[i])) for i in winners]
    counts=np.bincount(selected_dna,minlength=len(gs))
    return {
        'next_pool': counts/counts.sum(),
        'recovered':n_selected,
        'valid':n_valid,
        'doublet_fraction_occupied':float(np.mean(np.array(multiplicities)>1)),
        'doublet_fraction_selected':float(np.mean(np.array([multiplicities[i] for i in winners])>1)),
        'screened_occupied':positive,
        'total_droplets_equivalent':int(math.ceil(positive/(1-math.exp(-lam)))),
        'mean_copies_per_occupied':float(np.mean(k_total)),
        'mean_selected_ratio':float(np.mean(np.asarray(score)[winners])),
    }


def run(seed,sc,lam,positive,rounds):
    rng=np.random.default_rng(seed)
    gs=optics.genotypes(4)
    prior=np.ones(len(gs))/len(gs)
    near=np.array([sum(g[i] for i in (0,2,4)) for g in gs])
    high=near==3
    record=[]
    for ix in range(rounds):
        result=simulate_positive_droplets(rng,sc,gs,prior,positive,lam)
        if result is None:raise RuntimeError('gate eliminates all droplets')
        new=result.pop('next_pool')
        record.append({'round':ix+1,'high_three_near_before':float(prior@high),
                       'high_three_near_after':float(new@high),
                       'mean_nominal_AE_after':float(np.dot(new,[optics.ae(g) for g in gs])),**result})
        prior=new
    independent_fresh=optics.screen_population(rng,sc,gs,16)
    fresh_means=np.array([independent_fresh[g]['corrected_ae'] for g in gs])
    fresh_selected=float(prior@fresh_means)
    fresh_uniform=float(np.mean(fresh_means))
    incumbent=float(fresh_means[np.argmax([optics.ae(g) for g in gs])])
    return {'scenario':sc.name,'seed':seed,'lam':lam,'rounds':record,
            'fresh_reexpressed_AE_weighted_pool':fresh_selected,
            'fresh_reexpressed_AE_uniform_pool':fresh_uniform,
            'fresh_reexpressed_AE_incumbent_direct_geometric':incumbent,
            'final_genome_pool':{''.join(map(str,g)):float(prior[i]) for i,g in enumerate(gs)},
            'all_measurement_and_wet_recovery_rates_unmeasured':True}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--lambda-templates',type=float,default=0.05)
    p.add_argument('--positive',type=int,default=4000)
    p.add_argument('--rounds',type=int,default=2)
    p.add_argument('--seed',type=int,default=20261103)
    p.add_argument('--save',action='store_true')
    args=p.parse_args()
    out=[run(args.seed,sc,args.lambda_templates,args.positive,args.rounds) for sc in (optics.OPT,optics.STRESS)]
    for r in out:
        print(r['scenario'])
        for k in r['rounds']:
            print('  round',k['round'],'near-3 fraction',round(k['high_three_near_before'],4),'->',round(k['high_three_near_after'],4),
                  'sorted',k['recovered'],'of',k['total_droplets_equivalent'],'doublets-selected',round(k['doublet_fraction_selected'],4))
        print('  fresh selected/uniform/direct:',r['fresh_reexpressed_AE_weighted_pool'],r['fresh_reexpressed_AE_uniform_pool'],r['fresh_reexpressed_AE_incumbent_direct_geometric'])
    if args.save:
        Path('/mnt/data/pooled_photonic_selection_v2_results.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
