const {chromium, webkit} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const base = 'http://127.0.0.1:5113';
const stage = process.argv[2] || 'review';
const channel = process.argv[3] || 'chrome';
const out = path.join(process.env.LAYOUT_REPORT_DIR || path.join(require('node:os').tmpdir(), 'ensinar-c-layout'), stage + '-' + channel);
const screens = [[320,568],[375,667],[768,1024],[844,390],[1024,768],[1100,700],[1120,630],[1280,720],[1366,768],[1536,864],[1920,1080],[2560,1440]];

(async () => {
    await fs.mkdir(out, {recursive:true});
    const browser = channel === 'webkit' ? await webkit.launch({headless:true}) : await chromium.launch({channel, headless:true});
    try {
        const context = await browser.newContext();
        const page = await context.newPage();
        const errors = [];
        const failures = [];
        const results = [];
        page.on('pageerror', e => errors.push(e.message));
        page.on('response', r => {if(r.status() >= 400) failures.push({url:r.url(),status:r.status()});});
        async function check(route, width, height) {
            await page.setViewportSize({width,height});
            await page.goto(base + route, {waitUntil:'load'});
            const data = await page.evaluate(() => {
                const width = document.documentElement.clientWidth;
                const selector = e => e.id ? '#' + e.id : e.tagName.toLowerCase() + '.' + [...e.classList].join('.');
                const overflow = [...document.querySelectorAll('body *')].filter(e => {
                    if(e.closest('.CodeMirror, .console-modal, pre, .sidebar nav')) return false;
                    const b = e.getBoundingClientRect();
                    return b.width && (b.right > width + 1 || b.left < -1);
                }).map(e => ({element:selector(e),right:Math.round(e.getBoundingClientRect().right)}));
                const sidebar = document.querySelector('.sidebar');
                const sidebarHidden = sidebar && getComputedStyle(sidebar).position === 'fixed' && sidebar.scrollHeight > sidebar.clientHeight + 1 && getComputedStyle(sidebar).overflowY === 'visible';
                return {scrollWidth:document.documentElement.scrollWidth,width,overflow:overflow.slice(0,10),sidebarHidden};
            });
            results.push({route,width,height,...data});
            if (data.scrollWidth > width + 1 || data.overflow.length || data.sidebarHidden) console.log(JSON.stringify(results.at(-1)));
            if ([320,768,1120,1366].includes(width) && ['/dashboard','/perfil','/compilador','/estudar/2?licao=6'].includes(route)) {
                await page.screenshot({path:path.join(out, route.split('?')[0].replaceAll('/','-') + '-' + width + '.png'),fullPage:false});
            }
            if(route === '/compilador' || route === '/desafio-diario') {
                const open = page.getByRole('button',{name:'Abrir terminal',exact:true});
                if(await open.count()) {
                    await open.click();
                    const modal = await page.evaluate(() => {
                        const e = document.querySelector('.console-modal.ativo');
                        if(!e) return {missing:true};
                        const w = e.querySelector('.console-window').getBoundingClientRect();
                        const input = e.querySelector('input');
                        const footer = e.querySelector('.console-footer').getBoundingClientRect();
                        const i = input?.getBoundingClientRect();
                        return {clipped: footer.bottom > innerHeight || footer.top < w.top || (i && i.bottom > footer.top),footerBottom:footer.bottom,inputBottom:i?.bottom};
                    });
                    if(modal.clipped || modal.missing) console.log(JSON.stringify({route,width,height,modal}));
                    results.push({route,width,height,modal});
                    if([320,844,1120].includes(width)) await page.screenshot({path:path.join(out,'terminal-'+route.slice(1)+'-'+width+'.png')});
                }
            }
        }
        for(const route of ['/','/login','/cadastro']) for(const [w,h] of [screens[0],screens[2],screens[6],screens[10]]) await check(route,w,h);
        const login = await context.request.post(base + '/login',{form:{email:'teste@example.test',senha:'layout-test'}});
        if (!login.ok() || !login.url().endsWith('/dashboard')) throw Error('Login failed: ' + login.url());
        for(const route of ['/dashboard','/modulos','/perfil','/estudar/2?licao=6','/exercicio/6','/desafio-diario','/compilador','/favoritos','/revisao','/simulado','/historico-codigos']) {
            for(const [w,h] of screens) await check(route,w,h);
        }
        await fs.writeFile(path.join(out,'report.json'),JSON.stringify({results,errors:[...new Set(errors)],failures},null,2));
        const layoutFailures = results.filter(result => result.modal
            ? result.modal.clipped || result.modal.missing
            : result.scrollWidth > result.width + 1 || result.overflow.length || result.sidebarHidden);
        console.log(JSON.stringify({checks:results.length,layoutFailures:layoutFailures.length,errors:[...new Set(errors)],failures,out}));
        if (layoutFailures.length || errors.length || failures.length) throw Error('Browser layout regression; see report.json');
    } finally {await browser.close();}
})().catch(e => {console.error(e);process.exitCode=1;});
