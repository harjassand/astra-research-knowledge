import mpmath as mp
mp.mp.dps=70
n=5; d=2**n
H=mp.zeros(d); P=mp.zeros(d)
for b in range(d):
 z=lambda j: 1 if not ((b>>(n-1-j))&1) else -1
 for j in range(n):
  H[b,b]+=(mp.mpf('.91')+mp.mpf('.013')*(j%3))*z(j)
  H[b^(1<<(n-1-j)),b]+=mp.mpf('.67')+mp.mpf('.007')*(j%2)
 for j in range(n-1):
  H[b,b]+=mp.mpf('.43')*z(j)*z(j+1)
  H[b^(1<<(n-1-j)),b]+=mp.mpf('.19')*z(j+1)
 P[b,b]=z(n//2)
E,U=mp.eigsy(H); P=U.T*P*U; Delta=E[0]-E[d-1]; pole=2j*mp.pi/Delta
num=sum(P[0,c]*mp.exp(-pole*E[c])*P[c,d-1] for c in range(d))
print('n',n,'working decimal digits',mp.mp.dps)
print('width',mp.nstr(-Delta,50)); print('pole modulus',mp.nstr(abs(pole),50))
print('numerator',mp.nstr(num,50)); print('residue magnitude',mp.nstr(abs(-pole*mp.exp(pole*E[0])*num),50))
