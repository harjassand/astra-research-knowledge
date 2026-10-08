"""Exact-structure qutrit broadcaster from a symmetric cubic-phase tensor."""
import numpy as np

d = 3
omega = np.exp(2j * np.pi / 3)

def index(i, a, b):
    return 9*i + 3*a + b

def cubic_vector(beta=0, gamma=1, conjugate=False):
    psi = np.zeros(d**3, complex)
    for i in range(d):
        for a in range(d):
            b = (-i-a) % d
            phase = beta * (i*a + a*b + b*i) + gamma * i*a*b
            z = omega ** phase
            if conjugate:
                z = z.conjugate()
            psi[index(i,a,b)] = z / 3
    return psi

def marginal_choi(beta=0, gamma=1):
    p = cubic_vector(beta, gamma, False)
    q = cubic_vector(beta, gamma, True)
    Om = (np.outer(p,p.conj()) + np.outer(q,q.conj())) / 2
    Om3 = Om.reshape((d,d,d,d,d,d))
    # Choi RA = trace out B. Layout row (R,A,B), col (R',A',B').
    J = np.zeros((d*d,d*d), complex)
    for i in range(d):
        for a in range(d):
            for j in range(d):
                for ap in range(d):
                    J[i*d+a, j*d+ap] = sum(Om[index(i,a,b), index(j,ap,b)] for b in range(d))
    return Om, J

def gell_mann_basis():
    out = []
    for i in range(d):
        for j in range(i+1,d):
            A = np.zeros((d,d), complex); A[i,j]=A[j,i]=1
            B = np.zeros((d,d), complex); B[i,j]=-1j; B[j,i]=1j
            out.extend([A*np.sqrt(d/2), B*np.sqrt(d/2)])
    for k in range(1,d):
        A=np.zeros((d,d),complex)
        A[np.arange(k),np.arange(k)]=1
        A[k,k]=-k
        A *= np.sqrt(d/(k*(k+1)))
        out.append(A)
    return out

def main():
    Om,J=marginal_choi()
    Om3=Om.reshape(d,d,d,d,d,d)
    basis=gell_mann_basis()
    Phi=[]
    for A in basis:
        out=np.zeros((d,d),complex)
        for i in range(d):
            for j in range(d):
                for a in range(d):
                    for b in range(d):
                        out[a,b] += 3*J[i*d+a,j*d+b]*A[i,j]
        Phi.append(out)
    T=np.array([[np.trace(A.conj().T*0 + A.conj().T@PhiB).real/d for PhiB in Phi] for A in basis])
    print("Om_min_eig",np.linalg.eigvalsh(Om)[0])
    print("J_min_eig",np.linalg.eigvalsh(J)[0])
    print("R_marginal",np.round(np.einsum("iabjab->ij", Om3),5))
    print("J_output_marginal",np.round(np.einsum("iaib->ab",J.reshape(d,d,d,d)),5))
    print("J_swap_error",np.linalg.norm(J.reshape(d,d,d,d).transpose(1,0,3,2)-J.reshape(d,d,d,d)))
    print("J_imag_error",np.linalg.norm(J.imag))
    print("transfer_symmetry_error",np.linalg.norm(T-T.T))
    print("transfer",np.round(T,8))
    print("transfer_eigenvalues",np.round(np.linalg.eigvalsh(T),8))
    print("phase_family_spectra")
    for beta in range(3):
        for gamma in range(3):
            _,Jb=marginal_choi(beta,gamma)
            transfer=[]
            for A in basis:
                out=np.zeros((d,d),complex)
                for i in range(d):
                    for j in range(d):
                        for a in range(d):
                            for b in range(d):
                                out[a,b] += 3*Jb[i*d+a,j*d+b]*A[i,j]
                transfer.append(out)
            Tb=np.array([[np.trace(A.conj().T@B).real/d for B in transfer] for A in basis])
            print((beta,gamma),np.round(np.linalg.eigvalsh(Tb),8).tolist())

if __name__ == "__main__":
    main()
