"""New Pro3 source acquisition for a conditional-component event interface.

This is new work, not a reconstruction of missing historical helpers.  The
input language is finite Boolean sites, conjunctions of equality guards,
constant nonnegative rational rates, single-site silent writes, and marked
events with fixed-write resets.  It is not a Kappa/BioNetGen graph compiler.

Construction theorem (row-vector convention).  On every accepted input,
before the next marked event the silent generator is

  Q_C + sum_b Q_b(c),

where Q_C is autonomous.  Each marked hazard depends on the controller and
at most one acquired component.  Thus, conditional on a complete controller
path and an initial mixture branch, the surviving component processes are
independent killed finite chains.  Fixed-write event resets are products of
component maps and a controller map.  The initial law is an explicitly given
positive mixture of controller point masses and component product laws.

Proof: each silent rule writing C is checked to read only C.  Residual
read/write scopes and event read scopes are joined into connected components
(or checked against a requested partition).  A rule's exact rational rate is
then added to its local transition or hazard table for every matching local
assignment.  Lifting the resulting table to any global assignment recovers
the original rule rate.  Summing rules proves the generator/hazard identity.
An initial factor is confined to one component, and fixed writes never read
another component, proving the two product-law claims.  compile_interface
enumerates controller configurations and individual component configurations,
never their Cartesian product.  These local spaces can still be large; the
explicit limits reject them before allocation.  A separate 4-site reference
check below expands 16 assignments to check this implementation.

An accepting source certificate does not imply a small numerical history
mixture, a small posterior error, or an autonomous controller after an
arbitrary unsupported reset.  Numerical entrance certificates live in the
separate entrance executors.  Syntactic scope checking is sufficient, not
semantically complete: cancellation or redundant guards are not analyzed.
"""

from dataclasses import dataclass, replace
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


class SourceError(ValueError):
    """A rejection category and source-level witness, suitable for repair."""

    def __init__(self, category, **witness):
        self.category = category
        self.witness = witness
        super().__init__(f"{category}: {witness}")


@dataclass(frozen=True)
class Rule:
    name: str
    guard: tuple
    update: tuple
    rate: F
    mark: str | None = None


@dataclass(frozen=True)
class InitialFactor:
    sites: tuple
    # Lexicographic Boolean state order on these sites.
    probabilities: tuple


@dataclass(frozen=True)
class InitialBranch:
    weight: F
    controller_assignment: tuple
    factors: tuple


@dataclass(frozen=True)
class Program:
    nsites: int
    controller: tuple
    rules: tuple
    initial: tuple
    # Optional requested partition.  Otherwise infer components from scopes.
    leaf_blocks: tuple | None = None


@dataclass(frozen=True)
class Limits:
    max_controller_states: int = 256
    max_component_states: int = 256
    max_operator_entries: int = 1000000


@dataclass(frozen=True)
class Component:
    sites: tuple
    states: tuple
    generators: tuple  # One rational row generator per controller state.


@dataclass(frozen=True)
class Event:
    name: str
    mark: str
    owner: int | None
    hazards: tuple  # Controller-indexed local vectors; length 1 if owner=None.
    controller_reset: tuple
    # Only nonidentity fixed-write maps need storage.
    component_resets: tuple


@dataclass(frozen=True)
class CompiledInitial:
    weight: F
    controller_state: int
    component_rows: tuple


@dataclass(frozen=True)
class Interface:
    nsites: int
    controller: tuple
    controller_states: tuple
    controller_generator: tuple
    components: tuple
    events: tuple
    initial: tuple

    def killed_generator(self, component, controller_state):
        q = self.components[component].generators[controller_state]
        result = [list(row) for row in q]
        for event in self.events:
            if event.owner == component:
                for i, value in enumerate(event.hazards[controller_state]):
                    result[i][i] -= value
        return tuple(tuple(row) for row in result)

    def controller_killing(self, controller_state):
        return sum((event.hazards[controller_state][0] for event in self.events
                    if event.owner is None), F(0))


