"""Reproduce the focused illustrative study; no downloaded/hidden data needed.

OPENBLAS_NUM_THREADS=1 python -m paper_a_study.run_study
Results are deliberately small. No claims of Wei/Fang reproduction or calibrated
higher-order material constants are made by this script.
"""
from pathlib import Path
import csv,json,time,hashlib
import numpy as np
from scipy.optimize import minimize_scalar
from numpy.polynomial.hermite import hermgauss
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator,FormatStrFormatter
from paper_a_study.model import (Plate,MeshPlate,SI,CONST,gradient_strong_root,
    classical_strong_root,edge_field_residuals,temporal_energy_balance)

HERE=Path(__file__).resolve().parent;OUT=HERE/'results';CACHE=HERE/'cache'
OUT.mkdir(exist_ok=True);CACHE.mkdir(exist_ok=True)
DEGREE=22
AREF=CONST['q']*.026/1e19
HCRIT=np.sqrt((50e-9)**2*AREF/np.linalg.inv(Plate().C*SI['c44'])[2,2])
ETAS=[0.,-.05,.05]
COLORS={0.:'#155e75',-.05:'#16806a',.05:'#cc642f'}
LABELS={0.:'H = 0',-.05:'H = −0.05 H*',.05:'H = +0.05 H*'}
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
    'axes.labelcolor':'#263747','text.color':'#263747','axes.edgecolor':'#92a2b0',
    'svg.fonttype':'none','savefig.facecolor':'white','figure.facecolor':'white'})


def scalar(x):
    if isinstance(x,complex) or np.iscomplexobj(x):return {'real':float(x.real),'imag':float(x.imag)}
    if isinstance(x,np.generic):return x.item()
    raise TypeError(type(x))


def dump(name,data):
    (OUT/name).write_text(json.dumps(data,default=scalar,indent=2,allow_nan=False)+'\n')


