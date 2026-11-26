// ===== Penn workbench: interactive re-implementations of Gareth Penn's methods =====
const MORSE={A:'01',B:'1000',C:'1010',D:'100',E:'0',F:'0010',G:'110',H:'0000',I:'00',J:'0111',K:'101',L:'0100',M:'11',N:'10',O:'111',P:'0110',Q:'1101',R:'010',S:'000',T:'1',U:'001',V:'0001',W:'011',X:'1001',Y:'1011',Z:'1100'};
const MORSE_DOTS=Object.fromEntries(Object.entries(MORSE).map(([k,v])=>[k,v.replace(/1/g,'–').replace(/0/g,'·')]));
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function tokens(s){return (s.toUpperCase().match(/[A-Z]|\d+|\./g)||[]);}
// Penn: letters -> Morse (dah=1, dit=0); Arabic numbers -> plain base two; '.' = binary point
function pennBits(s,{digitsAsMorse=false}={}){
  const parts=[];
  for(const t of tokens(s)){
    if(t==='.'){parts.push({t,b:'.'});continue;}
    if(/\d/.test(t)){
      if(digitsAsMorse){for(const d of t){const m={'1':'01111','2':'00111','3':'00011','4':'00001','5':'00000','6':'10000','7':'11000','8':'11100','9':'11110','0':'11111'}[d];parts.push({t:d,b:m});}}
      else parts.push({t,b:BigInt(t).toString(2)});
    } else parts.push({t,b:MORSE[t]});
  }
  return parts;
}
function bitsToValue(bitstr){
  const [ip,fp='']=bitstr.split('.');
  const I=ip.replace(/^0+/,'')||'0';
  let iv=BigInt('0b'+I);
  if(!fp) return {int:iv,str:iv.toString()};
  let f=0, p=0.5; for(const ch of fp){ if(ch==='1') f+=p; p/=2; }
  return {int:iv,str:(Number(iv)+f).toPrecision(Math.min(17,String(iv).length+12)).replace(/0+$/,'')};
}
// ---------- Morse-binary encoder ----------
function runMorse(){
  const s=$('mb-in').value, dm=$('mb-dm').checked;
  const parts=pennBits(s,{digitsAsMorse:dm});
  const bitstr=parts.map(p=>p.b).join('');
  const v=bitsToValue(bitstr);
  let html='<table class="mini"><tr>'+parts.map(p=>`<th>${esc(p.t)}</th>`).join('')+'</tr><tr>'+parts.map(p=>`<td class="mono">${p.t==='.'?'.':(MORSE_DOTS[p.t]||'')}</td>`).join('')+'</tr><tr>'+parts.map(p=>`<td class="mono">${p.b}</td>`).join('')+'</tr></table>';
  html+=`<p>Bit string: <span class="mono">${bitstr}</span> (${bitstr.replace('.','').length} bits)<br>Base-ten value: <b class="big">${v.str}</b>`;
  if(!bitstr.includes('.')){const n=v.int; const sv=n.toString();
    html+=` &nbsp; <span class="muted">digits read as a date (Penn style): ${dateReadings(sv).join(' · ')||'—'}</span>`;}
  html+='</p>';
  $('mb-out').innerHTML=html;
}
function dateReadings(s){
  const out=[]; const n=s.length;
  // split M-D-YY / MM-DD-YY etc.
  for(let a=1;a<=2;a++)for(let b=1;b<=2;b++){const c=n-a-b; if(c!==2&&c!==4)continue;
    const m=+s.slice(0,a), d=+s.slice(a,a+b), y=s.slice(a+b); if(m>=1&&m<=12&&d>=1&&d<=31) out.push(`${m}-${d}-${y}`);}
  return [...new Set(out)];
}
// ---------- Number -> Morse words (dictionary redivision decoder) ----------
let DICT=null;
function buildDict(){
  if(DICT) return DICT; DICT=new Map(); let maxL=0;
  WORDS.forEach((w,i)=>{const b=[...w].map(c=>MORSE[c]).join(''); const sc=-Math.log10(i+20)-(w.length===1&&w!=='A'&&w!=='I'?3:0);
    if(!DICT.has(b)) DICT.set(b,[]); const L=DICT.get(b); if(L.length<3) L.push([sc,w]); maxL=Math.max(maxL,b.length);});
  DICT.maxL=maxL; return DICT;
}
function decodeBits(B,K=25,lead=4){
  const D=buildDict(); const res=[];
  for(let z=0;z<=lead;z++){
    const BB='0'.repeat(z)+B; const beam=Array.from({length:BB.length+1},()=>[]); beam[0]=[[0,[]]];
    for(let i=0;i<BB.length;i++){
      if(!beam[i].length) continue; beam[i].sort((a,b)=>b[0]-a[0]); beam[i]=beam[i].slice(0,K);
      for(let L=1;L<=Math.min(D.maxL,BB.length-i);L++){const key=BB.substr(i,L); const ws=D.get(key); if(!ws) continue;
        for(const [sc,w] of ws) for(const [s,arr] of beam[i]) beam[i+L].push([s+sc,arr.concat(w)]);}
    }
    for(const [s,arr] of beam[BB.length]) res.push([s,z,arr.join(' ')]);
  }
  res.sort((a,b)=>b[0]-a[0]); const seen=new Set(), out=[];
  for(const r of res){ if(seen.has(r[2])) continue; seen.add(r[2]); out.push(r); if(out.length>=K) break;}
  return out;
}
function runDecode(){
  let s=$('dec-in').value.trim(); let B;
  if(/^[01]+$/.test(s)&&$('dec-isbits').checked) B=s; else { try{B=BigInt(s.replace(/[^0-9]/g,'')).toString(2);}catch(e){$('dec-out').textContent='Enter a whole number or a 0/1 string.';return;} }
  const r=decodeBits(B,30).slice(0,12);
  $('dec-out').innerHTML=`<p class="mono">${B} (${B.length} bits)</p><ol>`+r.map(([s,z,t])=>`<li><b>${esc(t)}</b> <span class="muted">${z?`(${z} leading zero${z>1?'s':''} restored)`:''}</span></li>`).join('')+'</ol><p class="muted">Ranked by word frequency. Note how many fluent readings any number has; this is the noise problem Penn calls a "noise-to-signal ratio".</p>';
}
// ---------- Redivision search ----------
function runRedivision(){
  const text=$('rd-text').value.toUpperCase(), target=$('rd-target').value;
  const chars=[]; let bits='', map=[];
  for(const t of (text.match(/[A-Z]|\d+/g)||[])){
    const b=/\d/.test(t)?BigInt(t).toString(2):MORSE[t]; chars.push({t,start:bits.length,len:b.length}); bits+=b; }
  const tb=/^[01]+$/.test(target.trim())?target.trim():pennBits(target).map(p=>p.b).join('');
  if(!tb){$('rd-out').textContent='Enter a target word or bit string.';return;}
  const hits=[]; let k=bits.indexOf(tb);
  while(k>=0){hits.push(k); k=bits.indexOf(tb,k+1);}
  let html=`<p>Target bits: <span class="mono">${tb}</span> (${tb.length} bits; chance per position ≈ 1/${Math.pow(2,tb.length).toLocaleString()}). Text stream: ${bits.length} bits. Found <b>${hits.length}</b> occurrence(s).</p><ul>`;
  for(const h of hits.slice(0,40)){
    const cover=chars.filter(c=>c.start<h+tb.length && c.start+c.len>h);
    const exact=cover.length&&cover[0].start===h&&cover[cover.length-1].start+cover[cover.length-1].len===h+tb.length;
    html+=`<li class="mono">${cover.map(c=>c.t).join('')} ${exact?'<span class="ok">(perfect redivision)</span>':'<span class="muted">(cuts into end letters)</span>'} — starts in character #${chars.indexOf(cover[0])+1}</li>`;
  }
  $('rd-out').innerHTML=html+'</ul>';
}
// ---------- Gematria ----------
const ROMAN={I:1,V:5,X:10,L:50,C:100,D:500,M:1000};
function runGematria(){
  const s=$('gm-in').value.toUpperCase().replace(/[^A-Z]/g,''); const e3=$('gm-e3').checked;
  const vals=[...s].map(c=>c==='E'&&e3?3:c.charCodeAt(0)-64);
  const sum=vals.reduce((a,b)=>a+b,0); const roman=[...s].reduce((a,c)=>a+(ROMAN[c]||0),0);
  const dr=n=>{while(n>9)n=[...String(n)].reduce((a,b)=>a+ +b,0);return n;};
  $('gm-out').innerHTML=`<p class="mono">${[...s].map((c,i)=>c+'='+vals[i]).join(' + ')}</p><p>Sum: <b class="big">${sum}</b> &nbsp; Roman-numeral letters only: <b>${roman}</b> &nbsp; casting out nines: <b>${dr(sum)}</b> &nbsp; sum read as a date: ${dateReadings(String(sum)).join(', ')||'—'}</p>`;
}
// ---------- WIZARD ----------
const mirror=c=>String.fromCharCode(155-c.charCodeAt(0));
function runWizard(){
  const s=$('wz-in').value.toUpperCase();
  const letters=s.replace(/[^A-Z]/g,'');
  const at=[...s].map(c=>/[A-Z]/.test(c)?mirror(c):c).join('');
  const cnt={}; for(const c of letters) cnt[c]=(cnt[c]||0)+1;
  const res={}, pairs=[];
  for(const a of 'ABCDEFGHIJKLM'){const b=mirror(a); const k=Math.min(cnt[a]||0,cnt[b]||0); if(k) pairs.push(`${a}${b}×${k}`); if((cnt[a]||0)-k) res[a]=(cnt[a]||0)-k; if((cnt[b]||0)-k) res[b]=(cnt[b]||0)-k;}
  const resStr=Object.keys(res).sort().map(c=>c.repeat(res[c])).join('');
  $('wz-out').innerHTML=`<p>Reverse alphabet (A↔Z, B↔Y …): <span class="mono">${esc(at)}</span></p><p>WIZARD pairs that "drop out": <span class="mono">${pairs.join(' ')||'none'}</span></p><p>Residue (${resStr.length} of ${letters.length} letters): <b class="mono big">${resStr||'∅'}</b> — mirror of residue: <span class="mono">${[...resStr].map(mirror).join('')}</span></p>`;
}
// ---------- 17-column grid with coordinates, intersections, calendar ----------
let G={cells:[],w:17,sel:[]};
function gridClean(s){const t=s.toUpperCase(); if(/^[01.\s]+$/.test(t)) return t.replace(/\s/g,'').split(''); return (t.match(/[A-Z0-9]/g)||[]);}
function runGrid(){
  G.w=Math.max(2,+$('g-w').value||17); G.cells=gridClean($('g-in').value); G.sel=[];
  const hl=$('g-find').value.toUpperCase().replace(/[^A-Z0-9]/g,''); const marks=new Set();
  if(hl){const str=G.cells.join(''); let k=str.indexOf(hl); while(k>=0){for(let i=0;i<hl.length;i++)marks.add(k+i); k=str.indexOf(hl,k+1);}}
  const rows=Math.ceil(G.cells.length/G.w); let h='<table class="grid"><tr><th></th>'+Array.from({length:G.w},(_,c)=>`<th>${c+1}</th>`).join('')+'</tr>';
  for(let r=0;r<rows;r++){h+=`<tr><th>${r+1}</th>`; for(let c=0;c<G.w;c++){const i=r*G.w+c; const ch=G.cells[i]||''; h+=`<td data-i="${i}" class="${marks.has(i)?'hl':''}" onclick="gridClick(${i})">${ch}</td>`;} h+='</tr>';}
  $('g-out').innerHTML=h+'</table>'; $('g-info').innerHTML=`${G.cells.length} alphanumeric characters → ${rows} rows of ${G.w}. Click two cells.`;
}
function rc(i){return [Math.floor(i/G.w)+1, i%G.w+1];}
function calDate(i){
  const ap=+$('g-apos').value, ad=$('g-adate').value; if(!ap||!ad) return '';
  const d=new Date(ad+'T12:00:00Z'); d.setUTCDate(d.getUTCDate()+(i+1-ap));
  return d.toISOString().slice(0,10);
}
function gridClick(i){
  if(G.sel.length>=2) G.sel=[]; G.sel.push(i);
  document.querySelectorAll('#g-out td.sel').forEach(td=>td.classList.remove('sel'));
  G.sel.forEach(j=>{const td=document.querySelector(`#g-out td[data-i="${j}"]`); if(td) td.classList.add('sel');});
  const info=G.sel.map(j=>{const [r,c]=rc(j); const cd=calDate(j); return `<b>${G.cells[j]}</b> #${j+1} at (row ${r}, col ${c}) → reads "${r},${c}" / ${r}${c}${cd?` · calendar date ${cd}`:''}`;});
  let h=info.join('<br>');
  if(G.sel.length===2){const [a,b]=G.sel; const [r1,c1]=rc(a),[r2,c2]=rc(b); const dr=Math.abs(r2-r1), dc=Math.abs(c2-c1);
    const x1=(r1-1)*G.w+c2, x2=(r2-1)*G.w+c1;
    h+=`<br>Difference of positions: <b>${Math.abs(b-a)}</b> · rectangle (inclusive) ${dr+1}×${dc+1} = <b>${(dr+1)*(dc+1)}</b> · right-triangle legs ${dr},${dc} → hypotenuse √<b>${dr*dr+dc*dc}</b> · intersections: row ${r1}×col ${c2} = #${x1} (${G.cells[x1-1]||'·'}), row ${r2}×col ${c1} = #${x2} (${G.cells[x2-1]||'·'})`;}
  $('g-info').innerHTML=h;
}
// ---------- Day of year / day counts ----------
function runDays(){
  const a=$('d-a').value, b=$('d-b').value; let h='';
  if(a){const d=new Date(a+'T12:00:00Z'); const j=Math.round((d-new Date(Date.UTC(d.getUTCFullYear(),0,1,12)))/864e5)+1; h+=`Day of year: <b>${j}</b> (Penn's "Julian date") · binary ${j.toString(2)} · reads ${dateReadings(String(j)).join(', ')||'—'}<br>`;}
  if(a&&b){const n=Math.round((new Date(b+'T12:00:00Z')-new Date(a+'T12:00:00Z'))/864e5); h+=`Days from A to B: <b>${n}</b> · binary ${Math.abs(n).toString(2)} · digits as date: ${dateReadings(String(Math.abs(n))).join(', ')||'—'} · ÷17 = ${(n/17).toFixed(3)}`;}
  $('d-out').innerHTML=h;
}
// ---------- Squares, cubes, taxicab, factors ----------
function factor(n){const f=[];let d=2n;while(d*d<=n){while(n%d===0n){f.push(d);n/=d;}d+=d===2n?1n:2n;}if(n>1n)f.push(n);return f;}
function runNum(){
  const n=BigInt($('n-in').value.replace(/[^0-9]/g,'')||'0'); if(n===0n){$('n-out').textContent='';return;}
  const N=Number(n); const out=[];
  const isq=Math.round(Math.sqrt(N)), icb=Math.round(Math.cbrt(N));
  if(BigInt(isq)**2n===n) out.push(`perfect square (${isq}²)`); if(BigInt(icb)**3n===n) out.push(`perfect cube (${icb}³)`);
  const cubes=[]; for(let a=1;2*a**3<=N;a++){const r=N-a**3; const b=Math.round(Math.cbrt(r)); if(b**3===r) cubes.push(`${a}³+${b}³`);}
  const sqs=[]; for(let a=0;2*a*a<=N&&a<1e5;a++){const r=N-a*a; const b=Math.round(Math.sqrt(r)); if(b*b===r) sqs.push(`${a}²+${b}²`);}
  const fs=factor(n).map(String);
  $('n-out').innerHTML=`<p>Factors: <span class="mono">${fs.join(' × ')}</span>${n%17n===0n?` · <b>TIMES 17</b> (= ${n/17n} × 17)`:''}<br>${out.join(' · ')}<br>Sum of two cubes: ${cubes.join(', ')||'no'}${cubes.length>=2?' ← <b>taxicab-type</b>':''}<br>Sum of two squares: ${sqs.slice(0,8).join(', ')||'no'}<br>Binary: <span class="mono">${n.toString(2)}</span> · digit root ${(N-1)%9+1}</p>`;
}
// ---------- 42020-style: one number shown many ways ----------
function runMany(){
  const x=Number($('m-in').value); if(!x){$('m-out').textContent='';return;}
  const r=[['hexadecimal',x.toString(16).toUpperCase()],['square',BigInt(x)**2n],['cube',BigInt(x)**3n],['square root',Math.sqrt(x).toPrecision(13)],['cube root',Math.cbrt(x).toPrecision(12)],['log₁₀',Math.log10(x).toPrecision(12)],['log₂',Math.log2(x).toPrecision(12)],['ln',Math.log(x).toPrecision(12)]];
  for(let b=2;b<=9;b++) r.push([`base ${b}`,x.toString(b)]);
  $('m-out').innerHTML='<table class="mini">'+r.map(([k,v])=>`<tr><th>${k}</th><td class="mono">${v}</td></tr>`).join('')+'</table>';
}
function runBases(){
  const vals=$('b-in').value.split(/[\s,]+/).filter(Boolean); const sets=vals.map(v=>{const m=new Map(); for(let b=2;b<=36;b++){const p=parseInt(v,b); if(!isNaN(p)&&p.toString(b).toUpperCase()===v.toUpperCase()) m.set(p,b);} return m;});
  const common=[...sets[0].keys()].filter(k=>sets.every(s=>s.has(k)));
  $('b-out').innerHTML=common.length?common.map(k=>`<b>${k}</b> = `+vals.map((v,i)=>`${v}<sub>${sets[i].get(k)}</sub>`).join(' = ')).join('<br>'):'No single number has all of these representations (bases 2–36).';
}
// ---------- Transposition (write rows, read columns) ----------
function runTrans(){
  const s=$('t-in').value.replace(/\s/g,''); const w=+$('t-w').value||7; const rows=Math.ceil(s.length/w);
  let grid='<table class="grid">'; for(let r=0;r<rows;r++){grid+='<tr>'+Array.from({length:w},(_,c)=>`<td>${esc(s[r*w+c]||'')}</td>`).join('')+'</tr>';} grid+='</table>';
  let cols=''; for(let c=0;c<w;c++) for(let r=0;r<rows;r++) cols+=s[r*w+c]||'';
  $('t-out').innerHTML=grid+`<p>Read down the columns: <b class="mono">${esc(cols)}</b></p>`;
}
// ---------- Rebus & nines ----------
function runRebus(){
  const x=+$('rb-x').value, y=+$('rb-y').value; if(isNaN(x)||isNaN(y)) return;
  const clock=(x<60&&y>=1&&y<=12)?`as clock time: ${x} minutes before ${y}:00 = <b>${y===1?12:y-1}:${String(60-x).padStart(2,'0')}</b> (Penn: "22 before 9" = 8:38 → the .38)`:'';
  const arith=`as subtraction (Penn: "103 before MIKADO"): ${y} − ${x} = <b>${y-x}</b>`;
  $('rb-out').innerHTML=`"${x} before ${y}": ${x>y?(clock||'(subtraction does not apply when X &gt; Y)'):arith+(clock?' · '+clock:'')}<br>"${x} over ${y}" (division): <b>${(x/y).toPrecision(6)}</b> (Penn: 76 over 38 = 2 = TWO)`;
}
// ---------- Radian on the map ----------
function bearing(a,b){const r=Math.PI/180;const [la1,lo1]=[a[0]*r,a[1]*r],[la2,lo2]=[b[0]*r,b[1]*r];const x=Math.sin(lo2-lo1)*Math.cos(la2),y=Math.cos(la1)*Math.sin(la2)-Math.sin(la1)*Math.cos(la2)*Math.cos(lo2-lo1);return (Math.atan2(x,y)/r+360)%360;}
function runRadian(){
  const P=[...document.querySelectorAll('.rad-pt')].map(r=>({name:r.dataset.n,lat:+r.querySelector('.lat').value,lon:+r.querySelector('.lon').value}));
  const D=P[0], A=P[1], B=P[2]; const ang=Math.abs(bearing([D.lat,D.lon],[A.lat,A.lon])-bearing([D.lat,D.lon],[B.lat,B.lon]));
  const lat0=37.70, lat1=38.68, lon0=-122.62, lon1=-121.80, k=Math.cos(38.15*Math.PI/180);
  const W=520, sc=W/((lon1-lon0)*k), H=Math.round((lat1-lat0)*sc);
  const X=lon=>(lon-lon0)*k*sc, Y=lat=>(lat1-lat)*sc;
  let s=`<svg viewBox="0 0 ${W} ${H}" class="map"><rect width="${W}" height="${H}" fill="#f4f1ea"/>`;
  for(const p of P){s+=`<circle cx="${X(p.lon)}" cy="${Y(p.lat)}" r="5" fill="${p===D?'#a33':'#235'}"/><text x="${X(p.lon)+7}" y="${Y(p.lat)-6}" font-size="12">${esc(p.name)}</text>`;}
  for(const p of [A,B]) s+=`<line x1="${X(D.lon)}" y1="${Y(D.lat)}" x2="${X(p.lon)}" y2="${Y(p.lat)}" stroke="#a33" stroke-width="1.5"/>`;
  s+='</svg>';
  $('rad-out').innerHTML=s+`<p>Angle at ${esc(D.name)} between ${esc(A.name)} and ${esc(B.name)}: <b class="big">${ang.toFixed(2)}°</b> &nbsp; (1 radian = 57.30°; difference ${(ang-57.2958).toFixed(2)}°)</p>`;
}
// ---------- Catalog "try it" ----------
function tryDemo(widget,preset){
  const go=(id,inp,fn)=>{ if(inp!=null) $(inp).value=preset; fn(); document.getElementById(id).scrollIntoView({behavior:'smooth',block:'start'}); document.getElementById(id).classList.add('flash'); setTimeout(()=>document.getElementById(id).classList.remove('flash'),1500);};
  switch(widget){
    case 'morse': go('w-morse','mb-in',runMorse); break;
    case 'redivision': { const [t,g]=String(preset).split('|'); $('rd-text').value=t||''; $('rd-target').value=g||''; go('w-redivision',null,runRedivision); break; }
    case 'gematria': go('w-gematria','gm-in',runGematria); break;
    case 'wizard': go('w-wizard','wz-in',runWizard); break;
    case 'grid17': case 'calendar': case 'hypotenuse': { const [t,f]=String(preset).split('|'); $('g-in').value=t; $('g-find').value=f||''; go('w-grid',null,runGrid); break; }
    case 'dayofyear': { const [a,b]=String(preset).split('|'); $('d-a').value=a||''; $('d-b').value=b||''; go('w-days',null,runDays); break; }
    case 'cubes': case 'squares': go('w-num','n-in',runNum); break;
    case 'nines': go('w-num','n-in',runNum); break;
    case 'rebus': { const [x,y]=String(preset).split('|'); $('rb-x').value=x; $('rb-y').value=y; go('w-rebus',null,runRebus); break; }
    case 'base': go('w-bases','b-in',runBases); break;
    case 'radian': go('w-radian',null,runRadian); break;
    case 'transposition': { const [t,w]=String(preset).split('|'); $('t-in').value=t; $('t-w').value=w||7; go('w-trans',null,runTrans); break; }
    case 'anagram': go('w-wizard','wz-in',runWizard); break;
    default: break;
  }
}
// ---------- Anagram / algebraic summation ----------
function letterCount(s){const c={}; for(const ch of s.toUpperCase().replace(/[^A-Z]/g,'')) c[ch]=(c[ch]||0)+1; return c;}
function runAnagram(){
  const [a,b]=$('an-in').value.split('|'); const ca=letterCount(a||'');
  const alg=Object.entries(ca).sort((x,y)=>y[1]-x[1]||x[0].localeCompare(y[0])).map(([k,v])=>v>1?`${k}<sup>${v}</sup>`:k).join(' ');
  const reps=Object.values(ca).filter(v=>v>1).reduce((s,v)=>s+v,0);
  let h=`<p>Letters of A: <span class="mono">${alg}</span> (Penn's "algebraic summation": repeated letters become exponents; their total = ${reps})</p>`;
  if(b!==undefined){const cb=letterCount(b); const keys=new Set([...Object.keys(ca),...Object.keys(cb)]); const diffA=[],diffB=[];
    for(const k of keys){const d=(ca[k]||0)-(cb[k]||0); if(d>0) diffA.push(k.repeat(d)); if(d<0) diffB.push(k.repeat(-d));}
    h+= (!diffA.length&&!diffB.length)?'<p class="ok"><b>Exact anagram.</b> All the parts fit and nothing is left over.</p>':`<p>Not exact. Left over in A: <b class="mono">${diffA.join('')||'—'}</b>; missing from A: <b class="mono">${diffB.join('')||'—'}</b></p>`;}
  $('an-out').innerHTML=h;
}
// ---------- Binary converter (numbers, constants) ----------
const CONST={pi:Math.PI,phi:(1+Math.sqrt(5))/2,e:Math.E,sqrt10:Math.sqrt(10),radian:180/Math.PI,sqrt2:Math.SQRT2};
function fracBits(x,n){let f=x-Math.floor(x),b='';for(let i=0;i<n;i++){f*=2;if(f>=1){b+='1';f-=1;}else b+='0';}return b;}
function runBinary(){
  const s=$('bn-in').value.trim(); let h='';
  if(/^[01]+$/.test(s)){ const v=BigInt('0b'+s); const r=decodeBits(s,20).slice(0,6);
    h=`<p>Binary <span class="mono">${s}</span> = <b class="big">${v}</b></p><p>Morse readings: ${r.map(x=>'<b>'+esc(x[2])+'</b>').join(' · ')}</p>`; }
  else if(/^[a-z0-9]+:\d+$/i.test(s)){ const [k,n]=s.split(':'); const x=CONST[k.toLowerCase()]; if(x===undefined){$('bn-out').textContent='Known constants: '+Object.keys(CONST).join(', ');return;}
    const fb=fracBits(x,+n); const r=decodeBits(fb,20).slice(0,6);
    h=`<p>${k} = ${x} → binary ${Math.floor(x).toString(2)}.<b class="mono">${fb}</b> (${n} fraction bits)</p><p>Fraction bits as Morse: ${r.map(x=>'<b>'+esc(x[2])+'</b>').join(' · ')}</p>`; }
  else { let x; try{ x=Function('pi','phi','e',`return (${s.replace(/[^0-9+\-*/().a-z ]/gi,'')});`)(Math.PI,(1+Math.sqrt(5))/2,Math.E);}catch(e){x=NaN;}
    if(isNaN(x)){$('bn-out').textContent='Enter a number, an expression like 130*pi, a 0/1 string, or const:bits (pi:13, phi:19).';return;}
    const ib=Math.floor(x).toString(2), fb=Number.isInteger(x)?'':fracBits(x,16); const r=decodeBits(ib,20).slice(0,6);
    h=`<p>${s} = <b>${x}</b> → binary <b class="mono">${ib}${fb?'.'+fb:''}</b></p><p>Integer bits as Morse: ${r.map(x=>'<b>'+esc(x[2])+'</b>').join(' · ')}</p>`; }
  $('bn-out').innerHTML=h;
}
// ---------- Right triangle ----------
function runTri(){
  const [a,b]=$('tr-in').value.split(/[ ,]+/).map(Number); if(isNaN(a)||isNaN(b)) return; const h2=a*a+b*b;
  const r=decodeBits(h2.toString(2),20).slice(0,6);
  $('tr-out').innerHTML=`<p>Legs ${a}, ${b} → hypotenuse √<b class="big">${h2}</b> = ${Math.sqrt(h2).toFixed(4)}. Penn reads the number under the root: ${h2} = binary <span class="mono">${h2.toString(2)}</span> → ${r.map(x=>'<b>'+esc(x[2])+'</b>').join(' · ')}</p>`;
}
// extend tryDemo
const _tryDemo=tryDemo;
tryDemo=function(widget,preset){
  const go=(id,fn)=>{fn(); const el=document.getElementById(id); el.scrollIntoView({behavior:'smooth',block:'start'}); el.classList.add('flash'); setTimeout(()=>el.classList.remove('flash'),1500);};
  if(widget==='anagram'){ $('an-in').value=preset; return go('w-anagram',runAnagram); }
  if(widget==='binary'){ $('bn-in').value=preset; return go('w-binary',runBinary); }
  if(widget==='hypotenuse'){ $('tr-in').value=preset; return go('w-tri',runTri); }
  if(widget==='decode'){ const p=String(preset); if(/^[01]+$/.test(p)){$('dec-in').value=p; $('dec-isbits').checked=true;} else if(/^\d+$/.test(p)){$('dec-in').value=p; $('dec-isbits').checked=false;} else {$('dec-in').value=pennBits(p).map(x=>x.b).join(''); $('dec-isbits').checked=true;} return go('w-decode',runDecode); }
  if(widget==='grid17'){ const [t,f,ap,ad]=String(preset).split('|'); $('g-in').value=t; $('g-find').value=f||''; if(ap){$('g-apos').value=ap;} if(ad){$('g-adate').value=ad;} return go('w-grid',runGrid); }
  return _tryDemo(widget,preset);
};
// ---------- Penn vocabulary readings (exact, reversed, word + binary tail) ----------
const PENNVOC=['MIKE','MIKEO','MIKEPI','OHARE','ERAHO','BER','BERTA','GENE','BM','ME','I','OH','MHO','TIME','TIMES','TIMEX','TITAN','THEEND','DEATH','BIRTH','DESK','LIFE','DEAD','NINE','TWO','ONE','THREE','BUS','MOM','MAMA','MOTHER','NAME','TAXI','HALF','GOSE','GOOSE','BASIN','KING','NINES','DONUTJAM','IK','UE','PW','ZODIAC','GENEBERTA','RADIAN','JULY','MIKADO','PI'];
function pennVocab(bits){
  const out=[]; const strip=b=>b.replace(/^0+/,'');
  for(const w of PENNVOC){ const wb=[...w].map(c=>MORSE[c]).join('');
    if(strip(wb)===strip(bits)) out.push(`<b>${w}</b> (exact)`);
    else if(bits.startsWith(wb)&&bits.length>wb.length){ const t=bits.slice(wb.length); if(t[0]==='1'&&t.length<=12) out.push(`<b>${w} ${parseInt(t,2)}</b> (word + binary ${t})`); if(/^0+$/.test(t)) out.push(`<b>${w}</b> × 2<sup>${t.length}</sup> (trailing zeros)`); }
  }
  return out.length?`<p>Penn-vocabulary readings: ${out.join(' · ')}</p>`:'';
}
const _runBinary=runBinary;
runBinary=function(){ _runBinary(); const s=$('bn-in').value.trim(); let bits='';
  if(/^[01]+$/.test(s)) bits=s; else if(/^[a-z0-9]+:\d+$/i.test(s)){const [k,n]=s.split(':'); if(CONST[k.toLowerCase()]!==undefined) bits=fracBits(CONST[k.toLowerCase()],+n);} else {const x=Number(s); if(Number.isInteger(x)&&x>0) bits=x.toString(2);}
  if(bits) $('bn-out').innerHTML+=pennVocab(bits);
};
const _runDecode=runDecode;
runDecode=function(){ _runDecode(); let s=$('dec-in').value.trim(); let B=(/^[01]+$/.test(s)&&$('dec-isbits').checked)?s:(/^\d+$/.test(s)?BigInt(s).toString(2):''); if(B) $('dec-out').innerHTML=pennVocab(B)+$('dec-out').innerHTML; };
// auto-select the first highlighted grid cell after a "Try it"
const _tryDemo2=tryDemo;
tryDemo=function(widget,preset){ _tryDemo2(widget,preset); if(widget==='grid17'||widget==='calendar'){ const td=document.querySelector('#g-out td.hl'); if(td) gridClick(+td.dataset.i); } };
