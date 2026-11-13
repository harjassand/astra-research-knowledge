LAMINATE SHEAR TRANSFER, SHAPE WRITING AND RETAINED STIFFNESS
ROOT independent physical-model and primary-source contracts, 13 November 2026 UTC

This note investigates a specific candidate operation: reshape continuous generic
thin sheets by allowing relative feed, then make them carry useful loads through
reversible interlayer coupling. Keeping the same stock while changing its rest
geometry could support reusable fixtures or structures. Neither a large stiffness
ratio nor an electroadhesive clutch is by itself that complete operation. This is
a conditional mechanics construction, not a working invention or novelty claim.

OWN artifacts, in this directory:
ROOT_LAMINATE_SHEAR_TRANSFER_AND_WRITABLE_GEOMETRY_SCREEN_20261113.py
8678 ASCII bytes, SHA256 5c9d0557fab088507f727ef7e8a912eb1aa52d395dedf420d40dde87bb013d29
ROOT_LAMINATE_SHEAR_TRANSFER_AND_WRITABLE_GEOMETRY_SCREEN_20261113.json
7564 ASCII bytes, SHA256 544fc778b3c43c1c976af8fe587ea0ce6fd1e8fb60d7033c9ab68748b838e48c

The whole OWN script was independently read back equal to the composed source.
It executes with already-available NumPy in one bounded serial process, without
installation, external services or producer code. Section/mode identities, the
perfect-composite finite-element limit, root moment balance, monotonic coupling
and spatial refinement were checked. These checks validate the declared model,
not the material, contact, geometry writer, manufacturing yield or useful system.

1. Governing constructions actually read

Gaeta et al., Jamming Metal Sheets Using Electropermanent Magnets for Stiffness
Modulation, author accepted 2025 paper, DOI 10.1109/LRA.2025.3579246.
https://sites.bu.edu/ranzani-lab/files/2025/06/Jamming_Metal_Sheets_Using_Electropermanent_Magnets_for_Stiffness_Modulation-1.pdf
Actual main text 37--812, including fabrication, tests and conclusion, was read.
Prepared 25-micrometre steel sheets, sanding, laser cutting, thermal encapsulation
and glued EPMs are real prior construction. Four local EPMs switch finite stacks;
the stated 50 mJ/pulse is calculated, not a complete-system energy meter. In the
30 mm three-point test, ten layers change 28.41 to 47.76 mN/mm; twenty change
56.04 to 64.76. This is useful measured stiffness modulation, not complete
composite locking. Dynamic tests omit MRF stacks after observed shape retention.
The displayed squared-position-spectrum integral has dimensions length^2*time;
joules require a further calibrated mechanical model. No uncollected data were
reanalyzed. Figures, code, videos, manufacturer originals and cited papers were
not followed; load-bearing arbitrary shape writing, fatigue and full costs remain
outside this read experimental scope.

Levine et al., Electroadhesive Clutches with Enhanced Force Capacity Using Soft
Dielectric Interfaces, 2025, DOI 10.1002/adem.202402244.
https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/adem.202402244
Actual main 170--206 was read. Tests vary compliance, width, voltage, dielectric
modulus and roughness; interfacial separation limits the tested clutches. On-state
capacity and off-state resistance depend on surface forces as well as voltage.
Roughness improves switchability while reducing capacity. Thus a Coulomb pressure
model alone does not supply the measured contact behavior. The first followup at
207 timed out. Later multimodulus construction, Methods, life and supplementary
data are UNREAD and the identity is HELD. No measured material property from this
paper was fitted to the OWN laminate model.

DextrES, 2018, DOI 10.1145/3242587.3242657:
https://www.epfl.ch/labs/lmts/wp-content/uploads/2019/02/DextrES_final.pdf
First governing PDF open failed at 12371652 bytes. No governing device passage was
read. Search-rendered performance was not imported. The identity is HELD, including
other providers, versions and exports. No alternate or recovery was attempted.

Every source check completed locally before navigation. A failed read is an
observation limit, not evidence against its technology. All older known/unknown
source, access and transfer holds persist. No linked producer artifact was read
or executed. The two new held identities are operational restrictions, not
scientific assumptions, and are not appended to scientist questions.

2. A physically different model from serial adjustable joints

Take N continuous, individually bendable metal foils, separated by gaps d, with
centroid spacing h=t+d. All foils have width b, thickness t and modulus E. Normal
restraint is assumed to enforce a common transverse position and rotation theta.
It is a necessary unsupplied physical operation. Each foil has an independent
axial centroid displacement u_i(x). Fixed support gives u_i(0)=theta(0)=0; the free
end has no applied axial force or moment. An applied transverse tip force F does
work F*integral(theta dx) in the straight, small-deflection model.

Let EA=E*b*t, B0=N*E*b*t^3/12 and ks=G*b/d. G is an INTRODUCED effective tangent
shear modulus after contact, not a measured bulk or adhesive parameter. The
potential energy is

  1/2 integral[ EA sum_i u_i'^2 + B0 theta'^2
          + ks sum_i (u_(i+1)-u_i+h*theta)^2 ] dx
       - F integral(theta dx).

This explicitly keeps axial continuity. It is not the earlier segmented serial
spring surrogate silently combined with continuous tape. The dielectric gaps add
real section height and estimated mass. Their own axial and bending stiffness is
neglected. Normal deformation, separation, frictional slip, fracture, wrinkling,
large rotations and failure are not included. Common transverse restraint is not
granted by merely applying an electrical command.

At perfect stick, u_i=-y_i*theta and
  B_full = B0 + EA sum_i y_i^2.
