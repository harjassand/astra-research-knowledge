"""Exact two-cluster B(P) interleaving check on one clean L=8 surface."""
from itertools import combinations, product
import json
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
SRC = HERE / 'followup_check.py'
spec = importlib.util.spec_from_file_location('followup_check', SRC)
fc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fc)


def run():
    torus = fc.Torus(8)
    clean = (0,) * 64
    even_tiles = [(p, tile) for p, tile in torus.tiles if p == 0]
    tested = 0
    simultaneous = 0
    safe = 0
    sequential_branches = {'P_then_Q': 0, 'Q_then_P': 0}
    disabled_guards = {'P_then_Q': 0, 'Q_then_P': 0}
    second_option_counts = {'P_then_Q': {}, 'Q_then_P': {}}
    final_gate_debt_counts = {}
    first = None
    failures = []
    failure_kinds = {}

    def is_union_of_even_forward_debts(final):
        # On the zero base, the even tiles form a disjoint 2x2 tiling. A
        # forward gate debt makes exactly one such tile all ones.
        for v, z in enumerate(final):
            if z not in (0, 1):
                return False
        for _, tile in even_tiles:
            vals = {final[v] for v in tile}
            if len(vals) > 1:
                return False
        return True

    # Exactly two 0->1 faults in each of two distinct even tiles.
    for i, key_p in enumerate(even_tiles):
        for key_q in even_tiles[i + 1:]:
            tile_p, tile_q = key_p[1], key_q[1]
            for sites_p in combinations(tile_p, 2):
                for sites_q in combinations(tile_q, 2):
                    observed = list(clean)
                    for v in sites_p + sites_q:
                        observed[v] = 1
                    observed = tuple(observed)
                    tested += 1
                    cand_p = torus.b_candidates(observed, key_p)
                    cand_q = torus.b_candidates(observed, key_q)
                    if not cand_p or not cand_q:
                        continue
                    simultaneous += 1
                    if first is None:
                        first = {
                            'tiles': [list(tile_p), list(tile_q)],
                            'fault_sites': [list(sites_p), list(sites_q)],
                            'initial_B_option_counts': [len(cand_p), len(cand_q)],
                        }
                    case_failures = []
                    # Explore all P-then-Q branches, re-evaluating Q's guard.
                    for state_p, label_p in cand_p:
                        next_q = torus.b_candidates(state_p, key_q)
                        if not next_q:
                            disabled_guards['P_then_Q'] += 1
                            case_failures.append({'order': 'P_then_Q', 'first': str(label_p),
                                                  'reason': 'Q guard disabled after P'})
                        count = str(len(next_q))
                        second_option_counts['P_then_Q'][count] = second_option_counts['P_then_Q'].get(count, 0) + 1
                        sequential_branches['P_then_Q'] += len(next_q)
                        for final, label_q in next_q:
                            if not torus.valid(final):
                                case_failures.append({'order': 'P_then_Q', 'first': str(label_p),
                                                      'second': str(label_q),
                                                      'reason': 'final not globally valid'})
                            elif not is_union_of_even_forward_debts(final):
                                case_failures.append({'order': 'P_then_Q', 'first': str(label_p),
                                                      'second': str(label_q),
                                                      'reason': 'final not a union of even-tile forward debts'})
                            else:
                                gates = sum(1 for _, tile in even_tiles
                                            if all(final[v] == 1 for v in tile))
                                final_gate_debt_counts[str(gates)] = final_gate_debt_counts.get(str(gates), 0) + 1
                    # Explore all Q-then-P branches, re-evaluating P's guard.
                    for state_q, label_q in cand_q:
                        next_p = torus.b_candidates(state_q, key_p)
                        if not next_p:
                            disabled_guards['Q_then_P'] += 1
                            case_failures.append({'order': 'Q_then_P', 'first': str(label_q),
                                                  'reason': 'P guard disabled after Q'})
                        count = str(len(next_p))
                        second_option_counts['Q_then_P'][count] = second_option_counts['Q_then_P'].get(count, 0) + 1
                        sequential_branches['Q_then_P'] += len(next_p)
                        for final, label_p in next_p:
                            if not torus.valid(final):
                                case_failures.append({'order': 'Q_then_P', 'first': str(label_q),
                                                      'second': str(label_p),
                                                      'reason': 'final not globally valid'})
                            elif not is_union_of_even_forward_debts(final):
                                case_failures.append({'order': 'Q_then_P', 'first': str(label_q),
                                                      'second': str(label_p),
                                                      'reason': 'final not a union of even-tile forward debts'})
                            else:
                                gates = sum(1 for _, tile in even_tiles
                                            if all(final[v] == 1 for v in tile))
                                final_gate_debt_counts[str(gates)] = final_gate_debt_counts.get(str(gates), 0) + 1
                    if case_failures:
                        for failure in case_failures:
                            reason = failure['reason']
                            failure_kinds[reason] = failure_kinds.get(reason, 0) + 1
                        failures.append({
                            'tiles': [list(tile_p), list(tile_q)],
                            'fault_sites': [list(sites_p), list(sites_q)],
                            'initial_B_option_counts': [len(cand_p), len(cand_q)],
                            'failures': case_failures[:4],
                        })
                    else:
                        safe += 1
    return {
        'scope': 'L=8, q=8, all-zero clean surface; all unordered pairs of distinct even tiles; all 6x6 choices of two 0->1 faults inside each tile; exact B option enumeration and both sequential orders with guard recomputation.',
        'counts': {'two_cluster_fault_patterns_tested': tested,
                   'both_B_triggers_initially_enabled': simultaneous,
                   'both_orders_all_branches_safe': safe,
                   'patterns_with_order_or_validity_failure': len(failures),
                   'failure_branches_by_reason': failure_kinds,
                   'second_guard_disabled_count': disabled_guards,
                   'second_B_option_counts': second_option_counts,
                   'sequential_branches_checked': sequential_branches,
                   'final_number_of_forward_tile_debts': final_gate_debt_counts},
        'first_simultaneous_case': first,
        'first_failure': failures[0] if failures else None,
    }


if __name__ == '__main__':
    result = run()
    output = HERE / 'INTERLEAVING_RESULTS.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