def rational(value, location):
    if not isinstance(value, (int, F)):
        raise SourceError('nonexact_number', location=location, value=repr(value))
    if value < 0:
        raise SourceError('negative_number', location=location, value=str(value))
    return F(value)


def assignments(value, nsites, location):
    result = {}
    for site, bit in value:
        if type(site) is not int or not 0 <= site < nsites or bit not in (0, 1):
            raise SourceError('invalid_assignment', location=location,
                              assignment=(site, bit))
        if site in result:
            raise SourceError('repeated_site', location=location, site=site)
        result[site] = bit
    return result


def states(sites):
    return tuple(product((0, 1), repeat=len(sites)))


def matching(guard, environment):
    return all(environment[site] == bit for site, bit in guard.items())


def local_generator(sites, local_states, rule_data, controller_env):
    index = {state: i for i, state in enumerate(local_states)}
    q = [[F(0) for _ in local_states] for _ in local_states]
    for i, state in enumerate(local_states):
        env = controller_env | dict(zip(sites, state))
        for rule, guard, update in rule_data:
            if matching(guard, env):
                changed = env | update
                j = index[tuple(changed[site] for site in sites)]
                if i != j:
                    q[i][j] += F(rule.rate)
                    q[i][i] -= F(rule.rate)
    return tuple(tuple(row) for row in q)


