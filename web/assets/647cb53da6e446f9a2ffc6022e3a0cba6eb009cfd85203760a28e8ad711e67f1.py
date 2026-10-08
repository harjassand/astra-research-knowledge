"""Finite checks of the pinned ordered-matrix construction for h=1,2.

These checks validate the literal pattern/host indexing and one old/new copy.
They do not prove the universal distance or copy-location assertions.
"""

from __future__ import annotations

import json
from pathlib import Path


S = 64


def make_modes(h: int):
    modes = []
    for i in range(1, h + 1):
        modes.extend(
            [
                ("V+", i, None),
                ("V-", i, None),
                ("W+", i, 0),
                ("W+", i, 1),
                ("W-", i, 0),
                ("W-", i, 1),
            ]
        )
    return modes


def make_pattern():
    anchor = [[0] * S for _ in range(S)]
    for u in range(S):
        for v in range(S):
            if 32 <= u < 64 and 59 <= v < 64:
                a = u - 32
                bit = v - 59
                anchor[u][v] = (a >> (4 - bit)) & 1
            else:
                anchor[u][v] = int(u != v)
    e1 = [int(i == 0) for i in range(S)]
    e2 = [int(i == 1) for i in range(S)]
    pattern = [anchor[i] + [e1[i], e2[i]] for i in range(S)]
    pattern.append(e1 + [1, 0])
    pattern.append(e2 + [1, 1])
    return anchor, pattern


def build_axis(h: int, m: int, is_row: bool):
    modes = make_modes(h)
    groups = {}
    labels = []
    for mode in modes:
        groups[mode] = []
        for u in range(S):
            block = list(range(len(labels), len(labels) + m))
            labels.extend(block)
            groups[mode].append(block)

    blocks = {}

    def add_block(sign: str, depth: int, p: int):
        size = m >> depth
        block = list(range(len(labels), len(labels) + size))
        labels.extend(block)
        blocks[(sign, depth, p)] = block

    def visit(depth: int, p: int):
        if depth == h:
            leaf = [len(labels)]
            labels.append(leaf[0])
            blocks[("+", depth, p)] = leaf
            blocks[("-", depth, p)] = leaf
            return
        if is_row:
            add_block("-", depth, p)
            visit(depth + 1, 2 * p)
            visit(depth + 1, 2 * p + 1)
            add_block("+", depth, p)
        else:
            add_block("+", depth, p)
            visit(depth + 1, 2 * p)
            visit(depth + 1, 2 * p + 1)
            add_block("-", depth, p)

    visit(0, 0)
    if is_row:
        dummy = list(range(len(labels), len(labels) + m))
        labels.extend(dummy)
    else:
        # The dummy column block precedes all variable columns.
        # Rebuild the column axis with its dummy in the required position.
        anchor_len = len(modes) * S * m
        variable_labels = labels[anchor_len:]
        labels = labels[:anchor_len]
        dummy = list(range(len(labels), len(labels) + m))
        labels.extend(dummy)
        offset = len(labels) - len(variable_labels)
        labels.extend(range(offset, offset + len(variable_labels)))
        blocks = {key: [x + m for x in value] for key, value in blocks.items()}
    return labels, groups, blocks, dummy


def union_blocks(blocks, sign: str, depth: int, nodes):
    return {x for p in nodes for x in blocks[(sign, depth, p)]}


