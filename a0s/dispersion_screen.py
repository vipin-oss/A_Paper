"""A0-S uniform-mode screening, not edge scattering or a new physical model.

Imports the unchanged A0-R analytic Galerkin model. Adds a separately derived
12-state strong-equation propagator for its f=0, A=ell^2 C, reciprocal-H subset.
Radiation checks are kinematic diagnostics only: no Maxwell field is added.
"""
from __future__ import annotations
from pathlib import Path
import sys
import numpy as np
from scipy.linalg import expm, svdvals, eigvals, solve, svd
from scipy.optimize import root

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'a0r'))
from complex_dispersion import (ComplexPlate, SI, CONST, derived,
                                eight_state_boundary, independent_spatial_root)

C_LIGHT=299792458.  # Exact SI definition, not a fitted ZnO constant.
DISTANCE=100e-6


def reconstruct_mode(plate,modes,j):
    state=modes['vectors'][:,j]
    ur=state[:plate.m];nr=state[2*plate.m:]
    scale=np.sqrt(np.vdot(ur,plate.Mr@ur).real)
    ur=ur/scale;nr=nr/scale
    pr=modes['pu']@ur-modes['pn']@nr
    u=np.zeros(2*plate.n,complex);p=np.zeros(plate.n,complex);n=np.zeros(plate.n,complex)
    u[plate.udofs]=ur;p[plate.pdofs]=pr;n[plate.ndofs]=nr
    return dict(omega=modes['omega'][j],U=u,Phi=p,N=n,
                maximum_temporal_growth=float(np.max(modes['all_s'].real)))


def mass_mac(plate,u,v):
    return float(abs(np.vdot(u,plate.M@v))**2/
                 (np.vdot(u,plate.M@u).real*np.vdot(v,plate.M@v).real))


def longitudinal_cutoff(plate):
    """Lowest oscillatory thickness mode with >90% U3 kinetic mass at K=0."""
    modes=plate.temporal_modes(0.)
    candidates=[]
    for j in range(len(modes['omega'])):
        mode=reconstruct_mode(plate,modes,j)
        u=mode['U'];m3=np.vdot(u[plate.n:],plate.W@u[plate.n:]).real
        if m3>.9 and mode['omega'].real>1:
            candidates.append(mode)
    if not candidates:raise RuntimeError('No resolved longitudinal cutoff in selected parity.')
    return min(candidates,key=lambda m:m['omega'].real)


def tracked_mode(plate,K,reference):
    modes=plate.temporal_modes(float(K))
    candidates=[reconstruct_mode(plate,modes,j) for j in range(len(modes['omega']))]
    macs=[mass_mac(plate,reference['U'],m['U']) for m in candidates]
    j=int(np.argmax(macs))
    answer=candidates[j];answer['MAC']=macs[j]
    return answer


def twelve_state_operator(plate,K,Omega):
    """Independent strong assembly; no basis, Galerkin matrix, or field routine.

    y=(U1,U3,V1=U1',V3=U3',Phi,N,T1,T3,R1,R3,D3,Gamma3).
    T_i=S_i3-iK tau_i13, R_i=tau_i33, engineering shear convention.
    Valid for the stated f=0, isotropic-gradient-in-l index A=ell^2 C subset.
    H has all three symmetry-allowed ha,hb,hc contributions.
    """
    ell2=plate.ell_SI**2/plate.sc['d']**2
    if ell2<=0:raise ValueError('Use independent eight-state system for A=H=0.')
    p=plate.props;c0=SI['c44'];kapref=SI['kappa33']
    c11,c13,c33,c44=[p[key]/c0 for key in ['c11','c13','c33','c44']]
    e15,e31,e33=[p[key]/np.sqrt(c0*kapref) for key in ['e15','e31','e33']]
    kap1,kap3=p['kappa11']/kapref,p['kappa33']/kapref
    # Recompute scaling directly from physical constants, not analytic matrices.
    theta=CONST['q']*p['electron_diffusivity']/p['electron_mobility']
    a=theta/plate.sc['n0'];d=plate.sc['d']
    cs=np.sqrt(c0/p['rho'])
    Q=CONST['q']*d/np.sqrt(kapref*a)
    alpha=p['electron_diffusivity']/(d*cs)
    ha,hb,hc=plate.H_SI/(d*np.sqrt(a*c0))
    den=1-ha*ha/(ell2*c33)
    if den<=0:raise ValueError('Principal electrochemical/gradient block is inadmissible.')

    def rhs(y):
        ux,uz,vx,vz,phi,N,t1,t3,r1,r3,D3,g3=y
        shear=vx+1j*K*uz
        sn11=c11*1j*K*ux+c13*vz
        sn33=c13*1j*K*ux+c33*vz
        phip=(e31*1j*K*ux+e33*vz-D3)/kap3
        uxx=r1/(ell2*c44)-1j*K*vz
        uzz=(r3-ha*N)/(ell2*c33)-1j*K*(c13/c33)*vx
        z11=ell2*(c11*1j*K*vx+c13*uzz)+hb*N
        r1p=(1+ell2*K*K)*c44*shear+e15*1j*K*phi-1j*K*hc*N-1j*K*z11-t1
        r3p=(1+ell2*K*K)*sn33+e33*phip-1j*K*r1-t3
        Np=(-g3/alpha-ha*r3p/(ell2*c33)
            -1j*K*(hb+hc-ha*c13/c33)*uxx+hc*K*K*vz+Q*phip)/den
        mu=N+ha*uzz+(hb+hc)*1j*K*vx-hc*K*K*uz-Q*phi
        D1=e15*shear-kap1*1j*K*phi
        t1p=-Omega*Omega*ux-1j*K*((1+ell2*K*K)*sn11+e31*phip)
        t3p=-Omega*Omega*uz-1j*K*((1+ell2*K*K)*c44*shear+e15*1j*K*phi-1j*K*hc*N)
        return np.array([vx,vz,uxx,uzz,phip,Np,t1p,t3p,r1p,r3p,
                         -1j*K*D1-Q*N,1j*Omega*N-alpha*K*K*mu])
    return np.stack([rhs(column) for column in np.eye(12)],axis=1)


