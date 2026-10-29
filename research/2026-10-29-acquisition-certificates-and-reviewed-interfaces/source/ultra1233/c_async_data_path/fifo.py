"""Literal noisy-bit state space and nominal atomic micropipeline actions.

Input/output records returned here are host accounting, never persistent
state consulted by the controller. No random path or hardware is simulated.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class FIFO:
    capacity: int
    packet_bits: int

    def __post_init__(self):
        if self.capacity < 1 or self.packet_bits < 1:
            raise ValueError("positive capacity and packet width required")

    @property
    def physical_bits(self):
        return (self.packet_bits + 1) * self.capacity + 1

    def tag(self, state, site):
        return (state >> (self.packet_bits * self.capacity + site)) & 1

    def payload(self, state, site):
        return (state >> (self.packet_bits * site)) & ((1 << self.packet_bits) - 1)

    def write_tag(self, state, site, value):
        position = self.packet_bits * self.capacity + site
        return (state & ~(1 << position)) | (int(value) << position)

    def write_payload(self, state, site, value):
        if not 0 <= value < (1 << self.packet_bits):
            raise ValueError("packet value outside the specified alphabet")
        mask = ((1 << self.packet_bits) - 1) << (self.packet_bits * site)
        return (state & ~mask) | (value << (self.packet_bits * site))

    def occupancy(self, state):
        return tuple(self.tag(state, j - 1) ^ self.tag(state, j)
                     for j in range(1, self.capacity + 1))

    def queue(self, state):
        e = self.occupancy(state)
        return tuple(self.payload(state, j - 1)
                     for j in range(self.capacity, 0, -1) if e[j - 1])

    def workload(self, state):
        return sum((self.capacity + 1 - j) * e
                   for j, e in enumerate(self.occupancy(state), 1))

    def input_capture(self, state, value):
        if self.tag(state, 0) != self.tag(state, 1):
            return state, False
        new = self.write_payload(state, 0, value)
        new = self.write_tag(new, 0, 1 - self.tag(state, 0))
        return new, True

    def internal(self, state, site):
        if not 1 <= site < self.capacity:
            raise ValueError("an internal site is between1 and M-1")
        prev, here, after = (self.tag(state, site - 1), self.tag(state, site),
                             self.tag(state, site + 1))
        if prev == here or here != after:
            return state, False
        new = self.write_payload(state, site, self.payload(state, site - 1))
        return self.write_tag(new, site, prev), True

    def output_commit(self, state):
        m = self.capacity
        if self.tag(state, m - 1) == self.tag(state, m):
            return state, None
        value = self.payload(state, m - 1)
        return self.write_tag(state, m, self.tag(state, m - 1)), value

    def fault(self, state, mask):
        if not 0 <= mask < (1 << self.physical_bits):
            raise ValueError("fault mask outside the actual physical state")
        return state ^ mask