def table(name,rows):
    with (OUT/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def savefig(name,fig):
    fig.savefig(OUT/(name+'.svg'),bbox_inches='tight')
    fig.savefig(CACHE/(name+'.png'),dpi=160,bbox_inches='tight');plt.close(fig)


def propagate_R(r,Lm,d):
    # Isolated-channel self-flux ratio at the SAME reference plane on both legs.
    edge=r['backward_reflection_self_power']*np.exp(2*(r['incident_K'].imag-r['backward_K'].imag)*r['reference_distance_m']/d)
    return float(edge*np.exp(2*(r['backward_K'].imag-r['incident_K'].imag)*Lm/d))


def main():
    start=time.time();checks=[]
    def check(name,value,limit,relation='le'):
        ok=bool(value<=limit if relation=='le' else value>=limit)
        checks.append(dict(name=name,value=float(value),relation=relation,limit=float(limit),passed=ok))
        if not ok:raise RuntimeError(f'{name}: {value} {relation} {limit} failed')
    p0=Plate(degree=DEGREE)
    curves={};models={};modes={};disp=[]
    for eta in ETAS:
        p=Plate(degree=DEGREE,H=eta*HCRIT);models[eta]=p;m=p.cutoff();rows=[];saved=[]
        for K in np.linspace(0,1.2,61):
            m=p.temporal(K,m);saved.append(m)
            row=dict(eta=eta,K=float(K),frequency_Hz=float(m['omega'].real*p.fscale),
                temporal_HWHM_Hz=float(-m['omega'].imag*p.fscale),
                power_FWHM_Hz=float(-2*m['omega'].imag*p.fscale),
                mass_MAC=m['MAC'],maximum_generator_growth=m['maximum_growth'])
            rows.append(row);disp.append(row)
        curves[eta]=rows;modes[eta]=saved
        check(f'MAC eta={eta}',min(r['mass_MAC'] for r in rows),.999,relation='ge')
        check(f'growth eta={eta}',max(r['maximum_generator_growth'] for r in rows),1e-8)
        print(f'dispersion H/H*={eta:+.2f} traced',flush=True)
    ref=modes[0.][25]
    optimum=minimize_scalar(lambda K:p0.temporal(K,ref)['omega'].real,
                            bounds=(.35,.75),method='bounded',options={'xatol':1e-10})
    kmin=float(optimum.x);omin=float(optimum.fun);ocut=modes[0.][0]['omega'].real
    omega=(omin+ocut)/2
    raw,_,_=p0.waves(0,omega)
    wi=min([w for w in raw if w['power']>0],key=lambda w:abs(w['K']-.75))
    wb=min([w for w in raw if w['power']<0],key=lambda w:abs(w['K']-.28))
    ky=float(wi['K'].real*np.sin(np.radians(10)))
    ig=np.sqrt(wi['K']**2-ky**2);bg=np.sqrt(wb['K']**2-ky**2)
    protocol=dict(degree=DEGREE,d_m=p0.d,n0_m3=p0.n0,mobility=p0.mobility,
        diffusivity=p0.diffusivity,ell_m=p0.ell_SI,synthetic_f3333_C_per_m=p0.flexo_SI,
        synthetic_Hstar_J_m=HCRIT,Hstar_reference_n_m3=1e19,
        omega_real=omega,frequency_Hz=omega*p0.fscale,ky_real=ky,
        baseline_cutoff_omega=ocut,baseline_minimum_omega=omin,baseline_Kmin=kmin,
        reference_distance_m=10*p0.d,electrical='ideal grounded all faces and edge',
        carriers='blocking all faces and edge',mechanical='free, including weak corner line forces',
        source_status='Wei structural reference only; full baseline reproduction unavailable',
        coefficient_status='A, f, H synthetic; not calibrated ZnO constants',
        scope='static/local, quasistatic electrical, carrier loss only')
    dump('protocol.json',protocol)
    primary=[];solutions={};weak=[];independent=[];temporal_checks=[]
    for eta in ETAS:
        p=models[eta];r,s=p.edge(ky,omega,ig,bg);primary.append(r);solutions[eta]=s
        check(f'edge rank eta={eta}',r['edge_rank'],r['edge_size'],relation='ge')
        check(f'negative channel eta={eta}',r['negative_direction'],1,relation='ge')
        check(f'edge residual eta={eta}',r['edge_scaled_residual'],1e-10)
        check(f'control volume power eta={eta}',r['power_balance_relative'],1e-8)
        check(f'edge power eta={eta}',abs(r['edge_power']),1e-10)
        for port in ['incident','backward']:
            d=r[port]
            check(f'positive energy {port} eta={eta}',d['energy'],0,relation='ge')
            check(f'modal power {port} eta={eta}',d['balance'],2e-6)
            for field in ['momentum','gauss','carrier','traction','double_traction','blocking']:
                check(f'{field} {port} eta={eta}',d[field],1e-8)
            K=np.sqrt(r[port+'_K']**2+ky**2)
            exact=gradient_strong_root(p,omega=omega,guess=K)
            delta=abs(exact-K)
            independent.append(dict(eta=eta,kind='spatial_'+port,K_real=K.real,K_imag=K.imag,
                delta_dimensionless=delta,frequency_error_Hz=0.))
            check(f'12 state {port} eta={eta}',delta,1e-9)
        K=abs(wb['K'].real);m=p.temporal(K,modes[eta][14]);root=gradient_strong_root(p,K=K,guess=m['omega'])
        independent.append(dict(eta=eta,kind='temporal',K_real=K,K_imag=0.,
            delta_dimensionless=abs(root-m['omega']),frequency_error_Hz=abs(root-m['omega'])*p.fscale))
        check(f'12 state frequency eta={eta}',abs(root-m['omega'])*p.fscale,1.)
        tb=temporal_energy_balance(p,K,m);tb['eta']=eta;temporal_checks.append(tb)
        check(f'temporal energy balance eta={eta}',tb['relative_balance'],5e-6)
        e=edge_field_residuals(p,omega,ky,s)
        e={k:v for k,v in e.items() if np.isscalar(v)};e['eta']=eta;weak.append(e)
        check(f'independent edge weak force eta={eta}',e['independent_weak_mechanical'],1e-9)
        print(f'edge eta={eta:+.2f}: Rb(2um)={r["backward_reflection_self_power"]:.9f}, angle={r["reflected_angle_deg"]:.5f}',flush=True)
    table('independent_roots.csv',independent);table('edge_weak_residuals.csv',weak)
    table('temporal_energy_balance.csv',temporal_checks)
    dump('primary_edge.json',primary)

    # Classical limit: separate eight-state propagator, both electrical face laws.
    classical=[]
    for electric in ['ground','open']:
        pc=Plate(degree=DEGREE,ell=0,flexo=0,electric=electric)
        candidates=pc.temporal(.1)
        m=min([a for a in candidates if a['omega'].real>1 and
            np.vdot(a['U'][2*pc.n:],pc.W@a['U'][2*pc.n:]).real>.85],key=lambda a:a['omega'].real)
        for K in [.3,.7,1.]:
            m=pc.temporal(K,m);root=classical_strong_root(pc,K,m['omega'],electric)
            error=abs(root-m['omega'])*pc.fscale
            classical.append(dict(electric=electric,K=K,frequency_Hz=m['omega'].real*pc.fscale,
                FWHM_Hz=-2*m['omega'].imag*pc.fscale,error_Hz=error))
            check(f'classical eight-state {electric} K={K}',error,1.)
    table('classical_validation.csv',classical)

    # Resolution checks at fixed physical drive and ky, never retuned per H.
    conv=[]
    for eta in ETAS:
        previous=None
        for degree in [14,18,22,26]:
            p=Plate(degree=degree,H=eta*HCRIT);r,s=p.edge(ky,omega,ig,bg)
            conv.append(dict(method='Legendre',resolution=degree,eta=eta,
                R_B=r['backward_reflection_self_power'],K_B_real=r['backward_K'].real,
                K_B_imag=r['backward_K'].imag,power_error=r['power_balance_relative']))
            if previous and degree==26:
                check(f'degree R convergence eta={eta}',abs(r['backward_reflection_self_power']-previous),1e-7)
            previous=r['backward_reflection_self_power']
        for elements in ([8,16,24,32] if eta==0 else [32]):
            p=MeshPlate(elements=elements,H=eta*HCRIT);r,s=p.edge(ky,omega,ig,bg)
            conv.append(dict(method='C1 cubic Hermite',resolution=elements,eta=eta,
                R_B=r['backward_reflection_self_power'],K_B_real=r['backward_K'].real,
                K_B_imag=r['backward_K'].imag,power_error=r['power_balance_relative']))
            if elements==32:
                target=primary[ETAS.index(eta)]['backward_reflection_self_power']
                check(f'independent mesh R eta={eta}',abs(r['backward_reflection_self_power']-target),5e-6)
                check(f'independent mesh energy eta={eta}',r['power_balance_relative'],2e-7)
        print(f'convergence eta={eta:+.2f} done',flush=True)
    table('convergence.csv',conv)

    # Matched frequency and H effects. Same drive/ky across H at every abscissa.
    frequency=[]
    for frac in np.linspace(.23,.8,13):
        om=omin+frac*(ocut-omin)
        for eta in ETAS:
            p=models[eta];r,_=p.edge(ky,om,ig,bg)
            check(f'frequency scan direction {frac:.4f} eta={eta}',r['negative_direction'],1,relation='ge')
            frequency.append(dict(eta=eta,frequency_Hz=om*p.fscale,R_B=r['backward_reflection_self_power'],
                R_B_at_100um=propagate_R(r,100e-6,p.d),angle_deg=r['reflected_angle_deg'],
                power_balance_error=r['power_balance_relative']))
    table('frequency_scan.csv',frequency)
    sensitivity=[];sweep_directions=[]
    for eta in np.linspace(-.05,.05,21):
        p=Plate(degree=DEGREE,H=eta*HCRIT);r,_=p.edge(ky,omega,ig,bg)
        sweep_directions.append(r['negative_direction'])
        m=p.temporal(wb['K'].real,modes[0.][14])
        sensitivity.append(dict(eta=float(eta),H_J_m=float(eta*HCRIT),R_B_edge=propagate_R(r,0,p.d),
            R_B_2um=r['backward_reflection_self_power'],R_B_100um=propagate_R(r,100e-6,p.d),
            L_E_incident_m=p.d/(2*r['incident_K'].imag),L_E_backward_m=p.d/(2*abs(r['backward_K'].imag)),
            temporal_frequency_Hz=m['omega'].real*p.fscale,temporal_FWHM_Hz=-2*m['omega'].imag*p.fscale,
            angle_deg=r['reflected_angle_deg'],power_balance_error=r['power_balance_relative']))
    table('H_sensitivity.csv',sensitivity);table('dispersion.csv',disp)
    check('all matched sweeps control-volume power',max(r['power_balance_error'] for r in frequency+sensitivity),1e-8)
    check('all H sweep negative directions',min(sweep_directions),1,relation='ge')
    check('no gain backward self-flux in matched sweeps',max([r['R_B'] for r in frequency]+[r['R_B_2um'] for r in sensitivity]),1.)
    print('matched parameter curves done',flush=True)

    # A real solved angular spectrum, not an assumed reflected ray diagram.
    beam_metrics=[];beam_image=None
    x=np.linspace(-60e-6,0,191);y=np.linspace(-60e-6,20e-6,201)
    XX,YY=np.meshgrid(x/p0.d,y/p0.d)
    for nodes in [17,25]:
        t,w=hermgauss(nodes);kys=ky+np.sqrt(2)*.013*t;weights=w/np.sqrt(np.pi)
        ui=[];ub=[];kis=[];kbs=[];Rs=[]
        bz,_=p0.basis(np.array([.25]),0)
        for kval,weight in zip(kys,weights):
            r,s=p0.edge(float(kval),omega,ig,bg)
            ib=s['index_backward'];q=s['incident']['q']
            phase=np.exp(-1j*np.angle((bz[0]@q[2*p0.n:3*p0.n])[0]))
            ui.append(q[:p0.nu]*phase*weight)
            ub.append(s['Y'][:p0.nu,ib]*s['amplitudes'][ib]*phase*weight)
            kis.append(r['incident_K']);kbs.append(r['backward_K']);Rs.append(r['backward_reflection_self_power'])
        images=[]
        for U,K in [(np.array(ui).T,np.array(kis)),(np.array(ub).T,np.array(kbs))]:
            E=np.exp(1j*(K[:,None,None]*XX[None,:,:]+kys[:,None,None]*YY[None,:,:])).reshape(nodes,-1)
            gram=U.conj().T@p0.M@U
            intensity=np.sum(E.conj()*(gram@E),axis=0).real.reshape(XX.shape)
            images.append(np.maximum(intensity,0))
        j=int(np.argmin(abs(x+40e-6)))
        centroids=[float(np.sum(y*im[:,j])/np.sum(im[:,j])) for im in images]
        beam_metrics.append(dict(nodes=nodes,x_m=float(x[j]),incident_centroid_y_m=centroids[0],
            backward_centroid_y_m=centroids[1],minimum_sampled_R=float(min(Rs)),maximum_sampled_R=float(max(Rs))))
        if nodes==25:beam_image=images
    check('beam backward centroid quadrature convergence m',
          abs(beam_metrics[1]['backward_centroid_y_m']-beam_metrics[0]['backward_centroid_y_m']),1e-7)
    check('beam backward centroid negative',-beam_metrics[1]['backward_centroid_y_m'],1e-5,relation='ge')
    dump('beam_validation.json',beam_metrics)
    print('computed backward-channel beam done',flush=True)

    # Numerical plots. Every line is a calculated matched comparison.
    fig,ax=plt.subplots(1,3,figsize=(12,3.45),layout='constrained')
    f0=np.array([r['frequency_Hz'] for r in curves[0.]])
    for eta in ETAS:
        rows=curves[eta];K=[r['K'] for r in rows];f=np.array([r['frequency_Hz'] for r in rows])
        kw=dict(color=COLORS[eta],label=LABELS[eta],lw=1.9,ls='-' if eta==0 else '--')
        ax[0].plot(K,f/1e9,**kw);ax[1].plot(K,(f-f0)/1e3,**kw)
        ax[2].plot(K,np.array([r['power_FWHM_Hz'] for r in rows])/1e3,**kw)
    ax[0].axhline(omega*p0.fscale/1e9,color='#9aaab5',lw=1,ls=':');ax[0].legend(fontsize=8)
    for a in ax:a.set_xlabel('K = |k∥| d');a.grid(alpha=.15)
    ax[0].set_ylabel('Frequency (GHz)');ax[1].set_ylabel('Matched frequency shift (kHz)');ax[2].set_ylabel('Temporal power FWHM (kHz)')
    ax[0].set_title('(a) Tracked guided family');ax[1].set_title('(b) H effect, same K');ax[2].set_title('(c) Carrier damping, same K')
    savefig('dispersion_and_H',fig)

    fig,ax=plt.subplots(1,3,figsize=(12,3.5),layout='constrained')
    for eta in ETAS:
        rows=[r for r in frequency if r['eta']==eta];f=np.array([r['frequency_Hz'] for r in rows])/1e9
        kw=dict(color=COLORS[eta],label=LABELS[eta],lw=1.8)
        ax[0].plot(f,100*np.array([r['R_B'] for r in rows]),**kw)
        ax[1].plot(f,100*np.array([r['R_B_at_100um'] for r in rows]),**kw)
        ax[2].plot(f,[r['angle_deg'] for r in rows],**kw)
    ax[0].legend(fontsize=8)
    for a in ax:
        a.set_xlabel('Common drive frequency (GHz)');a.grid(alpha=.15)
        a.xaxis.set_major_locator(MaxNLocator(nbins=4,steps=[1,2,5,10]))
        a.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    ax[0].set_ylabel('Backward self-flux / incident (%)');ax[1].set_ylabel('Backward self-flux / incident (%)');ax[2].set_ylabel('Signed reflected energy angle (deg)')
    ax[0].set_title('(a) Reference plane 2 µm from edge');ax[1].set_title('(b) Reference plane 100 µm from edge');ax[2].set_title('(c) Negative angle, fixed real ky')
    savefig('edge_conversion',fig)

    fig,ax=plt.subplots(1,3,figsize=(12,3.5),layout='constrained')
    ee=np.array([r['eta'] for r in sensitivity])
    for key,label,color in [('R_B_edge','Edge channel self-flux','#8b9ba5'),('R_B_2um','2 µm reference','#155e75'),('R_B_100um','100 µm reference','#cc642f')]:
        ax[0].plot(ee,100*np.array([r[key] for r in sensitivity]),label=label,color=color,lw=1.9)
    for key,label,ls in [('L_E_incident_m','Incident','--'),('L_E_backward_m','Backward','-')]:
        ax[1].semilogy(ee,np.array([r[key] for r in sensitivity])*1e6,label=label,color='#155e75' if ls=='-' else '#16806a',ls=ls,lw=1.9)
    ax[2].plot(ee,np.array([r['temporal_FWHM_Hz'] for r in sensitivity])/1e3,color='#cc642f',lw=1.9)
    for a in ax:a.set_xlabel('Synthetic H333 / H*');a.axvline(0,color='#b7c2c9',ls=':',lw=1);a.grid(alpha=.15)
    ax[0].set_ylabel('Backward self-flux / incident (%)');ax[1].set_ylabel('Spatial energy attenuation length (µm)');ax[2].set_ylabel('Temporal power FWHM (kHz)')
    ax[0].legend(fontsize=8);ax[1].legend(fontsize=8)
    ax[0].set_title('(a) Same real drive and ky');ax[1].set_title('(b) Same real drive and ky');ax[2].set_title('(c) Same real K, not a spatial rate')
    savefig('H_parameter_effect',fig)

    fig,ax=plt.subplots(1,2,figsize=(10,4.3),layout='constrained')
    for a,im,title in zip(ax,beam_image,['(a) Computed incident channel','(b) Solved backward reflected channel']):
        norm=im/im.max()
        pic=a.pcolormesh(x*1e6,y*1e6,norm,shading='auto',cmap='magma',vmin=0,vmax=1,rasterized=True)
        a.axvline(0,color='#155e75',lw=2);a.set_xlabel('x (µm), edge at 0');a.set_ylabel('y (µm)');a.set_title(title)
        a.set_aspect('equal');fig.colorbar(pic,ax=a,label='Branch kinetic intensity / own maximum',shrink=.8)
    ax[0].annotate('',xy=(-22,-3.9),xytext=(-42,-7.4),arrowprops=dict(arrowstyle='->',color='#155e75',lw=2.4))
    ax[1].annotate('',xy=(-40,-21),xytext=(-20,-10.5),arrowprops=dict(arrowstyle='->',color='#155e75',lw=2.4))
    ax[1].text(-57,-54,'Energy away from edge; R at 2 µm = 2.31%',color='white',fontsize=8)
    savefig('computed_channel_beam',fig)

    # Compact audit with explicit non-passed NON-numerical requirements.
    audit=dict(numerical_checks=len(checks),passed=sum(r['passed'] for r in checks),checks=checks,
        published_Wei_or_Fang_reproduction='UNVERIFIED: full governing equations not accessible',
        Qu_exact_equivalence='UNRESOLVED: coupling novelty provisional; no absence claim',
        material_calibration='NOT ESTABLISHED: synthetic A/f/H and transferred bulk Hall transport',
        corner_pointwise_stress='NOT CERTIFIED: use converged variational boundary functional',
        numerical_interpretation='Backward edge conversion in specified static/local grounded Galerkin model',
        runtime_seconds=time.time()-start)
    dump('validation.json',audit)
    hashes={str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='sha256.json'}
    for name in ['model.py','run_study.py','test_model.py','__init__.py']:
        path=HERE/name;hashes[str(path.relative_to(HERE.parent))]=hashlib.sha256(path.read_bytes()).hexdigest()
    for name in ['a0/materials.json','a0/requirements.txt']:
        path=HERE.parent/name;hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    dump('sha256.json',hashes)
    print(f'{audit["passed"]}/{audit["numerical_checks"]} checks passed in {audit["runtime_seconds"]:.1f}s',flush=True)


if __name__=='__main__':main()
