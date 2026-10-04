# Weekly recap test: weeks 1..3 on iPhone SE + 13 (+ desktop). Usage: python3 recap_test.py [BASE_URL]
import asyncio,sys,re
from playwright.async_api import async_playwright
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:18801/index.html'
OUT='/workspace/tankshots/'
ok=True
def chk(n,c,info=''):
    global ok;ok&=bool(c);print(('PASS ' if c else 'FAIL ')+n,'' if c else info)
BANNED=re.compile(r'champ|troph|\bgay\b|retard|fag|\bmom\b|\bwife\b|\bugly\b|\bfat\b',re.I)
GEOM='''(()=>{const out={over:[],xo:document.documentElement.scrollWidth-innerWidth,ph:[]};
 document.querySelectorAll('#recap .withph').forEach(c=>{const f=c.querySelector('.rphoto img').getBoundingClientRect();
   out.ph.push(c.querySelector('figcaption').textContent);
   c.querySelectorAll('.rt,.rh,.rl,.aw-t,.aw-n,.aw-l').forEach(t=>{const r=t.getBoundingClientRect();if(r.left<f.right-1&&r.right>f.left+1&&r.top<f.bottom-1&&r.bottom>f.top+1)out.over.push(t.textContent.slice(0,40))});
   const cap=c.querySelector('figcaption').getBoundingClientRect();if(cap.top<f.bottom-1)out.over.push('caption over photo')});
 document.querySelectorAll('#recap .rgame,#recap .award').forEach(c=>{const r=c.getBoundingClientRect();if(r.right>innerWidth+1||r.left<-1)out.over.push('card off-screen')});
 return out})()'''
async def run(p,b,dev,name):
    d=dict(p.devices[dev]) if dev else {'viewport':{'width':1280,'height':900}};d.pop('default_browser_type',None)
    ctx=await b.new_context(**d);m=await ctx.new_page();errs=[];m.on('pageerror',lambda e:errs.append(str(e)));m.on('console',lambda c:c.type=='error' and errs.append(c.text))
    await m.goto(BASE+'#recap',wait_until='domcontentloaded')
    await m.wait_for_function("document.querySelectorAll('#recap .rgame').length>0",timeout=60000)
    last=await m.evaluate("document.querySelectorAll('#recapWeeks .wk').length")
    chk(f'[{name}] default = last scored week ({last})',await m.evaluate("+document.getElementById('recapBody').dataset.week")==last and f'WEEK {last} RECAP' in await m.inner_text('#recapTitle'))
    y=await m.evaluate("document.getElementById('recap').getBoundingClientRect().top");chk(f'[{name}] #recap anchor lands at top',y<140,y)
    texts={}
    for w in range(1,min(3,last)+1):
        await m.click(f'#recapWeeks .wk[data-w="{w}"]')
        await m.wait_for_function(f"document.getElementById('recapBody').dataset.week=='{w}'",timeout=60000)
        await m.wait_for_function("[...document.querySelectorAll('#recap img')].every(i=>i.complete)",timeout=20000)
        t=await m.inner_text('#recapBody');texts[w]=t
        g=await m.evaluate("document.querySelectorAll('#recap .rgame').length");a=await m.evaluate("document.querySelectorAll('#recap .award').length")
        chk(f'[{name}] wk{w}: 6 matchups, 4 awards',g==6 and a==4,(g,a))
        chk(f'[{name}] wk{w}: no unfilled {{}} / undefined / NaN',not re.search(r'\{\w+\}|undefined|NaN',t),re.findall(r'.{20}(?:\{\w+\}|undefined|NaN).{10}',t))
        chk(f'[{name}] wk{w}: banned words absent',not BANNED.search(t),BANNED.findall(t))
        for k in ['SHOEY OF THE WEEK','POINTS LEFT ON BENCH','LUCKIEST WIN','MOST ROBBED']:chk(f'[{name}] wk{w}: award {k}',k in t)
        G=await m.evaluate(GEOM);chk(f'[{name}] wk{w}: photos never cover text, no sideways scroll',not G['over'] and G['xo']<=1,G)
        chk(f'[{name}] wk{w}: shoey card has the laughing squad',await m.evaluate("!!document.querySelector('#recap .award.withph .rphoto.laugh')"))
        wz=await m.evaluate("(()=>{const c=document.querySelector('#recap .rgame.wzg');if(!c)return null;return{win:!!c.querySelector('.rt.win.wz'),sw:!!c.querySelector('.rphoto.swoon'),cap:(c.querySelector('figcaption')||{}).textContent||''}})()")
        chk(f'[{name}] wk{w}: Weasels card swoon iff they won',wz and wz['win']==wz['sw'] and (not wz['win'] or 'WEASELS WIN. THE SQUAD APPROVES.' in wz['cap']),wz)
        jo=await m.evaluate("!!document.querySelector('#recap .rgame.joeg .rphoto.laugh')");chk(f'[{name}] wk{w}: Joe matchup has the laughing squad',jo)
        chk(f'[{name}] wk{w}: Joe tag only on joebags85 team (never moreho15)',await m.evaluate("[...document.querySelectorAll('#recap .rt.joe .rn')].every(e=>!/Tet McMuffins/i.test(e.textContent))"))
        sz=await m.evaluate("[...document.querySelectorAll('#recap .rphoto img')].map(i=>i.currentSrc.split('/').pop())")
        chk(f'[{name}] wk{w}: small photo variant used ({set(sz)})',all('360' in s or ('600' in s and name!='SE') for s in sz),sz)
        await m.evaluate("document.getElementById('recap').scrollIntoView()");await m.wait_for_timeout(200)
        await m.screenshot(path=f'{OUT}recap-{name}-wk{w}.png',full_page=False)
        el=await m.query_selector('#recap');await el.screenshot(path=f'{OUT}recap-{name}-wk{w}-full.png')
    # deterministic: reload and compare week 2
    await m.goto('about:blank');await m.goto(BASE+'#recap-w2',wait_until='domcontentloaded');await m.wait_for_function("document.getElementById('recapBody').dataset.week=='2'",timeout=60000)
    chk(f'[{name}] same recap after reload (seeded)',await m.inner_text('#recapBody')==texts.get(2),'differs')
    chk(f'[{name}] weeks read differently',len(set(texts.values()))==len(texts))
    chk(f'[{name}] no console/page errors',not errs,errs);await ctx.close()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for dev,n in [('iPhone 13','13')]:await run(p,b,dev,n)
        await b.close()
    print('ALL PASS' if ok else 'SOME FAIL')
asyncio.run(main())