def strong_boundary(plate,K,Omega):
    if plate.ell_SI==0:
        return eight_state_boundary(K,Omega,d=plate.sc['d'],n0=plate.sc['n0'],props=plate.props)
    F=twelve_state_operator(plate,K,Omega)
    # U1, V3, T3, R1, D3, Gamma3 even; remaining six states odd.
    mid=np.eye(12)[:,[0,3,7,8,10,11]]
    bc=np.zeros((6,12),complex)
    for j,idx in enumerate([6,7,8,9,10,11]):bc[j,idx]=1.
    bc[4,4]=-CONST['epsilon0']/SI['kappa33']*K
    boundary=bc@expm(.5*F)@mid
    scaled=boundary/np.maximum(np.linalg.norm(boundary,axis=1),1e-30)[:,None]
    scaled/=np.maximum(np.linalg.norm(scaled,axis=0),1e-30)[None,:]
    singular=svdvals(scaled)
    return dict(determinant=np.linalg.det(scaled),
                singular_relative=float(singular[-1]/singular[0]),matrix=boundary)


def strong_root(plate,kind,fixed,guess):
    if kind not in ('temporal','spatial'):raise ValueError(kind)
    def fun(x):
        value=complex(*x)
        K,om=(fixed,value) if kind=='temporal' else (value,fixed)
        det=strong_boundary(plate,K,om)['determinant']
        return [det.real,det.imag]
    ans=root(fun,[complex(guess).real,complex(guess).imag],tol=1e-11)
    value=complex(*ans.x)
    K,om=(fixed,value) if kind=='temporal' else (value,fixed)
    diag=strong_boundary(plate,K,om)
    return dict(value=value,converged=bool(diag['singular_relative']<2e-8),
                scipy_success=bool(ans.success),singular_relative=diag['singular_relative'],
                nfev=int(ans.nfev))


def radiation_screen(plate,K,Omega):
    """Conservative light-line diagnostic, not a radiative eigenmode solution.

    EM branch q=sqrt(k^2-(omega/c)^2) is computed only as a consistency scale.
    The bulk equations and quasistatic boundary operator are NOT replaced.
    """
    klight=float(np.real(Omega))*plate.sc['cs']/C_LIGHT
    qm=np.sqrt(complex(K*K-klight*klight))
    if qm.real<0:qm=-qm
    return dict(vacuum_laplace_decay=bool(K.real>0),
                K_light=klight,above_vacuum_phase_light_line=bool(K.real>klight),
                q_EM_real=float(qm.real),q_EM_imag=float(qm.imag),
                relative_EM_exponent_change=float(abs((qm-K)/K)),
                full_Maxwell_radiation_solved=False,acoustic_exterior='vacuum; no elastic radiation continuum')