def make_roles(h: int, rblocks, cblocks, rstar, cstar):
    row_roles = {}
    col_roles = {}
    for mode in make_modes(h):
        kind, i, d = mode
        if kind == "V+":
            r1 = union_blocks(rblocks, "+", i, range(1 << i))
            r2 = union_blocks(rblocks, "+", i - 1, range(1 << (i - 1)))
            c1 = set(cstar)
            c2 = union_blocks(cblocks, "+", i - 1, range(1 << (i - 1)))
        elif kind == "V-":
            r1 = union_blocks(rblocks, "-", i - 1, range(1 << (i - 1)))
            r2 = union_blocks(rblocks, "-", i, range(1 << i))
            c1 = set(cstar)
            c2 = union_blocks(cblocks, "-", i - 1, range(1 << (i - 1)))
        elif kind == "W+":
            nodes = [p for p in range(1 << i) if p % 2 == d]
            r1 = union_blocks(rblocks, "+", i, nodes)
            r2 = set(rstar)
            c1 = union_blocks(cblocks, "+", i - 1, range(1 << (i - 1)))
            c2 = union_blocks(cblocks, "+", i, nodes)
        else:
            nodes = [p for p in range(1 << i) if p % 2 == d]
            r1 = union_blocks(rblocks, "-", i, nodes)
            r2 = set(rstar)
            c1 = union_blocks(cblocks, "-", i, nodes)
            c2 = union_blocks(cblocks, "-", i - 1, range(1 << (i - 1)))
        assert not (r1 & r2)
        assert not (c1 & c2)
        row_roles[(mode, 1)] = r1
        row_roles[(mode, 2)] = r2
        col_roles[(mode, 1)] = c1
        col_roles[(mode, 2)] = c2
    return row_roles, col_roles


