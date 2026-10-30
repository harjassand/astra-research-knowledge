"""Exact two-step adaptive design using a retained read-once risk tree.

No hypothetical source outcome is physically acquired.  The returned policy
is (first leaf, second leaf if first outcome is 0, second leaf if it is 1).
With intervals, L bounds that concrete policy's gain and U bounds the exact
optimal adaptive two-step gain.  All arithmetic and scanning work is paid.
"""
from dataclasses import dataclass
from risk_compiler import IV, bounded, high, low, square


@dataclass(frozen=True)
class Policy:
    first: int
    second_if_zero: int
    second_if_one: int


def choose(candidates):
    j = max(range(len(candidates)), key=lambda i: low(candidates[i][0]))
    value, plan = candidates[j]
    if isinstance(value, IV):
        value = IV(value.lo, max(high(v) for v, _ in candidates))
    return value, plan


def adaptive_two_step(tree):
    """O(nodes + sum_i depth(i)*arity) arithmetic; O(nodes) extra space.

    Uses only the current one-observation gain at each subtree.  The outside
    derivative pass is recomputed and charged on each call.  No fast dynamic
    maintenance of the optimal adaptive first action is claimed.
    """
    assert tree.budget >= 1
    nodes = tree.nodes
    make = tree.make
    outside = [None] * len(nodes)
    outside[tree.root] = make(1)
    for v in range(tree.root, -1, -1):
        node = nodes[v]
        for a, child in enumerate(node.children):
            outside[child] = outside[v] * node.derivative[1 << a]
    choices = []
    groups = 0
    for i, leaf in enumerate(nodes):
        if leaf.children:
            continue
        first_gain = square(outside[i]) * leaf.gain[1]
        conditional = []
        for x in (0, 1):
            alpha = make(leaf.alpha + x)
            beta = make(leaf.beta + 1 - x)
            snew = alpha + beta
            new_mean = bounded(alpha / snew, 0, 1)
            new_one_gain = bounded(new_mean * (1-new_mean) / square(snew+1), 0, 0.25)
            candidates = [(bounded(square(outside[i]) * new_one_gain, 0, 0.25), i)]
            delta = new_mean - leaf.mean
            a_node = i
            v = leaf.parent
            while v >= 0:
                parent = nodes[v]
                a = parent.children.index(a_node)
                for b, sibling in enumerate(parent.children):
                    if b == a:
                        continue
                    slope = parent.derivative[1 << b] + parent.derivative[(1 << a) | (1 << b)] * delta
                    factor = square(outside[v] * slope)
                    value = bounded(factor * nodes[sibling].gain[1], 0, 0.25)
                    # The retained child argmax recovers a concrete leaf.
                    candidates.append((value, sibling))
                delta = parent.derivative[1 << a] * delta
                a_node, v = v, parent.parent
            groups += len(candidates)
            value, selected_subtree = choose(candidates)
            selected_leaf = tree.plan(1, selected_subtree)[0]
            conditional.append((value, selected_leaf))
        score = bounded(first_gain + (1-leaf.mean)*conditional[0][0]
                        + leaf.mean*conditional[1][0], 0, 0.25)
        choices.append((score, Policy(i, conditional[0][1], conditional[1][1])))
    value, policy = choose(choices)
    return value, policy, {'outside_derivative_nodes':len(nodes),
                           'first_actions':len(choices),
                           'conditional_groups':groups}


def reversible_hypothetical_baseline(tree):
    """Same O(nh) adaptive optimization with ordinary temporary updates.

    Intended for an exact tree with budget=1.  Saved alpha/beta are restored
    after each hypothetical outcome; ancestors are recomputed.  Counters
    include all maintenance.  This calls no physical source.
    """
    assert not tree.interval and tree.budget == 1
    from fractions import Fraction
    prior_variance = tree.nodes[tree.root].variance
    choices = []
    leaves = [i for i,n in enumerate(tree.nodes) if not n.children]
    for i in leaves:
        leaf = tree.nodes[i]
        alpha, beta = leaf.alpha, leaf.beta
        probability = alpha/(alpha+beta)
        expected_final_risk = Fraction(0)
        second = []
        for x,weight in ((0,1-probability),(1,probability)):
            tree.observe(i,x)
            root=tree.nodes[tree.root]
            expected_final_risk += weight*(root.variance-root.gain[1])
            second.append(tree.plan(1)[0])
            leaf.alpha,leaf.beta=alpha,beta
            tree.refresh_ancestors(i)
        choices.append((prior_variance-expected_final_risk,Policy(i,*second)))
    return choose(choices)