def spatial_diagnostics(plate,K,Omega):
    row=dict(K=K,Omega_drive=float(Omega),
             root_scalar_residual=float(abs(conditioned_scalar(plate,K,Omega))),
             radiation=radiation_screen(plate,K,Omega))
    mode=conditioned_fields(plate,K,Omega)
    row['residuals']=plate.residuals(K,Omega,mode)
    if K.real>0:
        e=plate.spatial_energy(K,Omega,mode)
        row['transport']=e
        row['power_survival_100um']=float(np.exp(-2*abs(K.imag)*DISTANCE/plate.sc['d']))
        row['admissible_backward']=bool(e['backward'] and e['passive_direction'] and K.imag<0
                                         and e['mean_energy']>0
                                         and row['radiation']['above_vacuum_phase_light_line']
                                         and row['radiation']['q_EM_real']>0)
        row['transport_screen_pass']=bool(row['admissible_backward']
                                         and row['power_survival_100um']>=.1
                                         and e['power_fraction_one_phase_wavelength']>=.1
                                         and row['radiation']['relative_EM_exponent_change']<=.01)
    else:
        row['admissible_backward']=row['transport_screen_pass']=False
    return row


def condensed_stiffness(plate,K,Omega):
    """Exact block Gaussian elimination reduces high-order stiffness roundoff.

    The retained analytic operator is unchanged. High polynomial DOFs are
    solved out, not discarded: its Schur complement has exactly the same
    zeros whenever Dhh is nonsingular. Eight low mechanical DOFs suffice for
    conditioning of this bounded L1 family; convergence tests vary p.
    """
    D,Pu,Nu=plate.spatial_stiffness(K,Omega)
    low=np.where((plate.udofs % plate.n)<=7)[0]
    high=np.setdiff1d(np.arange(plate.m),low)
    if len(high):
        lift=-solve(D[np.ix_(high,high)],D[np.ix_(high,low)])
        small=D[np.ix_(low,low)]+D[np.ix_(low,high)]@lift
    else:lift=np.zeros((0,len(low)));small=D
    return small,low,high,lift,Pu,Nu


def conditioned_scalar(plate,K,Omega):
    small,low,_,_,_,_=condensed_stiffness(plate,K,Omega)
    values=eigvals(small,plate.Mr[np.ix_(low,low)])
    return values[np.argmin(abs(values))]/(Omega*Omega)


def conditioned_root(plate,Omega,guess):
    def fun(x):
        v=conditioned_scalar(plate,complex(*x),Omega)
        return np.array([v.real,v.imag])
    # Explicit centered differences avoid default sqrt(eps) probes through
    # high-order numerical noise; this is a root algorithm, not a model edit.
    def jac(x):
        h=1e-4
        return np.column_stack([(fun(x+h*np.eye(2)[j])-fun(x-h*np.eye(2)[j]))/(2*h) for j in range(2)])
    ans=root(fun,[complex(guess).real,complex(guess).imag],jac=jac,tol=1e-10)
    K=complex(*ans.x);res=float(abs(conditioned_scalar(plate,K,Omega)))
    return dict(K=K,converged=bool(res<2e-10),scalar_residual=res,
                scipy_success=bool(ans.success),evaluations=int(ans.nfev))


def conditioned_fields(plate,K,Omega):
    small,low,high,lift,Pu,Nu=condensed_stiffness(plate,K,Omega)
    _,ss,vh=svd(small)
    ur=np.zeros(plate.m,complex);ur[low]=vh[-1].conj();ur[high]=lift@ur[low]
    ur/=np.sqrt(np.vdot(ur,plate.Mr@ur).real)
    U=np.zeros(2*plate.n,complex);Phi=np.zeros(plate.n,complex);N=np.zeros(plate.n,complex)
    U[plate.udofs]=ur;Phi[plate.pdofs]=Pu@ur;N[plate.ndofs]=Nu@ur
    return dict(U=U,Phi=Phi,N=N,stiffness_singular_relative=float(ss[-1]/ss[0]))


