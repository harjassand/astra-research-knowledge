#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
g++ -O3 -march=native -std=c++17 benchmark_cpp.cpp -o benchmark_cpp
: > benchmark_results.ndjson
./benchmark_cpp 256 32 5000 5 16 4 >> benchmark_results.ndjson
./benchmark_cpp 1024 64 1000 5 16 1 >> benchmark_results.ndjson
./benchmark_cpp 1024 64 1000 5 16 4 >> benchmark_results.ndjson
./benchmark_cpp 4096 64 1000 5 16 1 >> benchmark_results.ndjson
./benchmark_cpp 4096 64 1000 5 16 4 >> benchmark_results.ndjson
./benchmark_cpp 4096 64 1000 5 16 64 >> benchmark_results.ndjson
./benchmark_cpp 4096 256 500 5 32 4 >> benchmark_results.ndjson
./benchmark_cpp 16384 16 500 5 32 4 >> benchmark_results.ndjson
python - <<'PY'
import json
p='benchmark_results.ndjson'
with open(p) as f: rows=[json.loads(line) for line in f if line.strip()]
with open('benchmark_results.json','w') as f: json.dump(rows,f,indent=2)
print(json.dumps(rows,indent=2))
PY
