"""NEW marked-root projection of the fixed Cycle8 literal certificate.

This does not execute the inherited closure or its old finite gate. The
accepted predecessor guarantees are a dependency, with their exact hash.
The new finite obligation is one distinct-neighbor, <=1-flag degree2 root
witness for each active-degree family in the marked-midpoint context.
"""
from pathlib import Path
import hashlib, json, time, resource

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = '63f4cdfd7ccc3b3159782a28a144a199422a315975aa207e5d144e8659e53525'


def main():
    start, cpu = time.perf_counter(), time.process_time()
    path = ROOT / 'sources/cycle8_selected/loaded_star_certificate.json'
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED
    source = json.loads(raw)
    rows = []
    for family in source['families']:
        if max(family['degree']) > 3:
            continue
        possibilities = []
        for i, sig in enumerate(family['targets']):
            a, b, dl, nl, fl, dr, nr, fr = sig
            if a == b:
                continue
            for z in range(4):
                if z in (a, b) or ((fl | fr) >> z) & 1:
                    continue
                flags = (1 << a if (nl >> z) & 1 else 0) | (1 << b if (nr >> z) & 1 else 0)
                if flags.bit_count() <= 1:
                    possibilities.append((flags.bit_count(), i, z, flags, sig))
        assert possibilities, ('empty marked guarantee', family['id'])
        count, i, z, flags, sig = min(possibilities)
        rows.append(dict(family=family['id'], degree=family['degree'],
                         target_index=i, inherited_target=sig, root_color=z,
                         root_neighbor_colors=[sig[0], sig[1]], root_degree=2,
                         root_flag_upper_mask=flags, flag_count_upper=count))
    result = dict(schema='astra-marked-midpoint-projection/v1',
                  predecessor_certificate_sha256=EXPECTED, rows=rows,
                  cases=len(rows), all_nonempty=True,
                  guarantee='Each specified degree2 nontriangle atom root admits distinct neighbor colors and at most one far-repeat flag; one mark only.',
                  wall_seconds=time.perf_counter()-start,
                  cpu_seconds=time.process_time()-cpu,
                  peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
    out = ROOT / 'results/marked_root_projection.json'
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}, indent=2))


if __name__ == '__main__':
    main()