def strong_energy(plate,K,Omega,nquad=80):
    """Independent quadrature and state reconstruction of gradient-mode power.

    Uses the strong-equation propagator, not Galerkin coefficients, basis
    derivatives, residuals, or its field/energy routine. Same derived balance
    law, including exterior and tangential hyperstress face power.
    """
    if plate.ell_SI<=0:raise ValueError('12-state gradient subset only.')
    if K.real<=0 or abs(complex(Omega).imag)>1e-14:raise ValueError('Real drive; decaying sheet.')
    Omega=float(np.real(Omega));F=twelve_state_operator(plate,K,Omega)
    B=strong_boundary(plate,K,Omega)['matrix']
    row=np.maximum(np.linalg.norm(B,axis=1),1e-30)
    br=B/row[:,None];col=np.maximum(np.linalg.norm(br,axis=0),1e-30)
    _,_,vh=svd(br/col[None,:]);v0=vh[-1].conj()/col
    center=np.eye(12)[:,[0,3,7,8,10,11]]@v0
    x,w=np.polynomial.legendre.leggauss(nquad);z=x/2;w=w/2
    Y=np.stack([expm(t*F)@center for t in z])
    norm=np.sqrt(np.sum(w*(abs(Y[:,0])**2+abs(Y[:,1])**2)))
    Y/=norm;center/=norm
    Yp=Y@F.T;Ypp=Yp@F.T
    p=plate.props;c0=SI['c44'];kr=SI['kappa33'];ell2=(plate.ell_SI/plate.sc['d'])**2
    C=np.array([[p['c11'],p['c13'],0],[p['c13'],p['c33'],0],[0,0,p['c44']]])/c0
    E=np.array([[0,0,p['e15']],[p['e31'],p['e33'],0]])/np.sqrt(c0*kr)
    kap=np.diag([p['kappa11']/kr,p['kappa33']/kr]);eps=CONST['epsilon0']/kr
    a=CONST['q']*p['electron_diffusivity']/p['electron_mobility']/plate.sc['n0']
    ha,hb,hc=plate.H_SI/(plate.sc['d']*np.sqrt(a*c0));alpha=p['electron_diffusivity']/(plate.sc['d']*np.sqrt(c0/p['rho']))
    Q=CONST['q']*plate.sc['d']/np.sqrt(kr*a)
    ux,uz,vx,vz,phi,N=[Y[:,j] for j in range(6)]
    strain=np.stack([1j*K*ux,vz,vx+1j*K*uz],axis=1)
    strainz=np.stack([1j*K*vx,Yp[:,3],Yp[:,2]+1j*K*vz],axis=1)
    gp=np.stack([1j*K*phi,Yp[:,4]],axis=1)
    elastic=strain@C.T;mx=ell2*1j*K*elastic+N[:,None]*np.array([0,0,hc])
    mz=ell2*strainz@C.T+N[:,None]*np.array([hb,ha,0])
    z11p=ell2*(C[0,0]*1j*K*Yp[:,2]+C[0,1]*Ypp[:,3])+hb*Yp[:,5]
    S11=(1+ell2*K*K)*elastic[:,0]+E[1,0]*Yp[:,4]-z11p
    S13=Y[:,6]+1j*K*mz[:,0]
    disp=np.stack([ux,uz],axis=1);vel=-1j*Omega*disp
    velz=-1j*Omega*np.stack([vx,vz],axis=1);velx=K*Omega*disp
    mech=-S11*vel[:,0].conj()-S13*vel[:,1].conj()
    mech-=(mx[:,0]*velx[:,0].conj()+mx[:,2]*velz[:,0].conj()
           +mx[:,2]*velx[:,1].conj()+mx[:,1]*velz[:,1].conj())
    D=strain@E.T-gp@kap.T
    mu=N+ha*Yp[:,3]+(hb+hc)*1j*K*vx-hc*K*K*uz-Q*phi
    chem=mu*(-alpha*1j*K*mu).conj()
    electric=phi*(-1j*Omega*D[:,0]).conj()
    ends=np.stack([expm(t*F)@center for t in [-.5,.5]])
    ep=ends@F.T
    ez=np.stack([1j*K*ends[:,2],ep[:,3],ep[:,2]+1j*K*ends[:,3]],axis=1)
    emz=ell2*ez@C.T+ends[:,5,None]*np.array([hb,ha,0])
    ev=-1j*Omega*ends[:,:2]
    face=-.5*np.real((emz[1,0]*ev[1,0].conj()+emz[1,2]*ev[1,1].conj())
                      -(emz[0,0]*ev[0,0].conj()+emz[0,2]*ev[0,1].conj()))
    vacuum_power=-.25*Omega*eps*np.sum(abs(ends[:,4])**2)
    power=.5*np.real(np.sum(w*(mech+electric+chem)))+face+vacuum_power
    quad=lambda v,c:np.einsum('qi,ij,qj->q',v.conj(),c,v).real
    Hg=ha*Yp[:,3]+(hb+hc)*1j*K*vx-hc*K*K*uz
    density=(Omega*Omega*np.sum(abs(disp)**2,axis=1)+quad(strain,C)
             +ell2*(abs(K)**2*quad(strain,C)+quad(strainz,C))
             +quad(gp,kap)+abs(N)**2+2*np.real(N.conj()*Hg))
    energy=.25*np.sum(w*density)+eps*abs(K)**2/(4*K.real)*np.sum(abs(ends[:,4])**2)
    diss=.5*alpha*np.sum(w*(abs(K*mu)**2+abs(Y[:,11]/alpha)**2))
    return dict(power=float(power),mean_energy=float(energy),dissipation=float(diss),
                face_hyperstress_power=float(face),vacuum_power=float(vacuum_power),
                spatial_balance_relative=float(abs(2*K.imag*power-diss)/max(diss,1e-30)),
                energy_velocity_m_s=float(power/energy*np.sqrt(c0/p['rho'])))
