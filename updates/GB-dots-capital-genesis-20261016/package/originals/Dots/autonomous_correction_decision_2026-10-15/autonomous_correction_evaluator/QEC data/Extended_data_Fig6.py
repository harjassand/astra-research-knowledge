from qutip import *
from qutip.control import *
import numpy as np
import multiprocessing
import time
import math
import scipy.optimize as sc
import scipy.linalg as sl
import matplotlib.pyplot as plt # plotting library
from scipy.optimize import minimize, curve_fit


'''
这个程序考虑逻辑态的相位和错误态的相位分开做平均
'''


###### 得到不同失谐、不同时刻下有重复自动纠错操作的保真度，这里考虑重复自动纠错会引入一个逻辑比特上长漂的相位积累，Kraus算符形式
###### state and Hamiltonian
dim = 4
psi_minus_3 = basis(4, 0)                                                      # D_5/2
psi_minus_1 = basis(4, 1)
psi_plus_1 = basis(4, 2)
psi_plus_3 = basis(4, 3)     
###### logical state and error state
psi_L0 = 1/2*psi_minus_3+np.sqrt(3)/2*psi_plus_1
psi_L1 = np.sqrt(3)/2*psi_minus_1+1/2*psi_plus_3
psi_E0 = -np.sqrt(3)/2*psi_minus_3+1/2*psi_plus_1
psi_E1 = -1/2*psi_minus_1+np.sqrt(3)/2*psi_plus_3
psi_set = [psi_L1, psi_L0]
cons_state = 2
###### operator
S_z = (-3/2*psi_minus_3*psi_minus_3.dag()
       -1/2*psi_minus_1*psi_minus_1.dag()
       +1/2*psi_plus_1*psi_plus_1.dag()
       +3/2*psi_plus_3*psi_plus_3.dag())
R_0 = psi_L0*psi_L0.dag()+psi_L1*psi_L1.dag()
R_1 = psi_L0*psi_E0.dag()+psi_L1*psi_E1.dag()
p_AQEC = 0.00
p_init = 0.00
K_init_0 = np.sqrt(1-p_init)*(psi_L0*psi_L0.dag()+psi_L1*psi_L1.dag())           # encoding过程对应的Kraus operator
K_init_1 = np.sqrt(p_init)*(psi_E0*psi_L0.dag()+psi_E1*psi_L1.dag())             # encoding过程对应的Kraus operator
K_AQEC_0 = np.sqrt(1-p_AQEC)*(psi_L0*psi_L0.dag()+psi_L1*psi_L1.dag())           # AQEC过程对应的Kraus operator 唯像的形式
K_AQEC_1 = np.sqrt(p_AQEC)*(psi_E0*psi_L0.dag()+psi_E1*psi_L1.dag())             # AQEC过程对应的Kraus operator 唯像的形式
p_0 = 0.98
p_1 = 0.02
Delta_theta = np.sqrt(0.06)
K_AQEC_r0 = np.sqrt(p_0)*(Delta_theta*(psi_E0*psi_E0.dag()+psi_E1*psi_E1.dag())
                         +(psi_L0*psi_L0.dag()+psi_L1*psi_L1.dag()))
K_AQEC_r1 = np.sqrt(p_1*(1-Delta_theta**2))*(psi_E0*psi_L0.dag()+psi_E1*psi_L1.dag())
K_AQEC_r2 = np.sqrt(p_0*(1-Delta_theta**2))*(psi_L0*psi_E0.dag()+psi_L1*psi_E1.dag())
K_AQEC_r3 = np.sqrt(p_1)*(Delta_theta*(psi_L0*psi_L0.dag()+psi_L1*psi_L1.dag())
                         +np.cos(np.sqrt(2)*np.pi/2)*(psi_E0*psi_E0.dag()+psi_E1*psi_E1.dag()))
K_AQEC_r4 = np.sqrt(p_1)*np.sin(np.sqrt(2)*np.pi/2)*(psi_L0*psi_E0.dag()+psi_L1*psi_E1.dag())
#print((K_AQEC_r0.dag()*K_AQEC_r0+K_AQEC_r1.dag()*K_AQEC_r1+
#       K_AQEC_r2.dag()*K_AQEC_r2+K_AQEC_r3.dag()*K_AQEC_r3+
#       K_AQEC_r4.dag()*K_AQEC_r4).tr())

