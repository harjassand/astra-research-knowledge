#!/usr/bin/env python3
"""Candidate recognition domains for a source-anchored ten-dimer 6HB photonic rod.
Twenty physical PDI-bearing positions, two isogeometric alternative site-specific
PDI staple products per position: 40 shared reagent stocks (NOT 40 dyes/object).
Allele b in {0,1} at paired unit j selects BOTH its PDI positions.
These are 24nt unmodified DNA domains, NOT full PDI phosphoramidite staples.
No caDNAno routing, full-sequence fold, physical mismatch kinetics or PDI backbone
melting model is available. Do not order/synthesize based on this file alone.
"""
import random, json
from pathlib import Path
from Bio.Seq import Seq
from Bio.SeqUtils import MeltingTemp as mt

RNG=random.Random(20261103)
A='ACGT'
def rc(s):return str(Seq(s).reverse_complement())
def longest(a,b):
    longest=0
    for offset in range(-len(b)+1,len(a)):
        run=0
        for i in range(max(0,offset),min(len(a),offset+len(b))):
            if a[i] == b[i-offset]:
                run+=1; longest=max(longest,run)
            else: run=0
    return longest
def tm(s):return float(mt.Tm_NN(s,Na=50,Mg=12,dnac1=100,dnac2=100))
def build():
    found=[]
    tries=0
    while len(found)<40 and tries<3000000:
        tries+=1
        s=''.join(RNG.choices(A,k=24))
        gc=(s.count('C')+s.count('G'))/24
        if not (.45<=gc<=.55) or any(b*4 in s for b in A):continue
        if longest(s,rc(s))>6 or not (69<=tm(s)<=76):continue
        if any(longest(s,v)>7 or longest(s,rc(v))>7 for v in found):continue
        found.append(s)
    if len(found)!=40:raise ValueError(f'found only {len(found)} after {tries} attempts')
    ds=[]
    for j in range(10):
        for locus in (0,1):
            for allele in (0,1):
                pos=4*j+2*locus+allele
                ds.append(dict(unit=j+1, position_in_pair=locus+1, allele=allele,
                               scaffold_24nt_5to3=found[pos],
                               PDI_staple_recognition_24nt_5to3=rc(found[pos]),
                               predicted_unmodified_duplex_Tm_C=round(tm(found[pos]),2)))
    return dict(status='IN_SILICO_ONLY_UNVALIDATED',n_genome_alleles=2**10,
                physical_positions_per_rod=20,shared_alternative_PDI_staple_stocks=40,
                staple_stock_identity='site-index-specific, PDI insertion position depends on allele',
                dye_count_per_correctly_expressed_rod=20, n_variable_scaffold_domains_per_genome=20,
                variable_scaffold_nt_per_genome=480,
                longest_non_cognate_contiguous_match=max(longest(s,rc(v)) for i,s in enumerate(found) for k,v in enumerate(found) if i!=k),
                Tm_unmodified_range_C=[round(min(tm(s) for s in found),2),round(max(tm(s) for s in found),2)],
                trials=tries,
                status_warnings=[
                    'The reported Tm is for an unmodified full DNA 24mer: PDI insertion into a staple backbone invalidates it',
                    'A 24-nt sequence motif cannot be asserted to sit on a structural staple or preserve 6HB routing',
                    'Global folding, intramolecular off-target, and strand-swap cross-talk are unchecked',
                    'Source Gorman 2024 folded distinct separately supplied staple sets, not this mixed genotype/cargo ensemble',
                    'Proposed geometry changes 0Delta vs 4Delta need complete crossovers and PDI insertion maps'],
                cassettes=ds)
if __name__=='__main__':
    d=build();out=Path('/mnt/data/pdi_common_bath_cassette_code_unvalidated.json')
    out.write_text(json.dumps(d,indent=2));print(out)
    print('all',len(d['cassettes']),'trials',d['trials'],'Tm',d['Tm_unmodified_range_C'],'max nc',d['longest_non_cognate_contiguous_match'])
    for rec in d['cassettes'][:8]:print(rec)