def compile_interface(source, limits=Limits()):
    """Acquire local operators without forming the product of their spaces."""
    n = source.nsites
    if type(n) is not int or n < 1:
        raise SourceError('invalid_site_count', nsites=n)
    controller = tuple(sorted(source.controller))
    if (len(set(controller)) != len(controller)
            or any(type(i) is not int or not 0 <= i < n for i in controller)):
        raise SourceError('invalid_controller', sites=source.controller)
    cset = set(controller)
    leaf_sites = set(range(n)) - cset
    data = []
    names = set()
    for rule in source.rules:
        if not isinstance(rule.name, str) or not rule.name or rule.name in names:
            raise SourceError('invalid_rule_name', name=rule.name)
        names.add(rule.name)
        rational(rule.rate, rule.name + '.rate')
        guard = assignments(rule.guard, n, rule.name + '.guard')
        update = assignments(rule.update, n, rule.name + '.update')
        if rule.mark is None:
            if len(update) != 1:
                raise SourceError('silent_write_arity', rule=rule.name,
                                  written_sites=sorted(update))
            if set(update) <= cset and set(guard) - cset:
                raise SourceError('controller_not_autonomous', rule=rule.name,
                                  leaf_reads=sorted(set(guard) - cset))
        elif not isinstance(rule.mark, str) or not rule.mark:
            raise SourceError('invalid_event_mark', rule=rule.name, mark=rule.mark)
        data.append((rule, guard, update))

    # Locality scopes include hazards as well as silent dynamics.  A coupled
    # hazard can be handled by merging residual components, subject to budget.
    scopes = []
    for rule, guard, update in data:
        if rule.rate == 0:
            continue
        scope = ((set(guard) | set(update)) if rule.mark is None else set(guard)) - cset
        if scope:
            scopes.append((rule.name, tuple(sorted(scope))))
    if source.leaf_blocks is None:
        parent = {site: site for site in leaf_sites}

        def root(site):
            while parent[site] != site:
                parent[site] = parent[parent[site]]
                site = parent[site]
            return site

        for _, scope in scopes:
            for site in scope[1:]:
                parent[root(site)] = root(scope[0])
        groups = {}
        for site in sorted(leaf_sites):
            groups.setdefault(root(site), []).append(site)
        blocks = tuple(sorted((tuple(group) for group in groups.values())))
    else:
        blocks = tuple(tuple(sorted(block)) for block in source.leaf_blocks)
        flat = [site for block in blocks for site in block]
        if any(not block for block in blocks) or len(flat) != len(set(flat)) or set(flat) != leaf_sites:
            raise SourceError('invalid_component_partition', blocks=blocks)
    owner = {site: b for b, block in enumerate(blocks) for site in block}
    for rule_name, scope in scopes:
        touched = sorted({owner[site] for site in scope})
        if len(touched) > 1:
            raise SourceError('component_scope_crossing', rule=rule_name,
                              leaf_scope=scope, components=touched)
    ccount = 2 ** len(controller)
    sizes = [2 ** len(block) for block in blocks]
    if ccount > limits.max_controller_states:
        raise SourceError('controller_state_budget', required=ccount,
                          allowed=limits.max_controller_states)
    for block, size in zip(blocks, sizes):
        if size > limits.max_component_states:
            involved = [name for name, scope in scopes if set(scope) & set(block)]
            raise SourceError('component_state_budget', sites=block, required=size,
                              allowed=limits.max_component_states, rules=involved)
    entries = ccount * ccount + ccount * sum(size * size for size in sizes)
    if entries > limits.max_operator_entries:
        raise SourceError('operator_entry_budget', required=entries,
                          allowed=limits.max_operator_entries)

    cstates = states(controller)
    cindex = {state: i for i, state in enumerate(cstates)}
    cenvs = [dict(zip(controller, state)) for state in cstates]
    crules = [(r, g, u) for r, g, u in data
              if r.mark is None and r.rate and set(u) <= cset]
    cq = local_generator(controller, cstates, crules, {})
    components = []
    for b, block in enumerate(blocks):
        local_states = states(block)
        local_rules = [(r, g, u) for r, g, u in data
                       if r.mark is None and r.rate and set(u) - cset
                       and owner[next(iter(u))] == b]
        generators = tuple(local_generator(block, local_states, local_rules, env)
                           for env in cenvs)
        components.append(Component(block, local_states, generators))

    events = []
    for rule, guard, update in data:
        if rule.mark is None or not rule.rate:
            continue
        leaf_read = set(guard) - cset
        b = owner[next(iter(leaf_read))] if leaf_read else None
        local_states = components[b].states if b is not None else ((),)
        block = blocks[b] if b is not None else ()
        hazards = tuple(tuple(F(rule.rate) if matching(guard, env | dict(zip(block, state)))
                              else F(0) for state in local_states) for env in cenvs)
        creset = tuple(cindex[tuple((env | update)[site] for site in controller)] for env in cenvs)
        resets = []
        for dest in sorted({owner[site] for site in set(update) - cset}):
            component = components[dest]
            index = {state: i for i, state in enumerate(component.states)}
            mapping = tuple(index[tuple((dict(zip(component.sites, state)) | update)[site]
                                         for site in component.sites)] for state in component.states)
            resets.append((dest, mapping))
        events.append(Event(rule.name, rule.mark, b, hazards, creset, tuple(resets)))

    initial = []
    total_weight = F(0)
    for a, branch in enumerate(source.initial):
        weight = rational(branch.weight, f'initial[{a}].weight')
        total_weight += weight
        cenv = assignments(branch.controller_assignment, n, f'initial[{a}].controller')
        if set(cenv) != cset:
            raise SourceError('initial_controller_scope', branch=a,
                              supplied=sorted(cenv), required=controller)
        per_block = [[] for _ in blocks]
        covered = set()
        for f, factor in enumerate(branch.factors):
            sites = tuple(factor.sites)
            if (not sites or len(set(sites)) != len(sites) or not set(sites) <= leaf_sites
                    or covered & set(sites)):
                raise SourceError('initial_factor_partition', branch=a, factor=f, sites=sites)
            covered.update(sites)
            touched = {owner[site] for site in sites}
            if len(touched) != 1:
                raise SourceError('initial_factor_crossing', branch=a, factor=f,
                                  sites=sites, components=sorted(touched))
            probabilities = tuple(rational(p, f'initial[{a}].factor[{f}]') for p in factor.probabilities)
            if len(probabilities) != 2 ** len(sites) or sum(probabilities, F(0)) != 1:
                raise SourceError('initial_factor_not_probability', branch=a, factor=f,
                                  entries=len(probabilities), sum=str(sum(probabilities, F(0))))
            per_block[next(iter(touched))].append((sites, dict(zip(states(sites), probabilities))))
        if covered != leaf_sites:
            raise SourceError('initial_sites_missing', branch=a, missing=sorted(leaf_sites - covered))
        rows = []
        for b, component in enumerate(components):
            row = []
            for state in component.states:
                env = dict(zip(component.sites, state))
                probability = F(1)
                for sites, table in per_block[b]:
                    probability *= table[tuple(env[site] for site in sites)]
                row.append(probability)
            rows.append(tuple(row))
        initial.append(CompiledInitial(weight, cindex[tuple(cenv[site] for site in controller)], tuple(rows)))
    if total_weight != 1:
        raise SourceError('initial_weights_not_probability', sum=str(total_weight))
    return Interface(n, controller, cstates, cq, tuple(components), tuple(events), tuple(initial))


