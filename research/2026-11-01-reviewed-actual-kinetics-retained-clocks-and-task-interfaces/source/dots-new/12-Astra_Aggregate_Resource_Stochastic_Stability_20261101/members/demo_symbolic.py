import json
import aggregate_mass as A
print(json.dumps(A.G.encode(A.construct(A.fixture(),2)),indent=2))
