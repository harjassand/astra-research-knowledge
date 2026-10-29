# Eight-CNOT four-spin singlet encoder
2026-10-29. Root analytic construction. The separately written executed netlist and independent receipt govern their own byte versions. No optimality or historical-priority claim.

Use pair Bell labels beta_ab=(|0,b>+(-1)^a|1,b xor1>)/sqrt2, implemented by H on a followed by CNOT a->b. Thus beta00=Phi+, beta01=Psi+, beta10=Phi−, beta11=Psi−. In these labels the desired orthonormal singlet-code basis is

 psi0=beta11 tensor beta11,
 psi1=(beta00 tensor beta00−beta10 tensor beta10−beta01 tensor beta01)/sqrt3.

Expanding psi1 gives (|0011>+|1100>−(|0101>+|0110>+|1001>+|1010>)/2)/sqrt3. Both states have total spin zero; equivalently psi0 couples two spin-zero pairs and psi1 couples two spin-one pairs to spin zero.

Let label pair A=(a,b) initially contain logical qubit a and a clean b=0; pair B=(c,d) is00. Apply:
1. X_a X_b.
2. R_y(theta1) on b conditioned on a=0, theta1=−2 arcsin(sqrt(2/3)).
3. R_y(pi/2) on a conditioned on b=0.
4. Z_a Z_b.
5. CNOT a->c and CNOT b->d, copying computational Bell labels coherently.
6. Bell transforms H_a,CNOT a->b and H_c,CNOT c->d.

For logical0, step1 yields11 in A, both controlled rotations are inactive, and step4 gives total phase+1. Copying and Bell transforms yieldpsi0. For logical1, step1 yields01. Step2 gives sqrt(2/3)|00>+|01>/sqrt3. Step3 gives(|00>+|01>+|10>)/sqrt3. Step4 flips exactly01 and10, giving the three required Bell-label amplitudes. Copying plus Bell transforms yieldspsi1. Linearity proves the isometry on arbitrary logical inputs entangled with any reference.

A negative-controlled R_y(theta) is exactly X_control, R_y(theta/2)_target, CNOT, R_y(-theta/2)_target, CNOT, X_control, in chronological order. Each costs two CNOT and four one-qubit gates. The full encoder therefore has8 CNOT and14 one-qubit gates on four qubits, with no fifth work qubit. The inverse reverses gates and rotation signs, with the same count. Arbitrary-pair connectivity is assumed for this count; routing and real calibration are separate. Known learned local frame rotations add four one-qubit operations on encoding and four inverse operations on decoding.

For arbitrary physical output, the inverse unitary alone followed by discarding the three ancillas need not equal the previously used canonical decoder. Measure those ancillas: if allzero, retain logicaloutput; otherwise reset logicaloutput to the declared fixedstate. This implements D(X)=E† X E+Tr[(I−EE†)X] tau exactly. It also shows why a different full-unitary completion of the same two encoded columns gives the same reset-completed channel. The older500-CNOT QR construction is mathematically valid but superseded for resource estimates by this explicit circuit.

Counts omit the three ancillary measurements and conditional reset and do not treat their errors as free. The gates contain algebraic rotation amplitudes and can be approximated by a specified hardware gate set only with a separately budgeted synthesis/calibration error. No laboratory performance, fault-tolerance threshold or generic advantage over a conventional controller is asserted; every controller using this same inner code may use this encoder.
