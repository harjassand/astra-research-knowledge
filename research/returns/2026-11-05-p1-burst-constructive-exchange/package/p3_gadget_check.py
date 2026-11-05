"""Exact finite adversarial check of the two-round sparse-fault gadget.

This checks its semantic core, not a hardware simulation or the full hierarchy.
Each round holds five Info copies fixed, recomputes a full repetition word in
three separate passes, and takes pointwise majority.  A single spacetime island
may change one Info position, every retained Hold at that position, and one
entire pass arbitrarily.  One refresh round before the logical identity gate
must yield a regular output from any input, and preserve every regular input.
"""
import json
from pathlib import Path

FULL = 31

def logical(x):
    return int(x.bit_count() >= 3)

def regular(x):
    return x.bit_count() <= 1 or x.bit_count() >= 4

def setbit(x, i, b):
    return (x & ~(1 << i)) | (b << i)

def majority_words(a, b, c):
    return (a & b) | (a & c) | (b & c)

def run(initial, fault_round, fault_pass, fault_site, new_info, held_site_values, spoiled_word):
    info = initial
    for r in range(2):
        held = [0, 0, 0]
        for j in range(3):
            if (r, j) == (fault_round, fault_pass):
                info = setbit(info, fault_site, new_info)
                for h in range(3):
                    held[h] = setbit(held[h], fault_site, (held_site_values >> h) & 1)
                held[j] = spoiled_word
            else:
                held[j] = FULL if logical(info) else 0
        info = majority_words(*held)
    return info

def main():
    cases = 0
    regular_input_cases = 0
    for initial in range(32):
        for r in range(2):
            for j in range(3):
                for site in range(5):
                    for new_info in range(2):
                        for held_values in range(8):
                            for spoiled in range(32):
                                out = run(initial, r, j, site, new_info, held_values, spoiled)
                                assert regular(out), (initial, r, j, site, new_info, held_values, spoiled, out)
                                if regular(initial):
                                    assert logical(out) == logical(initial)
                                    regular_input_cases += 1
                                cases += 1
    vote_cases = 0
    for initial in range(32):
        for fault_round in range(2):
            for site in range(5):
                for new_bit in range(2):
                    x = initial
                    for r in range(2):
                        x = FULL if logical(x) else 0
                        if r == fault_round:
                            x = setbit(x, site, new_bit)
                    assert regular(x)
                    if regular(initial):
                        assert logical(x) == logical(initial)
                    vote_cases += 1
    result = {
        "status": "all exact adversarial finite checks passed",
        "scope": "semantic gadget only; not a simulation of the full multiscale physical circuit",
        "arbitrary_input_words": 32,
        "regular_input_words": 12,
        "active_pass_fault_cases": cases,
        "regular_input_active_cases": regular_input_cases,
        "vote_or_boundary_fault_cases": vote_cases,
        "guarantees": [
            "one fault island: arbitrary input becomes regular after one refresh round and one logical round",
            "one fault island: regular input logical value is preserved",
            "fault may corrupt one whole pass and all retained state at one spatial copy"
        ]
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