def star_source(n=24, gamma=F(7, 10)):
    """The same scientific parameters as tensor_separator_entrance.run_case."""
    rules = [Rule('controller_opens', ((0, 0),), ((0, 1),), gamma)]
    factors = []
    for i in range(n):
        site = i + 1
        alpha = F(3, 5) + F(i, 100)
        beta = F(2, 5) + F(i % 5, 50)
        kappa = F(3, 2) + F(i % 3, 10)
        rules.extend((Rule(f'up_{i}', ((site, 0),), ((site, 1),), alpha),
                      Rule(f'down_{i}', ((site, 1),), ((site, 0),), beta),
                      Rule(f'event_{i}', ((0, 1), (site, 1)), ((site, 0),), kappa, f'reaction_{i}')))
        factors.append(InitialFactor((site,), (beta / (alpha + beta), alpha / (alpha + beta))))
    return Program(n + 1, (0,), tuple(rules),
                   (InitialBranch(F(1), ((0, 0),), tuple(factors)),))


def one_open_binary_executor(interface, event_mark, time):
    """Checked bridge to the AVAILABLE specialized correlated entrance code.

    The general source compiler is broader than this numerical executor.  The
    bridge rejects recurrent controllers, controller-dependent local silent
    rates, nonstationary initialization, and unsupported event/reset patterns.
    """
    from tensor_separator_entrance import BinaryModule, Entrance
    if len(interface.controller) != 1 or len(interface.initial) != 1:
        raise SourceError('executor_scope', requirement='one controller bit and one initial branch')
    gamma = interface.controller_generator[0][1]
    if gamma <= 0 or interface.controller_generator != ((-gamma, gamma), (F(0), F(0))):
        raise SourceError('executor_controller', requirement='single irreversible opening')
    initial = interface.initial[0]
    if initial.weight != 1 or initial.controller_state != 0:
        raise SourceError('executor_initial_controller', requirement='controller initially closed')
    modules = []
    chosen = []
    for b, component in enumerate(interface.components):
        if len(component.sites) != 1 or component.generators[0] != component.generators[1]:
            raise SourceError('executor_component', component=b,
                              requirement='binary controller-independent silent dynamics')
        q = component.generators[0]
        alpha, beta = q[0][1], q[1][0]
        local_events = [event for event in interface.events if event.owner == b]
        if len(local_events) != 1:
            raise SourceError('executor_event_count', component=b, count=len(local_events))
        event = local_events[0]
        kappa = event.hazards[1][1]
        if (alpha <= 0 or beta <= 0 or kappa <= 0
                or event.hazards != ((F(0), F(0)), (F(0), kappa))
                or event.controller_reset != (0, 1)
                or event.component_resets != ((b, (0, 0)),)):
            raise SourceError('executor_event_scope', event=event.name)
        if initial.component_rows[b] != (beta / (alpha + beta), alpha / (alpha + beta)):
            raise SourceError('executor_initial_stationarity', component=b)
        modules.append(BinaryModule(alpha, beta, kappa))
        if event.mark == event_mark:
            chosen.append(b)
    if any(event.owner is None for event in interface.events) or len(chosen) != 1:
        raise SourceError('executor_mark', mark=event_mark, matching_components=chosen)
    return Entrance(modules, gamma, F(time), chosen[0])


