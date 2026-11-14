# Auxiliary geometric-face counting: four directions, paid hole entropy

This is ONLY a counting construction, not a new source sampler or a change to fixed-diagonal connectivity. Original allowed components remain NE/SW-augmented connected. The auxiliary hull/holes below are GEOMETRIC faces, and need NOT equal the original fixed-graph filled hull/holes.

## Encoding proof
LetS be a finite allowed component lifted into a b-by-bcellbox. FormG from ALL edges of its closedunit squares, including internalgrid edges. G is a connectedfiniteplanargraph because augmentedadjacency implies squares shareanedgeorvertex. A connectedplanegraph has one facialboundarywalk for eachface; the walk may repeatvertices (and generally may traversebridges twice). For thisG a physicalboundaryedge abuts one occupiedcellandoneemptyface, so it belongs to the appropriatephysicalfacewalk. Internalgrid edges onlyboundoccupiedunitcellfaces and arenot counted asphysicalperimeter.

LetWout be the boundarywalk of the unboundedface. Filling ALL boundedemptyfaces yields anauxiliaryfilledsetF, consisting oftheoriginaloccupiedcellsandthoseemptycells. Wout reconstructsF by integerwindingafterchoosingorientation. Repeatedvertices areallowed. The boundedEMPTYfaces have boundarywalksW_h thatlikewise reconstructtheircellsetsH_h by winding. DoNOTencode occupiedunitcellfaces asholes. No claimthattheseH_h agreewithfixed-diagonal graphholes, or thattheir connectivityconventionmatches originalsource.

EncodeF by canonicaldualvertexontorus andcompletephysicaldirectionword. AtouterlengthP thereareatmostn4^P codes. Rootfactor n is retained. Startingvertex+directions uniquelydeterminethewalk, henceF; invalidwordsovercount. Foraholefaceinsidebboxb, thereareatmost(b+1)^2canonicalrootvertices and4^q wordsatperimeterq. Encodeholes asanunorderedsetofdistinctcanonicalfacecodes. Recover S=F\unionH_h. Thus theencodingisinjective regardlessofcompatibilityconstraints discardedin theupperbound.

Everyphysicalboundaryedgebelongs either toouteremptyface or toexactlyoneboundedemptyface. Everyfilledcellis eitheroriginallyoccupiedoroneofthoseemptyfaces. Therefore
 P(S)=P(F)+sum_h P(H_h),
 |S|=|F|-sum_h|H_h|,
 E(S)=8P(F)-.04|F|+sum_h[8P(H_h)+.04|H_h|].

Let κ=sum_{q>=4}(4exp(-8))^q. Eachformalholeobjecthasweightatmostexp(-8q). Summingallformalunorderedsets(discardingoverlap/incompatibility) gives product_code(1+z_code)<=exp(sumz_code)<=exp((b+1)^2κ).

Hence forcomponentouterperimeter>=p0, enclosedinbboxb:
 sum_S exp(-E(S)) <= n exp((b+1)^2κ) sum_{P>=p0}[4exp(-(8-.01b))]^P.
Use |F|/P(F)<=b/4, or the sharper |F|<=min(P(F)^2/16,bP(F)/4).

## Firstexit application
ForanalyticboxRcore, existingfirst-additiongeometrygives b=2R+1 andouterwidth>=R+1. Auxiliaryholefilldoesnotchangespans, henceP(F)>=2R+4. Possibledeletedgates<=b², retainedindetailedbalancefluxbound. This applies tooriginalfixed-diagonalcomponentsbecauseeachisageometricallyconnectedS; geometriccountingmerelyovercounts.

AtR164: b329,p0332;4exp(-4.71)<1/27; holegasexponent(330)^2κ≈3.52e-7. Coreactivity canbe boundedwith exactsingleton term andsharperisoperimetriclow-Pbound. Existingrenewalfluxdivisionthenyieldsaroughfirstexitupperboundaround10^-455 withcoarserationalconstants. Sourceagentisindependentlycomputingcertifiedscalarbounds.

## Verification status
Sourceagentexecutedindependentrawgeometricfacechecks:2360smallallowedpolymers,250boundedemptyfaces,1101touchingouterwalks; uniquewalkreconstructionandP/energyfactorizationpassed. Generalargumentaboveusesstandardconnectedplanegraphfacialwalkfacts, notfiniteenumerationasproof. Needreview canonicalorientation/windingdecoderandtoruslift details. This is NOT a post-exitdurationbound or completednumeratortheorem.
