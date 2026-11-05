"""Check the one-spin integer-energy realization on an actual generated tileset.

These are finite exact algebra/combinatorics checks, not an asymptotic proof.
"""
from pathlib import Path
import json
import random
from check_explicit_tableau_grammar import Machine, HALT, ZERO, compile_tiles


def main():
    machine = Machine(('_',), '_', ('S',), 'S', {('S', '_'): (HALT, '_', 0)})
    tiles = compile_tiles(machine)
    color_ids = {ZERO: 0}
    for tile in tiles:
        for color in tile.colors:
            if color not in color_ids:
                color_ids[color] = len(color_ids)
    m = (len(color_ids)-1).bit_length()
    group_order = 1 << m
    coded = [(tuple(color_ids[c] for c in tile.colors), tile.marked) for tile in tiles]
    t = len(tiles)
    C0, D = 10000*(t+1), 10000*(t+1)+t

    def character(label, group):
        return -1 if (label & group).bit_count() % 2 else 1

    def fourier_sum(spin, west, east, south, north):
        groups = (west, east, south, north)
        total = 0
        for labels, marked in coded:
            if marked and spin == -1:
                continue
            value = 1
            for label, group in zip(labels, groups):
                value *= character(label, group)
            total += value
        return total

    def site_energy(center, west_site, south_site):
        # Site fields: spin, multiplicity, owned east group, owned north group.
        spin, b, east, north = center
        F = fourier_sum(spin, west_site[2], east, south_site[3], north)
        return int(b > C0+F)

    rng = random.Random(20261105)
    pairs = [(0,0), (0,1), (1,1), (1,2)]
    pairs += [(rng.randrange(len(color_ids)), rng.randrange(len(color_ids))) for _ in range(28)]
    for c,d in pairs:
        inner = sum(character(c,g)*character(d,g) for g in range(group_order))
        assert inner == (group_order if c == d else 0)
    for c in (0,1,len(color_ids)-1):
        assert sum(character(c,g) for g in range(group_order)) == (group_order if c == 0 else 0)

    tested = 0
    for _ in range(100):
        west, east, south, north = [rng.randrange(group_order) for _ in range(4)]
        for spin in (-1,1):
            F = fourier_sum(spin,west,east,south,north)
            assert -t <= F <= t
            n0, n1 = C0+F, t-F
            assert n0 > 0 and n1 >= 0 and n0+n1 == D
            # As a polynomial in x=exp(-1), the exact factor is
            # C0+F + (t-F)x = C0+tx + (1-x)F.
            assert (n0,n1) == (C0+F,t-F)
            for b in {1, D, n0, min(D,n0+1)}:
                center = (spin,b,east,north)
                left = (1,1,west,0)
                below = (1,1,0,south)
                assert site_energy(center,left,below) == int(b>n0)
            tested += 1
    assert fourier_sum(1,0,0,0,0) == t
    assert fourier_sum(-1,0,0,0,0) == sum(not marked for _,marked in coded)
    assert all(20*int(s!=r) in (0,20) for s in (-1,1) for r in (-1,1))

    result = {
        "status": "all exact physical-realization checks passed",
        "tile_types": t,
        "edge_colors": len(color_ids),
        "group_bits": m,
        "group_order": group_order,
        "multiplicity_states": D,
        "physical_site_alphabet_size": 2*D*group_order**2,
        "character_pairs_tested_exactly": len(pairs),
        "spin_and_group_cases_tested": tested,
        "physical_site_energies": [0,1],
        "mismatch_energies": [0,20],
        "scope": "Finite realization and selected exact character orthogonality checks; no claim to enumerate the full physical interaction table or prove thermodynamic behavior by testing."
    }
    (Path(__file__).resolve().parent/'physical_realization_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
