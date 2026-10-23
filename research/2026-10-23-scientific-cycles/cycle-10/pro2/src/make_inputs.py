"""Build the one new non-theta/triangle/adjacent-cut receiving input."""
from pathlib import Path
import hashlib, json, resource, time

ROOT = Path(__file__).resolve().parents[1]


def main():
    start, cpu = time.perf_counter(), time.process_time()
    source = ROOT/'sources/native_atom_9.json'
    raw = source.read_bytes(); atom = json.loads(raw)
    n = atom['n']; edges = [tuple(sorted(e)) for e in atom['edges']]
    recipe = [dict(kind='unchanged_non_theta_atom', ids=list(range(n)),
                   source='sources/native_atom_9.json', sha256=hashlib.sha256(raw).hexdigest())]

    def cycle(length, root):
        nonlocal n
        ids = [root]+list(range(n, n+length-1)); n += length-1
        edges.extend(tuple(sorted((ids[i],ids[(i+1)%length]))) for i in range(length))
        recipe.append(dict(kind='cycle', ids=ids))
        return ids

    def theta(lengths, root, branch, position):
        nonlocal n
        hubs = [n, n+1]; n += 2; paths = []
        for j, length in enumerate(lengths):
            path = [hubs[0]]
            for i in range(1, length):
                if (j, i) == (branch, position):
                    path.append(root)
                else:
                    path.append(n); n += 1
            path.append(hubs[1]); paths.append(path)
            edges.extend(tuple(sorted(e)) for e in zip(path,path[1:]))
        recipe.append(dict(kind='theta', paths=paths))
        return paths

    # Actual adjacent degree-two marks 6 and 8 of the same non-theta atom.
    c = cycle(4, 6)
    # Both possible common-channel endpoints of this child are actual cuts;
    # whichever channel is admitted must exercise the outgoing stop message.
    cycle(3, c[1]); cycle(3, c[3])
    t = theta([2,3,5], 8, 2, 2)
    cycle(4, t[2][3])  # Mark adjacent to the theta's real incoming root.
    cycle(4, 0)
    obj = dict(name='mixed_non_theta_adjacent_marks', n=n, edges=sorted(edges),
               purpose='Native original graph testing non-theta atom, adjacent marks, actual long-path root, C3 and compulsory stop message.',
               construction_record=recipe)
    p = ROOT/'inputs/mixed_non_theta_adjacent_marks.json'
    p.write_text(json.dumps(obj,indent=2)+'\n')
    receipt = dict(wall_seconds=time.perf_counter()-start, cpu_seconds=time.process_time()-cpu,
                   peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                   input='inputs/'+p.name, bytes=p.stat().st_size,
                   sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                   n=n, m=len(edges), scope='Input construction and serialization, not theorem discovery.')
    (ROOT/'results/INPUT_BUILD.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
