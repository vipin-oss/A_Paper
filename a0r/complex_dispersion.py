"""Focused A0-R uniform-plate checks. NO edge/scattering implementation.

Analytic (not Hermitian) continuation in complex K, finite drift-diffusion,
exact quasistatic exterior on the positive-phase sheet q_vac = K.
Only the already reported longitudinal-thickness family is investigated.
The calibrated numerical model is still the classical f=A=H=0 LIMIT.
Any nonzero gradient/H coefficients below are explicitly synthetic.

A0 sources/code and Blueprint V2.1 are imported/read, never edited.
"""
from __future__ import annotations

from pathlib import Path
import sys
import numpy as np
from scipy.linalg import eig, eigh, expm, solve, svd, svdvals
from scipy.optimize import root

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'a0'))
from dispersion import Plate, SI, CONST, derived, elastic_matrix


def elastic_from(p):
    return np.array([[p['c11'],p['c12'],p['c13'],0,0,0],
                     [p['c12'],p['c11'],p['c13'],0,0,0],
                     [p['c13'],p['c13'],p['c33'],0,0,0],
                     [0,0,0,p['c44'],0,0],[0,0,0,0,p['c44'],0],
                     [0,0,0,0,0,p['c66']]],float)


class ComplexPlate(Plate):
    """One parity family, same sagittal geometry and source constants as A0."""
    def __init__(self, degree=22, d=1e-6, n0=1e19, ell=0., H=None,
                 eta=0., direction=(1.,0.,0.), overrides=None, vacuum=True):
        super().__init__(degree=degree,d=d,n0=n0,ell_rel=ell/d,eta=0.,vacuum=vacuum)
        self.props = dict(SI)
        self.props.update(overrides or {})
        self.props['c66']=(self.props['c11']-self.props['c12'])/2
        self.C6=elastic_from(self.props)
        self.C=self.C6[np.ix_([0,2,4],[0,2,4])]/self.sc['c0']
        # Keep reference normalization fixed when perturbing material constants.
        kapref=SI['kappa33']
        self.e=np.array([[0,0,self.props['e15']],
                         [self.props['e31'],self.props['e33'],0.]])/np.sqrt(self.sc['c0']*kapref)
        self.kap=np.diag([self.props['kappa11']/kapref,self.props['kappa33']/kapref])
        self.sc['alpha']=self.props['electron_diffusivity']/(d*self.sc['cs'])
        self.sc['tau_diffusion']=d*d/self.props['electron_diffusivity']
        self.sc['tau_dielectric']=self.props['kappa33']/(CONST['q']*n0*self.props['electron_mobility'])
        # This checkpoint varies elastic/piezo constants, not M/D thermodynamics.
        theta=CONST['q']*self.props['electron_diffusivity']/self.props['electron_mobility']
        if abs(theta/self.sc['theta']-1)>1e-12:
            raise ValueError('Keep the sourced Einstein ratio fixed.')
        self.ell_SI=ell
        invC=np.linalg.inv(self.C6)
        self.sc['cschur']=1/invC[2,2]
        # ha,hb,hc correspond to H333, H113=H223, H131=H311=H232=H322.
        def contraction(h):
            ha,hb,hc=np.asarray(h,float)
            hz=np.array([hb,hb,ha,0,0,0])
            return float(hz@invC@hz+hc*hc*(invC[3,3]+invC[4,4]))
        vec=np.asarray(direction,float)
        if H is None:
            if eta and (ell <= 0 or not np.any(vec)):
                raise ValueError('Synthetic H needs a positive gradient modulus and direction.')
            hcrit=(ell*np.sqrt(self.sc['a']/contraction(vec))) if ell>0 and np.any(vec) else 0.
            H=np.asarray(vec)*eta*hcrit
        self.H_SI=np.asarray(H,float)
        self.schur_fraction=contraction(self.H_SI)/(ell*ell*self.sc['a']) if ell>0 else 0.
        if ell<=0 and np.any(self.H_SI):
            raise ValueError('H != 0 at A=0 is inadmissible.')
        if self.schur_fraction>=1:
            raise ValueError('Strict full-3D Schur bound violated.')
        self.hvec=self.H_SI/(d*np.sqrt(self.sc['a']*self.sc['c0']))
        self.h=self.hvec[0]  # only for compatibility; A0 methods are not used for general H.
        self.h_SI=self.H_SI[0]
        # L1-family parity: U1 even, U3/Phi/N odd. No gauge singularity at K=0.
        even=np.arange(0,self.n,2); odd=np.arange(1,self.n,2)
        self.udofs=np.r_[even,self.n+odd]
        self.pdofs=self.ndofs=odd
        self.Mr=self.M[np.ix_(self.udofs,self.udofs)]
        self.Wr=self.W[np.ix_(odd,odd)]
        self.m=len(self.udofs);self.nc=len(odd)

    def analytic_matrices(self,K,qvac=None):
        """Formal Fourier adjoints B(-K)^T, NOT B(K)^H for complex K."""
        qvac=complex(K) if qvac is None else complex(qvac)
        B,Bz,_,_,G,_=self.operators(K)
        Bm,Bzm,_,_,Gm,_=self.operators(-K)
        def form(a,c,b):
            return np.einsum('qai,ab,qbj,q->ij',a,c,b,self.w,optimize=True)
        Kuu=(1+self.ell**2*K*K)*form(Bm,self.C,B)+self.ell**2*form(Bzm,self.C,Bz)
        Kup=form(Bm,self.e.T,G)
        Kpu=form(Gm,self.e,B)
        P=form(Gm,self.kap,G)+self.eps*qvac*(self.ends[0].T@self.ends[0])
        L=form(Gm,np.eye(2),G)
        ha,hb,hc=self.hvec
        hz=np.array([hb,ha,0.]);hx=np.array([0.,0.,hc])
        F=np.einsum('qai,a,qj,q->ij',Bzm,hz,self.b[0],self.w,optimize=True)
        F+=np.einsum('qai,a,qj,q->ij',-1j*K*Bm,hx,self.b[0],self.w,optimize=True)
        Fnu=np.einsum('qai,a,qj,q->ji',Bz,hz,self.b[0],self.w,optimize=True)
        Fnu+=np.einsum('qai,a,qj,q->ji',1j*K*B,hx,self.b[0],self.w,optimize=True)
        u,p=self.udofs,self.pdofs
        return dict(Kuu=Kuu[np.ix_(u,u)],Kup=Kup[np.ix_(u,p)],
                    Kpu=Kpu[np.ix_(p,u)],P=P[np.ix_(p,p)],
                    F=F[np.ix_(u,p)],Fnu=Fnu[np.ix_(p,u)],L=L[np.ix_(p,p)])

    def spatial_stiffness(self,K,Omega):
        a=self.analytic_matrices(K)
        B=-1j*Omega*self.Wr+self.sc['alpha']*a['L']
        Zp=solve(B,self.sc['alpha']*self.sc['Q']*a['L'])
        Zu=solve(B,-self.sc['alpha']*a['L']@solve(self.Wr,a['Fnu']))
        Pu=solve(a['P']+self.sc['Q']*self.Wr@Zp,a['Kpu']-self.sc['Q']*self.Wr@Zu)
        Nu=Zp@Pu+Zu
        D=a['Kuu']-Omega*Omega*self.Mr+a['Kup']@Pu+a['F']@Nu
        return D,Pu,Nu

    def spatial_scalar(self,K,Omega):
        D,_,_=self.spatial_stiffness(K,Omega)
        values=eig(D,self.Mr,right=False)
        return values[np.argmin(np.abs(values))]/(Omega*Omega)

    def spatial_root(self,Omega,guess,tol=1e-10):
        def fun(x):
            y=self.spatial_scalar(complex(*x),Omega)
            return [y.real,y.imag]
        result=root(fun,[complex(guess).real,complex(guess).imag],tol=tol)
        K=complex(*result.x)
        residual=abs(self.spatial_scalar(K,Omega))
        return dict(K=K,converged=bool(residual<2e-9),
                    scipy_success=bool(result.success),scalar_residual=float(residual),
                    evaluations=int(result.nfev),exterior_decays=bool(K.real>0))

    def spatial_fields(self,K,Omega):
        D,Pu,Nu=self.spatial_stiffness(K,Omega)
        _,s,vh=svd(D)
        ur=vh[-1].conj()
        ur/=np.sqrt(np.real(np.vdot(ur,self.Mr@ur)))
        u=np.zeros(2*self.n,complex);p=np.zeros(self.n,complex);n=np.zeros(self.n,complex)
        u[self.udofs]=ur;p[self.pdofs]=Pu@ur;n[self.ndofs]=Nu@ur
        return dict(U=u,Phi=p,N=n,stiffness_singular_relative=float(s[-1]/s[0]))

    def frozen_mode(self,K,near=7.4325):
        a=self.analytic_matrices(K)
        Pu=solve(a['P'],a['Kpu'])
        Kf=a['Kuu']+a['Kup']@Pu
        values,vectors=eigh(Kf,self.Mr)
        oms=np.sqrt(np.maximum(values,0))
        j=int(np.argmin(abs(oms-near)))
        u=np.zeros(2*self.n,complex);p=np.zeros(self.n,complex);n=np.zeros(self.n,complex)
        u[self.udofs]=vectors[:,j];p[self.pdofs]=Pu@vectors[:,j]
        return dict(omega=float(oms[j]),U=u,Phi=p,N=n)

    def temporal_modes(self,K):
        a=self.analytic_matrices(float(K))
        pu=solve(a['P'],a['Kpu']);pn=solve(a['P'],self.sc['Q']*self.Wr)
        Kf=a['Kuu']+a['Kup']@pu
        R=a['F']-a['Kup']@pn
        An=self.Wr+self.sc['Q']*self.Wr@pn
        Ru=a['Fnu']-self.sc['Q']*self.Wr@pu
        L=self.sc['alpha']*solve(self.Wr,a['L'])@solve(self.Wr,np.eye(self.nc))
        mm,nn=self.m,self.nc
        Z=np.zeros((mm,mm),complex)
        T=np.block([[Z,np.eye(mm),np.zeros((mm,nn))],
                    [-solve(self.Mr,Kf),Z,-solve(self.Mr,R)],
                    [-L@Ru,np.zeros((nn,mm)),-L@An]])
        ss,v=eig(T)
        indices=np.where(ss.imag < -1e-5)[0]
        indices=indices[np.argsort(-ss[indices].imag)]
        return dict(omega=1j*ss[indices],vectors=v[:,indices],
                    all_s=ss,operator=T,pu=pu,pn=pn,Kf=Kf,R=R,An=An)

    def temporal_mode(self,K,near=7.4325):
        modes=self.temporal_modes(K)
        j=int(np.argmin(np.abs(modes['omega']-near)))
        omega=modes['omega'][j]
        state=modes['vectors'][:,j]
        ur=state[:self.m]; nr=state[2*self.m:]
        scale=np.sqrt(np.real(np.vdot(ur,self.Mr@ur)))
        ur=ur/scale;nr=nr/scale
        pr=modes['pu']@ur-modes['pn']@nr
        u=np.zeros(2*self.n,complex);p=np.zeros(self.n,complex);n=np.zeros(self.n,complex)
        u[self.udofs]=ur;p[self.pdofs]=pr;n[self.ndofs]=nr
        return dict(omega=omega,U=u,Phi=p,N=n,
                    maximum_temporal_growth=float(np.max(modes['all_s'].real)))

    def fields_general(self,K,U,Phi,N,basis=None):
        b=self.b if basis is None else basis
        ux=[v@U[:self.n] for v in b];uz=[v@U[self.n:] for v in b]
        pp=[v@Phi for v in b];nn=[v@N for v in b]
        strain=[np.stack([1j*K*ux[r],uz[r+1],ux[r+1]+1j*K*uz[r]],axis=1) for r in range(4)]
        gp=[np.stack([1j*K*pp[r],pp[r+1]],axis=1) for r in range(3)]
        ha,hb,hc=self.hvec;hz=np.array([hb,ha,0]);hx=np.array([0,0,hc])
        sigma=strain[0]@self.C.T+gp[0]@self.e
        dsigma=strain[1]@self.C.T+gp[1]@self.e
        mx=self.ell**2*(1j*K*strain[0])@self.C.T+nn[0][:,None]*hx
        mz=self.ell**2*strain[1]@self.C.T+nn[0][:,None]*hz
        dxz=self.ell**2*(1j*K*strain[1])@self.C.T+nn[1][:,None]*hx
        dzmz=self.ell**2*strain[2]@self.C.T+nn[1][:,None]*hz
        dzzmz=self.ell**2*strain[3]@self.C.T+nn[2][:,None]*hz
        S=sigma-1j*K*mx-dzmz;Sz=dsigma-1j*K*dxz-dzzmz
        D=strain[0]@self.e.T-gp[0]@self.kap.T
        Dz=strain[1]@self.e.T-gp[1]@self.kap.T
        mu=[nn[r]+strain[r+1]@hz+1j*K*(strain[r]@hx)-self.sc['Q']*pp[r] for r in range(3)]
        return dict(ux=ux,uz=uz,phi=pp,N=nn,strain=strain,gp=gp,sigma=sigma,
                    mx=mx,mz=mz,S=S,Sz=Sz,D=D,Dz=Dz,mu=mu)

    def residuals(self,K,Omega,mode):
        f=self.fields_general(K,mode['U'],mode['Phi'],mode['N'])
        b=self.fields_general(K,mode['U'],mode['Phi'],mode['N'],self.ends)
        def norm(x):
            return float(np.sqrt(np.sum(self.w*np.abs(x)**2))) if x.ndim==1 else float(np.sqrt(np.sum(self.w[:,None]*np.abs(x)**2)))
        u=np.stack([f['ux'][0],f['uz'][0]],axis=1)
        force=np.stack([1j*K*f['S'][:,0]+f['Sz'][:,2],1j*K*f['S'][:,2]+f['Sz'][:,1]],axis=1)
        gauss=1j*K*f['D'][:,0]+f['Dz'][:,1]+self.sc['Q']*f['N'][0]
        rate=-1j*Omega*f['N'][0]
        diff=self.sc['alpha']*(f['mu'][2]-K*K*f['mu'][0])
        tr=np.stack([b['S'][:,2]-1j*K*b['mz'][:,0],b['S'][:,1]-1j*K*b['mz'][:,2]],axis=1)
        ec=b['D'][:,1]-np.array([-1.,1.])*self.eps*K*b['phi'][0]
        stress=max(norm(f['sigma']),norm(f['S']),1e-30)
        return dict(momentum=norm(force+Omega**2*u)/max(norm(force),norm(Omega**2*u),1e-30),
                    gauss=norm(gauss)/max(norm(K*f['D'][:,0]),norm(f['Dz'][:,1]),norm(self.sc['Q']*f['N'][0]),1e-30),
                    carrier=norm(rate-diff)/max(norm(rate),norm(diff),1e-30),
                    traction=float(np.max(abs(tr)))/stress,
                    double_traction=float(np.max(abs(b['mz'][:,[2,1]])))/stress,
                    vacuum=float(np.max(abs(ec)))/max(norm(f['D']),1e-30),
                    blocking=float(np.max(abs(b['mu'][1])))/max(norm(f['mu'][1]),1e-30))

    def temporal_energy(self,K,Omega,mode):
        if abs(complex(K).imag)>1e-14 or K<0:
            raise ValueError('Real nonnegative K required for temporal energy balance.')
        f=self.fields_general(K,mode['U'],mode['Phi'],mode['N'])
        b=self.fields_general(K,mode['U'],mode['Phi'],mode['N'],self.ends)
        u=np.stack([f['ux'][0],f['uz'][0]],axis=1)
        quad=lambda x,c: np.einsum('qi,ij,qj->q',x.conj(),c,x).real
        strain_energy=quad(f['strain'][0],self.C)
        strain_energy+=self.ell**2*(K*K*quad(f['strain'][0],self.C)+quad(f['strain'][1],self.C))
        ha,hb,hc=self.hvec
        Hg=ha*f['strain'][1][:,1]+hb*f['strain'][1][:,0]+hc*1j*K*f['strain'][0][:,2]
        density=(abs(Omega)**2*np.sum(abs(u)**2,axis=1)+strain_energy+quad(f['gp'][0],self.kap)
                 +abs(f['N'][0])**2+2*np.real(f['N'][0].conj()*Hg))
        energy=.25*np.sum(self.w*density)+.25*self.eps*K*np.sum(abs(b['phi'][0])**2)
        diss=.5*self.sc['alpha']*np.sum(self.w*(abs(K*f['mu'][0])**2+abs(f['mu'][1])**2))
        gamma=-complex(Omega).imag
        return dict(mean_energy=float(energy),dissipation=float(diss),
                    temporal_balance_relative=float(abs(2*gamma*energy-diss)/max(diss,1e-30)))

    def spatial_energy(self,K,Omega,mode):
        if abs(complex(Omega).imag)>1e-14 or K.real<=0:
            raise ValueError('Real driving frequency and decaying positive-phase vacuum sheet required.')
        Omega=float(np.real(Omega))
        f=self.fields_general(K,mode['U'],mode['Phi'],mode['N'])
        b=self.fields_general(K,mode['U'],mode['Phi'],mode['N'],self.ends)
        u=np.stack([f['ux'][0],f['uz'][0]],axis=1)
        uz=np.stack([f['ux'][1],f['uz'][1]],axis=1)
        v=-1j*Omega*u;vz=-1j*Omega*uz;vx=K*Omega*u
        mx=f['mx']
        mech=-np.sum(f['S'][:,[0,2]]*v.conj(),axis=1)
        mech-=(mx[:,0]*vx[:,0].conj()+mx[:,2]*vz[:,0].conj()
               +mx[:,2]*vx[:,1].conj()+mx[:,1]*vz[:,1].conj())
        electric=f['phi'][0]*(-1j*Omega*f['D'][:,0]).conj()
        gammax=-self.sc['alpha']*1j*K*f['mu'][0]
        chem=f['mu'][0]*gammax.conj()
        power=.5*np.real(np.sum(self.w*(mech+electric+chem)))
        bv=-1j*Omega*np.stack([b['ux'][0],b['uz'][0]],axis=1)
        fp=.5*np.real(np.sum(b['mz'][:,[0,2]]*bv.conj(),axis=1))
        face_correction=-(fp[1]-fp[0]);power+=face_correction
        # q_vac = K; use its positive real part in exact exterior integrals.
        vacuum_power=-.25*Omega*self.eps*np.sum(abs(b['phi'][0])**2)
        power+=vacuum_power
        quad=lambda x,c: np.einsum('qi,ij,qj->q',x.conj(),c,x).real
        strain_energy=quad(f['strain'][0],self.C)
        strain_energy+=self.ell**2*(abs(K)**2*quad(f['strain'][0],self.C)+quad(f['strain'][1],self.C))
        ha,hb,hc=self.hvec
        Hg=ha*f['strain'][1][:,1]+hb*f['strain'][1][:,0]+hc*1j*K*f['strain'][0][:,2]
        density=(Omega*Omega*np.sum(abs(u)**2,axis=1)+strain_energy+quad(f['gp'][0],self.kap)
                 +abs(f['N'][0])**2+2*np.real(f['N'][0].conj()*Hg))
        vacuum_energy=self.eps*abs(K)**2/(4*K.real)*np.sum(abs(b['phi'][0])**2)
        energy=.25*np.sum(self.w*density)+vacuum_energy
        diss=.5*self.sc['alpha']*np.sum(self.w*(abs(K*f['mu'][0])**2+abs(f['mu'][1])**2))
        balance=abs(2*K.imag*power-diss)/max(abs(diss),1e-30)
        d=self.sc['d']; ki=abs(K.imag)/d
        return dict(power=float(power),mean_energy=float(energy),dissipation=float(diss),
                    energy_velocity_m_s=float(power/energy*self.sc['cs']),
                    spatial_balance_relative=float(balance),vacuum_power=float(vacuum_power),
                    face_hyperstress_power=float(face_correction),
                    alpha_amplitude_m_minus1=float(ki),amplitude_1e_length_m=float(1/ki),
                    energy_1e_length_m=float(1/(2*ki)),phase_wavelength_m=float(2*np.pi*d/K.real),
                    backward=bool(power<0 and K.real>0),passive_direction=bool(K.imag*power>0),
                    power_fraction_10um=float(np.exp(-2*ki*1e-5)),
                    power_fraction_100um=float(np.exp(-2*ki*1e-4)),
                    power_fraction_1mm=float(np.exp(-2*ki*1e-3)),
                    power_fraction_one_phase_wavelength=float(np.exp(-4*np.pi*abs(K.imag)/K.real)))