sigma_0 = psi_L1*psi_L1.dag()+psi_L0*psi_L0.dag()
sigma_1 = psi_L1*psi_L0.dag()+psi_L0*psi_L1.dag()
sigma_2 = -psi_L1*psi_L0.dag()+psi_L0*psi_L1.dag()
sigma_3 = psi_L1*psi_L1.dag()-psi_L0*psi_L0.dag()
sigma_operators = [sigma_0,sigma_1,sigma_2,sigma_3]
I = sigma_0
LGroup = []

def QST(rho):
    P_x_1 = 1/2*(psi_L0+psi_L1)*(psi_L0.dag()+psi_L1.dag())
    P_y_1 = 1/2*(psi_L1+1j*psi_L0)*(psi_L1.dag()-1j*psi_L0.dag())
    P_z_1 = psi_L1*psi_L1.dag()
    temp_tomo_a = (1/2*sigma_0
                  +1/2*((2*P_x_1-I)*rho).tr()*(sigma_1)
                  +1/2*((2*P_y_1-I)*rho).tr()*(1j*sigma_2)
                  +1/2*((2*P_z_1-I)*rho).tr()*(sigma_3)
                  )
    return(temp_tomo_a)

# 矩阵beta_{mn}^{jk}
sigma_mn = sigma_operators
beta_1 = []
for mn in range(cons_state**4):
    beta_1.append([])
    for j in range(cons_state**2):
        temp_rho = psi_set[j//cons_state]*psi_set[j%cons_state].dag() 
        temp_rho = sigma_mn[mn//(cons_state**2)]*temp_rho*(sigma_mn[mn%(cons_state**2)].dag())
        for k in range(cons_state**2):
            temp_beta = (temp_rho*(psi_set[k//cons_state]*psi_set[k%cons_state].dag())).tr()
            beta_1[mn].append(temp_beta)


###### analysis of fidelity loss
N_delta = 13
Fi_AQEC=[]
T_AQEC = 75
tau_AQEC = 1
N_AQEC = int(T_AQEC/tau_AQEC)-1
sigma_delta = 0.1
sigma_phi_L = 0.044
sigma_phi_E = 0.44
n_step = 40
n_slice = 40
n_total = n_slice*int(T_AQEC/tau_AQEC)
tlist_AQEC = np.linspace(0, tau_AQEC, n_slice)
#psi_initial = np.sqrt(1/2)*(psi_L0-psi_L1)
#psi_initial = psi_L1
psi_initial = np.sqrt(1/2)*psi_L0-1j*np.sqrt(1/2)*psi_L1
LGroup = []
'''
###### 得到不同失谐、不同时刻下有纠错操作的保真度
weight_r=0
weight_p=0
for temp_phi in range(N_delta):
    # 计算权重
    weight_r=weight_r+np.sqrt(1/2/np.pi)/sigma_delta*np.exp(-((temp_phi-N_delta//2)*sigma_delta/6)**2/2/sigma_delta**2)
    weight_p=weight_p+np.sqrt(1/2/np.pi)/sigma_phi*np.exp(-((temp_phi-N_delta//2)*sigma_phi/6)**2/2/sigma_phi**2)
    phi = (temp_phi-N_delta//2)*sigma_phi/6
    U_phi = (-1j*psi_L1*psi_L1.dag()*phi-1j*psi_E1*psi_E1.dag()*10*phi).expm()
    Fi_AQEC.append([])
    for temp_delta in range(N_delta):
        delta = (temp_delta-N_delta//2)*sigma_delta/6
        # 计算保真度
        Fi_AQEC[temp_phi].append([])
        H_0=delta*S_z                    
        rho=psi_initial*psi_initial.dag()
        # rho=K_init_0*rho*K_init_0.dag()+K_init_1*rho*K_init_1.dag()
        Fi_AQEC[temp_phi][temp_delta].append(expect(rho, psi_initial*psi_initial.dag()))
        for temp in range(N_AQEC+1):                                                 # temp1 = tau * j j表示第j个脉冲
            result=mesolve(H_0, rho, tlist_AQEC, LGroup)
            for temp_1 in range(n_slice//n_step):
                rho = result.states[temp_1*n_step+(n_step-1)]
                # rho = R_0*rho*R_0.dag()+R_1*rho*R_1.dag()
                # rho = K_AQEC_0*rho*K_AQEC_0.dag()+K_AQEC_1*rho*K_AQEC_1.dag()
                rho = (K_AQEC_r0*rho*K_AQEC_r0.dag()+
                       K_AQEC_r1*rho*K_AQEC_r1.dag()+
                       K_AQEC_r2*rho*K_AQEC_r2.dag()+
                       K_AQEC_r3*rho*K_AQEC_r3.dag()+
                       K_AQEC_r4*rho*K_AQEC_r4.dag())
                rho = U_phi*rho*U_phi.dag()
                Fi_AQEC[temp_phi][temp_delta].append(expect(rho, psi_initial*psi_initial.dag())) 
                                                                                   # 得到不同失谐、不同时刻下有纠错操作的保真度
'''
###### 得到不同时刻AQEC操作的过程保真度
# 计算权重
weight_r=0
weight_p_L=0
weight_p_E=0
for temp in range(N_delta):
    weight_r=weight_r+np.sqrt(1/2/np.pi)/sigma_delta*np.exp(-((temp-N_delta//2)*sigma_delta/2)**2/2/sigma_delta**2)
    weight_p_L=weight_p_L+np.sqrt(1/2/np.pi)/sigma_phi_L*np.exp(-((temp-N_delta//2)*sigma_phi_L/2)**2/2/sigma_phi_L**2)
    weight_p_E=weight_p_E+np.sqrt(1/2/np.pi)/sigma_phi_E*np.exp(-((temp-N_delta//2)*sigma_phi_E/2)**2/2/sigma_phi_E**2)
# 计时
time_start=time.time()
# 建立一个list，存放了不同初始态、演化到不同时刻的量子态
rho_tomo = []
for i in range(cons_state**2):
    rho_tomo.append([])
    for j in range(int(T_AQEC/tau_AQEC)+1):
        rho_tomo[i].append(0*I)
# 对角的态作为初始态进行演化
for i in range(cons_state):
    psi_initial = psi_set[i]
    for temp_phi_L in range(N_delta):
        phi_L = (temp_phi_L-N_delta//2)*sigma_phi_L/2
        for temp_phi_E in range(N_delta):
            phi_E = (temp_phi_E-N_delta//2)*sigma_phi_E/2
            U_phi = (-1j*psi_L1*psi_L1.dag()*phi_L-1j*psi_E1*psi_E1.dag()*10*phi_E).expm()
            for temp_delta in range(N_delta):
                delta = (temp_delta-N_delta//2)*sigma_delta/2
                H_0=delta*S_z                    
                rho=psi_initial*psi_initial.dag()
                rho_tomo[i*cons_state+i][0] = rho
                for temp in range(N_AQEC+1):                                                 # temp1 = tau * j j表示第j个脉冲            
                    result=mesolve(H_0, rho, tlist_AQEC, LGroup)                
                    rho = result.states[-1]
                    rho = (K_AQEC_r0*rho*K_AQEC_r0.dag()+
                           K_AQEC_r1*rho*K_AQEC_r1.dag()+
                           K_AQEC_r2*rho*K_AQEC_r2.dag()+
                           K_AQEC_r3*rho*K_AQEC_r3.dag()+
                           K_AQEC_r4*rho*K_AQEC_r4.dag())
                    rho = U_phi*rho*U_phi.dag()
                    temp_tomo = QST(rho)
                    rho_tomo[i*cons_state+i][temp+1] += (temp_tomo
                                                         *np.sqrt(1/2/np.pi)/sigma_phi_L*np.exp(-((temp_phi_L-N_delta//2)*sigma_phi_L/2)**2/2/sigma_phi_L**2)
                                                         *np.sqrt(1/2/np.pi)/sigma_phi_E*np.exp(-((temp_phi_E-N_delta//2)*sigma_phi_E/2)**2/2/sigma_phi_E**2)
                                                         *np.sqrt(1/2/np.pi)/sigma_delta*np.exp(-((temp_delta-N_delta//2)*sigma_delta/2)**2/2/sigma_delta**2)
                                                         )/weight_r/weight_p_L/weight_p_E 
for i in range(cons_state):
    for j in range(i+1, cons_state):
        psi_initial_1 = 1/np.sqrt(2)*(psi_set[i]+psi_set[j])
        psi_initial_2 = 1/np.sqrt(2)*(psi_set[i]+1j*psi_set[j])
        for temp_phi_L in range(N_delta):
            phi_L = (temp_phi_L-N_delta//2)*sigma_phi_L/2
            for temp_phi_E in range(N_delta):
                phi_E = (temp_phi_E-N_delta//2)*sigma_phi_E/2
                U_phi = (-1j*psi_L1*psi_L1.dag()*phi_L-1j*psi_E1*psi_E1.dag()*10*phi_E).expm()
                for temp_delta in range(N_delta):
                    delta = (temp_delta-N_delta//2)*sigma_delta/2
                    H_0 = delta*S_z
                    rho_1 = psi_initial_1*psi_initial_1.dag()
                    rho_2 = psi_initial_2*psi_initial_2.dag()
                    rho_tomo[i*cons_state+j][0] = rho_1+1j*rho_2-(1+1j)/2*(rho_tomo[i*cons_state+i][0]+rho_tomo[j*cons_state+j][0])
                    rho_tomo[j*cons_state+i][0] = rho_1-1j*rho_2-(1-1j)/2*(rho_tomo[i*cons_state+i][0]+rho_tomo[j*cons_state+j][0])
                    for temp in range(N_AQEC+1):                                                 # temp1 = tau * j j表示第j个脉冲
                        result_1=mesolve(H_0, rho_1, tlist_AQEC, LGroup)
                        result_2=mesolve(H_0, rho_2, tlist_AQEC, LGroup)
                        rho_1 = result_1.states[-1]
                        rho_2 = result_2.states[-1]
                        rho_1 = (K_AQEC_r0*rho_1*K_AQEC_r0.dag()+
                                 K_AQEC_r1*rho_1*K_AQEC_r1.dag()+
                                 K_AQEC_r2*rho_1*K_AQEC_r2.dag()+
                                 K_AQEC_r3*rho_1*K_AQEC_r3.dag()+
                                 K_AQEC_r4*rho_1*K_AQEC_r4.dag())
                        rho_2 = (K_AQEC_r0*rho_2*K_AQEC_r0.dag()+
                                 K_AQEC_r1*rho_2*K_AQEC_r1.dag()+
                                 K_AQEC_r2*rho_2*K_AQEC_r2.dag()+
                                 K_AQEC_r3*rho_2*K_AQEC_r3.dag()+
                                 K_AQEC_r4*rho_2*K_AQEC_r4.dag())
                        rho_1 = U_phi*rho_1*U_phi.dag()
                        rho_2 = U_phi*rho_2*U_phi.dag()
                        temp_tomo_1 = QST(rho_1)
                        temp_tomo_2 = QST(rho_2)
                        rho_tomo[i*cons_state+j][temp+1] += ((temp_tomo_1+1j*temp_tomo_2-(1+1j)/2*(rho_tomo[i*cons_state+i][temp+1]+rho_tomo[j*cons_state+j][temp+1]))
                                                             *np.sqrt(1/2/np.pi)/sigma_phi_L*np.exp(-((temp_phi_L-N_delta//2)*sigma_phi_L/2)**2/2/sigma_phi_L**2)
                                                             *np.sqrt(1/2/np.pi)/sigma_phi_E*np.exp(-((temp_phi_E-N_delta//2)*sigma_phi_E/2)**2/2/sigma_phi_E**2)
                                                             *np.sqrt(1/2/np.pi)/sigma_delta*np.exp(-((temp_delta-N_delta//2)*sigma_delta/2)**2/2/sigma_delta**2)
                                                             )/weight_r/weight_p_L/weight_p_E  
                        rho_tomo[j*cons_state+i][temp+1] += ((temp_tomo_1-1j*temp_tomo_2-(1-1j)/2*(rho_tomo[i*cons_state+i][temp+1]+rho_tomo[j*cons_state+j][temp+1]))
                                                             *np.sqrt(1/2/np.pi)/sigma_phi_L*np.exp(-((temp_phi_L-N_delta//2)*sigma_phi_L/2)**2/2/sigma_phi_L**2)
                                                             *np.sqrt(1/2/np.pi)/sigma_phi_E*np.exp(-((temp_phi_E-N_delta//2)*sigma_phi_E/2)**2/2/sigma_phi_E**2)
                                                             *np.sqrt(1/2/np.pi)/sigma_delta*np.exp(-((temp_delta-N_delta//2)*sigma_delta/2)**2/2/sigma_delta**2)
                                                             )/weight_r/weight_p_L/weight_p_E 
         
# 不同时刻的lambda_jk矩阵
alpha = []
for temp in range(N_AQEC+1):
    alpha.append([])
    for i in range(cons_state**2):
        for j in range(cons_state**2):
            temp_alpha = (rho_tomo[i][temp]*(psi_set[j//cons_state]*psi_set[j%cons_state].dag())).tr()
            alpha[temp].append(temp_alpha)
# 不同时刻实际信道的Kraus operators与average fidelity
Fi_t_AQEC = []
Fi_t_AQEC_pro = []
beta_1 = np.array(beta_1)
beta_inv = sl.pinv(beta_1)
for temp in range(N_AQEC+1):
    alpha_t = np.array(alpha[temp])
    chi = (beta_inv.T) @ alpha_t
    chi = chi.reshape(cons_state**2, cons_state**2)
    Fi_t_AQEC_pro.append(np.real(chi[0][0]))
    chi_eigenvals, chi_eigenvects = np.linalg.eig(chi)
    eigenvalue = chi_eigenvals
    chi_eigenvals[np.real(chi_eigenvals)<0] = 0
    chi_eigenvals = np.real(chi_eigenvals)/sum(np.real(chi_eigenvals))
    G = []
    for i in range(len(chi_eigenvals)):
        temp_G = 0
        for j in range(cons_state**2):
            temp_G += np.sqrt(chi_eigenvals[i])*chi_eigenvects[j][i]*sigma_mn[j]
        G.append(temp_G)
    U_Targ=I
    temp_F = 0
    for i in range(len(chi_eigenvals)):
        temp_F += 1/6*((G[i].dag()*G[i]).tr()+abs((U_Targ.dag()*G[i]).tr())**2)
    Fi_t_AQEC.append(temp_F)
np.savetxt("fidelity_t_AQEC_process.txt", Fi_t_AQEC_pro)
np.savetxt("fidelity_t_AQEC_average.txt", Fi_t_AQEC)    

###### 解析解
def exact_AQEC(n):
    if n==0:
        return (1-p_init)
    else:
        temp_fi = 0    
        for j in range(n):
            for k in range(j+1):
                temp = ((3/4)*np.exp(-(sigma_delta*tau_AQEC)**2/2*(n+2*j-4*k)**2)
                        +(3/8-1/2*p_init)*np.exp(-(sigma_delta*tau_AQEC)**2/2*(n+2*j-4*k-2)**2)
                        +(-1/8+1/2*p_init)*np.exp(-(sigma_delta*tau_AQEC)**2/2*(n+2*j-4*k+2)**2))
                C_n_j = math.factorial(n-1)/math.factorial(j)/math.factorial(n-1-j)
                C_j_k = math.factorial(j)/math.factorial(k)/math.factorial(j-k)
                temp_fi += C_n_j*(3/4)**(n-1-j)*C_j_k*(-1/8+1/2*p_AQEC)**(j-k)*(3/8-1/2*p_AQEC)**k*temp
    return ((1-p_AQEC)*(2/3+1/3*temp_fi))
#   return ((1-p_AQEC)*(2/3+1/3*temp_fi))
'''
def exp_AQEC(n, beta):
    return (1-p_AQEC)*(2/3+1/3*((9/8-1/2*p_AQEC)*np.exp(-n/2*(sigma_delta*tau_AQEC*beta)**2)
                               -(1/8-1/2*p_AQEC)*np.exp(-9*n/2*(sigma_delta*tau_AQEC*beta)**2))**n)
def exp_AQEC(n, gamma):
    return 2/3+1/3*(9/8*np.exp(-1/2*(sigma_delta*tau_AQEC*gamma)**2)
                   -1/8*np.exp(-9/2*(sigma_delta*tau_AQEC*gamma)**2))**n
'''
def exp_0beta(n, tau_2, a, c, beta):
    return a-c+c*np.exp(-(tau_AQEC*n/tau_2)**(beta))
def exp_01(n, tau_2, a, c):
    return a-c+c*np.exp(-(tau_AQEC*n/tau_2)**1)
def exp_02(n, tau_2, a, c):
    return a-c+c*np.exp(-(tau_AQEC*n/tau_2)**2)
def exp_03(n, tau_2, a, c):
    return a-c+c*np.exp(-(tau_AQEC*n/tau_2)**3)
def exp_04(n, tau_2, a, c):
    return a-c+c*np.exp(-(tau_AQEC*n/tau_2)**4)
def exp_ansatz(n, tau_2, tau_1, a, c):
    return a-c+c*np.exp(-(tau_AQEC*n/tau_2)**2-(tau_AQEC*n/tau_1)**1)
n_set_AQEC = np.linspace(0, N_AQEC+1, len(Fi_t_AQEC))
n_set_AQEC = [int(num) for num in n_set_AQEC]
#Fi_t_AQEC_analytic = []
#for temp_t in range(len(n_set_AQEC)):
#    t = n_set_AQEC[temp_t]
#    Fi_t_AQEC_analytic.append(exact_AQEC(t))    
'''
### 拟合平均保真度
# poptAQEC0ana, pcovAQEC0ana = curve_fit(exp_0beta, n_set_AQEC, Fi_t_AQEC_analytic, p0=[1.0, 2/3, 1/3, 0.75], bounds=([0.0, 0.5, 0.2, 0.2], [np.inf, 0.8, 0.5, 3]))
poptAQEC0beta, pcovAQEC0beta = curve_fit(exp_0beta, n_set_AQEC, Fi_t_AQEC, p0=[1.0, 2/3, 1/3, 0.75], bounds=([0.0, 0.5, 0.2, 0.2], [np.inf, 0.8, 0.5, 3]))
poptAQEC1, pcovAQEC1 = curve_fit(exp_01, n_set_AQEC, Fi_t_AQEC, p0=[1.0, 2/3, 1/3], bounds=([0.0, 0.5, 0.2], [np.inf, 0.8, 0.5]))
poptAQEC2, pcovAQEC2 = curve_fit(exp_02, n_set_AQEC, Fi_t_AQEC, p0=[1.0, 2/3, 1/3], bounds=([0.0, 0.5, 0.2], [np.inf, 0.8, 0.5]))
poptAQECa, pcovAQECa = curve_fit(exp_ansatz, n_set_AQEC, Fi_t_AQEC, p0=[1.0, 1.0, 2/3, 1/3], bounds=([0.0, 0.0, 0.5, 0.2], [np.inf, np.inf, 0.8, 0.5]))
Fi_t_AQEC_0ana = []
#for temp_t in range(len(n_set_AQEC)):
#    t = n_set_AQEC[temp_t]
#    Fi_t_AQEC_0ana.append(exp_0beta(t, poptAQEC0ana[0], poptAQEC0ana[1], poptAQEC0ana[2], poptAQEC0ana[3]))
Fi_t_AQEC_0beta = []
for temp_t in range(len(n_set_AQEC)):
    t = n_set_AQEC[temp_t]
    Fi_t_AQEC_0beta.append(exp_0beta(t, poptAQEC0beta[0], poptAQEC0beta[1], poptAQEC0beta[2], poptAQEC0beta[3]))
Fi_t_AQEC_1 = []
for temp_t in range(len(n_set_AQEC)):
    t = n_set_AQEC[temp_t]
    Fi_t_AQEC_1.append(exp_01(t, poptAQEC1[0], poptAQEC1[1], poptAQEC1[2]))
Fi_t_AQEC_2 = []
for temp_t in range(len(n_set_AQEC)):
    t = n_set_AQEC[temp_t]
    Fi_t_AQEC_2.append(exp_02(t, poptAQEC2[0], poptAQEC2[1], poptAQEC2[2]))
Fi_t_AQEC_a = []
for temp_t in range(len(n_set_AQEC)):
    t = n_set_AQEC[temp_t]
    Fi_t_AQEC_a.append(exp_ansatz(t, poptAQECa[0], poptAQECa[1], poptAQECa[2], poptAQECa[3]))
# print(poptAQEC0ana[0], poptAQEC0ana[1], poptAQEC0ana[2], poptAQEC0ana[3])
print(poptAQEC0beta[0], poptAQEC0beta[1], poptAQEC0beta[2], poptAQEC0beta[3])

t_set_AQEC = np.linspace(0, T_AQEC, len(Fi_t_AQEC))
plt.figure(9)
plt.plot(t_set_AQEC, Fi_t_AQEC, linewidth=3.0, color='grey', linestyle='-', label='AQEC')
# plt.plot(t_set_AQEC, Fi_t_AQEC_analytic, linewidth=3.0, color='seagreen', linestyle='-', label='AQEC_analytic')
plt.plot(t_set_AQEC, Fi_t_AQEC_0beta, linewidth=3.0, color='cyan', linestyle=':', label='AQEC')
plt.plot(t_set_AQEC, Fi_t_AQEC_0ana, linewidth=3.0, color='violet', linestyle=':', label='AQEC')
plt.plot(t_set_AQEC, Fi_t_AQEC_1, linewidth=3.0, color='k', linestyle='--', label='AQEC')
plt.plot(t_set_AQEC, Fi_t_AQEC_2, linewidth=3.0, color='pink', linestyle='--', label='AQEC')
'''

### 拟合过程保真度
n_set_AQEC = np.linspace(0, N_AQEC+1, len(Fi_t_AQEC_pro))
n_set_AQEC = [int(num) for num in n_set_AQEC]
poptAQEC0beta, pcovAQEC0beta = curve_fit(exp_0beta, n_set_AQEC, Fi_t_AQEC_pro, p0=[1.0, 0.9, 1/2, 0.75], bounds=([0.0, 0.8, 1/3, 0.2], [np.inf, 1.0, 2/3, 3]))
poptAQEC1, pcovAQEC1 = curve_fit(exp_01, n_set_AQEC, Fi_t_AQEC_pro, p0=[1.0, 0.9, 1/2], bounds=([0.0, 0.8, 1/3], [np.inf, 1.0, 2/3]))
poptAQEC2, pcovAQEC2 = curve_fit(exp_02, n_set_AQEC, Fi_t_AQEC_pro, p0=[1.0, 0.9, 1/2], bounds=([0.0, 0.8, 1/3], [np.inf, 1.0, 2/3]))
#poptAQECa, pcovAQECa = curve_fit(exp_ansatz, n_set_AQEC, Fi_t_AQEC_pro, p0=[1.0, 1.0, 1/2, 1/2], bounds=([0.0, 0.0, 1/3, 1/3], [np.inf, np.inf, 2/3, 2/3]))
#Fi_t_AQEC_0ana = []
#for temp_t in range(len(n_set_AQEC)):
#    t = n_set_AQEC[temp_t]
#    Fi_t_AQEC_0ana.append(exp_0beta(t, poptAQEC0ana[0], poptAQEC0ana[1], poptAQEC0ana[2], poptAQEC0ana[3]))
Fi_t_AQEC_0beta = []
for temp_t in range(len(n_set_AQEC)):
    t = n_set_AQEC[temp_t]
    Fi_t_AQEC_0beta.append(exp_0beta(t, poptAQEC0beta[0], poptAQEC0beta[1], poptAQEC0beta[2], poptAQEC0beta[3]))
Fi_t_AQEC_1 = []
for temp_t in range(len(n_set_AQEC)):
    t = n_set_AQEC[temp_t]
    Fi_t_AQEC_1.append(exp_01(t, poptAQEC1[0], poptAQEC1[1], poptAQEC1[2]))
Fi_t_AQEC_2 = []
for temp_t in range(len(n_set_AQEC)):
    t = n_set_AQEC[temp_t]
    Fi_t_AQEC_2.append(exp_02(t, poptAQEC2[0], poptAQEC2[1], poptAQEC2[2]))
#Fi_t_AQEC_a = []
#for temp_t in range(len(n_set_AQEC)):
#    t = n_set_AQEC[temp_t]
#    Fi_t_AQEC_a.append(exp_ansatz(t, poptAQECa[0], poptAQECa[1], poptAQECa[2], poptAQECa[3]))
# print(poptAQEC0ana[0], poptAQEC0ana[1], poptAQEC0ana[2], poptAQEC0ana[3])
print(poptAQEC0beta[0], poptAQEC0beta[1], poptAQEC0beta[2], poptAQEC0beta[3])
print(poptAQEC2[0], poptAQEC2[1], poptAQEC2[2])

###### 画图
colorlist = ['k', (226/255, 133/255, 157/255), (143/255, 170/255, 220/255)]
t_set_AQEC = np.linspace(0, T_AQEC, len(Fi_t_AQEC))
plt.figure(10)
# fig = plt.figure(figsize = (6.0, 4.0))
plt.plot(t_set_AQEC, Fi_t_AQEC_pro, linewidth=3.0, color=colorlist[0], linestyle='-', label='    ')
# plt.plot(t_set_AQEC, Fi_t_AQEC_analytic, linewidth=3.0, color='seagreen', linestyle='-', label='AQEC_analytic')
#plt.plot(t_set_AQEC, Fi_t_AQEC_0beta, linewidth=3.0, color='cyan', linestyle=':', label='AQEC')
#plt.plot(t_set_AQEC, Fi_t_AQEC_0ana, linewidth=3.0, color='violet', linestyle=':', label='AQEC')
plt.plot(t_set_AQEC, Fi_t_AQEC_1, linewidth=3.0, color=colorlist[1], linestyle='--', label='    ')
plt.plot(t_set_AQEC, Fi_t_AQEC_2, linewidth=3.0, color=colorlist[2], linestyle='--', label='    ')
xaxis = [0.0, 25.0, 50.0, 75.0]
yaxis = [0.4, 0.6, 0.8, 1.0]
plt.xticks(xaxis,(r'0', r'80', r'160', r'240'), fontsize=16, color='w')
plt.yticks(yaxis,(r'$0.4$', r'$0.6$', r'$0.8$', r'$1.0$'), fontsize=16, color='w')
plt.xlim(-7.5, 82.5)
plt.ylim(0.34, 1.06)
plt.xlabel("    ", fontsize=16)
plt.ylabel("    ", fontsize=16)
plt.rcParams['xtick.direction'] = 'out'                                         # 将x轴的刻度方向设置向内
plt.rcParams['ytick.direction'] = 'out'                                         # 将y轴的刻度方向设置向内
plt.legend(fontsize=20, ncol=1, handlelength=1.5, handletextpad=0.2, borderpad=0.5, labelspacing=0.5, columnspacing=1.0, bbox_to_anchor=(0.80, 1.02), loc='upper right', frameon=False)
plt.tick_params(axis="both", which="major", direction="out", width=2, length=5, pad=5)
bwith = 2 #边框宽度设置为2
ax = plt.gca()#获取边框
#设置边框
ax.spines['bottom'].set_linewidth(bwith)#图框下边
ax.spines['left'].set_linewidth(bwith)#图框左边
ax.spines['top'].set_linewidth(bwith)#图框上边
ax.spines['right'].set_linewidth(bwith)#图框右边
plt.savefig("fidelity_t_AQEC_process.svg", bbox_inches='tight')
plt.show()