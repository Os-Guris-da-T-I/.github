#!/usr/bin/env python3
"""
Gera os GIFs animados (carmesim / japonês) em assets/*.gif.
Cada cena é desenhada num <canvas> (Chromium via playwright), frame a frame, em loop perfeito,
e montada com ffmpeg (paleta otimizada).

Uso:   python3 tools/gifs.py            # todos
       python3 tools/gifs.py slash      # só um (sakura | slash | rain | torii)
Precisa de: playwright (chromium) + ffmpeg.
"""
import os, subprocess, sys, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets")

SCENES = {            # name: (width, height, loop seconds, fps)
    "sakura": (1000, 300, 6, 12),
    "slash":  (1000, 120, 3, 15),
    "rain":   (1000, 230, 4, 12),
    "torii":  (1000, 330, 6, 12),
}

HTML = r"""<!doctype html><meta charset=utf-8>
<style>
@font-face{font-family:'GD';font-weight:700;src:url('fonts/Outfit-Bold.ttf')}
@font-face{font-family:'GD';font-weight:400;src:url('fonts/Outfit-Regular.ttf')}
@font-face{font-family:'GJ';font-weight:700;src:url('fonts/kanji-subset.otf')}
@font-face{font-family:'GM';font-weight:400;src:url('fonts/JetBrainsMono-Regular.ttf')}
body{margin:0;background:#000}canvas{display:block}
</style><canvas id=c></canvas>
<script>
const TAU=Math.PI*2, fract=x=>x-Math.floor(x);
function rng(s){return()=>{s|=0;s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
let cv,ctx,W,H;
const PET=new Path2D("M0 0C-5.5-3-6.5-10.5-2.4-13.2L0-11L2.4-13.2C6.5-10.5 5.5-3 0 0Z");
const FUJI=new Path2D("M-230 0C-150-6-100-60-40-108Q0-122 40-108C100-60 150-6 230 0Z");
const CAP=new Path2D("M-40-108L-75-79L-58-84L-48-76L-36-90L-24-78L-10-92L2-80L14-92L26-78L38-90L48-76L58-84L75-79L40-108Q0-122-40-108Z");
function vgrad(stops,y0=0,y1=H){const g=ctx.createLinearGradient(0,y0,0,y1);stops.forEach(([o,c])=>g.addColorStop(o,c));return g}
function shippo(){const t=document.createElement('canvas');t.width=t.height=36;const x=t.getContext('2d');x.strokeStyle='rgba(255,59,87,.09)';x.lineWidth=1;
 for(const [a,b] of [[0,0],[36,0],[0,36],[36,36],[18,18]]){x.beginPath();x.arc(a,b,18,0,TAU);x.stroke()}
 ctx.fillStyle=ctx.createPattern(t,'repeat');ctx.fillRect(0,0,W,H)}
function sunRays(cx,cy,r,t,alpha=.3,len=2.6){const n=24;ctx.save();ctx.translate(cx,cy);ctx.rotate(t*TAU/n);
 const g=ctx.createRadialGradient(0,0,r,0,0,r*len);g.addColorStop(0,`rgba(255,59,87,${alpha})`);g.addColorStop(1,'rgba(255,59,87,0)');ctx.fillStyle=g;
 for(let i=0;i<n;i++){const a0=(i*360/n-3.2)*Math.PI/180,a1=(i*360/n+3.2)*Math.PI/180;ctx.beginPath();
  ctx.moveTo(r*1.05*Math.cos(a0),r*1.05*Math.sin(a0));ctx.lineTo(r*len*Math.cos(a0),r*len*Math.sin(a0));ctx.lineTo(r*len*Math.cos(a1),r*len*Math.sin(a1));ctx.lineTo(r*1.05*Math.cos(a1),r*1.05*Math.sin(a1));ctx.fill()}ctx.restore()}
function sun(cx,cy,r,t,a=1){ctx.save();ctx.globalAlpha=a;const rr=r*(1+.018*Math.sin(t*TAU));
 let g=ctx.createRadialGradient(cx,cy,r*.5,cx,cy,r*1.6);g.addColorStop(0,'rgba(255,42,69,.4)');g.addColorStop(1,'rgba(255,42,69,0)');ctx.fillStyle=g;ctx.beginPath();ctx.arc(cx,cy,r*1.6,0,TAU);ctx.fill();
 g=ctx.createRadialGradient(cx,cy,0,cx,cy,rr);g.addColorStop(0,'#ff5a6e');g.addColorStop(.7,'#e01a3c');g.addColorStop(1,'#b30f2b');ctx.fillStyle=g;ctx.beginPath();ctx.arc(cx,cy,rr,0,TAU);ctx.fill();ctx.restore()}
function fuji(cx,by,sc,fill,snow='rgba(255,226,230,.9)'){ctx.save();ctx.translate(cx,by);ctx.scale(sc,sc);ctx.fillStyle=fill;ctx.fill(FUJI);
 ctx.strokeStyle='rgba(255,179,185,.18)';ctx.lineWidth=1.2;ctx.stroke(FUJI);ctx.fillStyle=snow;ctx.fill(CAP);ctx.restore()}
function torii(cx,by,sc,fill,accent){ctx.save();ctx.translate(cx,by);ctx.scale(sc,sc);ctx.fillStyle=fill;
 ctx.beginPath();ctx.moveTo(-70,-98);ctx.quadraticCurveTo(0,-82,70,-98);ctx.lineTo(66,-86);ctx.quadraticCurveTo(0,-72,-66,-86);ctx.closePath();ctx.fill();
 ctx.strokeStyle=accent;ctx.lineWidth=1.4/1;ctx.beginPath();ctx.moveTo(-70,-98);ctx.quadraticCurveTo(0,-82,70,-98);ctx.stroke();
 ctx.fillRect(-58,-84,116,6);ctx.fillRect(-50,-66,100,8);ctx.fillRect(-42,-80,10,80);ctx.fillRect(32,-80,10,80);ctx.fillRect(-3,-82,6,16);ctx.restore()}
function waves(y,R,rows,t,c0,c1,ring='rgba(255,214,214,.28)'){const mix=(a,b,k)=>a.map((v,i)=>Math.round(v+(b[i]-v)*k));
 const h=s=>[1,3,5].map(i=>parseInt(s.slice(i,i+2),16));const A=h(c0),B=h(c1);const sh=-(t%1)*2*R;
 for(let r=0;r<rows;r++){const k=r/Math.max(1,rows-1);const col=mix(A,B,k);const cy=y+R*.5*r+R*.5;const off=(r%2?R:0)+sh;
  for(let c=-2;c<W/(2*R)+3;c++){const cx=c*2*R+off;ctx.fillStyle=`rgb(${col})`;ctx.strokeStyle=ring;ctx.lineWidth=1;ctx.beginPath();ctx.arc(cx,cy,R,0,TAU);ctx.fill();ctx.stroke();
   for(const f of [.7,.42]){ctx.beginPath();ctx.arc(cx,cy,R*f,0,TAU);ctx.stroke()}}}}
function petals(t,n,seed,{k=[1,2],wind=140,sz=[.7,1.3],cols=['#ffc2cc','#ff8fa3','#ffd9df','#ff6b82'],a=.9,y0=-30,y1=H+30}={}){
 const r=rng(seed);for(let i=0;i<n;i++){const x0=r()*W,kk=k[Math.floor(r()*k.length)],off=r(),amp=20+r()*40,sc=sz[0]+r()*(sz[1]-sz[0]),col=cols[Math.floor(r()*cols.length)],rk=(1+Math.floor(r()*2))*(r()<.5?-1:1),ro=r()*TAU;
  const p=fract(t*kk+off);const y=y0+p*(y1-y0);let x=x0+wind*p+Math.sin(TAU*(t*kk*2+off))*amp;x=((x%(W+80))+(W+80))%(W+80)-40;
  const fade=Math.min(1,p*8,(1-p)*8);ctx.save();ctx.globalAlpha=a*fade;ctx.translate(x,y);ctx.rotate(ro+TAU*t*rk);ctx.scale(sc*1.4,sc*1.4*(.55+.45*Math.cos(TAU*(t*2*kk+off))));ctx.fillStyle=col;ctx.fill(PET);ctx.restore()}}
function embers(t,n,seed,y0=H,y1=0){const r=rng(seed);for(let i=0;i<n;i++){const x0=r()*W,kk=1+Math.floor(r()*2),off=r(),rad=.8+r()*1.8,drift=(r()-.5)*60;const p=fract(t*kk+off);
  ctx.globalAlpha=Math.sin(Math.PI*p)*.9;ctx.fillStyle=['#ff3b57','#ff7a5c','#ffb3b9'][i%3];ctx.beginPath();ctx.arc(x0+drift*p,y0+(y1-y0)*p,rad,0,TAU);ctx.fill()}ctx.globalAlpha=1}
function txt(s,x,y,font,fill,{align='center',track=0,glow=0,gc='rgba(255,59,87,.9)',a=1}={}){ctx.save();ctx.globalAlpha=a;ctx.font=font;ctx.textAlign=align;ctx.letterSpacing=track+'px';ctx.fillStyle=fill;
 if(glow){ctx.shadowColor=gc;ctx.shadowBlur=glow}ctx.fillText(s,x+track/2,y);ctx.restore()}
function lantern(x,top,h,t,ph,ch='玄'){const ang=Math.sin(TAU*t+ph)*.1;ctx.save();ctx.translate(x,top);ctx.rotate(ang);
 ctx.strokeStyle='#7a2c38';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(0,-400);ctx.lineTo(0,16);ctx.stroke();
 const w=h*.78,cy=16+h/2;let g=ctx.createRadialGradient(0,cy,0,0,cy,h*1.0);g.addColorStop(0,`rgba(255,59,87,${.4+.15*Math.sin(TAU*t*2+ph)})`);g.addColorStop(1,'rgba(255,59,87,0)');ctx.fillStyle=g;ctx.beginPath();ctx.arc(0,cy,h*1.0,0,TAU);ctx.fill();
 ctx.fillStyle='#1d0409';ctx.strokeStyle='rgba(240,194,123,.6)';ctx.lineWidth=.8;ctx.fillRect(-w*.3,12,w*.6,6);ctx.strokeRect(-w*.3,12,w*.6,6);
 g=ctx.createLinearGradient(-w/2,0,w/2,0);g.addColorStop(0,'#a50f2a');g.addColorStop(.45,'#ff4560');g.addColorStop(1,'#9c0e27');ctx.fillStyle=g;ctx.beginPath();ctx.ellipse(0,cy,w/2,h/2,0,0,TAU);ctx.fill();
 ctx.strokeStyle='rgba(107,13,29,.75)';for(const k of [.18,.34,.5,.66,.82]){ctx.beginPath();ctx.moveTo(-w/2+1,16+h*k);ctx.quadraticCurveTo(0,16+h*k+4,w/2-1,16+h*k);ctx.stroke()}
 ctx.fillStyle='#1d0409';ctx.fillRect(-w*.3,16+h-2,w*.6,6);ctx.strokeStyle='#f0c27b';ctx.beginPath();ctx.moveTo(0,16+h+4);ctx.lineTo(0,16+h+14);ctx.stroke();ctx.fillStyle='#f0c27b';ctx.beginPath();ctx.arc(0,16+h+16,1.8,0,TAU);ctx.fill();
 txt(ch,0,cy+h*.17,`700 ${h*.5}px GJ`,'rgba(255,243,239,.93)');ctx.restore()}
function frame_border(){ctx.strokeStyle='rgba(255,59,87,.55)';ctx.lineWidth=1.2;ctx.strokeRect(.5,.5,W-1,H-1);ctx.strokeStyle='rgba(255,59,87,.16)';ctx.lineWidth=1;ctx.strokeRect(6.5,6.5,W-13,H-13);
 ctx.strokeStyle='rgba(255,59,87,.75)';ctx.lineWidth=1.4;const i=12,l=18;ctx.beginPath();
 ctx.moveTo(i,i+l);ctx.lineTo(i,i);ctx.lineTo(i+l,i);ctx.moveTo(W-i-l,i);ctx.lineTo(W-i,i);ctx.lineTo(W-i,i+l);ctx.moveTo(W-i,H-i-l);ctx.lineTo(W-i,H-i);ctx.lineTo(W-i-l,H-i);ctx.moveTo(i+l,H-i);ctx.lineTo(i,H-i);ctx.lineTo(i,H-i-l);ctx.stroke()}
function vignette(){const g=ctx.createRadialGradient(W/2,H/2,H*.4,W/2,H/2,W*.62);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(10,1,5,.45)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H)}

const SC={
 sakura(t){
  ctx.fillStyle=vgrad([[0,'#12020a'],[.55,'#4a0a18'],[1,'#b3162f']]);ctx.fillRect(0,0,W,H);shippo();
  sunRays(500,150,95,t,.34);sun(500,150,95,t,.9);
  fuji(170,H-14,1.0,'#7a1830');fuji(840,H-14,.9,'#7a1830');fuji(80,H-8,1.05,'#5c0f22');fuji(930,H-8,1.0,'#4e0c1d');
  torii(310,H-6,.7,'#1d0409','#ff3b57');torii(700,H-6,.7,'#1d0409','#ff3b57');
  waves(H-42,20,3,t,'#b3162f','#3a0a15');
  embers(t,22,7);
  const pulse=.75+.25*Math.sin(TAU*t);
  txt('学ぶ・創る・分かち合う',500,148,'700 44px GJ','#fff3ef',{track:10,glow:22*pulse});
  txt('APRENDA. CONSTRUA. COMPARTILHE.',500,186,'700 17px GD','#ffd6d6',{track:7});
  petals(t,26,3,{wind:260});
  vignette();frame_border()},
 slash(t){
  ctx.fillStyle=vgrad([[0,'#1d0409'],[1,'#5a0b1b']]);ctx.fillRect(0,0,W,H);shippo();
  const y=H/2,P=.34,head=-80+(W+160)*Math.min(1,t/P),inS=t<P;
  ctx.strokeStyle='rgba(255,59,87,.22)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();
  const cutA=t<P?1:Math.max(0,1-(t-P)/.5);
  if(t>0){ctx.save();ctx.globalAlpha=cutA;const g=ctx.createLinearGradient(0,0,Math.max(head,1),0);g.addColorStop(0,'rgba(255,59,87,0)');g.addColorStop(1,'rgba(255,230,232,1)');
   ctx.strokeStyle=g;ctx.lineWidth=2.2;ctx.shadowColor='#ff3b57';ctx.shadowBlur=18;ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(Math.min(head,W),y);ctx.stroke();ctx.restore()}
  if(inS||t<P+.06){ctx.save();ctx.translate(head,y);ctx.rotate(-.5);const g=ctx.createLinearGradient(-90,0,30,0);g.addColorStop(0,'rgba(255,59,87,0)');g.addColorStop(.8,'rgba(255,255,255,.95)');g.addColorStop(1,'rgba(255,255,255,0)');
   ctx.fillStyle=g;ctx.shadowColor='#ff3b57';ctx.shadowBlur=24;ctx.fillRect(-90,-2,120,4);ctx.restore()}
  const r=rng(11);for(let i=0;i<30;i++){const b=r()*P,vx=(r()-.3)*160,vy=(r()-.5)*220,life=.4+r()*.3;const age=t-b;if(age>0&&age<life){const bx=-80+(W+160)*(b/P);
   const px=bx+vx*age,py=y+vy*age+260*age*age;ctx.globalAlpha=1-age/life;ctx.fillStyle=i%2?'#ffb3b9':'#ff3b57';ctx.beginPath();ctx.arc(px,py,1+r()*1.6,0,TAU);ctx.fill();ctx.globalAlpha=1}}
  const ta=t<P?0:(t<P+.08?(t-P)/.08:Math.max(0,1-(t-.6)/.35));
  const flick=1-.25*(Math.sin(t*90)>.6?1:0)*(t<P+.2?1:0);
  if(ta>0){txt('継続は力なり',500,y+14,'700 40px GJ','#fff3ef',{track:16,glow:26,a:Math.min(1,ta)*flick});
   txt('PERSISTÊNCIA É PODER',500,y+40,'700 12px GD','#ff8fa3',{track:9,a:Math.min(1,ta)*.9})}
  petals(t,6,5,{wind:100,sz:[.5,.8],y0:-20,y1:H+20});frame_border()},
 rain(t){
  ctx.fillStyle=vgrad([[0,'#12020a'],[1,'#4a0a18']]);ctx.fillRect(0,0,W,H);
  const chars='アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン技学創道心力夢侍刀日月本玄01'.split('');
  const colw=16,cols=Math.floor(W/colw),r=rng(21);ctx.font='700 15px GJ';ctx.textAlign='center';
  for(let c=0;c<cols;c++){const k=1+Math.floor(r()*2),off=r(),len=8+Math.floor(r()*12),step=Math.floor(r()*1000);const p=fract(t*k*.5+off);const headY=p*(H+len*16)-len*8;
   for(let j=0;j<len;j++){const yy=headY-j*16;if(yy<-16||yy>H+16)continue;const idx=(step+j*7+Math.floor(t*12)*(j%3+1))%chars.length;const a=Math.pow(1-j/len,1.6);
    ctx.fillStyle=j===0?`rgba(255,230,232,${a})`:`rgba(255,59,87,${a*.8})`;if(j===0){ctx.shadowColor='#ff3b57';ctx.shadowBlur=12}ctx.fillText(chars[idx],c*colw+colw/2,yy);ctx.shadowBlur=0}}
  const g=ctx.createRadialGradient(W/2,H/2,60,W/2,H/2,330);g.addColorStop(0,'rgba(18,2,10,.93)');g.addColorStop(.6,'rgba(18,2,10,.72)');g.addColorStop(1,'rgba(18,2,10,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  txt('技術',500,92,'700 18px GJ','#ff3b57',{track:14});
  txt('ENSINANDO T.I. PRO BRASIL INTEIRO',500,132,'700 31px GD','#fff3ef',{track:5,glow:14*(.7+.3*Math.sin(TAU*t))});
  txt('ブラジル全土にITを無料で',500,166,'700 17px GJ','#ffd6d6',{track:8});
  ctx.fillStyle='#ff3b57';if(Math.floor(t*4)%2===0)ctx.fillRect(500+ctx.measureText('').width,0,0,0);
  embers(t,14,9);frame_border()},
 torii(t){
  ctx.fillStyle=vgrad([[0,'#0c0105'],[.6,'#3a0914'],[1,'#7a1226']]);ctx.fillRect(0,0,W,H);shippo();
  const wl=238;sunRays(500,120,70,t,.22,3);sun(500,128,70,t,.75);
  fuji(150,wl,1.05,'#5c0f22');fuji(860,wl,.95,'#4e0c1d');
  for(let i=0;i<3;i++){const sh=(t*(i+1)*W)%W;ctx.globalAlpha=.10+.04*i;const g=ctx.createLinearGradient(0,0,W,0);g.addColorStop(0,'rgba(255,179,185,0)');g.addColorStop(.5,'rgba(255,179,185,1)');g.addColorStop(1,'rgba(255,179,185,0)');ctx.fillStyle=g;
   for(const s of [sh-W,sh])ctx.fillRect(s,wl-70-i*34,W,26);ctx.globalAlpha=1}
  const gl=.55+.25*Math.sin(TAU*t);ctx.save();ctx.shadowColor='#ff3b57';ctx.shadowBlur=30*gl;torii(500,wl,2.15,'#240409','#ff5a6e');ctx.restore();
  for(const [x,ph,h] of [[190,0,50],[330,1.5,38],[670,3,38],[810,4.5,50]])lantern(x,12,h,t,ph);
  ctx.fillStyle=vgrad([[0,'#4a0a18'],[1,'#12020a']],wl,H);ctx.fillRect(0,wl,W,H-wl);
  ctx.save();ctx.beginPath();ctx.rect(0,wl,W,H-wl);ctx.clip();ctx.globalAlpha=.22;ctx.translate(500,wl);ctx.scale(1,-.55);ctx.translate(-500,-0);
  ctx.save();ctx.translate(500,0);ctx.scale(2.15,2.15);ctx.fillStyle='#ff3b57';ctx.fillRect(-42,-80,10,80);ctx.fillRect(32,-80,10,80);ctx.fillRect(-58,-84,116,6);ctx.restore();ctx.restore();
  for(let i=0;i<9;i++){const yy=wl+8+i*10,ph=TAU*(t+i*.11);ctx.strokeStyle=`rgba(255,120,140,${.12+.05*Math.sin(ph)})`;ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(220+Math.sin(ph)*14,yy);ctx.lineTo(780+Math.sin(ph+1)*14,yy);ctx.stroke()}
  txt('君は一人じゃない',500,288,'700 34px GJ','#fff3ef',{track:14,glow:20*(.7+.3*Math.sin(TAU*t*2)),a:1});
  txt('VOCÊ NUNCA ESTARÁ SOZINHO',500,314,'700 13px GD','#ff8fa3',{track:8});
  embers(t,26,13,wl,20);petals(t,12,4,{wind:180,sz:[.6,1]});vignette();frame_border()},
};

window.render=async(name,w,h,tt)=>{cv=document.getElementById('c');cv.width=W=w;cv.height=H=h;ctx=cv.getContext('2d');await document.fonts.load('700 20px GD');await document.fonts.load('400 20px GD');await document.fonts.load('700 20px GJ');
 ctx.clearRect(0,0,W,H);SC[name](tt)};
</script>"""


def make(name, pw):
    w, h, T, fps = SCENES[name]
    n = int(T * fps)
    tmp = tempfile.mkdtemp(prefix=f"gif_{name}_")
    html = os.path.join(HERE, f"_gif_{name}.html")
    open(html, "w", encoding="utf-8").write(HTML)
    page = pw.new_page(viewport={"width": w, "height": h})
    page.goto("file://" + html)
    for i in range(n):
        page.evaluate(f"render('{name}',{w},{h},{i / n})")
        page.locator("#c").screenshot(path=os.path.join(tmp, f"f{i:03d}.png"))
    page.close()
    os.remove(html)
    out = os.path.join(OUT, f"gif-{name}.gif")
    vf = "split[a][b];[a]palettegen=max_colors=96:stats_mode=full[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(tmp, "f%03d.png"),
                    "-vf", vf, "-loop", "0", out], check=True)
    shutil.rmtree(tmp)
    print(f"gif-{name}.gif  {w}x{h}  {n} frames  {os.path.getsize(out) / 1024:.0f} KB")


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    only = sys.argv[1:] or list(SCENES)
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for name in only:
            make(name, b)
        b.close()