def with_product_mixture_initial(source, weights, probability_one, controller_assignment):
    """Express a supplied positive Boolean product mixture in the source grammar.

    This checks representation compatibility through compile_interface.  It
    does not prove an externally supplied approximation-error certificate.
    The supplied law itself is interpreted exactly, as rational probabilities.
    """
    sites = sorted(set(range(source.nsites)) - set(source.controller))
    if len(weights) != len(probability_one):
        raise SourceError('entrance_mixture_length', weights=len(weights), rows=len(probability_one))
    branches = []
    for k, (weight, row) in enumerate(zip(weights, probability_one)):
        if len(row) != len(sites):
            raise SourceError('entrance_factor_count', branch=k, supplied=len(row), required=len(sites))
        factors = tuple(InitialFactor((site,), (1 - p, p)) for site, p in zip(sites, row))
        branches.append(InitialBranch(weight, tuple(controller_assignment), factors))
    updated = replace(source, initial=tuple(branches))
    return updated, compile_interface(updated)


def small_reference_check():
    """An expanded 16-state semantic check, separate from source acquisition."""
    rules = (
        Rule('c_up', ((0, 0),), ((0, 1),), F(2, 3)),
        Rule('c_down', ((0, 1),), ((0, 0),), F(1, 5)),
        Rule('a_up_c0', ((0, 0), (1, 0)), ((1, 1),), F(1, 2)),
        Rule('a_up_c1', ((0, 1), (1, 0)), ((1, 1),), F(4, 5)),
        Rule('a_down', ((1, 1),), ((1, 0),), F(2, 3)),
        Rule('b_up', ((1, 1), (2, 0)), ((2, 1),), F(3, 4)),
        Rule('b_down', ((2, 1),), ((2, 0),), F(7, 9)),
        Rule('d_up_c0', ((0, 0), (3, 0)), ((3, 1),), F(1, 6)),
        Rule('d_up_c1', ((0, 1), (3, 0)), ((3, 1),), F(5, 6)),
        Rule('d_down', ((3, 1),), ((3, 0),), F(1, 4)),
        Rule('A', ((0, 1), (2, 1)), ((2, 0),), F(2, 7), 'A'),
        Rule('B', ((0, 0), (3, 1)), ((0, 1), (3, 0), (1, 0)), F(3, 8), 'B'),
    )
    initial = (InitialBranch(F(1, 3), ((0, 0),),
                             tuple(InitialFactor((i,), (F(1, 2), F(1, 2))) for i in (1, 2, 3))),
               InitialBranch(F(2, 3), ((0, 1),),
                             tuple(InitialFactor((i,), (F(1, 4), F(3, 4))) for i in (1, 2, 3))))
    source = Program(4, (0,), rules, initial)
    interface = compile_interface(source)
    assert [component.sites for component in interface.components] == [(1, 2), (3,)]
    checks = 0
    for x in product((0, 1), repeat=4):
        env = dict(enumerate(x))
        c = interface.controller_states.index((x[0],))
        local = [component.states.index(tuple(x[i] for i in component.sites))
                 for component in interface.components]
        explicit = {}
        for rule in rules:
            if rule.mark is None and matching(dict(rule.guard), env):
                changed = env | dict(rule.update)
                y = tuple(changed[i] for i in range(4))
                if x != y:
                    explicit[y] = explicit.get(y, F(0)) + rule.rate
        acquired = {}
        for j, rate in enumerate(interface.controller_generator[c]):
            if j != c and rate:
                y = (interface.controller_states[j][0],) + x[1:]
                acquired[y] = acquired.get(y, F(0)) + rate
        for b, component in enumerate(interface.components):
            for j, rate in enumerate(component.generators[c][local[b]]):
                if j != local[b] and rate:
                    changed = env | dict(zip(component.sites, component.states[j]))
                    y = tuple(changed[i] for i in range(4))
                    acquired[y] = acquired.get(y, F(0)) + rate
        assert explicit == acquired
        checks += 1
        for event in interface.events:
            rule = next(rule for rule in rules if rule.name == event.name)
            rate = event.hazards[c][local[event.owner] if event.owner is not None else 0]
            assert rate == (rule.rate if matching(dict(rule.guard), env) else 0)
            changed = env | dict(zip(interface.controller,
                                    interface.controller_states[event.controller_reset[c]]))
            for b, mapping in event.component_resets:
                component = interface.components[b]
                changed.update(zip(component.sites, component.states[mapping[local[b]]]))
            assert changed == env | dict(rule.update)
            checks += 2
        p_source = F(0)
        for branch in initial:
            if matching(dict(branch.controller_assignment), env):
                probability = branch.weight
                for factor in branch.factors:
                    probability *= dict(zip(states(factor.sites), factor.probabilities))[tuple(x[i] for i in factor.sites)]
                p_source += probability
        p_compiled = F(0)
        for branch in interface.initial:
            if branch.controller_state == c:
                probability = branch.weight
                for b, row in enumerate(branch.component_rows):
                    probability *= row[local[b]]
                p_compiled += probability
        assert p_source == p_compiled
        checks += 1
    return source, {'expanded_states': 16, 'exact_semantic_comparisons': checks,
                    'controller_states': 2, 'component_states': [4, 2],
                    'conditional_local_rates_checked': True,
                    'positive_initial_mixture_checked': True,
                    'controller_and_multicomponent_fixed_reset_checked': True}


