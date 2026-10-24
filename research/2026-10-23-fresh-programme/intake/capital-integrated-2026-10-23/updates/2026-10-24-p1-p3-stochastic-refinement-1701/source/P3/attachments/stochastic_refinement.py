"""Least universal rational-linear stochastic refinement from explicit jump lists.

This executable is an exact-arithmetic prototype, not an optimized solver. It
does not enumerate population states in order to acquire or verify the quotient.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import re
import time

from quotient_actions import Network, Echelon, add, close_space, encode, project_residual, same_span


@dataclass
class Jump:
    label: str
    nu: dict[int,Q]
    # (independent parameter label, repeated-index monomial) -> rational coefficient
    propensity: dict[tuple[str,tuple[int,...]],Q]


@dataclass
class JumpSystem:
    names: list[str]
    initial: list[Q]
    parameter_values: dict[str,Q]
    jumps: list[Jump]
    provenance: dict

    @property
    def n(self): return len(self.names)


def phosphorylation(path):
    net=Network(path)
    return JumpSystem(net.names,net.initial,net.constants,
        [Jump(r.label,r.stoich,{(r.parameter,r.reactants):r.coefficient}) for r in net.reactions],
        {'path':str(path),'sha256':net.sha256,'interpretation':'Source mass action; all reactants distinct so stochastic and deterministic monomials coincide; symbolic catalysts interpreted as rate parameters.'})


def parse_named_rate_source(path):
    path=Path(path);raw=path.read_text();vals={}
    for line in raw.split('begin init')[1].split('end init')[0].splitlines():
        z=line.strip().split('=')
        if z[0].strip(): vals[z[0].strip()]=Q(z[1].strip()) if len(z)==2 else Q(0)
    source=[];species=set();parameters=set()
    for line in raw.split('begin reactions')[1].split('end reactions')[0].splitlines():
        line=line.strip()
        if not line:continue
        lhs,tail=line.split('->');rhs,rate=tail.rsplit(',',1);rate=rate.strip()
        a=Counter(s.strip() for s in lhs.split('+'));b=Counter(s.strip() for s in rhs.split('+'))
        species.update(a);species.update(b);parameters.add(rate)
        source.append((line,a,b,rate))
    names=[s for s in vals if s in species];index={s:i for i,s in enumerate(names)}
    assert not species.intersection(parameters)
    assert set(names)==species
    jumps=[]
    for line,a,b,par in source:
        # Explicitly refuse an unimplemented falling-factorial convention.
        if any(k!=1 for k in a.values()):raise ValueError('Repeated stochastic reactant needs falling-factorial expansion')
        mon=tuple(sorted(index[s] for s in a))
        nu={index[s]:Q(b[s]-a[s]) for s in a.keys()|b.keys() if b[s]!=a[s]}
        jumps.append(Jump(line,nu,{(par,mon):Q(1)}))
    return JumpSystem(names,[vals[s] for s in names],{p:vals[p] for p in parameters},jumps,
        {'path':str(path),'sha256':hashlib.sha256(raw.encode()).hexdigest(),
         'interpretation':'All reaction species including constant genes and artificial sink retained; arrow rate symbols treated independently. All reactants distinct.'})


def projected_jump(L,nu):
    return tuple(sum(row.get(i,0)*a for i,a in nu.items()) for row in L)


def group_propensities(system,L):
    groups={};members=defaultdict(list);coefficient_additions=0
    for j,rxn in enumerate(system.jumps):
        delta=projected_jump(L,rxn.nu)
        members[delta].append(j)
        p=groups.setdefault(delta,{})
        for key,c in rxn.propensity.items():
            add(p,key,c);coefficient_additions+=1
    return groups,dict(members),coefficient_additions


def gradient_rows(propensity):
    out={}
    for (par,mon),c in propensity.items():
        for j,k in Counter(mon).items():
            m=list(mon);m.remove(j)
            add(out.setdefault((par,tuple(m)),{}),j,c*k)
    return {k:v for k,v in out.items() if v}


def drift_matrices(system):
    mats={}
    for jump in system.jumps:
        for key,row in gradient_rows(jump.propensity).items():
            M=mats.setdefault(key,{})
            for i,nu in jump.nu.items():
                for j,c in row.items():add(M,(i,j),nu*c)
    return {k:m for k,m in mats.items() if m}


def refine(system,seed):
    t0=time.perf_counter();space=Echelon(system.n)
    for row in seed:space.insert(row)
    initial_rank=len(space.rows);rounds=[];witnesses=[]
    for iteration in range(system.n-initial_rank+1):
        L,pivots=space.rref();groups,members,adds=group_propensities(system,L)
        oldrank=len(space.rows);tested=0;added=[]
        # Freeze the old grouping throughout a round. Regroup after all additions.
        for delta,poly in groups.items():
            if not any(delta):continue
            for key,row in gradient_rows(poly).items():
                tested+=1
                p=space.insert(row)
                if p is not None:
                    added.append(p)
                    witnesses.append({'round':iteration,'old_rank':oldrank,'projected_jump':delta,
                                      'source_reactions':members[delta],
                                      'gradient_coefficient_key':key,'necessary_row':row})
        rounds.append({'rank_before':oldrank,'rank_after':len(space.rows),
                       'projected_jump_groups_including_zero':len(groups),
                       'nonzero_groups':sum(any(d) for d in groups),
                       'source_coefficient_additions':adds,'gradient_rows_tested':tested,
                       'new_pivots':added})
        if not added:break
    else:raise AssertionError('Rank termination bound violated')
    L,pivots=space.rref();groups,members,adds=group_propensities(system,L)
    certificate_checks=0
    for delta,poly in groups.items():
        if not any(delta):continue
        for row in gradient_rows(poly).values():
            assert not project_residual(row,L,pivots)
            certificate_checks+=1
    # Canonical R sets all nonpivot x coordinates to zero. Keep q(Ry) factored;
    # here each source propensity is a monomial, so only pivot-only terms survive.
    pindex={j:i for i,j in enumerate(pivots)};compiled=[]
    for delta,poly in groups.items():
        if not any(delta):continue
        qbar={}
        for (par,mon),c in poly.items():
            if all(j in pindex for j in mon):
                add(qbar,(par,tuple(sorted(pindex[j] for j in mon))),c)
        compiled.append({'delta':delta,'propensity':qbar,'source_reactions':members[delta]})
    return {'L':L,'pivots':pivots,'initial_rank':initial_rank,'rank':len(L),
            'rounds':rounds,'necessary_extension_witnesses':witnesses,
            'compiled_jumps':compiled,'exact_certificate_gradient_checks':certificate_checks,
            'rational_elimination_updates':space.reduction_updates,
            'max_basis_coefficient_bits':space.max_bits,'seconds':time.perf_counter()-t0}


def eval_poly(poly,x,parameters):
    result=Q(0)
    for (par,mon),c in poly.items():
        a=c*(parameters[par] if par else Q(1))
        for j in mon:a*=x[j]
        result+=a
    return result


def eval_compiled(compiled,y,parameters):
    return {tuple(j['delta']):eval_poly(j['propensity'],y,parameters) for j in compiled}


def output(L,x):
    return tuple(sum(a*x[j] for j,a in row.items()) for row in L)


def exact_generator_checks(system,result,states):
    checks=0
    for x in states:
        y=output(result['L'],x);actual=defaultdict(Q)
        for rxn in system.jumps:
            delta=projected_jump(result['L'],rxn.nu)
            if any(delta):actual[delta]+=eval_poly(rxn.propensity,x,system.parameter_values)
        compiled=eval_compiled(result['compiled_jumps'],y,system.parameter_values)
        for delta,rate in compiled.items():
            assert rate==actual[delta]
            assert rate>=0
            checks+=2
    return checks


def noise_intervention(system):
    # Source one-based reactions 6 and4 have opposite projected mean increments.
    # Add eta*kOnE*E*S3 to both hazards. Relative controls are eta for6 and
    # eta*(kOnE/kOffE)*E for4. No inverse E, and neither creates boundary jumps.
    E=system.names.index('S0');s3=system.names.index('S3')
    return JumpSystem(system.names,system.initial,{**system.parameter_values,'eta_kOnE':Q(7,10)},
        system.jumps+[Jump('extra binding source reaction6',dict(system.jumps[5].nu),{('eta_kOnE',tuple(sorted((E,s3)))):Q(1)}),
                      Jump('extra dissociation source reaction4',dict(system.jumps[3].nu),{('eta_kOnE',tuple(sorted((E,s3)))):Q(1)})],
        {**system.provenance,'intervention':'Root-designed mathematical channel feedback on independent source; eta=1 for algebra. Rates/actuation not empirically acquired.'})


def check_noise_witness(system,L):
    # E=F=1, one protein in EU versus UE. Same old representation.
    xa=[Q(0)]*system.n;xb=list(xa)
    for x in (xa,xb):x[0]=x[1]=Q(1)
    xa[system.names.index('S3')]=Q(1);xb[system.names.index('S4')]=Q(1)
    assert output(L,xa)==output(L,xb)
    extra=system.jumps[-2:];drifts=[];variations=[]
    for x in (xa,xb):
        drift=[Q(0)]*len(L);var=Q(0)
        for rxn in extra:
            d=projected_jump(L,rxn.nu);q=eval_poly(rxn.propensity,x,system.parameter_values)
            for i,v in enumerate(d):drift[i]+=q*v
            var+=q*d[0]**2
        drifts.append(drift);variations.append(var)
    assert not any(drifts[0]) and not any(drifts[1])
    assert variations==[Q(7,5),Q(0)]
    return {'same_macro_state':output(L,xa),'hidden_states':[xa,xb],
            'added_drift':drifts,'added_free_kinase_quadratic_variation':variations,
            'legal_boundary_note':'Both added rates contain E*S3; at E=0 or S3=0 they vanish.'}


def algebraic_audits():
    # Deliberately authored counterexample audits, never scientific efficacy cases.
    # Hidden jump is initially invisible; first new rate row makes it visible.
    sys=JumpSystem(['X','B','C'],[Q(0),Q(1),Q(1)],{},[
        Jump('B-catalyzed X birth',{0:Q(1)},{('',(1,)):Q(1)}),
        Jump('C-catalyzed B birth',{1:Q(1)},{('',(2,)):Q(1)})],{'authored':True})
    rr=refine(sys,[{0:Q(1)}]);assert [z['rank_after'] for z in rr['rounds']]==[2,3,3]
    # Nonlinear propensity must be differentiated as a full polynomial.
    fall=JumpSystem(['X','B'],[Q(0),Q(2)],{},[
        Jump('2B catalyzes X birth',{0:Q(1)},{('',(1,1)):Q(1),('',(1,)):Q(-1)})],{'authored':True})
    ff=refine(fall,[{0:Q(1)}]);assert ff['rank']==2
    # Global versus a frozen N=1 class: the same source channel never fires there.
    assert eval_poly(fall.jumps[0].propensity,[Q(0),Q(0)],{})==0
    assert eval_poly(fall.jumps[0].propensity,[Q(0),Q(1)],{})==0
    return {'regrouping_rank_path':[z['rank_after'] for z in rr['rounds']],
            'falling_factorial_rank':ff['rank'],
            'fixed_class_full_domain_distinction_checked':True,
            'scope':'Authored known proof challenges, no unseen efficacy claim.'}


def run(phosph_path,quorum_path):
    t0=time.perf_counter();out={'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'imports_sha256':hashlib.sha256(Path(__file__).with_name('quotient_actions.py').read_bytes()).hexdigest(),
         'exposure':'Source m2 and quorum equations known before this development run; new refinement outcomes not yet executed. This is development, not held-out transfer.'}
    systems={'phosphorylation':phosphorylation(phosph_path),'quorum_sensing':parse_named_rate_source(quorum_path)}
    for name,s in systems.items():
        obs=[{0:Q(1)},{1:Q(1)}] if name=='phosphorylation' else [{s.names.index('AI2_extra'):Q(1)}]
        L,p,receipt=close_space(s.n,obs,drift_matrices(s))
        warm=refine(s,L);fresh=refine(s,obs)
        assert same_span(warm['L'],fresh['L'],s.n)
        states=[s.initial,[Q(1)]*s.n,[Q((j*7+3)%11) for j in range(s.n)]]
        checks=exact_generator_checks(s,warm,states)
        out[name]={'source':s.provenance,'species':s.n,'channels':len(s.jumps),
                   'observable_rows':obs,'drift_acquisition':receipt,'warm':warm,'fresh':fresh,
                   'warm_fresh_same_space':True,'exact_numeric_generator_checks':checks,
                   'distinct_columns_of_drift_L':len({tuple(row.get(j,0) for row in L) for j in range(s.n)}),
                   'source_parameter_defaults':s.parameter_values}
        if name=='phosphorylation':
            changed=noise_intervention(s)
            L2,p2,r2=close_space(s.n,obs,drift_matrices(changed))
            assert same_span(L,L2,s.n)
            extension=refine(changed,L)
            direct=refine(changed,obs)
            assert same_span(extension['L'],direct['L'],s.n)
            out['mean_preserving_noise_intervention']={'source':changed.provenance,
                'drift_same_as_old_representation':True,'drift_acquisition':r2,
                'witness':check_noise_witness(changed,L),'warm':extension,'fresh':direct,
                'warm_fresh_same_space':True,
                'exact_numeric_generator_checks':exact_generator_checks(changed,extension,states)}
    out['algebraic_challenges']=algebraic_audits();out['total_seconds']=time.perf_counter()-t0
    return out


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('phosph_source');ap.add_argument('quorum_source');ap.add_argument('output')
    a=ap.parse_args();dest=Path(a.output)
    if dest.exists():raise SystemExit('Refuse to overwrite execution receipt')
    start=time.perf_counter()
    try:
        data=run(a.phosph_source,a.quorum_source);dest.write_text(json.dumps(encode(data),indent=2)+'\n')
        print(json.dumps({name:{'species':v.get('species'),'drift_rank':v.get('drift_acquisition',{}).get('rank'),
                    'stochastic_rank':v.get('warm',{}).get('rank'),'rounds':v.get('warm',{}).get('rounds'),
                    'warm_seconds':v.get('warm',{}).get('seconds'),'fresh_seconds':v.get('fresh',{}).get('seconds')}
                  for name,v in data.items() if isinstance(v,dict) and 'warm' in v}))
        print(json.dumps({'algebraic_challenges':data['algebraic_challenges'],'total_seconds':data['total_seconds']}))
    except BaseException as exc:
        dest.with_suffix('.FAILED.json').write_text(json.dumps({'exception':repr(exc),'seconds':time.perf_counter()-start,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
        raise
