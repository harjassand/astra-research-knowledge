#!/usr/bin/env python3
"""Build unchanged official SharpSAT-TD sources with its CMake-listed commands.

CMake is absent in the environment. The source lists, C/C++ flags and linked
libraries below reproduce the checked-in top-level/flowcutter CMakeLists.txt.
Development libraries are extracted from official Ubuntu archives locally.
"""
from pathlib import Path
import json
import subprocess
import time

here = Path(__file__).resolve().parent
source = here/'vendor/sharpsat-td'
deps = here/'vendor/deps/usr'
out = source/'local_build'
out.mkdir(exist_ok=True)
includes = ['-I'+str(deps/'include'), '-I'+str(deps/'include/x86_64-linux-gnu')]
flags = ['-std=c++11','-O3','-Wall','-Wextra','-Wshadow','-g','-Wfatal-errors',
         '-Wno-sign-compare','-Wno-literal-suffix','-DMPFR_USE_NO_MACRO'] + includes
libs = deps/'lib/x86_64-linux-gnu'
commands = [
    ['gcc','-std=c99','-Wall','-msse4.1','-mpclmul','-DMPFR_USE_NO_MACRO',
     '-c',str(source/'src/clhash/clhash.c'),'-o',str(out/'clhash.o')],
    ['g++']+flags+[str(source/p) for p in [
        'src/main.cpp', 'src/preprocessor/graph.cpp', 'src/preprocessor/instance.cpp',
        'src/preprocessor/oracle.cpp','src/preprocessor/preprocessor.cpp',
        'src/preprocessor/subsumer.cpp','src/preprocessor/treewidth.cpp',
        'src/preprocessor/twpp.cpp','src/decomposition.cpp']]
    +[str(out/'clhash.o'),str(libs/'libmpfr.a'),str(libs/'libgmpxx.a'),
      str(libs/'libgmp.a'),'-o',str(out/'sharpSAT')],
    ['g++']+flags+[str(source/'flowcutter'/p) for p in [
        'pace.cpp','cell.cpp','greedy_order.cpp','list_graph.cpp','tree_decomposition.cpp']]
    +['-o',str(out/'flow_cutter_pace17')]
]
started=time.perf_counter()
with (here/'sharpsat_td_build.log').open('w') as log:
    for command in commands:
        print('building', command[-1], flush=True)
        subprocess.run(command, cwd=source, stdout=log, stderr=subprocess.STDOUT, check=True)
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
result={'official_repository':'https://github.com/Laakeri/sharpsat-td',
        'commit':sha,'commands':commands,'build_seconds':time.perf_counter()-started,
        'note':'No source changes; manual command expansion of CMakeLists because CMake unavailable. Static GMP/MPFR linkage.'}
(here/'sharpsat_td_build.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='commands'},indent=2))
