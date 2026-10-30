"""Opaque COMPUTATIONAL native source for one complete receiver experiment.

No physical source/device is acquired. Born probabilities are exact rational
Heisenberg contractions for a128-qubit Clifford with mixed magic junk;
63-bit rounded tickets are then drawn by one seeded PCG64. Ideal-IID risk
claims belong to the mathematical contract, not to the seeded PRNG.
Receiver code does NOT import this backend or read its hidden model.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import random
import time

import numpy as np

from pauli_compiler import canonical,make_tableau,map_tableau,inverse,sign

BASE=Path(__file__).resolve().parent
N=128; LOGICAL=63; PATCH=list(range(61,66))
SOURCE_ID='native128-depth2-mixedmagic-v1'
CODE=(0,1,3,2)  # local digit I,X,Y,Z -> (x,z) bit code x+2z


def save(name,x):
    (BASE/name).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')


def source_gates():
    rr=random.Random(20261030)
    junk=[i for i in range(N) if i!=LOGICAL]
    jg=[]
    for _ in range(4*N):
        a,b=rr.sample(junk,2)
        jg.append(('CX',a,b))
        jg.append((rr.choice(('H','S')),a))
    ug=[]
    for layer in range(2):
        for i in range(N):
            for _ in range(rr.randrange(3)):ug.append((rr.choice(('H','S')),i))
        for i in range(layer,N-1,2):
            ug.append(('CX',i,i+1) if rr.getrandbits(1) else ('CX',i+1,i))
    for i in range(N):
        for _ in range(rr.randrange(3)):ug.append((rr.choice(('H','S')),i))
    return jg,ug


class Source:
    def __init__(self,seed=20261030027):
        self.jg,self.ug=source_gates()
        self.inverse_tableau=make_tableau(N,inverse(self.jg+self.ug))
        self.noise_p=F(1,500);self.rotation_t=F(1,100)
        self.mu=1-self.noise_p
        self.cos=(1-self.rotation_t**2)/(1+self.rotation_t**2)
        self.sin=2*self.rotation_t/(1+self.rotation_t**2)
        self.rng=np.random.Generator(np.random.PCG64(seed))
        self.source_reads=0;self.ticket_TV=F(0)

    @lru_cache(None)
    def ideal_expect(self,ref,x,z,p):
        xx,zz,pp=map_tableau((x,z,p),self.inverse_tableau)
        logical=((xx>>LOGICAL)&1)+2*((zz>>LOGICAL)&1)
        if logical!=CODE[ref]:return F(0)
        neg=-1 if ref==2 else 1  # <Phi|Y tensor Y|Phi>=-1
        m=1<<LOGICAL;xx&=~m;zz&=~m
        # The raw phase of the stripped Y is removed with that local factor.
        pp=(pp-int(logical==3))%4
        return neg*sign((xx,zz,pp))*F(2,5)**((xx|zz).bit_count())

    @lru_cache(None)
    def expect(self,ref,x,z,p):
        """Actual fixed local rotation followed by depolarization; rational."""
        terms=[((0,0,0),F(1))]
        for j in range(N):
            a=(x>>j)&1;b=(z>>j)&1
            if not(a or b):continue
            if a and not b:options=[(1,0,self.mu*self.cos),(1,1,-self.mu*self.sin)]
            elif a and b:options=[(1,0,self.mu*self.sin),(1,1,self.mu*self.cos)]
            else:options=[(0,1,self.mu)]
            new=[]
            for (xx,zz,pp),w in terms:
                for aa,bb,v in options:
                    new.append(((xx|(aa<<j),zz|(bb<<j),(pp+aa*bb)%4),w*v))
            terms=new
        sg=sign((x,z,p))
        return sg*sum((w*self.ideal_expect(ref,*a) for a,w in terms),F(0))

    def tickets(self,prob,m):
        assert all(p>=0 for p in prob) and sum(prob)==1
        D=1<<63;prefix=F(0);cuts=[]
        for p in prob:
            prefix+=p;cuts.append((D*prefix.numerator)//prefix.denominator)
        assert cuts[-1]==D and cuts==sorted(cuts)
        ticket=self.rng.bit_generator.random_raw(m)>>np.uint64(1)
        out=np.searchsorted(np.asarray(cuts,dtype=np.uint64),ticket,side='right')
        hist=np.bincount(out,minlength=len(prob)).tolist()
        self.source_reads+=m;self.ticket_TV+=F(m*(len(prob)-1),D)
        return hist

    def local_law(self,ref,axes):
        w=len(PATCH);coeff=[]
        for mask in range(1<<(w+1)):
            x=z=0
            for j,site in enumerate(PATCH):
                if (mask>>j)&1:
                    a=CODE[axes[j]];x|=(a&1)<<site;z|=((a>>1)&1)<<site
            a=canonical(x,z)
            coeff.append(self.expect(ref if (mask>>w)&1 else 0,*a))
        # Exact Walsh transform gives all joint product-measurement probabilities.
        out=list(coeff);stride=1
        while stride<len(out):
            for i in range(0,len(out),2*stride):
                for j in range(stride):
                    a,b=out[i+j],out[i+j+stride];out[i+j]=a+b;out[i+j+stride]=a-b
            stride*=2
        return [p/len(out) for p in out]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode',choices=['discover','validate','audit'])
    args=ap.parse_args();start=time.perf_counter()
    src=Source(20261030027+['discover','validate','audit'].index(args.mode))
    if args.mode=='discover':
        shots=2048;rows=[]
        for ref in (1,3):
            for axes in itertools.product((1,2,3),repeat=len(PATCH)):
                rows.append({'reference':ref,'axes':list(axes),
                             'histogram':src.tickets(src.local_law(ref,axes),shots)})
        contract={'source_id':SOURCE_ID,'n':N,'q':1,'patch':PATCH,
                  'output_site':LOGICAL,'discovery_shots_per_setting':shots,
                  'discovery_absolute_error':'1/8','concentration_log_upper':16,
                  'validation_shots_per_candidate':65536,
                  'detector_and_known_gate_scope':'ideal known product-Pauli measurements; source contains unknown local coherent/depolarizing calibration',
                  'risk_model':'fixed memoryless CPTP source, fresh independent ideal shots; actual seeded ticket run is numerical',
                  'source_device_admission':'NOT_ACQUIRED'}
        save('INPUT_CONTRACT.json',contract)
        save('DISCOVERY_HISTOGRAMS.json',{'source_id':SOURCE_ID,'rows':rows})
    elif args.mode=='validate':
        req=json.loads((BASE/'VALIDATION_REQUEST.json').read_text())
        assert req['source_id']==SOURCE_ID
        rows=[]
        for r in req['candidates']:
            a=tuple(r['physical_pauli']);mean=src.expect(r['reference'],*a)
            bad,good=src.tickets([(1-mean)/2,(1+mean)/2],r['shots'])
            rows.append({'reference':r['reference'],'physical_pauli':list(a),
                         'shots':r['shots'],'bad':bad})
        save('VALIDATION_COUNTS.json',{'source_id':SOURCE_ID,
             'request_sha256':hashlib.sha256((BASE/'VALIDATION_REQUEST.json').read_bytes()).hexdigest(),
             'rows':rows})
    else:
        from pauli_compiler import apply
        dec=json.loads((BASE/'DECODER.json').read_text());inv=inverse(dec['routed_gates'])
        physical=[(0,0,0)]+[apply(canonical((1<<LOGICAL) if p in(1,2) else 0,
                                             (1<<LOGICAL) if p in(2,3) else 0),inv)
                              for p in(1,2,3)]
        corr={str(p):src.expect(p,*physical[p]) for p in(1,2,3)}
        fe=(1+corr['1']-corr['2']+corr['3'])/4
        save('TRUTH_AUDIT.json',{'scope':'exact rational same-source analysis; NOT a learner input',
             'decoded_Bell_correlations':{k:str(v) for k,v in corr.items()},
             'actual_decoded_Bell_fidelity':str(fe),
             'actual_decoded_Bell_fidelity_decimal':float(fe),
             'junk_preparation_Clifford_gates':len(src.jg),'unknown_shallow_Clifford_gates':len(src.ug),
             'arbitrary_junk_instance':'global Clifford of127 full-rank mixed magic qubits with Bloch(2/5,2/5,2/5)',
             'source_noise':'per-output depolarizingp1/500 after coherentZrotation with tan(theta/2)=1/100',
             'full_source_density_matrix_materialized':False})
    save('SOURCE_'+args.mode.upper()+'_EXECUTION.json',{
         'mode':args.mode,'scope':'exact rational Born laws + seeded rounded-ticket numerical application, no quantum device',
         'source_program_reads':src.source_reads,'requested_PCG64_bits':64*src.source_reads,
         'ideal_rounded_law_total_variation_upper':str(src.ticket_TV),
         'seconds_after_imports':time.perf_counter()-start,
         'actual_seeded_PRNG_not_an_IID_law_qualification':True})
    print(args.mode,src.source_reads,'reads',time.perf_counter()-start,'seconds')


if __name__=='__main__':main()
