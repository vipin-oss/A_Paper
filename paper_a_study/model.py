"""One focused, explicitly specified ZnO plate/edge calculation.

Static/local electric-enthalpy specialization; NOT a claimed transcription of
Wei's inaccessible complete model. Same physical fields u, phi, delta n.
mu is an exactly eliminable electrochemical-potential auxiliary, not new physics.
Grounded electric and blocking carrier boundaries; all elastic polarizations.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import Legendre,leggauss
from scipy.linalg import eig,solve,svd,matrix_balance,expm
from scipy.optimize import root

ROOT=Path(__file__).resolve().parents[1]
MATERIAL=json.loads((ROOT/'a0/materials.json').read_text())
SI=MATERIAL['SI'];CONST=MATERIAL['SI_definitions']


def tensor_matrix(v):
    """Engineering stress order 11,22,33,23,13,12 to symmetric tensor."""
    ans=np.zeros(v.shape[:-1]+(3,3),complex)
    ans[...,0,0]=v[...,0];ans[...,1,1]=v[...,1];ans[...,2,2]=v[...,2]
    ans[...,1,2]=ans[...,2,1]=v[...,3]
    ans[...,0,2]=ans[...,2,0]=v[...,4]
    ans[...,0,1]=ans[...,1,0]=v[...,5]
    return ans


class Plate:
    def __init__(self,degree=18,d=200e-9,n0=2e18,mobility=.0175,
                 diffusivity=.000455,ell=50e-9,flexo=1e-9,H=0.,electric='ground',
                 nquad=0,edge_electric='insulating'):
        self.degree=degree;self.n=degree+1;self.d=d;self.n0=n0
        self.cs=np.sqrt(SI['c44']/SI['rho']);self.fscale=self.cs/(2*np.pi*d)
        self.a=CONST['q']*diffusivity/(mobility*n0)
        self.Q=CONST['q']*d/np.sqrt(SI['kappa33']*self.a)
        self.alpha=diffusivity/(d*self.cs);self.lam=ell/d
        self.f=flexo/(d*np.sqrt(SI['c44']*SI['kappa33']))
        self.h=H/(d*np.sqrt(self.a*SI['c44']))
        self.H=H;self.flexo_SI=flexo;self.ell_SI=ell
        self.mobility=mobility;self.diffusivity=diffusivity;self.electric=electric
        # Electrical condition on the *reflecting edge* x=0.  The model of this
        # article is 'insulating': D_x(0,z) = 0, natural, one row of
        # boundary_vector on the potential test functions.  'ground' imposes
        # phi(0,z) = 0, a Dirichlet condition for a metallised edge; it is a
        # different boundary-value problem, it was the round-19 default, and it is
        # retained so that the round-19 baseline is reproducible exactly.
        if edge_electric not in ('ground','insulating'):raise ValueError(edge_electric)
        self.edge_electric=edge_electric
        c=SI;c0=c['c44'];kap=c['kappa33']
        self.C=np.array([[c['c11'],c['c12'],c['c13'],0,0,0],
                         [c['c12'],c['c11'],c['c13'],0,0,0],
                         [c['c13'],c['c13'],c['c33'],0,0,0],
                         [0,0,0,c['c44'],0,0],[0,0,0,0,c['c44'],0],
                         [0,0,0,0,0,(c['c11']-c['c12'])/2]])/c0
        self.e=np.array([[0,0,0,0,c['e15'],0],[0,0,0,c['e15'],0,0],
                         [c['e31'],c['e31'],c['e33'],0,0,0]])/np.sqrt(c0*kap)
        self.kap=np.diag([c['kappa11']/kap,c['kappa11']/kap,1.])
        invC=np.linalg.inv(self.C*c0)
        self.schur=H*H*invC[2,2]/(ell*ell*self.a) if ell else 0.
        if (ell==0 and H) or self.schur>=1:raise ValueError('H violates full 3D strict Schur bound')
        if ell==0 and flexo:raise ValueError('Classical validation uses f=A=H=0')
        if electric not in ('ground','open'):raise ValueError(electric)
        # 'ground' enforces phi=0 on both faces (two constraints).  For the
        # open-circuit problem phi is defined only up to an additive constant;
        # that constant is a genuine null vector of the electrostatic operator and
        # removing it (zero-mean gauge) is required for a non-singular system.
        self.np=self.n-2 if electric=='ground' else self.n-1
        self.nu=3*self.n;self.nw=self.nu+self.np+self.n
        self.iu=slice(0,self.nu);self.ip=slice(self.nu,self.nu+self.np)
        self.im=slice(self.nu+self.np,self.nw)
        # Gauss-Legendre on [-1/2, 1/2]: at least 64 nodes and at least
        # 2*degree+10.  `nquad` overrides the rule and exists only so that
        # quadrature sufficiency can be tested independently of the basis
        # (quadrature_audit.py); production runs use the default.
        self.nquad=int(nquad) or max(64,2*degree+10)
        self.z,self.weights=leggauss(self.nquad);self.z/=2;self.weights/=2
        self.b,self.pb=self.basis(self.z,4)
        self.eb,self.epb=self.basis(np.array([-.5,.5]),4)
        self.M=np.kron(np.eye(3),self.b[0].T@(self.weights[:,None]*self.b[0]))
        self.W=self.b[0].T@(self.weights[:,None]*self.b[0])

    def basis(self,z,order):
        b=[np.stack([np.sqrt(2*j+1)*2**r*Legendre.basis(j).deriv(r)(2*np.asarray(z))
                     for j in range(self.n)],axis=1) for r in range(order+1)]
        if self.electric=='ground':
            ratio=np.sqrt((2*np.arange(self.np)+1)/(2*np.arange(self.np)+5))
            pb=[v[:,:self.np]-v[:,2:]*ratio[None,:] for v in b]
        elif self.electric=='open':
            # Drop the constant Legendre mode: phi has zero thickness mean, which
            # fixes the electrostatic gauge without changing any field gradient.
            pb=[v[:,1:] for v in b]
        else:pb=[v.copy() for v in b]
        return b,pb

    @staticmethod
    def form(left,C,right,w):
        return np.einsum('qai,ab,qbj,q->ij',left,C,right,w,optimize=True)

    def strains(self,kx,ky,b=None,r=0):
        b=self.b if b is None else b
        B=np.zeros((len(b[0]),6,self.nu),complex);n=self.n
        B[:,0,:n]=1j*kx*b[r];B[:,1,n:2*n]=1j*ky*b[r];B[:,2,2*n:]=b[r+1]
        B[:,3,n:2*n]=b[r+1];B[:,3,2*n:]=1j*ky*b[r]
        B[:,4,:n]=b[r+1];B[:,4,2*n:]=1j*kx*b[r]
        B[:,5,:n]=1j*ky*b[r];B[:,5,n:2*n]=1j*kx*b[r]
        return B

    def temporal(self,K,reference=None,ky=0.):
        """Independent time generator in u,du/dt,N, with phi eliminated.

        ``ky`` is the conserved edge-tangential wavenumber.  It defaults to 0 so
        every existing call keeps its exact previous behaviour; passing the
        operating value evaluates the *same* weak form at the actual propagation
        geometry instead of the sagittal ky=0 plane.
        """
        B=self.strains(K,ky);Bz=self.strains(K,ky,r=1)
        G=np.stack([1j*K*self.pb[0],1j*ky*self.pb[0],self.pb[1]],axis=1)
        Bt=B.conj();Bzt=Bz.conj();Gt=G.conj();w=self.weights
        kk=K*K+ky*ky
        kuu=(1+self.lam**2*kk)*self.form(Bt,self.C,B,w)+self.lam**2*self.form(Bzt,self.C,Bz,w)
        cpu=self.form(Gt,self.e,B,w)
        cpu+=self.f*(self.pb[1].T@(w[:,None]*self.b[2]))@np.eye(self.nu)[2*self.n:]
        pp=self.form(Gt,self.kap,G,w)
        wp=self.pb[0].T@(w[:,None]*self.b[0])
        pu=solve(pp,cpu);pn=solve(pp,self.Q*wp)
        F=np.zeros((self.n,self.nu),complex)
        F[:,2*self.n:]=self.h*self.b[0].T@(w[:,None]*self.b[2])
        Kf=kuu+cpu.conj().T@pu;R=F.conj().T-cpu.conj().T@pn
        An=self.W+self.Q*wp.T@pn;Ru=F-self.Q*wp.T@pu
        lap=self.b[1].T@(w[:,None]*self.b[1])+kk*self.W
        L=self.alpha*solve(self.W,lap)@solve(self.W,np.eye(self.n))
        u=self.nu;nn=self.n;Z=np.zeros((u,u),complex)
        T=np.block([[Z,np.eye(u),np.zeros((u,nn))],
                    [-solve(self.M,Kf),Z,-solve(self.M,R)],
                    [-L@Ru,np.zeros((nn,u)),-L@An]])
        s,V=eig(T);js=np.where(s.imag < -1e-5)[0]
        js=js[np.argsort(-s[js].imag)]
        modes=[]
        for j in js:
            U=V[:u,j];N=V[2*u:,j];norm=np.sqrt(np.vdot(U,self.M@U).real)
            U=U/norm;N=N/norm;phi=pu@U-pn@N
            mu=N+solve(self.W,F@U-self.Q*wp.T@phi)
            modes.append(dict(omega=1j*s[j],q=np.r_[U,phi,mu],U=U,N=N,
                              maximum_growth=float(s.real.max())))
        if reference is None:return modes
        scores=[abs(np.vdot(reference['U'],self.M@m['U']))**2 for m in modes]
        j=int(np.argmax(scores));modes[j]['MAC']=float(scores[j]);return modes[j]

    def cutoff(self):
        modes=self.temporal(0)
        options=[m for m in modes if m['omega'].real>1 and
                 np.vdot(m['U'][2*self.n:],self.W@m['U'][2*self.n:]).real>.85]
        return min(options,key=lambda m:m['omega'].real)

    def operators(self,ky):
        """Coefficients of x derivatives, with z retained exactly in the basis."""
        q=len(self.z);nw=self.nw;n=self.n
        B=[np.zeros((q,6,nw),complex) for _ in range(3)]
        B[0][:,:,:self.nu]=self.strains(0,ky)
        B[1][:,0,:n]=self.b[0];B[1][:,4,2*n:3*n]=self.b[0];B[1][:,5,n:2*n]=self.b[0]
        Bz=[np.zeros_like(v) for v in B]
        Bz[0][:,:,:self.nu]=self.strains(0,ky,r=1)
        Bz[1][:,0,:n]=self.b[1];Bz[1][:,4,2*n:3*n]=self.b[1];Bz[1][:,5,n:2*n]=self.b[1]
        grad=[[np.zeros_like(B[0]) for _ in range(3)] for _ in range(3)]
        grad[0][1]=B[0];grad[0][2]=B[1]
        grad[1][0]=1j*ky*B[0];grad[1][1]=1j*ky*B[1]
        grad[2][0]=Bz[0];grad[2][1]=Bz[1]
        G=[np.zeros((q,3,nw),complex) for _ in range(3)]
        G[0][:,1,self.ip]=1j*ky*self.pb[0];G[0][:,2,self.ip]=self.pb[1]
        G[1][:,0,self.ip]=self.pb[0]
        MG=[np.zeros_like(v) for v in G]
        MG[0][:,1,self.im]=1j*ky*self.b[0];MG[0][:,2,self.im]=self.b[1]
        MG[1][:,0,self.im]=self.b[0]
        W=np.zeros((q,nw),complex)
        W[:,self.im]=self.b[0];W[:,self.ip]=self.Q*self.pb[0]
        W[:,2*n:3*n]-=self.h*self.b[2]
        U=np.zeros((q,3,nw),complex)
        for j in range(3):U[:,j,j*n:(j+1)*n]=self.b[0]
        return B,grad,G,MG,W,U

    def matrices(self,ky,omega):
        B,g,G,MG,W,U=self.operators(ky)
        A=np.zeros((3,3,self.nw,self.nw),complex);w=self.weights
        for r in range(3):
            for s in range(3):
                A[r,s]=self.form(B[r].conj(),self.C,B[s],w)
                for l in range(3):A[r,s]+=self.lam**2*self.form(g[l][r].conj(),self.C,g[l][s],w)
                A[r,s]+=self.form(G[r].conj(),self.e,B[s],w)+self.form(B[r].conj(),self.e.T,G[s],w)
                A[r,s]-=self.form(G[r].conj(),self.kap,G[s],w)
                A[r,s]-=1j*self.alpha/omega*self.form(MG[r].conj(),np.eye(3),MG[s],w)
                # The sole numerical flexoelectric component is f3333.
                A[r,s]+=self.f*(G[r][:,2,:].conj().T@(w[:,None]*g[2][s][:,2,:])
                                +g[2][r][:,2,:].conj().T@(w[:,None]*G[s][:,2,:]))
        A[0,0]-=omega**2*self.form(U.conj(),np.eye(3),U,w)
        A[0,0]-=W.conj().T@(w[:,None]*W)
        return A

    def polynomial(self,A,kx):
        return sum((-1j*kx)**r*(1j*kx)**s*A[r,s] for r in range(3) for s in range(3))

    def state_operator(self,A):
        """Canonical x-state, including natural corner forces in weak form."""
        nw=self.nw;nu=self.nu;second=self.lam>0
        if not second:
            inv=solve(A[1,1],np.eye(nw))
            F=np.block([[-inv@A[1,0],inv],
                        [A[0,0]-A[0,1]@inv@A[1,0],A[0,1]@inv]])
            return F
        ny=2*nw+2*nu
        W=np.eye(ny)[:nw];P=np.eye(ny)[nw:nw+nu]
        T=np.eye(ny)[nw+nu:2*nw+nu];R=np.eye(ny)[2*nw+nu:]
        DX=np.zeros((nw,ny),complex);DX[:nu]=P
        G=np.block([[A[2,2,:nu,:nu],A[2,1,:nu,nu:]],
                    [A[1,2,nu:,:nu],A[1,1,nu:,nu:]]])
        rhs=np.vstack([R-A[2,0,:nu]@W-A[2,1,:nu]@DX,
                       T[nu:]-A[1,0,nu:]@W-A[1,1,nu:]@DX])
        Z=solve(G,rhs)
        DX[nu:]=Z[nu:];DD=np.zeros_like(DX);DD[:nu]=Z[:nu]
        return np.vstack([DX,Z[:nu],A[0,0]@W+A[0,1]@DX+A[0,2]@DD,
                          A[1,0,:nu]@W+A[1,1,:nu]@DX+A[1,2,:nu]@DD-T[:nu]])

    def state_from_q(self,A,kx,q):
        T=sum((A[1,s]-1j*kx*A[2,s])@(q*(1j*kx)**s) for s in range(3))
        if self.lam:
            R=sum(A[2,s,:self.nu]@(q*(1j*kx)**s) for s in range(3))
            return np.r_[q,1j*kx*q[:self.nu],T,R]
        return np.r_[q,T]

    def state_parts(self,y):
        if self.lam:
            return y[:self.nw],y[self.nw:self.nw+self.nu],y[self.nw+self.nu:2*self.nw+self.nu],y[2*self.nw+self.nu:]
        return y[:self.nw],None,y[self.nw:],None

    def power(self,y,omega):
        q,p,T,R=self.state_parts(y)
        value=-np.dot(T[:self.nu],(-1j*omega*q[:self.nu]).conj())
        if self.lam:value-=np.dot(R,(-1j*omega*p).conj())
        value+=np.dot(q[self.ip],(-1j*omega*T[self.ip]).conj())
        value+=np.dot(q[self.im],(-1j*omega*T[self.im]).conj())
        return float(.5*value.real)

    def boundary_vector(self,y):
        """Edge residuals at x=0, in the order (mechanical, double, electric, carrier).

        T[:nu] is the traction-like flux conjugate to the displacement state,
        R = tau_j11 the x-normal double traction, T[ip] = D_x the x-normal
        electric displacement and T[im] = -J_x the x-normal carrier flux.  The
        electrical row is the only one that depends on `edge_electric`.
        """
        q,p,T,R=self.state_parts(y)
        flux=T[self.ip] if self.edge_electric=='insulating' else q[self.ip]
        if self.lam:return np.r_[T[:self.nu],R,flux,T[self.im]]
        return np.r_[T[:self.nu],flux,T[self.im]]

    def waves(self,ky,omega):
        A=self.matrices(ky,omega);F=self.state_operator(A)
        balanced,T=matrix_balance(F,permute=False,scale=True)
        values,V=eig(balanced);Y=T@V
        waves=[]
        for j in range(len(values)):
            K=-1j*values[j];y=Y[:,j];y/=np.linalg.norm(y)
            waves.append(dict(K=K,y=y,q=y[:self.nw],power=self.power(y,omega)))
        return waves,A,F

    def fields(self,kx,ky,q,b=None,pb=None):
        b=self.b if b is None else b;pb=self.pb if pb is None else pb
        U=q[:self.nu].reshape(3,self.n)
        us=[v@U.T for v in b];phis=[v@q[self.ip] for v in pb]
        mus=[v@q[self.im] for v in b]
        strain=[self.strains(kx,ky,b,r)@q[:self.nu] for r in range(4)]
        gp=[np.stack([1j*kx*phis[r],1j*ky*phis[r],phis[r+1]],axis=1) for r in range(3)]
        N=[mus[r]+self.Q*phis[r]-self.h*us[r+2][:,2] for r in range(3)]
        tau=[];dtau=[]
        for r in range(2):
            tt=[]
            for l,factor in [(0,1j*kx),(1,1j*ky),(2,None)]:
                v=self.lam**2*(factor*strain[r] if l<2 else strain[r+1])@self.C.T
                if l==2:v[:,2]+=self.f*phis[r+1]+self.h*N[r]
                tt.append(v)
            (tau if r==0 else dtau).extend(tt)
        sigma=strain[0]@self.C.T+gp[0]@self.e
        sigmaz=strain[1]@self.C.T+gp[1]@self.e
        S=sigma-1j*kx*tau[0]-1j*ky*tau[1]-dtau[2]
        tauzz=self.lam**2*strain[3]@self.C.T
        tauzz[:,2]+=self.f*phis[3]+self.h*N[2]
        Sz=sigmaz-1j*kx*dtau[0]-1j*ky*dtau[1]-tauzz
        D=strain[0]@self.e.T-gp[0]@self.kap.T;D[:,2]+=self.f*us[2][:,2]
        Dz=strain[1]@self.e.T-gp[1]@self.kap.T;Dz[:,2]+=self.f*us[3][:,2]
        return dict(u=us,strain=strain,phi=phis,mu=mus,N=N,gp=gp,tau=tau,dtau=dtau,
                    S=tensor_matrix(S),Sz=tensor_matrix(Sz),D=D,Dz=Dz,sigma=sigma)

    def mode_diagnostics(self,kx,ky,omega,q):
        f=self.fields(kx,ky,q);e=self.fields(kx,ky,q,self.eb,self.epb);w=self.weights
        v=-1j*omega*f['u'][0];edot=-1j*omega*f['strain'][0]
        powers=[]
        for l,k in [(0,kx),(1,ky)]:
            mech=-np.sum(f['S'][:,:,l]*v.conj(),axis=1)-np.sum(f['tau'][l]*edot.conj(),axis=1)
            electric=f['phi'][0]*(-1j*omega*f['D'][:,l]).conj()
            chemical=f['mu'][0]*(-self.alpha*1j*k*f['mu'][0]).conj()
            pe=.5*np.real(np.sum(w*(mech+electric+chemical)))
            tz=tensor_matrix(e['tau'][2]);ve=-1j*omega*e['u'][0]
            face=.5*np.real(np.sum(tz[:,:,l]*ve.conj(),axis=1))
            pe-=face[1]-face[0];powers.append(float(pe))
        quad=lambda v,C:np.einsum('qi,ij,qj->q',v.conj(),C,v).real
        grad=[1j*kx*f['strain'][0],1j*ky*f['strain'][0],f['strain'][1]]
        density=(omega**2*np.sum(abs(f['u'][0])**2,axis=1)+quad(f['strain'][0],self.C)
                 +self.lam**2*sum(quad(g,self.C) for g in grad)+quad(f['gp'][0],self.kap)
                 +abs(f['N'][0])**2+2*np.real(f['N'][0].conj()*self.h*f['u'][2][:,2]))
        energy=.25*np.sum(w*density)
        diss=.5*self.alpha*np.sum(w*((abs(kx)**2+ky**2)*abs(f['mu'][0])**2+abs(f['mu'][1])**2))
        force=1j*kx*f['S'][:,:,0]+1j*ky*f['S'][:,:,1]+f['Sz'][:,:,2]
        def norm(v):return float(np.sqrt(np.sum(w.reshape((-1,)+(1,)*(v.ndim-1))*abs(v)**2)))
        mom=norm(force+omega**2*f['u'][0])/max(norm(force),norm(omega**2*f['u'][0]),1e-30)
        gauss=1j*kx*f['D'][:,0]+1j*ky*f['D'][:,1]+f['Dz'][:,2]+self.Q*f['N'][0]
        carrier=-1j*omega*f['N'][0]-self.alpha*(f['mu'][2]-(kx*kx+ky*ky)*f['mu'][0])
        tr=e['S'][:,:,2]-1j*kx*tensor_matrix(e['tau'][2])[:,:,0]-1j*ky*tensor_matrix(e['tau'][2])[:,:,1]
        rr=tensor_matrix(e['tau'][2])[:,:,2]
        stress=max(norm(f['sigma']),norm(f['S']),1e-30)
        return dict(Px=powers[0],Py=powers[1],energy=float(energy),dissipation=float(diss),
            vEx=float(self.cs*powers[0]/energy),vEy=float(self.cs*powers[1]/energy),
            balance=float(abs(2*kx.imag*powers[0]-diss)/max(abs(diss),1e-30)),
            momentum=mom,gauss=norm(gauss)/max(norm(self.Q*f['N'][0]),norm(f['D']),1e-30),
            carrier=norm(carrier)/max(norm(omega*f['N'][0]),1e-30),
            traction=float(np.max(abs(tr))/stress),double_traction=float(np.max(abs(rr))/stress),
            blocking=float(np.max(abs(e['mu'][1]))/max(norm(f['mu'][0]),1e-30)),
            grounded_phi=float(np.max(abs(e['phi'][0]))))

    def edge(self,ky,omega,incident_guess,target_guess,L=10.):
        waves,A,F=self.waves(ky,omega)
        # Complex roots are selected by half-space decay; real roots by power.
        outgoing=[];incoming=[]
        for wave in waves:
            K=wave['K'];tol=2e-8*max(1,abs(K))
            out=(K.imag < -tol) or (abs(K.imag)<=tol and wave['power']<0)
            (outgoing if out else incoming).append(wave)
        expected=F.shape[0]//2
        if len(outgoing)!=expected:raise RuntimeError(f'Outgoing count {len(outgoing)} != {expected}')
        inc=min(incoming,key=lambda a:abs(a['K']-incident_guess))
        if inc['power']<=0:raise RuntimeError('Incident port is not positive-power')
        iy=inc['y']/np.sqrt(inc['power']);inc=dict(inc,y=iy,q=iy[:self.nw],power=1.)
        Y=np.stack([v['y'] for v in outgoing],axis=1);K=np.array([v['K'] for v in outgoing])
        B=np.stack([self.boundary_vector(Y[:,j]) for j in range(len(K))],axis=1)
        bi=self.boundary_vector(inc['y'])
        row=np.maximum(np.linalg.norm(B,axis=1),1e-30)
        C=B/row[:,None];rhs=-bi/row
        col=np.maximum(np.linalg.norm(C,axis=0),1e-30)
        u,s,vh=svd(C/col[None,:]);cut=1e-12*s[0]
        if np.sum(s>cut)!=len(s):
            raise RuntimeError('Unresolved rank deficiency in edge matching')
        aa=(vh.conj().T@((u.conj().T@rhs)/s))/col
        edge=inc['y']+Y@aa
        residual=np.linalg.norm(self.boundary_vector(edge)/row)/max(np.linalg.norm(bi/row),1e-30)
        ib=int(np.argmin(abs(K-target_guess)))
        fullY=np.column_stack([inc['y'],Y]);allK=np.r_[inc['K'],K];c=np.r_[1.,aa]
        left=fullY@(c*np.exp(-1j*allK*L))
        pleft=self.power(left,omega);pedge=self.power(edge,omega)
        inc_left=float(np.exp(2*inc['K'].imag*L))
        qmu=fullY[self.im,:]
        mu=self.b[0]@qmu;muz=self.b[1]@qmu;mux=mu*(1j*allK)[None,:]
        G=.5*self.alpha*(mux.conj().T@(self.weights[:,None]*mux)
              +ky*ky*mu.conj().T@(self.weights[:,None]*mu)+muz.conj().T@(self.weights[:,None]*muz))
        delta=1j*(allK[None,:]-allK.conj()[:,None])
        integral=np.full_like(delta,L)
        mask=abs(delta)>1e-10;integral[mask]=-np.expm1(-L*delta[mask])/delta[mask]
        diss=float(np.vdot(c,(G*integral)@c).real)
        selfout=np.array([self.power(Y[:,j],omega)*abs(aa[j])**2*np.exp(2*K[j].imag*L) for j in range(len(K))])
        cross=pleft-inc_left-selfout.sum()
        target=self.mode_diagnostics(K[ib],ky,omega,Y[:self.nw,ib])
        incident=self.mode_diagnostics(inc['K'],ky,omega,inc['q'])
        Rb=float(-selfout[ib]/inc_left)
        result=dict(ky=ky,omega=omega,frequency_Hz=omega*self.fscale,degree=self.degree,H_J_m=self.H,
             incident_K=inc['K'],backward_K=K[ib],backward_reflection_self_power=Rb,
             edge_scaled_residual=float(residual),edge_condition=float(s[0]/s[-1]),
             edge_rank=int(np.sum(s>cut)),edge_size=len(s),
             incident_angle_deg=float(np.degrees(np.arctan2(incident['Py'],incident['Px']))),
             reflected_angle_deg=float(np.degrees(np.arctan2(target['Py'],-target['Px']))),
             incident=incident,backward=target,reference_distance_m=L*self.d,
             incident_power_left=inc_left,total_power_left=pleft,edge_power=pedge,
             dissipation_control_volume=diss,cross_power_left=float(cross),
             total_outgoing_self_power=float(-selfout.sum()),
             power_balance_relative=float(abs(pleft-pedge-diss)/inc_left),
             power_balance_relative_dissipation=float(abs(pleft-pedge-diss)/max(abs(diss),1e-30)),
             backward_amplitude=aa[ib],outgoing_modes=len(K),
             negative_direction=bool(incident['Px']>0 and incident['Py']>0 and target['Px']<0 and target['Py']<0
                   and target['Px']*K[ib].real+target['Py']*ky<0))
        # Returned fields are optional scratch, not a dataset of massive arrays.
        return result,dict(incident=inc,Y=Y,K=K,amplitudes=aa,index_backward=ib,A=A,F=F)


def classical_strong_root(plate,K,guess,electric='ground'):
    """Independent eight-state classical sagittal system, no spectral matrices."""
    c0=SI['c44'];kap=SI['kappa33'];p=SI
    c11,c13,c33,c44=[p[k]/c0 for k in ['c11','c13','c33','c44']]
    e15,e31,e33=[p[k]/np.sqrt(c0*kap) for k in ['e15','e31','e33']]
    ka1=p['kappa11']/kap
    inv=np.linalg.inv(np.array([[c33,e33],[e33,-1.]]))
    def boundary(omega):
        def rhs(y):
            ux,uz,phi,N,t13,t33,D3,G3=y
            vz,phip=inv@np.array([t33-c13*1j*K*ux,D3-e31*1j*K*ux])
            vx=(t13-e15*1j*K*phi)/c44-1j*K*uz
            s11=c11*1j*K*ux+c13*vz+e31*phip
            D1=e15*(vx+1j*K*uz)-ka1*1j*K*phi
            return np.array([vx,vz,phip,plate.Q*phip-G3/plate.alpha,
                -omega*omega*ux-1j*K*s11,-omega*omega*uz-1j*K*t13,
                -1j*K*D1-plate.Q*N,1j*omega*N-plate.alpha*K*K*(N-plate.Q*phi)])
        F=np.stack([rhs(y) for y in np.eye(8)],axis=1)
        mid=np.eye(8)[:,[0,5,6,7]]
        bc=np.eye(8)[[4,5,2 if electric=='ground' else 6,7]]
        M=bc@expm(.5*F)@mid;M/=np.linalg.norm(M,axis=1)[:,None]
        return np.linalg.det(M)
    ans=root(lambda x:[boundary(complex(*x)).real,boundary(complex(*x)).imag],
             [guess.real,guess.imag],tol=1e-11)
    if abs(boundary(complex(*ans.x)))>1e-10:
        raise RuntimeError('Independent classical root residual failed')
    return complex(*ans.x)


def edge_field_residuals(plate,omega,ky,solution):
    """Independent traction/corner reconstruction, not canonical matrices.

    Natural corner forces enter the weak edge balance explicitly. Pointwise
    corner/traction errors are also retained, not confused with weak residuals.
    """
    z,w=leggauss(max(96,2*plate.degree+18));z/=2;w/=2
    b,pb=plate.basis(z,4);eb,epb=plate.basis(np.array([-.5,.5]),4)
    waves=[(solution['incident']['K'],solution['incident']['q'],1.)]
    waves += [(K,solution['Y'][:plate.nw,j],a) for j,(K,a) in enumerate(zip(solution['K'],solution['amplitudes']))]
    nq=len(z);T=np.zeros((nq,3),complex);R=T.copy();phi=np.zeros(nq,complex);gamma=phi.copy()
    corners=np.zeros((2,3),complex)
    inc_scale=0.
    for i,(K,q,a) in enumerate(waves):
        f=plate.fields(K,ky,q,b,pb);e=plate.fields(K,ky,q,eb,epb)
        tx=tensor_matrix(f['tau'][0]);txz=tensor_matrix(f['dtau'][0])
        te=f['S'][:,:,0]-1j*ky*tx[:,:,1]-txz[:,:,2]
        rr=tx[:,:,0]
        corner=tensor_matrix(e['tau'][2])[:,:,0]+tensor_matrix(e['tau'][0])[:,:,2]
        T+=a*te;R+=a*rr;corners+=a*corner
        phi+=a*f['phi'][0];gamma+=a*(-plate.alpha*1j*K*f['mu'][0])
        if i==0:inc_scale=np.sqrt(np.sum(w[:,None]*(abs(te)**2+abs(rr)**2)))
    weakT=b[0].T@(w[:,None]*T)+eb[0][1,:,None]*corners[1]-eb[0][0,:,None]*corners[0]
    weakR=b[0].T@(w[:,None]*R)
    denominator=max(inc_scale,1e-30)
    inner=abs(z)<.4
    return dict(independent_weak_mechanical=float(np.linalg.norm(np.r_[weakT.ravel(),weakR.ravel()])/denominator),
        edge_traction_inner_rms=float(np.sqrt(np.mean(abs(T[inner])**2))/denominator),
        edge_double_traction_rms=float(np.sqrt(np.mean(abs(R)**2))/denominator),
        corner_line_force_max=float(np.max(abs(corners))/denominator),
        grounded_phi_max=float(np.max(abs(phi))),blocking_current_max=float(np.max(abs(gamma))),
        # Stored for optional edge profiles, not a claimed pointwise solution.
        z=z,T=T,R=R,corner=corners)


def strong_gradient_matrix(plate,K,omega):
    """Independent sagittal 12-state z propagator, including nonzero f and H.

    State (u1,u3,u1',u3',phi,mu,t1,t3,r1,r3,D3,Gamma3).
    Derived directly from constitutive stresses and strong differential laws.
    """
    c0=SI['c44'];kap=SI['kappa33'];p=SI
    c11,c13,c33,c44=[p[k]/c0 for k in ['c11','c13','c33','c44']]
    e15,e31,e33=[p[k]/np.sqrt(c0*kap) for k in ['e15','e31','e33']]
    ka1=p['kappa11']/kap;ll=plate.lam**2;h=plate.h;f=plate.f
    inv=np.linalg.inv(np.array([[ll*c44,0,0],[0,ll*c33-h*h,f],[0,f,-1.]]))
    def rhs(y):
        u,v,up,vp,phi,mu,t1,t3,r1,r3,D3,G3=y
        upp,vpp,phip=inv@np.array([r1-ll*c44*1j*K*vp,
            r3-ll*c13*1j*K*up-h*(mu+plate.Q*phi),D3-e31*1j*K*u-e33*vp])
        N=mu+plate.Q*phi-h*vpp
        s11=c11*1j*K*u+c13*vp;s33=c13*1j*K*u+c33*vp;s13=c44*(up+1j*K*v)
        r1p=(1+ll*K*K)*s13+e15*1j*K*phi-1j*K*ll*(c11*1j*K*up+c13*vpp)-t1
        r3p=(1+ll*K*K)*s33+e33*phip-1j*K*r1-t3
        t1p=-omega**2*u-1j*K*((1+ll*K*K)*s11+e31*phip)
        t3p=-omega**2*v-1j*K*((1+ll*K*K)*s13+e15*1j*K*phi)
        D1=e15*(up+1j*K*v)-ka1*1j*K*phi
        return np.array([up,vp,upp,vpp,phip,-G3/plate.alpha,t1p,t3p,r1p,r3p,
                         -1j*K*D1-plate.Q*N,1j*omega*N-plate.alpha*K*K*mu])
    return np.stack([rhs(y) for y in np.eye(12)],axis=1)


def gradient_strong_root(plate,K=None,omega=None,guess=None):
    """Solve omega at given K, or K at real omega. No Galerkin matrices."""
    if (K is None)==(omega is None):raise ValueError('Supply one of K and omega')
    def boundary(x):
        kk,ww=(complex(*x),omega) if K is None else (K,complex(*x))
        F=strong_gradient_matrix(plate,kk,ww)
        # Nonzero f with polar piezoelectricity mixes the two thickness
        # parities. Use the FULL plate, not a symmetry-plane restriction.
        free=[0,1,2,3,5,10] if plate.electric=='ground' else [0,1,2,3,4,5]
        initial=np.eye(12)[:,free]
        bc=np.eye(12)[[6,7,8,9,4 if plate.electric=='ground' else 10,11]]
        M=bc@expm(F)@initial
        M/=np.maximum(np.linalg.norm(M,axis=1),1e-100)[:,None]
        return np.linalg.det(M)
    ans=root(lambda x:[boundary(x).real,boundary(x).imag],[guess.real,guess.imag],tol=1e-10)
    residual=abs(boundary(ans.x))
    if not np.isfinite(residual) or residual>1e-10:raise RuntimeError(f'Independent strong root failed: {ans.message}; {residual}')
    return complex(*ans.x)


class MeshPlate(Plate):
    """Independent C1 cubic-Hermite through-thickness Galerkin cross-check.

    Same continuum law and physical boundaries; different approximation space.
    All quadrature is elementwise. Canonical flux, not piecewise strong-field
    postprocessing, is used for the scattering comparison.
    """
    def __init__(self,elements=12,**kwargs):
        self.knots=np.linspace(-.5,.5,elements+1)
        self.spacing=np.diff(self.knots)
        self.nodeh=np.r_[self.spacing[0],(self.spacing[:-1]+self.spacing[1:])/2,self.spacing[-1]]
        super().__init__(degree=2*elements+1,**kwargs)
        z,w=leggauss(8)
        self.z=np.concatenate([(a+b)/2+(b-a)*z/2 for a,b in zip(self.knots[:-1],self.knots[1:])])
        self.weights=np.concatenate([(b-a)*w/2 for a,b in zip(self.knots[:-1],self.knots[1:])])
        self.b,self.pb=self.basis(self.z,4)
        self.eb,self.epb=self.basis(np.array([-.5,.5]),4)
        self.W=self.b[0].T@(self.weights[:,None]*self.b[0])
        self.M=np.kron(np.eye(3),self.W)

    def basis(self,z,order):
        from numpy.polynomial import Polynomial
        z=np.asarray(z);j=np.clip(np.searchsorted(self.knots,z,side='right')-1,0,len(self.spacing)-1)
        h=self.spacing[j];t=(z-self.knots[j])/h
        polynomials=[Polynomial([1,0,-3,2]),Polynomial([0,1,-2,1]),
                     Polynomial([0,0,3,-2]),Polynomial([0,0,-1,1])]
        b=[]
        for r in range(order+1):
            v=np.zeros((len(z),self.n))
            for k,P in enumerate(polynomials):
                node=j+(k//2);index=2*node+(k%2)
                scale=(h/self.nodeh[node]) if k%2 else 1.
                v[np.arange(len(z)),index]+=P.deriv(r)(t)*scale/h**r
            b.append(v)
        keep=[k for k in range(self.n) if k not in (0,self.n-2)]
        pb=[v[:,keep] for v in b] if self.electric=='ground' else [v.copy() for v in b]
        return b,pb


def temporal_energy_balance(plate,K,mode):
    """Independent positive stored-energy quadrature for a complex time pole.

    Uses |omega|^2, not omega^2, in kinetic energy. Temporal decay is not replaced
    by a group-velocity estimate of spatial attenuation.
    """
    f=plate.fields(K,0,mode['q']);w=plate.weights;omega=mode['omega']
    quad=lambda v,C:np.einsum('qi,ij,qj->q',v.conj(),C,v).real
    grad=[1j*K*f['strain'][0],f['strain'][1]]
    E=.25*np.sum(w*(abs(omega)**2*np.sum(abs(f['u'][0])**2,axis=1)
        +quad(f['strain'][0],plate.C)+plate.lam**2*sum(quad(g,plate.C) for g in grad)
        +quad(f['gp'][0],plate.kap)+abs(f['N'][0])**2
        +2*np.real(f['N'][0].conj()*plate.h*f['u'][2][:,2])))
    D=.5*plate.alpha*np.sum(w*(K*K*abs(f['mu'][0])**2+abs(f['mu'][1])**2))
    return dict(energy=float(E),dissipation=float(D),
        relative_balance=float(abs(-2*omega.imag*E-D)/max(D,1e-30)))
