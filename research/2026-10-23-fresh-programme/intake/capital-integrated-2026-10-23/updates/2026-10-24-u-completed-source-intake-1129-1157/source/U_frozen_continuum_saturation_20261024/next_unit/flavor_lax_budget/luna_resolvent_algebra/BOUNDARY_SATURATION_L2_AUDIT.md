# Boundary saturation: L2-to-L1 audit

Let \(f(v)=vD(v)\in L^2(\mathbb R;\mathbb R^3)\) and \(g(v)=vG(v)\in L^2(\mathbb R)\), extended by zero outside \([-1,1]\). For \(z=x+iy\), let \(L_y(x)=\int f(v)/(x+iy-v)\,dv\) and \(\ell_y(x)=\int g(v)/(x+iy-v)\,dv\). The L2 Plemelj theorem gives strong L2 boundary convergence as \(y\downarrow0\):
\[
L_y\to L_+=A+iB,\quad B=-\pi f;
\qquad \ell_y\to\ell_+=a+ib,\quad b=-\pi g,
\]
with A,B real vectors and a,b real scalars. Strong L2 convergence implies convergence of the bilinear squares in L1, since
\[
\|L_y\!\cdot L_y-L_+\!\cdot L_+\|_1
\le (\|L_y\|_2+\|L_+\|_2)\|L_y-L_+\|_2,
\]
and likewise for \(\ell_y^2\). Thus the off-cut identity \(L\cdot L=\ell^2\) passes to the boundary as an L1 identity, hence almost everywhere. Expanding the complex bilinear products gives
\[
|A|^2-|B|^2=a^2-b^2,\qquad A\cdot B=ab.
\]

The pointwise ball bound yields \(|B|=\pi|v||D|\le \pi|v||G|=|b|\). The real equation then gives \(|A|^2=a^2-b^2+|B|^2\le a^2\). If \(b\ne0\) and \(a\ne0\), the imaginary equation and Cauchy give
\[
|a||b|=|A\cdot B|\le |A||B|\le |a||b|,
\]
so both norm bounds saturate and A,B are parallel with \(A=(a/b)B\). If \(b\ne0\) and \(a=0\), the real equation says \(|A|^2=|B|^2-b^2\); combined with \(|B|\le|b|\), this forces \(A=0\) and \(|B|=|b|\), again \(A=(a/b)B\). Therefore \(|D(v)|=|G(v)|\) wherever \(vG(v)\ne0\), almost everywhere there. On \(G=0\), the ball bound already gives D=0; the remaining set \(v=0\) is null. Hence \(|D|=R\) a.e. No charge assumption, including \(q\ne0\), is used in this saturation conclusion.
