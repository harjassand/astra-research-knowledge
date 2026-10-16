"""Independent algebra check, not execution/import of acquired author code.

Reconstructs the diffusion terms printed in MPO_Mechanisms.jl lines 192-208,
assuming the absent projector helpers implement the paper's P_out.
"""
import json
M, threshold, d = 16, 15, 8.2207

def p_out(x):
    return all(n <= threshold for n in x) and any(n == threshold for n in x)

def rates(x):
    out = {}
    # DRg is appended to cancel i -> i+1. DLg is constructed but not appended.
    for source, destination, corrected in [(0, 1, True), (1, 0, False)]:
        if x[source] > 0 and x[destination] < M:
            y = list(x)
            y[source] -= 1
            y[destination] += 1
            out[tuple(y)] = d*x[source]*(1-int(p_out(x)) if corrected else 1)
    return out

tests = [((16,14),(15,15)), ((14,16),(15,15)),
         ((15,15),(14,16)), ((15,15),(16,14))]
result = [{"from":x,"to":y,"rate":rates(x).get(y,0)} for x,y in tests]
print(json.dumps({"assumption":"Absent projector helpers implement Appendix D P_out",
                  "upstream_executed":False,"checks":result},indent=2))
