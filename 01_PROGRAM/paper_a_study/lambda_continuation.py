"""Phase 03 limiting-case test: follow the operating-point branch from lambda=0.25 to 0.
Run from 01_PROGRAM/paper_a_study:  python3 -I lambda_continuation.py
Temporal modes at fixed ky=KY0, carriers retained, f=H=0, MAC-tracked."""
import sys,csv,numpy as np
sys.path.insert(0,'.')
from model import Plate
KY0=0.12981175031447484; K0=0.7361990195318475; OM0=7.633372404423294
def plate(lam,deg=18): return Plate(deg,ell=lam*200e-9,flexo=0.0)
def scan(p,ref,ks,center):
    d={}
    for order in ([k for k in ks if k>=center],[k for k in ks if k<center][::-1]):
        r=ref
        for K in order:
            r=p.temporal(K,reference=r,ky=KY0);d[float(K)]=(r['omega'].real,r['MAC'])
    kk=np.array(sorted(d));return kk,np.array([d[k][0] for k in kk]),min(v[1] for v in d.values())
def run(lams=(0.25,0.2,0.15,0.1,0.05,0.0),deg=18):
    path=np.linspace(0.25,0.0,26)
    p=plate(path[0],deg);ref=min(p.temporal(K0,ky=KY0),key=lambda m:abs(m['omega'].real-OM0))
    chain={}
    for lam in path:
        r=plate(lam,deg).temporal(K0,reference=ref,ky=KY0);chain[round(lam,4)]=r['omega'].real;ref=r
    rows=[]
    for lam in lams:
        p=plate(lam,deg);ms=p.temporal(K0,ky=KY0)
        ref=min(ms,key=lambda m:abs(m['omega'].real-chain[round(lam,4)]))
        kk,om,mac=scan(p,ref,np.linspace(0.15,1.25,111),K0)
        g=np.gradient(om,kk)
        # upper zero crossing of the group velocity (the zero-group-velocity point)
        idx=[i for i in range(len(kk)-1) if g[i]<0<=g[i+1]]
        kz=oz=None
        if idx:
            i=idx[-1];t=-g[i]/(g[i+1]-g[i]);kz=kk[i]+t*(kk[i+1]-kk[i]);oz=om[i]+t*(om[i+1]-om[i])
        rows.append(dict(lam=lam,Omega_K0=float(om[np.argmin(abs(kk-K0))]),min_group=float(g.min()),K_min_group=float(kk[g.argmin()]),K_zgv=kz,Omega_zgv=oz,min_MAC=float(mac),degree=deg))
    return rows
if __name__=='__main__':
    deg=int(sys.argv[1]) if len(sys.argv)>1 else 18
    rows=run(deg=deg)
    for r in rows:print({k:(round(v,4) if isinstance(v,float) else v) for k,v in r.items()})
    with open(f'lambda_continuation_deg{deg}.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