def build_host(h: int):
    m = 1 << h
    modes = make_modes(h)
    anchor, pattern = make_pattern()
    rlabels, rgroups, rblocks, rstar = build_axis(h, m, True)
    clabels, cgroups, cblocks, cstar = build_axis(h, m, False)
    assert len(rlabels) == len(clabels)
    n = len(rlabels)
    expected = (6 * h * S + 2 * h + 2) * m
    assert n == expected

    matrix = [bytearray(n) for _ in range(n)]
    row_anchor = {}
    col_anchor = {}
    for mode in modes:
        for u in range(S):
            for r in rgroups[mode][u]:
                row_anchor[r] = (mode, u)
            for c in cgroups[mode][u]:
                col_anchor[c] = (mode, u)

    # Anchor-by-anchor entries.
    for mode in modes:
        for u in range(S):
            for v in range(S):
                value = anchor[u][v]
                for r in rgroups[mode][u]:
                    for c in cgroups[mode][v]:
                        matrix[r][c] = value

    row_roles, col_roles = make_roles(h, rblocks, cblocks, rstar, cstar)

    # Non-anchor rows against anchor columns, and conversely.
    for mode in modes:
        for role in (1, 2):
            for r in row_roles[(mode, role)]:
                for u in range(S):
                    if u == role - 1:
                        for c in cgroups[mode][u]:
                            matrix[r][c] = 1
        for role in (1, 2):
            for c in col_roles[(mode, role)]:
                for u in range(S):
                    if u == role - 1:
                        for r in rgroups[mode][u]:
                            matrix[r][c] = 1

    # A dummy position has value one against every non-anchor position.
    nonanchor_rows = [r for r in range(n) if r not in row_anchor]
    nonanchor_cols = [c for c in range(n) if c not in col_anchor]
    for r in rstar:
        for c in nonanchor_cols:
            matrix[r][c] = 1
    for r in nonanchor_rows:
        for c in cstar:
            matrix[r][c] = 1

    # Variable-variable entries from the four rules in the source paper.
    row_info = {}
    col_info = {}
    for (sign, depth, p), block in rblocks.items():
        for r in block:
            row_info.setdefault(r, []).append((sign, depth, p))
    for (sign, depth, p), block in cblocks.items():
        for c in block:
            col_info.setdefault(c, []).append((sign, depth, p))

    for r, row_names in row_info.items():
        for c, col_names in col_info.items():
            values = []
            for rs, rd, rp in row_names:
                for cs, cd, cp in col_names:
                    if rs == cs == "+" and rd == cd:
                        values.append(int(rp <= cp))
                    if rs == cs == "-" and rd == cd and rd < h:
                        values.append(int(rp < cp))
                    if rs == cs == "+" and rd == cd + 1:
                        values.append(int(rp // 2 <= cp))
                    if rs == cs == "-" and rd == cd + 1:
                        values.append(int(rp // 2 < cp))
            assert len(set(values)) <= 1, (r, c, row_names, col_names, values)
            if values:
                matrix[r][c] = values[0]

    return {
        "h": h,
        "m": m,
        "n": n,
        "modes": modes,
        "pattern": pattern,
        "matrix": matrix,
        "row_groups": rgroups,
        "col_groups": cgroups,
        "row_blocks": rblocks,
        "col_blocks": cblocks,
        "row_dummy": rstar,
        "col_dummy": cstar,
    }


def is_copy(matrix, rows, cols, pattern):
    if len(rows) != len(pattern) or len(cols) != len(pattern):
        return False
    if any(a >= b for a, b in zip(rows, rows[1:])):
        return False
    if any(a >= b for a, b in zip(cols, cols[1:])):
        return False
    return all(matrix[r][c] == pattern[i][j] for i, r in enumerate(rows) for j, c in enumerate(cols))


def copy_positions(data, mode, body_rows, body_cols):
    ar = [group[0] for group in data["row_groups"][mode]]
    ac = [group[0] for group in data["col_groups"][mode]]
    return ar + list(body_rows), ac + list(body_cols)


def check(h: int):
    data = build_host(h)
    p = 0
    d = p % 2
    parent = p // 2
    leaf_r_plus = data["row_blocks"][("+", h, p)][0]
    leaf_r_minus = data["row_blocks"][("-", h, p)][0]
    leaf_c_plus = data["col_blocks"][("+", h, p)][0]
    leaf_c_minus = data["col_blocks"][("-", h, p)][0]
    parent_c_plus = data["col_blocks"][("+", h - 1, parent)][0]
    parent_c_minus = data["col_blocks"][("-", h - 1, parent)][0]
    dummy_r = data["row_dummy"][0]
    mode_w_minus = ("W-", h, d)
    mode_w_plus = ("W+", h, d)

    old_rows, old_cols = copy_positions(
        data, mode_w_minus, [leaf_r_minus, dummy_r], [leaf_c_minus, parent_c_minus]
    )
    assert is_copy(data["matrix"], old_rows, old_cols, data["pattern"])

    leaf_diagonal = [
        (data["row_blocks"][("+", h, q)][0], data["col_blocks"][("+", h, q)][0])
        for q in range(1 << h)
    ]
    assert len(leaf_diagonal) == data["m"]
    for r, c in leaf_diagonal:
        data["matrix"][r][c] = 0
    assert not is_copy(data["matrix"], old_rows, old_cols, data["pattern"])

    new_rows, new_cols = copy_positions(
        data, mode_w_plus, [leaf_r_plus, dummy_r], [parent_c_plus, leaf_c_plus]
    )
    assert is_copy(data["matrix"], new_rows, new_cols, data["pattern"])
    return {
        "h": h,
        "m": data["m"],
        "n": data["n"],
        "pattern_size": len(data["pattern"]),
        "distance_parameter_epsilon": f"1/{(6 * h * S + 2 * h + 2) ** 2}",
        "original_W_minus_copy_verified": True,
        "original_copy_broken_by_zeroing_leaf_diagonal": True,
        "new_W_plus_copy_created_by_same_edit": True,
        "leaf_diagonal_cells": len(leaf_diagonal),
        "universal_copy_location_or_distance_claim_checked": False,
    }


if __name__ == "__main__":
    results = [check(h) for h in (1, 2)]
    out = Path(__file__).with_name("CHECK_RESULTS.json")
    out.write_text(json.dumps({"status": "finite construction check only", "results": results}, indent=2) + "\n")
    print(json.dumps({"status": "finite construction check only", "results": results}, indent=2))