At zero shear coupling, only B0 remains. A huge ratio B_full/B0 does not establish
adequate absolute bending stiffness or enough interface capacity.

3. Exact modal separation of finite transfer stiffness

Let D be the adjacent-layer difference operator, L=D^T D, and c=D^T 1. For each
nonzero layer eigenpair (lambda_k,v_k), c_k=v_k^T c. For a spatial mode with
wavenumber-squared p, eliminating axial displacements gives

  B_eff(p) = B0 + EA*h^2 sum_k
        [c_k^2/lambda_k^2] * [ks*lambda_k/(EA*p+ks*lambda_k)].

The stiffness experienced by the full loaded beam depends on its spatial modes;
one scalar clutch force capacity cannot replace this expression. The low layer
mode has lambda_1=4*sin(pi/(2N))^2. Its transfer length is
  ell_1=sqrt(EA/(ks*lambda_1)).
For fixed per-interface properties it grows with N, even while the perfect-stick
section becomes stiffer. Short clamps, stronger interfaces, different geometry or
fewer load-sharing layers can change this; no all-laminate obstruction follows.
This is ordinary linear mechanics worked through here, not a new solver claim.

4. Introduced useful-load example and an actual design trade

Use N=100, b=20 mm, t=25 micrometres, d=20 micrometres, E=200 GPa,
length 300 mm and tip load 5 N. No source supplies the resulting material or
installed contact point. Total section height is 4.48 mm; the model counts 117 g
metal plus 11.88 g gap material before encasing, clamps, wires, support, controller,
writer and power. B0=0.0005208333 N*m^2 and B_full=16.8738333 N*m^2, with a nominal
ratio 32397.76.

Perfect stick gives 2.66678 mm tip deflection on 100 spatial elements. With
INTRODUCED G=1.5 MPa it gives 8.36022 mm, maximum rotation 0.032966 rad and slowest
transfer length 0.259910 m. Refinement to 50/100/200 elements gives
8.33847/8.36022/8.36832 mm. With G=100 MPa the 100-element value is 2.75493 mm.
For THIS geometry and intact linear contact, the tangent needed for <=3 mm is
about 26.3482 MPa. It is not an obtained material requirement or a universal
threshold; the actual contact stiffness and envelope remain to be established.

The G=0, 10 kPa and 100 kPa linear diagnostics exceed the introduced 0.1-rad
small-rotation screen. Their large calculated deflections/stresses are outside
the model's physical use; they are neither predicted real shapes nor measured
failure. The finite-coupling examples still require a real contact to remain
intact and a real transverse restraint. No modulus from the soft-clutch source
is transferred to this example.

An appealing soft interface can have large static adhesion yet insufficient
tangent shear stiffness over the beam length. A thinner dielectric changes both
transfer stiffness and this particular section's spacing; it cannot improve ks
while silently retaining free gap height. Stiff dielectric contacts, mechanically
retained collars or a different separated-skin geometry are legitimate options,
with their actual preload, separation, mass, friction, opening and manufacture.

5. Strength is a separate operation

For perfect composite bending under this point force, the required shear flow
at interface i is F*EA*abs(sum_(j<=i) y_j)/B_full. The maximum is
1666.7819 N/m, or 83.3391 kPa over the 20 mm width.

An INTRODUCED friction coefficient 0.3 and pressure difference 100 kPa would give
only 30 kPa ideal frictional capacity, corresponding to 1.79988 N tip load if full
stick is required. Exceedance invalidates that perfect-stick claim; it does not
solve the subsequent slip shape or rule out another mechanism. A discrete collar
every 20 mm would need about 111.119 N normal force at the critical interface
under the same ideal Coulomb law, before margins, transfer compliance and access.
These are possible finite physical requirements, not an acquired clamp or a
qualification of electroadhesion, which may instead fail by interfacial fracture.

6. Geometry writing still needs real material feed and state retention

A separate unloaded quarter-circle of radius 190.986 mm over 300 mm length
requires about 6.99790 mm difference between outermost and innermost foil lengths.
A writer must supply and retain that actual relative phase. Bonding equal lengths
at both ends does not give free arbitrary curvature. Controlled end slip, stock
feed or pre-existing excess length must have a physical path.

For freely sliding introduced foils, this curve has outer-fiber strain
6.54498e-5, stress 13.090 MPa, bending moment 0.00272708 N*m and elastic energy
0.00214184 J. This offers a concrete low-force forming possibility. It does not
qualify yield, cyclic life, edges, torsion, wrinkles, normal contact, end feed or
rest geometry after the writer withdraws. Jamming after forming also needs enough
capacity to resist elastic springback and the subsequent useful load. Releasing
a loaded region requires another real load path and energy capture.

No actuator per layer is demanded by the equations, but no shared writer,
addressable persistent lock, support or economical autonomous reconfiguration is
constructed. The actual EPM source already supplies local noncontinuous-power
switching; merely calling that programmable material is not a new invention.
Ordinary clamps, continuous-laminate and adjustable-fixture techniques receive the
same available primitives in any future whole-operation comparison.

7. Remaining scientific operation

Construct one coherent physical load path combining flexible feed, actual
differential registration, adequate incremental coupling, sufficient contact
capacity and a controlled release route. Then account for preparation, sensing,
writers, locks, power, maintenance and strong ordinary useful-operation alternatives.
This note supplies a calculable interface and a plausible unloaded forming scale,
not that apparatus, an accepted physical output, a general shape compiler or a
full-cycle advantage. No purchase, installation, outreach, laboratory or physical
experiment was performed or authorized by this work.