def demonstration():
    source = star_source()
    interface = compile_interface(source)
    executor = one_open_binary_executor(interface, 'reaction_0', F(3, 2))
    from tensor_separator_entrance import BinaryModule, Entrance
    expected_modules = [BinaryModule(F(3, 5) + F(i, 100), F(2, 5) + F(i % 5, 50),
                                     F(3, 2) + F(i % 3, 10)) for i in range(24)]
    assert executor.modules == expected_modules
    expected = Entrance(expected_modules, F(7, 10), F(3, 2), 0)
    interval_equalities = 0
    for u in (F(0), F(1, 4), F(3, 4), F(3, 2)):
        for actual_pair, expected_pair in zip(executor.vectors(u), expected.vectors(u)):
            for actual, target in zip(actual_pair, expected_pair):
                assert (actual.lo, actual.hi) == (target.lo, target.hi)
                interval_equalities += 1
    small_source, reference = small_reference_check()
    bad_sources = {
        'controller_reads_leaf': replace(source, rules=source.rules +
            (Rule('bad_controller', ((0, 0), (1, 1)), ((0, 1),), F(1)),)),
        'silent_multisite_write': replace(source, rules=source.rules +
            (Rule('bad_write', (), ((1, 0), (2, 0)), F(1)),)),
        'requested_partition_splits_silent_scope': replace(small_source,
            leaf_blocks=((1,), (2,), (3,))),
        'requested_partition_splits_hazard': replace(source,
            leaf_blocks=tuple((i,) for i in range(1, 25)),
            rules=source.rules + (Rule('bad_hazard', ((1, 1), (2, 1)), (), F(1), 'joint'),)),
        'initial_factor_crosses_components': replace(source, initial=(replace(source.initial[0],
            factors=(InitialFactor((1, 2), (F(1, 2), F(0), F(0), F(1, 2))),)
                    + source.initial[0].factors[2:]),)),
        'initial_weight_missing': replace(source, initial=(replace(source.initial[0], weight=F(1, 2)),)),
        'inexact_float_rate': replace(source, rules=source.rules +
            (Rule('bad_float', ((1, 0),), ((1, 1),), 0.1),)),
        'repeated_reset_site': replace(source, rules=source.rules +
            (Rule('bad_reset', ((1, 1),), ((1, 0), (1, 1)), F(1), 'bad'),)),
    }
    rejected = {}
    for name, bad in bad_sources.items():
        try:
            compile_interface(bad)
        except SourceError as error:
            rejected[name] = {'category': error.category, 'witness': error.witness}
        else:
            raise AssertionError(f'Expected rejection: {name}')
    # The compiler can also absorb a residual coupled hazard into one larger
    # component instead of incorrectly pretending that the old partition holds.
    merged = compile_interface(replace(star_source(3), rules=star_source(3).rules +
        (Rule('joint_hazard', ((1, 1), (2, 1)), (), F(1), 'joint'),)))
    assert [component.sites for component in merged.components] == [(1, 2), (3,)]
    try:
        one_open_binary_executor(compile_interface(small_source), 'A', F(1))
    except SourceError as error:
        rejected['broader_compiler_not_silently_used_by_specialized_executor'] = {
            'category': error.category, 'witness': error.witness}
    else:
        raise AssertionError('Executor accepted unsupported input')
    result = {
        'new_work': True,
        'source_grammar': 'Boolean guarded rational rules; single-site silent writes; fixed-write marked resets',
        'source_sites': source.nsites,
        'source_rules': len(source.rules),
        'controller_states_acquired': len(interface.controller_states),
        'components_acquired': len(interface.components),
        'local_state_rows_acquired': sum(len(component.states) for component in interface.components),
        'marked_event_branches': len(interface.events),
        'global_configurations_not_enumerated_by_compiler': str(2 ** source.nsites),
        'exact_match_to_existing_24_module_executor_parameters': True,
        'exact_interval_scalar_matches_to_existing_executor': interval_equalities,
        'previous_numerical_entrance_run_recomputed': False,
        'scope_merging_example_component_sites': [component.sites for component in merged.components],
        'small_expanded_reference': reference,
        'rejection_witnesses': rejected,
    }
    retained_file = Path(__file__).with_name('tensor_correlated_entrance_24sites.json')
    if retained_file.exists():
        with retained_file.open() as handle:
            retained = json.load(handle)
        assert F(retained['source_parameters']['gamma']) == executor.gamma
        assert len(retained['source_parameters']['modules']) == len(executor.modules)
        for recorded, actual in zip(retained['source_parameters']['modules'], executor.modules):
            assert tuple(F(recorded[key]) for key in ('alpha', 'beta', 'kappa')) == (
                actual.alpha, actual.beta, actual.kappa)
        weights = tuple(F(value) for value in retained['exact_rational_weights'])
        rows = tuple(tuple(F(value) for value in row)
                     for row in retained['exact_rational_probability_one'])
        controller_after = retained['source_record']['controller_after_event']
        _, retained_interface = with_product_mixture_initial(source, weights, rows,
                                                             ((0, controller_after),))
        firing = retained['source_record']['mark']
        assert all(branch.component_rows[firing] == (F(1), F(0))
                   for branch in retained_interface.initial)
        result['retained_correlated_entrance_initialization'] = {
            'file': retained_file.name,
            'positive_initial_branches_checked': len(retained_interface.initial),
            'normalization_checked_exactly': True,
            'source_parameters_match': True,
            'controller_and_firing_site_reset_match': True,
            'provided_initial_law_TV_upper_not_reproved': retained['posterior_total_variation_upper'],
            'existing_entrance_calculation_recomputed': False,
        }
    return result


if __name__ == '__main__':
    result = demonstration()
    print(json.dumps(result, indent=2))
    with open('source_interface_compiler_results.json', 'w') as handle:
        json.dump(result, handle, indent=2)
