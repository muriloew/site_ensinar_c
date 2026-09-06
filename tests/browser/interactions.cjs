const {chromium, webkit} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs/promises');
const base = 'http://127.0.0.1:5113';
const channel = process.argv[2] || 'chrome';

(async () => {
    const browser = channel === 'webkit' ? await webkit.launch({headless:true}) : await chromium.launch({channel,headless:true});
    try {
        const context = await browser.newContext({viewport:{width:1366,height:768}});
        const remote = [];
        await context.route('**/*', route => {
            if(new URL(route.request().url()).origin !== base) {remote.push(route.request().url());return route.abort();}
            return route.continue();
        });
        await context.request.post(base+'/login',{form:{email:'teste@example.test',senha:'layout-test'}});
        const page = await context.newPage();
        const errors = [];
        page.on('pageerror',error => errors.push(error.message));
        await page.goto(base+'/compilador');
        assert.equal(await page.evaluate(() => typeof io), 'function');
        const connected = await page.evaluate(() => new Promise(resolve => {
            const socket = io({transports:['polling'],timeout:4000});
            socket.on('connect',()=>{socket.disconnect();resolve(true);});
            socket.on('connect_error',()=>{socket.disconnect();resolve(false);});
        }));
        assert(connected,'The bundled terminal client must connect to the actual server');

        const source = '#include <stdio.h>\nint main(void) {\n    int n;\n    printf("Digite: ");\n    scanf("%d", &n);\n    printf("Resultado: %d\\n", n * 2);\n    return 0;\n}';
        await page.locator('.CodeMirror').click();
        await page.keyboard.press('ControlOrMeta+A');
        await page.keyboard.insertText(source);
        assert.equal(await page.evaluate(() => obterValorEditor('codigoCompilador')),source);
        await page.waitForFunction(code=>localStorage.getItem('ensinar-c-pratica-livre')===code,source);
        await page.reload();
        assert.equal(await page.evaluate(() => obterValorEditor('codigoCompilador')),source);
        await page.setViewportSize({width:375,height:667});
        assert.equal(await page.evaluate(() => obterValorEditor('codigoCompilador')),source);
        assert.equal(await page.locator('.ide-tool-button').nth(2).evaluate(e => e.scrollHeight <= e.clientHeight),true);

        // These events exercise the browser protocol without pretending to compile C on Windows.
        await page.evaluate(() => {
            const handlers = new Map();
            window.sentEvents = [];
            window.serverEvent = (event,payload) => handlers.get(event)?.(payload);
            window.io = () => ({on:(event,fn)=>handlers.set(event,fn),emit:(event,data)=>sentEvents.push({event,data})});
        });
        const compile = page.locator('.compiler-toolbar button').first();
        await compile.click();
        assert(await compile.isDisabled());
        assert.deepEqual(await page.evaluate(()=>sentEvents.at(-1)),{event:'compilar_real',data:{tipo:'compilador',codigo:source}});
        await page.evaluate(()=>{serverEvent('build_log',{ok:true,texto:'Build OK'});serverEvent('terminal_saida',{texto:'Digite: '});});
        const input = page.locator('#terminalInputCompilador');
        await input.fill('7');
        await input.press('Enter');
        assert.deepEqual(await page.evaluate(()=>sentEvents.at(-1)),{event:'terminal_entrada',data:{texto:'7\n'}});
        await page.evaluate(()=>{serverEvent('terminal_saida',{texto:'7\nResultado: 14\n'});serverEvent('terminal_finalizado');});
        assert.match(await page.locator('#saidaCompilador').innerText(),/Resultado: 14/);
        assert(await input.isDisabled());
        await page.keyboard.press('Escape');
        assert.equal(await page.locator('.console-modal.ativo').count(),0);
        assert(await compile.isEnabled());
        assert.equal(await compile.evaluate(e=>document.activeElement===e),true);
        await compile.click();
        await page.evaluate(()=>serverEvent('build_log',{ok:true,texto:'Build OK'}));
        await page.setViewportSize({width:375,height:280});
        await page.waitForFunction(()=>parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--console-viewport-height'))===280);
        assert(await input.isVisible());
        const bounds = await input.boundingBox();
        assert(bounds.y >= 0 && bounds.y + bounds.height <= 280);
        const out = process.env.LAYOUT_REPORT_DIR || path.join(require('node:os').tmpdir(), 'ensinar-c-layout');
        await fs.mkdir(out,{recursive:true});
        await page.screenshot({path:path.join(out,`terminal-keyboard-height-${channel}.png`)});
        await page.keyboard.press('Escape');
        assert(await compile.isEnabled(),'Cancelling must allow compiling again');
        assert.equal(await page.evaluate(()=>sentEvents.at(-1).event),'terminal_cancelar');
        assert.equal(await page.locator('main').evaluate(e=>e.inert),false);

        await page.setViewportSize({width:768,height:1024});
        await page.goto(base+'/exercicio/6');
        await page.locator('.CodeMirror').click();
        await page.keyboard.press('ControlOrMeta+A');
        const save = page.waitForResponse(r=>r.url().includes('/api/exercicio/salvar-rascunho') && r.request().method()==='POST');
        await page.keyboard.insertText(source);
        assert.equal((await save).status(),200);
        await page.waitForFunction(()=>document.querySelector('#statusSalvamento').classList.contains('saved'));
        await page.reload();
        assert.equal(await page.evaluate(()=>obterValorEditor('codigoExercicio')),source);
        await page.goto(base+'/modulos');
        await page.locator('#buscaModulos').fill('ponteiros');
        assert(await page.locator('[data-search]:visible').count()>0);
        assert(await page.locator('[data-search]:visible').count()<21);
        const backup = await context.request.get(base+'/backup-progresso');
        assert.equal(backup.status(),200);
        assert((await backup.json()).progresso.length > 0);
        assert.deepEqual(remote,[],'All frontend dependencies must come from the site itself');

        const restricted = await browser.newContext();
        await restricted.addInitScript(()=>{
            Storage.prototype.getItem = Storage.prototype.setItem = function(){throw new DOMException('Blocked','SecurityError');};
        });
        await restricted.request.post(base+'/login',{form:{email:'teste@example.test',senha:'layout-test'}});
        const limited = await restricted.newPage();
        limited.on('pageerror',error=>errors.push(error.message));
        await limited.goto(base+'/compilador');
        await limited.locator('.CodeMirror').click();
        await limited.keyboard.press('ControlOrMeta+A');
        await limited.keyboard.insertText(source);
        await limited.keyboard.press('ControlOrMeta+S');
        assert.equal(await limited.evaluate(()=>obterValorEditor('codigoCompilador')),source);
        assert.equal(await limited.locator('.ide-editor-toolbar').count(),1);
        assert.deepEqual(errors,[]);
        console.log('PASS: actual Socket.IO connection, local assets, keyboard editing, saved drafts, resizing, terminal events, cancel/reopen, focus, reduced height, search, backup, blocked storage.');
    } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
