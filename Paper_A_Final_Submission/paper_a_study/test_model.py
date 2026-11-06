"""Essential checks, independent propagators, and a solved edge conversion."""
import unittest
from unittest.mock import patch
import numpy as np
from paper_a_study.model import (Plate,MeshPlate,SI,CONST,gradient_strong_root,
    classical_strong_root,edge_field_residuals,temporal_energy_balance)

OMEGA=7.6333735784537335
KY=.12976738826550185
H_TEST=2.00485322e-23


class TestStudy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=Plate(degree=18)
        cls.r,cls.s=cls.p.edge(KY,OMEGA,.736+.00001j,.245-.00001j)

    def test_material_units_and_schur(self):
        self.assertAlmostEqual(self.p.diffusivity/self.p.mobility,.026)
        self.assertAlmostEqual(self.p.cs,2746.608754,places=5)
        self.assertAlmostEqual(Plate(H=H_TEST).schur,.0005,places=10)
        self.assertRaises(ValueError,Plate,H=2e-21)
        self.assertRaises(ValueError,Plate,H=H_TEST,ell=0,flexo=0)

    def test_H_changes_only_prescribed_constitutive_terms(self):
        p=self.p;h=Plate(degree=p.degree,H=H_TEST)
        rng=np.random.default_rng(4)
        q=rng.normal(size=p.nw)+1j*rng.normal(size=p.nw)
        qh=q.copy()
        qh[p.im]+=h.h*np.linalg.solve(p.W,p.b[0].T@(p.weights*(p.b[2]@q[2*p.n:3*p.n])))
        f=p.fields(.4,.1,q);g=h.fields(.4,.1,qh)
        np.testing.assert_allclose(g['N'][0],f['N'][0],atol=1e-12)
        np.testing.assert_allclose(g['sigma'],f['sigma'],atol=1e-12)
        np.testing.assert_allclose(g['D'],f['D'],atol=1e-12)
        np.testing.assert_allclose(g['tau'][2][:,2]-f['tau'][2][:,2],h.h*f['N'][0],atol=2e-12)
        for j in [0,1]:np.testing.assert_allclose(g['tau'][j],f['tau'][j],atol=1e-12)

    def test_temporal_vs_independent_spatial_polynomial(self):
        p=self.p;m=p.temporal(.3,p.cutoff());A=p.matrices(0,m['omega']);D=p.polynomial(A,.3)
        defect=np.linalg.norm(D@m['q'])/(np.linalg.norm(D)*np.linalg.norm(m['q']))
        self.assertLess(defect,1e-13)

    def test_first_order_linearization(self):
        p=self.p;A=p.matrices(.1,OMEGA);F=p.state_operator(A);K=.4
        q=np.random.default_rng(2).normal(size=p.nw);y=p.state_from_q(A,K,q)
        err=F@y-1j*K*y;D=p.polynomial(A,K)@q
        np.testing.assert_allclose(err[p.nw+p.nu:2*p.nw+p.nu],D,rtol=1e-12,atol=1e-7)
        self.assertLess(np.linalg.norm(err[:p.nw+p.nu])/max(np.linalg.norm(y),1e-30),1e-11)

    def test_reciprocity_at_oblique_wavenumber(self):
        p=self.p;A=p.matrices(.13,OMEGA);B=p.matrices(-.13,OMEGA)
        D=p.polynomial(A,.7);E=p.polynomial(B,-.7)
        self.assertLess(np.linalg.norm(D.T-E)/np.linalg.norm(D),1e-13)
        F=p.state_operator(A);G=p.state_operator(B);m=F.shape[0]//2
        J=np.block([[np.zeros((m,m)),np.eye(m)],[-np.eye(m),np.zeros((m,m))]])
        self.assertLess(np.linalg.norm(F.T@J+J@G)/np.linalg.norm(F),1e-12)

    def test_classical_exact_SH_modes(self):
        p=Plate(degree=18,ell=0,flexo=0);K=.8
        sh=[m['omega'] for m in p.temporal(K)
            if np.vdot(m['U'][p.n:2*p.n],p.W@m['U'][p.n:2*p.n]).real>.999]
        for j in range(3):
            exact=np.sqrt(p.C[5,5]*K*K+(j*np.pi)**2)
            self.assertLess(min(abs(a-exact) for a in sh),1e-9)

    def test_gradient_exact_fundamental_SH(self):
        p=self.p;K=.8;exact=np.sqrt(p.C[5,5]*K*K*(1+p.lam*p.lam*K*K))
        sh=[m['omega'] for m in p.temporal(K)
            if np.vdot(m['U'][p.n:2*p.n],p.W@m['U'][p.n:2*p.n]).real>.999]
        self.assertLess(min(abs(a-exact) for a in sh),1e-10)

    def test_independent_classical_grounded_and_open(self):
        for electric in ['ground','open']:
            p=Plate(degree=18,ell=0,flexo=0,electric=electric)
            modes=p.temporal(.1)
            ref=min((m for m in modes if m['omega'].real>1 and
                np.vdot(m['U'][2*p.n:],p.W@m['U'][2*p.n:]).real>.85),
                key=lambda m:m['omega'].real)
            for K in [.3,.7]:
                ref=p.temporal(K,ref)
                root=classical_strong_root(p,K,ref['omega'],electric=electric)
                self.assertLess(abs(root-ref['omega']),1e-10)

    def test_independent_nonzero_f_H_temporal(self):
        for H in [0,-H_TEST,H_TEST]:
            p=Plate(degree=18,H=H);m=p.temporal(.3,p.cutoff())
            root=gradient_strong_root(p,K=.3,guess=m['omega'])
            self.assertLess(abs(root-m['omega']),1e-10)
            self.assertGreater(-m['omega'].imag,0)

    def test_temporal_energy_dissipation_balance(self):
        for H in [0,-H_TEST,H_TEST]:
            p=Plate(degree=18,H=H);m=p.temporal(.3,p.cutoff())
            b=temporal_energy_balance(p,.3,m)
            self.assertGreater(b['energy'],0)
            self.assertGreater(b['dissipation'],0)
            self.assertLess(b['relative_balance'],5e-6)

    def test_independent_spatial_roots(self):
        for H in [0,-H_TEST,H_TEST]:
            p=Plate(degree=18,H=H);r,s=p.edge(KY,OMEGA,.736+.00001j,.245-.00001j)
            for name in ['incident_K','backward_K']:
                K=np.sqrt(r[name]**2+KY*KY)
                exact=gradient_strong_root(p,omega=OMEGA,guess=K)
                self.assertLess(abs(exact-K),1e-10)

    def test_outgoing_count_and_nonzero_backward_conversion(self):
        r=self.r
        self.assertEqual(r['outgoing_modes'],r['edge_size'])
        self.assertEqual(r['edge_rank'],r['edge_size'])
        self.assertTrue(r['negative_direction'])
        self.assertGreater(r['backward_reflection_self_power'],.01)
        self.assertLess(r['backward_reflection_self_power'],.04)
        self.assertLess(r['reflected_angle_deg'],-20)

    def test_modal_energy_flux_and_strong_residuals(self):
        p=self.p;r=self.r;s=self.s
        for diag,y in [(r['incident'],s['incident']['y']),
                       (r['backward'],s['Y'][:,s['index_backward']])]:
            self.assertGreater(diag['energy'],0)
            self.assertGreater(diag['dissipation'],0)
            self.assertAlmostEqual(diag['Px'],p.power(y,OMEGA),places=10)
            self.assertLess(diag['balance'],1e-6)
            for key in ['momentum','gauss','carrier','traction','double_traction','blocking']:
                self.assertLess(diag[key],1e-8,key)

    def test_interference_inclusive_finite_volume_power(self):
        for L in [2,10,30]:
            r,s=self.p.edge(KY,OMEGA,.736+.00001j,.245-.00001j,L=L)
            self.assertLess(r['power_balance_relative'],1e-9)
            self.assertLess(abs(r['edge_power']),1e-10)
            self.assertGreater(r['dissipation_control_volume'],0)
            self.assertGreater(abs(r['cross_power_left']),1e-8)

    def test_independent_weak_corner_reconstruction(self):
        e=edge_field_residuals(self.p,OMEGA,KY,self.s)
        self.assertLess(e['independent_weak_mechanical'],1e-9)
        self.assertLess(e['edge_double_traction_rms'],1e-10)
        self.assertLess(e['grounded_phi_max'],1e-10)
        # Deliberately NOT asserting a resolved pointwise corner traction.
        self.assertGreater(e['corner_line_force_max'],1e-4)

    def test_degree_convergence(self):
        p=Plate(degree=22);r,_=p.edge(KY,OMEGA,.736+.00001j,.245-.00001j)
        self.assertLess(abs(r['backward_reflection_self_power']-self.r['backward_reflection_self_power']),2e-8)
        self.assertLess(abs(r['backward_K']-self.r['backward_K']),1e-10)

    def test_independent_C1_mesh_approaches_spectral_edge(self):
        errors=[]
        for elements in [8,12,18]:
            p=MeshPlate(elements=elements);r,_=p.edge(KY,OMEGA,.736+.00001j,.245-.00001j)
            errors.append(abs(r['backward_reflection_self_power']-self.r['backward_reflection_self_power']))
            self.assertLess(r['power_balance_relative'],1e-7)
        self.assertTrue(errors[2]<errors[1]<errors[0])
        self.assertLess(errors[-1],3e-5)

    def test_singular_edge_system_is_rejected(self):
        from scipy.linalg import svd as actual_svd
        def singular(*args,**kwargs):
            u,s,v=actual_svd(*args,**kwargs);s[-1]=0;return u,s,v
        with patch('paper_a_study.model.svd',side_effect=singular):
            self.assertRaisesRegex(RuntimeError,'rank deficiency',self.p.edge,KY,OMEGA,.736,.245)


if __name__=='__main__':unittest.main(verbosity=2)
