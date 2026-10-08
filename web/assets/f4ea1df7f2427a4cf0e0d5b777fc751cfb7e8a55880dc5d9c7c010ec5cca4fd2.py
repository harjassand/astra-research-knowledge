from reproduce_chemostat import face_orbit
cases=[(0.300,(0,1)),(0.325,(0,1)),(0.300,(0,2)),(0.275,(0,2)),(0.200,(2,))]
for a,S in cases:
    print('case',a,[i+1 for i in S])
    for n in (240,480,960,1920):
        row=face_orbit(a,S,nstep=n)
        print(n,'support',[i+1 for i in row['support']],'cycles',row['cycles'],'resid',f"{row['periodic_residual']:.2e}",'lambda',*[f'{v:+.12e}' for v in row['lambda']])
