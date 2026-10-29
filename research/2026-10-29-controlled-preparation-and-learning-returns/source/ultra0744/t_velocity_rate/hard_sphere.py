"""Actual hard-sphere currency recursion and matched weighted comparator.

Floating implementation of an ideal-real construction. No population is used
by either recursive algorithm. Kac/DSMC below is a separate finite-N baseline.
"""
from dataclasses import dataclass, field
import heapq
import math
import random


def norm2(v):
    return sum(x*x for x in v)


def distance(v, w):
    return math.sqrt(sum((x-y)**2 for x, y in zip(v, w)))


def elastic(v, w, rng):
    # Uniform outgoing relative direction, angular measure of total mass one.
    z = 2.0*rng.random()-1.0
    angle = 2.0*math.pi*rng.random()
    radial = math.sqrt(max(0.0, 1.0-z*z))
    sigma = (radial*math.cos(angle), radial*math.sin(angle), z)
    radius = 0.5*distance(v, w)
    center = tuple(0.5*(x+y) for x, y in zip(v, w))
    return (tuple(x+radius*y for x, y in zip(center, sigma)),
            tuple(x-radius*y for x, y in zip(center, sigma)))


@dataclass
class Counts:
    events: int = 0
    source_draws: int = 0
    exponentials: int = 0
    collision_accepts: int = 0
    angles: int = 0
    outgoing_choices: int = 0
    final_attempts: int = 0
    final_rejects: int = 0
    max_stack: int = 0


@dataclass
class FiniteSource:
    velocities: tuple
    probabilities: tuple

    def __post_init__(self):
        if len(self.velocities) != len(self.probabilities):
            raise ValueError("source table mismatch")
        if any(p < 0 for p in self.probabilities):
            raise ValueError("negative source weight")
        if abs(sum(self.probabilities)-1.0) > 1e-14:
            raise ValueError("source weights do not sum to one")
        self.energy = sum(p*norm2(v) for v, p in
                          zip(self.velocities, self.probabilities))
        self.radius2 = max(map(norm2, self.velocities))

    def draw(self, rng, a, tilted=False):
        weights = self.probabilities
        if tilted:
            c = a+self.energy
            weights = tuple(p*(a+norm2(v))/c for v, p in
                            zip(self.velocities, self.probabilities))
        u = rng.random()
        total = 0.0
        for v, p in zip(self.velocities, weights):
            total += p
            if u < total:
                return v
        return self.velocities[-1]  # binary64 cumulative-rounding endpoint


@dataclass
class Frame:
    goal: float
    v: tuple
    mass: float = 1.0
    time: float = 0.0


class HardSphere:
    def __init__(self, source, a=1.0, seed=0):
        if a <= 0:
            raise ValueError("positive currency offset required")
        self.source = source
        self.a = a
        self.c = a+source.energy
        self.sqrt_a = math.sqrt(a)
        self.rng = random.Random(seed)

    def rate(self, v):
        return (self.c/self.a)*(math.sqrt(norm2(v))+self.sqrt_a)

    def _tree(self, t, counts, currency):
        if t < 0:
            raise ValueError("negative time")
        def new_frame(goal):
            counts.source_draws += 1
            return Frame(goal, self.source.draw(self.rng, self.a, currency))
        stack = [new_frame(t)]
        counts.max_stack = max(counts.max_stack, 1)
        while stack:
            frame = stack[-1]
            counts.exponentials += 1
            frame.time += self.rng.expovariate(1.0)/self.rate(frame.v)
            if frame.time <= frame.goal:
                counts.events += 1
                stack.append(new_frame(frame.time))
                counts.max_stack = max(counts.max_stack, len(stack))
                continue
            returned_v, returned_mass = frame.v, frame.mass
            stack.pop()
            if not stack:
                return returned_v, returned_mass
            parent = stack[-1]
            w = returned_v
            hw = self.a+norm2(w)
            accept = self.c*distance(parent.v, w)/(hw*self.rate(parent.v))
            if not (-1e-14 <= accept <= 1.0+1e-14):
                raise ArithmeticError("invalid collision probability")
            accepted = self.rng.random() < accept
            if accepted:
                counts.collision_accepts += 1
                counts.angles += 1
                p, q = elastic(parent.v, w, self.rng)
                if currency:
                    counts.outgoing_choices += 1
                    hp = self.a+norm2(p)
                    hq = self.a+norm2(q)
                    parent.v = p if self.rng.random() < hp/(hp+hq) else q
                else:
                    parent.v = p
            if not currency:
                # Fournier's output mass changes ALSO on a null collision.
                parent.mass *= returned_mass*hw/self.c
                if not math.isfinite(parent.mass):
                    raise ArithmeticError("weighted comparator mass overflow")
        raise AssertionError("unreachable")

    def currency(self, t, counts=None):
        counts = Counts() if counts is None else counts
        return self._tree(t, counts, True)[0]

    def physical(self, t, counts=None):
        counts = Counts() if counts is None else counts
        while True:
            counts.final_attempts += 1
            v = self.currency(t, counts)
            if self.rng.random() < self.a/(self.a+norm2(v)):
                return v
            counts.final_rejects += 1

    def weighted(self, t, counts=None):
        counts = Counts() if counts is None else counts
        return self._tree(t, counts, False)


def axis_source():
    return FiniteSource(tuple(tuple(sign if j == k else 0.0 for j in range(3))
                              for k in range(3) for sign in (-1.0, 1.0)),
                        (1.0/6.0,)*6)


def kac_population(source, size, horizon, seed=0):
    """Exact continuous-time finite-N Kac process, not exact nonlinear iid f_t.

    Each unordered pair collides at |v_i-v_j|/(N-1), so a tagged particle
    sees empirical normalized partner rate. Uniform pair proposal intensity
    is N*maxspeed, with acceptance |relative|/(2maxspeed). A lazy heap keeps
    the actual current maximum; no fixed unqualified speed cap is used.
    """
    if size < 2:
        raise ValueError("population >=2 required")
    rng = random.Random(seed)
    velocities = [source.draw(rng, 1.0) for _ in range(size)]
    versions = [0]*size
    heap = [(-norm2(v), i, 0) for i, v in enumerate(velocities)]
    heapq.heapify(heap)
    proposals = collisions = 0
    clock = 0.0
    while True:
        while heap[0][2] != versions[heap[0][1]]:
            heapq.heappop(heap)
        maxspeed = math.sqrt(-heap[0][0])
        if maxspeed == 0:
            break
        clock += rng.expovariate(size*maxspeed)
        if clock > horizon:
            break
        proposals += 1
        i = rng.randrange(size)
        j = rng.randrange(size-1)
        j += j >= i
        if rng.random() < distance(velocities[i], velocities[j])/(2*maxspeed):
            collisions += 1
            velocities[i], velocities[j] = elastic(velocities[i], velocities[j], rng)
            for index in (i, j):
                versions[index] += 1
                heapq.heappush(heap, (-norm2(velocities[index]), index, versions[index]))
    return velocities, {"proposals": proposals, "collisions": collisions,
                        "clock_overshoot": clock, "heap_entries_final": len(heap),
                        "finite_population": size,
                        "time_step_bias": False,
                        "nonlinear_population_bias_certified": False}