def eight_state_boundary(K,Omega,d=1e-6,n0=1e19,qvac=None,props=None):
    """Independent strong-equation half-thickness propagator, f=A=H=0.

    State = (U1,U3,Phi,N,T13,T33,D3,Gamma3), L1 parity at the midplane.
    No Galerkin stiffness, basis or differentiation matrices are reused.
    Analytic q_vac=K sheet, flagged separately for exterior admissibility.
    """
    p=dict(SI);p.update(props or {})
    sc=derived(d,n0);c0=sc['c0'];kapref=SI['kappa33']
    c11,c13,c33,c44=[p[s]/c0 for s in ['c11','c13','c33','c44']]
    e15,e31,e33=[p[s]/np.sqrt(c0*kapref) for s in ['e15','e31','e33']]
    ka1,ka3=p['kappa11']/kapref,p['kappa33']/kapref
    alpha=p['electron_diffusivity']/(d*sc['cs']);Q=sc['Q']
    eps=CONST['epsilon0']/kapref;qvac=K if qvac is None else qvac
    inv=np.linalg.inv(np.array([[c33,e33],[e33,-ka3]]))
    def rhs(y):
        ux,uz,phi,N,t13,t33,d3,g3=y
        uzp,phip=inv@np.array([t33-c13*1j*K*ux,d3-e31*1j*K*ux])
        uxp=(t13-e15*1j*K*phi)/c44-1j*K*uz
        s11=c11*1j*K*ux+c13*uzp+e31*phip
        d1=e15*(uxp+1j*K*uz)-ka1*1j*K*phi
        return np.array([uxp,uzp,phip,Q*phip-g3/alpha,
                         -Omega*Omega*ux-1j*K*s11,-Omega*Omega*uz-1j*K*t13,
                         -1j*K*d1-Q*N,1j*Omega*N-alpha*K*K*(N-Q*phi)])
    F=np.stack([rhs(col) for col in np.eye(8)],axis=1)
    mid=np.eye(8)[:,[0,5,6,7]]
    bc=np.zeros((4,8),complex)
    bc[0,4]=bc[1,5]=bc[2,6]=bc[3,7]=1
    bc[2,2]=-eps*qvac
    boundary=bc@expm(.5*F)@mid
    scaled=boundary/np.maximum(np.linalg.norm(boundary,axis=1),1e-30)[:,None]
    scaled/=np.maximum(np.linalg.norm(scaled,axis=0),1e-30)[None,:]
    singular=svdvals(scaled)
    return dict(determinant=np.linalg.det(scaled),
                singular_relative=float(singular[-1]/singular[0]),matrix=boundary)


def independent_spatial_root(Omega,guess,d=1e-6,n0=1e19,props=None):
    def fun(x):
        det=eight_state_boundary(complex(*x),Omega,d,n0,props=props)['determinant']
        return [det.real,det.imag]
    ans=root(fun,[complex(guess).real,complex(guess).imag],tol=1e-11)
    K=complex(*ans.x)
    b=eight_state_boundary(K,Omega,d,n0,props=props)
    return dict(K=K,converged=bool(b['singular_relative']<1e-9),
                scipy_success=bool(ans.success),singular_relative=b['singular_relative'])


def independent_temporal_root(K,guess,d=1e-6,n0=1e19):
    def fun(x):
        det=eight_state_boundary(K,complex(*x),d,n0)['determinant']
        return [det.real,det.imag]
    ans=root(fun,[complex(guess).real,complex(guess).imag],tol=1e-11)
    om=complex(*ans.x);b=eight_state_boundary(K,om,d,n0)
    return dict(omega=om,converged=bool(b['singular_relative']<1e-9),
                scipy_success=bool(ans.success),singular_relative=b['singular_relative'])
