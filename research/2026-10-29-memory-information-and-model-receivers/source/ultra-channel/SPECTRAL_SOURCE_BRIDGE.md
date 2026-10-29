# Exact convention bridge for the named standard expander import

HLW2006 is a SURVEY; it is not being represented as the original primary derivation. Its acquired Construction8.1/Theorem8.2 is a secondary locator. Attempts to acquire the original Gabber–Galil1981 PDF returned403/406 or metadata only. Jimbo–Maruoka1987 Springer exposed metadata; the STOC PDF returned403. No original bytes were read, and no paywall purchase was made.

The acquired primary research paper Gross–Eisert, *Quantum Margulis Expanders*, Section2.2, printed page724 (PDF page3), gives the exact four classical maps H0,H+,V0,V- and the normalized bound5sqrt2/8 independent of the modulus. Its later odd-modulus restriction concerns the quantum/Wigner construction, which is not imported here. The printed numerator was visually inspected: it is5sqrt2, not sqrt25. The paper itself imports this standard classical graph result from its references; we claim an acquired primary research statement of the ordinary theorem, not an original proof read from Gabber–Galil or a new spectral theorem.

URL: https://www.rintonpress.com/xxqic8/qic-8-89/0722-0733.pdf

Acquired PDF SHA256: ad3c8051b7cae7046032e39d7fc077e00d415bdff12e93f187e471222754c92d.

Gross–Eisert's maps are

    H0(x,y)=(x+2y,y),       H+(x,y)=(x+2y+1,y),
    V0(x,y)=(x,y+2x),       V-(x,y)=(x,y+2x-1).

Our source uses H0,H+,V0,V+ with V+(x,y)=(x,y+2x+1). The reflection R(x,y)=(-x,y), identified by root, obeys the exact INTEGER affine identities

    R H0 R=H0^-1,   R H+ R=H+^-1,
    R V0 R=V0^-1,   R V- R=V+^-1.

Therefore the sets of eight generators, including their inverses, are conjugate for EVERY modulus. Loops and parallel edges are preserved, and the normalized undirected adjacency operators are permutation-conjugate. No translation by a half-integer, oddness condition, unproved phase-space quantization, or change to the compiled finite graph is used.

check_spectral_bridge.py verifies these as four3-by-3 integer affine-matrix identities and pays the rational relaxation8-5sqrt2>4/5 by the integer inequality1250<1296. SPECTRAL_BRIDGE.json records the result. The source-backed standard theorem and this exact convention change are separate from the new graph-to-information proof and from the finite35-dimensional LDL consumer.
