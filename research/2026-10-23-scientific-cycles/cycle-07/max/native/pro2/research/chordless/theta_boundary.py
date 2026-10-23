"""Exact bounded-component extensions for parallel degree-two threads.

The interface theorem is restricted to theta networks. It is not a general
coloring algorithm for every chordless or series-parallel atom.
"""


class BoundaryObstruction(ValueError):
    pass


def distance_two_word(length, start, end):
    """Four-color path word, prescribed endpoints, all consecutive triples distinct.

    length counts edges. Needs length>=3, or length=2 with different endpoints.
    """
    if start not in range(4) or end not in range(4) or length < 2:
        raise ValueError("bad path contract")
    if length == 2:
        if start == end:
            raise BoundaryObstruction("equal endpoints of a two-edge path")
        return [start, next(c for c in range(4) if c not in (start, end)), end]
    colors = [start]
    # Leave two internal positions for the right-end constraint.
    for _ in range(1, length-2):
        colors.append(next(c for c in range(4) if c not in colors[-2:]))
    colors.append(next(c for c in range(4) if c not in colors[-2:] and c != end))
    colors.append(next(c for c in range(4) if c not in colors[-2:] and c != end))
    colors.append(end)
    assert len(colors) == length+1
    assert all(len(set(colors[i:i+3])) == 3 for i in range(length-1))
    return colors


def theta_graph(lengths):
    """Vertices0,1 are terminals; each supplied integer>=2 gives one thread."""
    lengths = tuple(lengths)
    if not 2 <= len(lengths) <= 4 or any(k < 2 for k in lengths):
        raise ValueError("need two to four threads, each length>=2")
    next_vertex = 2
    paths, edges = [], []
    for length in lengths:
        path = [0] + list(range(next_vertex, next_vertex+length-1)) + [1]
        next_vertex += length-1
        paths.append(path)
        edges.extend(zip(path, path[1:]))
    return list(range(next_vertex)), [tuple(sorted(e)) for e in edges], paths


def extend_theta(lengths, terminal_colors):
    """Four colors; prescribed terminals. Return full graph/color certificate.

    For equal terminal colors, s two-edge paths require s distinct channels.
    Exactly the s=4 case is excluded. No endpoint-color retuning is hidden.
    """
    vertices, edges, paths = theta_graph(lengths)
    a, b = terminal_colors
    if a not in range(4) or b not in range(4):
        raise ValueError("colors must lie in0..3")
    short_count = sum(len(p) == 3 for p in paths)
    if a == b and short_count > 3:
        raise BoundaryObstruction("four short branches need four colors other than terminal color")
    colors = {0:a, 1:b}
    unused_channels = iter(c for c in range(4) if c != a)
    channels = []
    for path in paths:
        if a == b and len(path) == 3:
            c = next(unused_channels)
            word = [a,c,a]
            channels.append(c)
        else:
            word = distance_two_word(len(path)-1, a, b)
        for v,c in zip(path,word):
            if v in colors and colors[v] != c:
                raise AssertionError("inconsistent terminal color")
            colors[v] = c
    return {"vertices":vertices, "edges":edges, "paths":paths,
            "colors":sorted(colors.items()), "terminal_colors":[a,b],
            "transmitting_channels":channels,
            "component_bound":len(paths)+1 if a != b else 2*len(paths)+1}


def free_three_color_theta(lengths):
    """Ordinary existential comparator: choose terminal colors0,1, K<=1+3r.

    It does not extend equal prescribed terminal colors. No claim of optimal K.
    """
    vertices, edges, paths = theta_graph(lengths)
    colors = {0:0,1:1}
    for path in paths:
        length = len(path)-1
        if length == 2:
            word = [0,2,1]
        elif length == 3:
            word = [0,2,0,1]
        else:
            word = [i%3 for i in range(length-1)]
            word.append(next(c for c in range(3) if c not in (word[-1],1)))
            word.append(1)
        for v,c in zip(path,word):
            if v in colors and colors[v] != c:
                raise AssertionError("inconsistent terminal color")
            colors[v] = c
    return {"vertices":vertices,"edges":edges,"paths":paths,
            "colors":sorted(colors.items()),"component_bound":1+3*len(paths)}


def cap_induction_witness(k):
    """Cycle C_(2k+1); its deleted-vertex coloring has cap k but cannot extend it."""
    if k < 2:
        raise ValueError("k>=2 required")
    left = [0 if i%2 == 0 else 2 for i in range(k)]
    right = [1 if (k-1-i)%2 == 0 else 3 for i in range(k)]
    colors = dict(enumerate(left+right))
    z = 2*k
    old_edges = [(i,i+1) for i in range(2*k-1)]
    edges = old_edges+[(0,z),(2*k-1,z)]
    return {"vertices":list(range(2*k+1)), "edges":edges, "deleted_vertex":z,
            "old_edges":old_edges, "old_colors":sorted(colors.items()),
            "boundary_edge":[k-1,k],"old_component_cap":k,
            "allowed_extension_colors":[2,3],"forced_new_component_size":k+1}
