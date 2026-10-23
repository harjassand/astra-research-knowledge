"""Explicit all-length star-three coloring for A_L, with bounded proof checks.

No producer imports. This module supplies the stronger ordinary control for
A_L; it does not certify a whole loaded-port grammar.
"""
from pathlib import Path
import json
import time
import resource

BASES = {2: (1, 0, 1), 3: (1, 0, 2, 1), 4: (1, 0, 2, 0, 1)}
BLOCK = (2, 0, 1)


def path_word(length):
    if type(length) is not int or length < 2:
        raise ValueError("A_L requires an integer L>=2")
    k = 2 + (length - 2) % 3
    return BASES[k] + BLOCK * ((length - k) // 3)


def atom(length):
    """Return the unchanged A_L support, with a=0,b=1,c=2."""
    word = path_word(length)
    colors = [0, 1, 1, 2, 2, 2, 2]
    edges = [(0, 3), (3, 1), (0, 4), (4, 1),
             (0, 5), (5, 2), (0, 6), (6, 2)]
    mids = list(range(7, 7 + length - 1))
    colors.extend(word[1:-1])
    chain = [1] + mids + [2]
    edges.extend(zip(chain, chain[1:]))
    return {"n": len(colors), "edges": [sorted(e) for e in edges],
            "colors": colors, "query_count": 3,
            "branch_vertices": {"a": 0, "b": 1, "c": 2},
            "path_word": list(word),
            "operator_constant_sq": "3/2", "frobenius_constant_sq": "2"}


def proper_star_word(w):
    return (all(a != b for a, b in zip(w, w[1:]))
            and all(not (w[i] == w[i+2] and w[i+1] == w[i+3])
                    for i in range(len(w) - 3)))


def check_graph(g):
    n, es, cs = g["n"], g["edges"], g["colors"]
    adj = [[] for _ in range(n)]
    assert len(es) == n + 2 and len({tuple(e) for e in es}) == len(es)
    for u, v in es:
        assert u < v and cs[u] != cs[v]
        adj[u].append(v)
        adj[v].append(u)
    assert max(map(len, adj)) == 4
    for u, v in es:
        ru = sum(cs[w] == cs[v] for w in adj[u])
        rv = sum(cs[w] == cs[u] for w in adj[v])
        assert ru == 1 or rv == 1
    return True


def main():
    start = time.perf_counter()
    base_records = []
    for k, w in BASES.items():
        assert len(w) == k+1 and w[0] == w[-1] == 1
        assert proper_star_word(w)
        g = atom(k)
        assert check_graph(g)
        base_records.append({"length": k, "word": list(w),
                             "full_graph_star_checked": True})
    suffixes = sorted({w[-3:] for w in BASES.values()})
    transitions = []
    for s in suffixes:
        w = s + BLOCK
        assert proper_star_word(w)
        assert w[-3:] == BLOCK
        transitions.append({"suffix": list(s), "append": list(BLOCK),
                            "next_suffix": list(w[-3:]),
                            "new_windows": [list(w[i:i+4]) for i in range(3)]})
    result = {"schema": "astra-cycle8-A-L-three-query-control/v1",
              "bases": base_records, "suffix_transitions": transitions,
              "all_size_argument": "STRONG_CONTROL_A_L.md",
              "size_sweep_performed": False, "passed": True,
              "wall_seconds_body": time.perf_counter() - start,
              "process_max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    Path(__file__).with_name("A_L_THREE_CONTROL_RESULT.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in
                      ("passed", "wall_seconds_body", "process_max_rss_kib")}))


if __name__ == "__main__":
    main()
