/* =========================================================
   AHLAN — atendente de pedidos do Suud
   Lê o cardápio direto do HTML (.dish[data-id]), monta o pedido
   ou a reserva e envia pronto pelo WhatsApp.
   ========================================================= */
(() => {
  const WHATSAPP = '5521967717717';
  const ADDRESS = 'Rua Otávio Carneiro, 8 · Icaraí, Niterói';
  const MAPS = 'https://www.google.com/maps/search/?api=1&query=Suud+Culin%C3%A1ria+%C3%81rabe+Rua+Ot%C3%A1vio+Carneiro+8+Icara%C3%AD+Niter%C3%B3i';

  const root = document.documentElement;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const box = $('#ahlan');
  if (!box) return;
  const panel = $('.ahlan__panel', box);
  const log = $('.ahlan__log', box);
  const form = $('.ahlan__composer', box);
  const input = $('input', form);
  const cartBar = $('[data-ahlan-cartbar]', box);
  const toastEl = $('.ahlan__toast', box);
  const launcher = $('.ahlan__launcher', box);
  const mini = $('.minicart');
  const header = $('.site-header');
  const isMobile = () => matchMedia('(max-width: 860px)').matches;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const DEFAULT_PH = input.placeholder;

  /* ---------- Cardápio: do HTML (página do cardápio) ou de menu-data.js ---------- */
  const domDishes = $$('.dish[data-id]');
  const MENU = !domDishes.length && window.SUUD_MENU ? window.SUUD_MENU : domDishes.map(li => {
    const cat = li.closest('.menu-cat');
    return {
      id: li.dataset.id,
      name: $('h4', li).textContent.trim(),
      desc: $('p', li).textContent.trim(),
      price: li.dataset.price ? parseFloat(li.dataset.price) : null,
      cat: cat.dataset.cat, catId: cat.id,
      veg: (li.dataset.tags || '').includes('veg'),
      el: li
    };
  });
  const byId = Object.fromEntries(MENU.map(m => [m.id, m]));
  const CATS = [];
  MENU.forEach(m => { if (!CATS.find(c => c.id === m.catId)) CATS.push({ id: m.catId, name: m.cat }); });
  const CAT_INTRO = {
    'cat-pastas': 'Nossas pastas, para comer com pão árabe quente:',
    'cat-entradas': 'Entradas para abrir o apetite:',
    'cat-mezzes': 'Mezzes e torres, feitos para dividir:',
    'cat-pratos': 'Pratos e saladas, do almoço ao jantar:',
    'cat-doces': 'Para fechar com doçura (ou acompanhar um café turco):'
  };
  const ALIASES = {
    hummus: 'homus humus hommus grao de bico', babaganoush: 'baba ganoush babaganuche berinjela', labanie: 'coalhada seca labneh',
    paes: 'pao pita', falafel: 'falafel faláfel', nayee: 'kibe cru quibe cru nayeh', 'kibe-frito': 'quibe kibe frito',
    'mini-kibe': 'quibe mini kibe', 'kibe-assado': 'quibe assado', esfiha: 'esfirra sfiha', 'mini-esfiha': 'esfirra',
    kafta: 'kafta kefta espeto', 'mini-kafta': 'kafta canela', 'mezze-byblos': 'mezze meze', 'mezze-capadocia': 'mezze meze capadocia',
    'mezze-mediterraneo': 'mezze meze charuto folha de uva', shawarma: 'shawarma xawarma sanduiche wrap', 'kebab-bodrum': 'kebab file mignon turco',
    tabule: 'tabbouleh salada trigo', 'cafe-turco': 'cafe', 'cha-turco': 'cha', mamul: 'maamoul doce', 'doces-variados': 'doce sobremesa',
    'combo-vegie': 'vegetariano combo', suudinho: 'infantil crianca kids'
  };

  const brl = v => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  const norm = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const wait = ms => new Promise(r => setTimeout(r, reduce ? 0 : ms));

  /* ---------- Estado ---------- */
  const state = { cart: new Map(), mode: null, started: false, flow: 0, pending: null, opener: null, followed: false };
  try {
    const saved = JSON.parse(sessionStorage.getItem('suud-cart') || '[]');
    saved.forEach(([id, q]) => byId[id] && q > 0 && state.cart.set(id, q));
  } catch (e) { /* armazenamento indisponível */ }
  const persist = () => { try { sessionStorage.setItem('suud-cart', JSON.stringify([...state.cart])); } catch (e) {} };

  const cartInfo = () => {
    let qty = 0, total = 0, unpriced = 0;
    state.cart.forEach((q, id) => { qty += q; const p = byId[id].price; if (p == null) unpriced += q; else total += p * q; });
    return { qty, total, unpriced };
  };

  function updateCart(bump) {
    const { qty, total, unpriced } = cartInfo();
    $$('[data-cart-count]').forEach(b => {
      b.textContent = qty; b.hidden = qty === 0;
      if (bump && qty) { b.classList.remove('is-bump'); void b.offsetWidth; b.classList.add('is-bump'); }
    });
    cartBar.hidden = qty === 0;
    $('[data-cart-qty]', cartBar).textContent = qty === 1 ? '1 item' : `${qty} itens`;
    $('[data-cart-total]', cartBar).textContent = brl(total) + (unpriced ? ' + itens a confirmar' : '') + ' · estimado';
    if (bump && qty) { cartBar.classList.remove('is-bump'); void cartBar.offsetWidth; cartBar.classList.add('is-bump'); }
    if (mini) {
      mini.hidden = qty === 0;
      $('[data-mini-qty]', mini).textContent = qty === 1 ? '1 item' : `${qty} itens`;
      $('[data-mini-total]', mini).textContent = brl(total) + (unpriced ? ' + a confirmar' : '');
      if (bump && qty) { mini.classList.remove('is-bump'); void mini.offsetWidth; mini.classList.add('is-bump'); }
    }
    root.classList.toggle('has-cart', qty > 0);
    $$('.dish[data-id]').forEach(li => {
      const b = $('.dish__add', li); if (!b) return;
      const q = state.cart.get(li.dataset.id);
      q ? b.setAttribute('data-count', q) : b.removeAttribute('data-count');
    });
    persist();
  }

  /* ---------- Abrir / fechar ---------- */
  /* Na página inicial o Ahlan fica aberto dentro da capa */
  const homeSlot = $('[data-ahlan-home]');
  function embed() {
    if (!homeSlot) return false;
    homeSlot.appendChild(panel);
    panel.classList.add('is-embedded');
    panel.style.removeProperty('top');
    box.dataset.state = 'embedded';
    return true;
  }
  function unembed() {
    if (panel.parentElement === box) return;
    box.insertBefore(panel, box.children[1]);
    panel.classList.remove('is-embedded');
  }

  function open(anchor = 'auto', intent = null) {
    const floating = root.classList.contains('is-floating');
    if (homeSlot && !floating && anchor !== 'launcher') {
      if (panel.parentElement !== homeSlot) embed();
      hideToast();
      if (window.SuudMenu) window.SuudMenu.close();
      if (!state.started) start(intent); else if (intent) handleIntent(intent);
      if (isMobile()) window.SuudScroll && window.SuudScroll.to(homeSlot, -10);
      else setTimeout(() => input.focus({ preventScroll: true }), 200);
      scrollLog();
      return;
    }
    unembed();
    box.dataset.anchor = anchor === 'auto' ? (floating ? 'launcher' : 'header') : anchor;
    if (box.dataset.anchor === 'header' && !isMobile()) panel.style.top = Math.max(0, header.getBoundingClientRect().bottom) + 'px';
    launcher.classList.toggle('is-pinned', box.dataset.anchor === 'launcher');
    const wasOpen = box.dataset.state === 'open';
    box.dataset.state = 'open';
    root.classList.add('ahlan-open');
    root.classList.remove('is-hidden-header');
    hideToast();
    if (window.SuudMenu) window.SuudMenu.close();
    if (isMobile() && window.SuudScroll) window.SuudScroll.stop();
    if (!wasOpen) setTimeout(() => { if (!isMobile()) input.focus({ preventScroll: true }); else panel.focus({ preventScroll: true }); }, 420);
    if (!state.started) start(intent);
    else if (intent) handleIntent(intent);
    scrollLog();
  }
  function close() {
    if (box.dataset.state !== 'open') return;
    box.dataset.state = 'closed';
    root.classList.remove('ahlan-open');
    panel.style.removeProperty('--drag');
    if (window.SuudScroll) window.SuudScroll.start();
    setTimeout(() => launcher.classList.remove('is-pinned'), 700);
    if (state.opener && document.contains(state.opener)) state.opener.focus({ preventScroll: true });
    if (homeSlot) setTimeout(() => { if (box.dataset.state !== 'open') embed(); }, 750);
  }

  document.addEventListener('click', e => {
    const opener = e.target.closest('[data-ahlan-open]');
    if (opener) {
      e.preventDefault();
      if (opener === launcher && box.dataset.state === 'open') { close(); return; }
      state.opener = opener;
      const anchor = (opener === launcher || opener.closest('.dock')) ? 'launcher' : opener.closest('.site-header') ? 'header' : 'auto';
      open(anchor, opener.dataset.ahlanIntent || null);
      return;
    }
    const addBtn = e.target.closest('[data-ahlan-add]');
    if (addBtn) {
      const id = addBtn.dataset.ahlanAdd;
      state.opener = addBtn;
      add(id, 'cta');
      if (box.dataset.state !== 'open') open('auto', () => afterPageAdd(id));
      else afterPageAdd(id);
      return;
    }
    if (e.target.closest('[data-ahlan-close]')) { close(); return; }
    const dishAdd = e.target.closest('.dish__add');
    if (dishAdd) {
      const id = dishAdd.closest('.dish').dataset.id;
      add(id, 'page');
      dishAdd.classList.remove('is-added'); void dishAdd.offsetWidth; dishAdd.classList.add('is-added');
      clearTimeout(dishAdd._t); dishAdd._t = setTimeout(() => dishAdd.classList.remove('is-added'), 1400);
    }
  });
  $('[data-ahlan-review]', box).addEventListener('click', () => runFlow(review));
  $('[data-ahlan-restart]', box).addEventListener('click', () => {
    state.flow++; resolvePending(null);
    chain = Promise.resolve();
    log.innerHTML = '';
    state.started = false; state.followed = false;
    start();
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && box.dataset.state === 'open') close(); });

  /* Arrastar para fechar (mobile) */
  (() => {
    const head = $('.ahlan__head', box);
    let y0 = null, dy = 0;
    head.addEventListener('pointerdown', e => { if (!isMobile() || e.target.closest('button')) return; y0 = e.clientY; dy = 0; box.classList.add('is-dragging'); head.setPointerCapture(e.pointerId); });
    head.addEventListener('pointermove', e => { if (y0 == null) return; dy = Math.max(0, e.clientY - y0); panel.style.setProperty('--drag', dy + 'px'); });
    const end = () => { if (y0 == null) return; box.classList.remove('is-dragging'); y0 = null; if (dy > 110) close(); else panel.style.setProperty('--drag', '0px'); };
    head.addEventListener('pointerup', end); head.addEventListener('pointercancel', end);
  })();

  /* ---------- Mensagens ---------- */
  let chain = Promise.resolve();
  const scrollLog = () => requestAnimationFrame(() => log.scrollTo({ top: log.scrollHeight, behavior: reduce ? 'auto' : 'smooth' }));

  function node(cls, html) {
    const m = document.createElement('div');
    m.className = 'm ' + cls;
    m.innerHTML = `<div class="m__b">${html}</div>`;
    log.appendChild(m); scrollLog();
    return m;
  }
  function say(html, delay) {
    const myFlow = state.flow;
    chain = chain.then(async () => {
      if (myFlow !== state.flow) return;
      const t = document.createElement('div');
      t.className = 'typing'; t.setAttribute('role', 'status');
      t.innerHTML = '<span class="sr-only">Ahlan está digitando</span><i></i><i></i><i></i>';
      log.appendChild(t); scrollLog();
      const len = html.replace(/<[^>]+>/g, '').length;
      await wait(delay ?? Math.min(1100, 380 + len * 7));
      t.remove();
      if (myFlow !== state.flow) return;
      node('m--bot', html);
    });
    return chain;
  }
  const userSay = text => node('m--user', esc(text));
  const note = html => node('m--note', html);
  const after = fn => { const f = state.flow; chain = chain.then(() => f === state.flow && fn()); return chain; };

  function chips(list) {
    const wrap = document.createElement('div');
    wrap.className = 'chips';
    list.forEach((c, i) => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'chip' + (c.solid ? ' chip--solid' : '');
      b.style.setProperty('--n', i);
      b.textContent = c.label;
      b.addEventListener('click', () => {
        if (wrap.classList.contains('is-used')) return;
        wrap.classList.add('is-used'); b.classList.add('is-picked');
        if (!c.silent) userSay(c.label);
        c.action();
      });
      wrap.appendChild(b);
    });
    log.appendChild(wrap); scrollLog();
    return wrap;
  }

  function rail(items) {
    const r = document.createElement('div');
    r.className = 'rail';
    items.filter(Boolean).forEach(m => {
      const c = document.createElement('article');
      c.className = 'card';
      c.innerHTML = `<span class="card__cat">${esc(m.cat)}</span><h4>${esc(m.name)}</h4><p>${esc(m.desc)}</p>
        <div class="card__foot"><span class="card__price">${m.price == null ? 'consulte' : brl(m.price)}</span>
        <button class="card__add" type="button" aria-label="Adicionar ${esc(m.name)}"><svg aria-hidden="true"><use href="#i-plus"/></svg><span>Adicionar</span></button></div>`;
      const btn = $('.card__add', c);
      btn.addEventListener('click', () => {
        add(m.id, 'chat');
        btn.classList.add('is-added'); $('span', btn).textContent = `${state.cart.get(m.id)} no pedido`;
      });
      r.appendChild(c);
    });
    log.appendChild(r); scrollLog();
    return r;
  }

  /* ---------- Perguntas que esperam resposta ---------- */
  function resolvePending(v) { const p = state.pending; state.pending = null; input.placeholder = DEFAULT_PH; if (p) p.resolve(v); }
  function askChoice(question, options, { allowText = false, placeholder } = {}) {
    const f = state.flow;
    return new Promise(resolve => {
      say(question).then(() => {
        if (f !== state.flow) return resolve(null);
        const w = chips(options.map(o => ({ label: o, action: () => resolvePending(o) })));
        state.pending = { resolve: v => { w.classList.add('is-used'); resolve(v); }, options, allowText };
        if (allowText) input.placeholder = placeholder || 'Ou escreva aqui…';
      });
    });
  }
  function askText(question, placeholder) {
    const f = state.flow;
    return new Promise(resolve => {
      say(question).then(() => {
        if (f !== state.flow) return resolve(null);
        state.pending = { resolve, text: true };
        input.placeholder = placeholder || 'Escreva aqui…';
        if (!isMobile()) input.focus({ preventScroll: true });
      });
    });
  }
  function runFlow(fn, ...args) {
    state.flow++;
    resolvePending(null);
    return fn(state.flow, ...args);
  }

  /* ---------- Fluxos ---------- */
  function greeting() {
    const h = new Date().getHours();
    return h < 12 ? 'Bom dia' : h < 18 ? 'Boa tarde' : 'Boa noite';
  }
  function start(intent) {
    state.started = true;
    say(`<strong>Ahlan wa sahlan!</strong> ${greeting()}.`, 450);
    say('Sou o Ahlan, do Suud. Monto seu pedido de delivery, preparo uma retirada ou reservo sua mesa. Se tiver dúvida sobre algum prato, é só perguntar.');
    after(() => {
      if (typeof intent === 'function') intent();
      else if (intent) handleIntent(intent);
      else mainChips();
    });
  }
  function mainChips() {
    chips([
      { label: 'Pedir delivery', action: () => runFlow(setMode, 'delivery') },
      { label: 'Retirar no Suud', action: () => runFlow(setMode, 'retirada') },
      { label: 'Reservar mesa', action: () => runFlow(booking) },
      { label: 'Me sugere algo', action: () => runFlow(suggest) }
    ]);
  }
  function handleIntent(intent) {
    if (typeof intent === 'function') return intent();
    const map = {
      delivery: () => runFlow(setMode, 'delivery'),
      reserva: () => runFlow(booking),
      review: () => runFlow(review),
      suggest: () => runFlow(suggest),
      evento: () => runFlow(events)
    };
    (map[intent] || mainChips)();
  }

  function setMode(f, mode) {
    state.mode = mode;
    say(mode === 'delivery'
      ? 'Perfeito, delivery. O que vai à mesa hoje?'
      : `Combinado: você retira aqui na ${ADDRESS}. O que vai querer?`);
    after(categoryChips);
  }
  function categoryChips(extra = true) {
    const list = CATS.map(c => ({ label: c.name, action: () => runFlow(showCat, c) }));
    if (extra) list.push({ label: 'Sugestões da casa', action: () => runFlow(suggest) });
    if (state.cart.size) list.push({ label: 'Revisar pedido', solid: true, action: () => runFlow(review) });
    chips(list);
  }
  function showCat(f, c) {
    say(CAT_INTRO[c.id] || c.name);
    after(() => rail(MENU.filter(m => m.catId === c.id)));
    after(() => chips([
      { label: 'Outras categorias', action: () => runFlow(() => { say('Claro. Qual delas?', 420); after(() => categoryChips(false)); }) },
      ...(state.cart.size ? [{ label: 'Revisar pedido', solid: true, action: () => runFlow(review) }] : [])
    ]));
    if (window.SuudMenuTabs) window.SuudMenuTabs.selectByPanel(c.id);
  }
  function suggest() {
    say('Se estiver em dúvida, comece por aqui:');
    say('<strong>Para dividir:</strong> Mezze Capadócia, com kafta, kibe e falafel lado a lado.<br><strong>Sem carne:</strong> falafel com hummus tahine e tabule.<br><strong>Para fechar:</strong> mamul com café turco.', 900);
    after(() => rail(['mezze-capadocia', 'falafel', 'hummus', 'tabule', 'mamul', 'cafe-turco'].map(id => byId[id])));
    after(() => categoryChips(false));
  }

  function add(id, source) {
    const m = byId[id];
    if (!m) return;
    state.cart.set(id, (state.cart.get(id) || 0) + 1);
    updateCart(true);
    if (navigator.vibrate && navigator.userActivation && navigator.userActivation.hasBeenActive) navigator.vibrate(12);
    const isOpen = box.dataset.state === 'open';
    if (source === 'page' && !isOpen && !isMobile()) {
      showToast({ msg: `<strong>${esc(m.name)}</strong> está no seu pedido.`, cta: 'Revisar pedido', action: () => open('launcher', 'review'), ttl: 4200, force: true });
    }
    if (source === 'page' && isOpen) note(`+ ${esc(m.name)} adicionado pelo cardápio`);
    if (source === 'chat') {
      if (!state.followed) {
        state.followed = true;
        clearTimeout(add._t);
        add._t = setTimeout(() => {
          if (state.pending) return;
          say('Anotado. Continue escolhendo que eu vou somando aqui embaixo.', 520);
          after(() => chips([
            { label: 'Outra categoria', action: () => runFlow(() => { say('Qual delas?', 380); after(() => categoryChips(false)); }) },
            { label: 'Revisar pedido', solid: true, action: () => runFlow(review) }
          ]));
        }, 900);
      }
    }
  }
  function afterPageAdd(id) {
    const m = byId[id];
    if (!m) return;
    say(`<strong>${esc(m.name)}</strong> está no seu pedido.`, 520);
    after(() => chips([
      { label: 'Revisar pedido', solid: true, action: () => runFlow(review) },
      { label: 'Continuar escolhendo', action: () => runFlow(() => { say('O que mais vai à mesa?', 420); after(() => categoryChips()); }) }
    ]));
  }

  function renderReview() {
    const wrap = document.createElement('div');
    wrap.className = 'review';
    const draw = () => {
      const { total, unpriced } = cartInfo();
      wrap.innerHTML = '';
      state.cart.forEach((q, id) => {
        const m = byId[id];
        const row = document.createElement('div');
        row.className = 'review__row';
        row.innerHTML = `<span class="review__name">${esc(m.name)}</span>
          <span class="stepper"><button type="button" aria-label="Remover um ${esc(m.name)}">−</button><span>${q}</span><button type="button" aria-label="Adicionar um ${esc(m.name)}">+</button></span>
          <span class="review__sub">${m.price == null ? 'a confirmar' : brl(m.price * q)}</span>`;
        const [minus, plus] = $$('button', row);
        minus.addEventListener('click', () => { const n = q - 1; n > 0 ? state.cart.set(id, n) : state.cart.delete(id); updateCart(); draw(); });
        plus.addEventListener('click', () => { state.cart.set(id, q + 1); updateCart(true); draw(); });
        wrap.appendChild(row);
      });
      if (!state.cart.size) { wrap.innerHTML = '<div class="review__row"><span class="review__name">Pedido vazio.</span></div>'; return; }
      const t = document.createElement('div');
      t.className = 'review__total';
      t.innerHTML = `<span>Total estimado${state.mode === 'delivery' ? ', sem taxa de entrega' : ''}${unpriced ? ' + itens a confirmar' : ''}</span><b>${brl(total)}</b>`;
      wrap.appendChild(t);
    };
    draw();
    log.appendChild(wrap); scrollLog();
  }
  function review() {
    if (!state.cart.size) {
      say('Seu pedido ainda está vazio. Que tal começar pelas pastas ou por um mezze?');
      after(() => categoryChips());
      return;
    }
    say('Aqui está o seu pedido. Ajuste as quantidades se quiser:', 520);
    after(renderReview);
    after(() => chips([
      { label: 'Continuar escolhendo', action: () => runFlow(() => { say('O que mais vai à mesa?', 400); after(() => categoryChips()); }) },
      { label: 'Finalizar pedido', solid: true, action: () => runFlow(checkout) }
    ]));
  }

  async function checkout(f) {
    if (!state.cart.size) return review();
    if (!state.mode) {
      const m = await askChoice('Vai ser delivery ou retirada aqui no Suud?', ['Delivery', 'Retirada no Suud']);
      if (m == null || f !== state.flow) return;
      state.mode = m === 'Delivery' ? 'delivery' : 'retirada';
    }
    const name = await askText('Para finalizar: qual é o seu nome?', 'Seu nome');
    if (name == null || f !== state.flow) return;
    let address = '';
    if (state.mode === 'delivery') {
      address = await askText(`Prazer, ${esc(name.split(' ')[0])}! Qual o endereço de entrega? Rua, número, complemento e bairro.`, 'Rua, número, bairro');
      if (address == null || f !== state.flow) return;
    }
    const pay = await askChoice(state.mode === 'delivery' ? 'Como prefere pagar?' : `Prazer, ${esc(name.split(' ')[0])}! Como prefere pagar?`, ['Pix', 'Cartão', 'Dinheiro']);
    if (pay == null || f !== state.flow) return;
    const obs = await askChoice('Alguma observação? Recheio das esfihas e kibes, ponto, sem cebola…', ['Sem observações'], { allowText: true, placeholder: 'Escreva sua observação…' });
    if (obs == null || f !== state.flow) return;

    const { total, unpriced } = cartInfo();
    const lines = [...state.cart].map(([id, q]) => { const m = byId[id]; return `${q}x ${m.name} — ${m.price == null ? 'a confirmar' : brl(m.price * q)}`; });
    const text = [
      'Olá, Suud! Quero fazer um pedido pelo site.',
      '',
      `*Pedido — ${state.mode === 'delivery' ? 'delivery' : 'retirada no Suud'}*`,
      ...lines,
      '',
      `Total estimado: ${brl(total)}${unpriced ? ' + itens a confirmar' : ''}${state.mode === 'delivery' ? ' (sem taxa de entrega)' : ''}`,
      '',
      `Nome: ${name}`,
      ...(address ? [`Endereço: ${address}`] : []),
      `Pagamento: ${pay}`,
      `Observações: ${obs}`
    ].join('\n');
    say('Pronto! Seu pedido está montado. É só enviar pelo WhatsApp que a equipe confirma valores, taxa e tempo de entrega.', 700);
    after(() => sendCard('Pedido pronto para enviar', text));
  }

  async function booking(f) {
    const people = await askChoice('Vamos reservar sua mesa. Para quantas pessoas?', ['2 pessoas', '3 a 4 pessoas', '5 a 8 pessoas', 'Mais de 8']);
    if (people == null || f !== state.flow) return;
    let when = await askChoice('Para quando?', ['Hoje', 'Amanhã', 'Este fim de semana', 'Outra data']);
    if (when == null || f !== state.flow) return;
    if (when === 'Outra data') { when = await askText('Qual data você prefere?', 'Ex.: sábado, 14/11'); if (when == null || f !== state.flow) return; }
    let time = await askChoice('E o horário?', ['Almoço', 'Fim de tarde', 'Jantar', 'Outro horário']);
    if (time == null || f !== state.flow) return;
    if (time === 'Outro horário') { time = await askText('Qual horário? Lembrando que abrimos das 11h às 22h.', 'Ex.: 20h30'); if (time == null || f !== state.flow) return; }
    const name = await askText('Em nome de quem fica a reserva?', 'Seu nome');
    if (name == null || f !== state.flow) return;
    const text = ['Olá, Suud! Gostaria de reservar uma mesa pelo site.', '', `Pessoas: ${people}`, `Quando: ${when}`, `Horário: ${time}`, `Nome: ${name}`].join('\n');
    say(`Perfeito, ${esc(name.split(' ')[0])}. Sua reserva está pronta para enviar; a equipe confirma a disponibilidade pelo WhatsApp.`, 700);
    after(() => sendCard('Reserva pronta para enviar', text));
  }

  function events() {
    say('O salão do Suud recebe aniversários, confraternizações, reuniões de família, aulas, palestras e eventos corporativos.');
    say('Conte para a equipe a data, o número de pessoas e o que você imagina. Eles apresentam as possibilidades do espaço.');
    after(() => sendCard('Falar sobre eventos', 'Olá, Suud! Gostaria de saber sobre eventos no espaço.\n\nData: \nNúmero de pessoas: \nTipo de evento: '));
  }

  function sendCard(title, text) {
    const c = document.createElement('div');
    c.className = 'send-card';
    c.innerHTML = `<h4>${esc(title)}</h4><pre>${esc(text)}</pre>
      <a href="https://wa.me/${WHATSAPP}?text=${encodeURIComponent(text)}" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#i-whats"/></svg>Enviar pelo WhatsApp</a>
      <small>Você revisa a mensagem no WhatsApp antes de enviar. Valores do site são de referência.</small>`;
    log.appendChild(c); scrollLog();
    after(() => chips([{ label: 'Voltar ao início', action: () => runFlow(() => { say('Em que mais posso ajudar?', 400); after(mainChips); }) }]));
  }

  /* ---------- Texto livre ---------- */
  form.addEventListener('submit', e => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    const p = state.pending;
    if (p && p.text) { userSay(text); resolvePending(text); return; }
    if (p && p.options) {
      const hit = p.options.find(o => norm(o) === norm(text));
      if (hit || p.allowText) { userSay(text); resolvePending(hit || text); return; }
    }
    userSay(text);
    runFlow(understand, text);
  });

  function search(q) {
    const words = norm(q).split(/[^a-z0-9]+/).filter(w => w.length > 2 && !['com', 'sem', 'uma', 'quero', 'para', 'que', 'tem', 'voces', 'pedir', 'gostaria'].includes(w));
    if (!words.length) return [];
    return MENU.map(m => {
      const hay = norm(`${m.name} ${ALIASES[m.id] || ''}`);
      const desc = norm(m.desc);
      let s = 0;
      words.forEach(w => { if (hay.includes(w)) s += 3; else if (desc.includes(w)) s += 1; });
      return { m, s };
    }).filter(x => x.s > 0).sort((a, b) => b.s - a.s).slice(0, 6).map(x => x.m);
  }

  const GLOSSARY = [
    { re: /nayee|kibe cru|quibe cru/, text: '<strong>Nayee</strong> é o kibe cru: carne bem temperada e trigo, servida crua. No Suud vem com cebola, hortelã e azeite.', ids: ['nayee', 'torre-nayee'] },
    { re: /labanie|labneh|coalhada/, text: '<strong>Labanie</strong> é a coalhada seca, cremosa e levemente ácida. Aqui ela é feita com leite orgânico.', ids: ['labanie'] },
    { re: /baba ?ganou?sh|baba ganuche|babaganuche/, text: '<strong>Babaganoush</strong> é a pasta de berinjela defumada. No Suud, ela vai misturada ao hummus tahine da casa.', ids: ['babaganoush'] },
    { re: /tahine|tahini/, text: '<strong>Tahine</strong> é a pasta de gergelim. Vai no hummus e no molho que acompanha falafel, kafta e shawarma.' },
    { re: /hummus|homus|humus/, text: '<strong>Hummus</strong> é a pasta de grão-de-bico com tahine e especiarias. Combina com pão árabe quente.', ids: ['hummus'] },
    { re: /falafel/, text: '<strong>Falafel</strong> é um bolinho frito de grão-de-bico, ervas e especiarias, servido com tahine. Não leva carne.', ids: ['falafel'] },
    { re: /maklie|kibe frito/, text: '<strong>Maklie</strong> é o kibe frito, crocante por fora e com recheio à sua escolha.', ids: ['kibe-frito', 'mini-kibe'] },
    { re: /il feren|kibe assado/, text: '<strong>Il Feren</strong> é o kibe assado no forno, com recheio à sua escolha.', ids: ['kibe-assado'] },
    { re: /kafta|kefta/, text: '<strong>Kafta</strong> é carne moída temperada com especiarias e grelhada no espeto. As mini kaftas vêm no pau de canela.', ids: ['kafta', 'mini-kafta'] },
    { re: /shawarma|xawarma/, text: '<strong>Shawarma</strong> é o sanduíche no pão folha, com folhas, tabule, molho de tahine e hortelã e cebola crispy.', ids: ['shawarma'] },
    { re: /tabule|tabbouleh/, text: '<strong>Tabule</strong> é a salada de trigo com tomate, cebolinha e hortelã.', ids: ['tabule'] },
    { re: /mamul|maamoul/, text: '<strong>Mamul</strong> é um doce de semolina recheado com tâmaras e castanhas, com água de flor de laranjeira.', ids: ['mamul'] },
    { re: /charuto|folha de uva/, text: '<strong>Charuto</strong> é a folha de uva enrolada e recheada. Ele aparece no Mezze Mediterrâneo.', ids: ['mezze-mediterraneo'] },
    { re: /mezze|meze/, text: '<strong>Mezze</strong> é uma seleção de pequenas porções servidas juntas, para todo mundo dividir. Temos três: Byblos, Capadócia e Mediterrâneo.', ids: ['mezze-byblos', 'mezze-capadocia', 'mezze-mediterraneo'] },
    { re: /arak|caipiarak/, text: '<strong>Arak</strong> é um destilado de anis. O Caipiarak leva arak, limão, açúcar, gelo e hortelã e é servido no salão.' }
  ];
  function glossary(t) {
    if (!/(o que e|o que eh|que e |significa|como e o|como e a|o que vem|explica)/.test(t)) return null;
    return GLOSSARY.find(g => g.re.test(t)) || null;
  }

  function understand(f, raw) {
    const t = norm(raw);
    const has = re => re.test(t);
    if (has(/^(oi|ola|opa|bom dia|boa tarde|boa noite|ahlan|salam|e ai)\b/)) { say(`${greeting()}! Como posso ajudar?`); return after(mainChips); }
    if (has(/obrigad|valeu|agradec/)) { say('Imagina! Bom apetite, e volte sempre.'); return; }
    if (has(/horario|abre|fecha|funciona|aberto|que horas/)) {
      say('O salão abre <strong>todos os dias, das 11h às 22h</strong>. Em feriados e nos aplicativos o horário pode variar.');
      return after(() => chips([{ label: 'Reservar mesa', action: () => runFlow(booking) }, { label: 'Pedir delivery', action: () => runFlow(setMode, 'delivery') }]));
    }
    if (has(/endereco|onde fica|onde voces|localiza|chegar|mapa|estacion/)) {
      say(`Estamos na <strong>${ADDRESS}</strong>. <a href="${MAPS}" target="_blank" rel="noopener">Abrir no Google Maps</a>`);
      return after(() => chips([{ label: 'Reservar mesa', action: () => runFlow(booking) }]));
    }
    if (has(/telefone|whats|contato|falar com|atendente humano|ligar/)) {
      say(`Nosso WhatsApp e telefone é o <strong>(21) 96771-7717</strong>. <a href="https://wa.me/${WHATSAPP}" target="_blank" rel="noopener">Abrir conversa</a>`);
      return;
    }
    if (has(/reserv|mesa para|mesa pra/)) return booking(f);
    if (has(/evento|aniversario|confraterniza|corporativ|festa|palestra|aula|reuniao/)) return events();
    if (has(/congelad/)) {
      say('Temos preparações congeladas para ter em casa. As opções variam; a equipe confirma o que está disponível hoje.');
      return after(() => sendCard('Perguntar sobre congelados', 'Olá, Suud! Quais congelados vocês têm disponíveis?'));
    }
    if (has(/encomenda|ceia|natal|fim de ano|reveillon/)) {
      say('Fazemos encomendas para ceias, festas e datas especiais. Conte para a equipe o que você precisa.');
      return after(() => sendCard('Fazer uma encomenda', 'Olá, Suud! Gostaria de fazer uma encomenda.\n\nData: \nPara quantas pessoas: \nO que gostaria: '));
    }
    if (has(/entrega|frete|taxa|demora|tempo de entrega|ifood|rappi/)) {
      say('Entregamos em Niterói. Taxa e tempo dependem do seu endereço e são confirmados pela equipe no WhatsApp, junto com o pedido.');
      return after(() => chips([{ label: 'Montar pedido de delivery', solid: true, action: () => runFlow(setMode, 'delivery') }]));
    }
    if (has(/pedido|carrinho|sacola|revisar|finaliz|fechar/)) return review();
    if (has(/vegan|vegetar|sem carne|nao como carne/)) {
      say('Sem carne, com muito sabor. Estas são as opções vegetarianas da casa:');
      after(() => rail(MENU.filter(m => m.veg)));
      say('Para dieta vegana, restrições ou alergias, vale confirmar os ingredientes com a equipe antes de pedir.', 700);
      return after(() => categoryChips(false));
    }
    const gloss = glossary(t);
    if (gloss) { say(gloss.text); if (gloss.ids) after(() => rail(gloss.ids.map(id => byId[id]).filter(Boolean))); return; }
    if (has(/sugest|recomend|indica|o que pedir|mais pedido|especialidade/)) return suggest();
    if (has(/^(cardapio|menu)|ver cardapio|o que tem|opcoes/)) { say('Por onde começamos?', 420); return after(() => categoryChips()); }
    if (has(/criança|crianca|infantil|kids/)) { say('Para os pequenos, o <strong>Suudinho</strong>: batata frita, mini kafta e arroz.'); return after(() => rail([byId.suudinho])); }
    if (has(/sobremesa|doce/)) return showCat(f, CATS.find(c => c.id === 'cat-doces'));
    if (has(/salada/)) return showCat(f, CATS.find(c => c.id === 'cat-pratos'));
    if (has(/pasta/)) return showCat(f, CATS.find(c => c.id === 'cat-pastas'));
    if (has(/bebida|drink|chopp|cerveja|vinho|refri|suco|caipiarak|arak/)) {
      say('No salão temos chopp, vinhos e drinks da casa, como o Caipiarak (arak, limão, açúcar e hortelã). No delivery, refrigerantes, águas e chás gelados: é só pedir nas observações.');
      return;
    }
    const found = search(raw);
    if (found.length) {
      say(found.length === 1 ? 'Encontrei no cardápio:' : 'Encontrei estas opções no cardápio:', 500);
      after(() => rail(found));
      return after(() => chips([{ label: 'Ver categorias', action: () => runFlow(() => { say('Qual delas?', 380); after(() => categoryChips(false)); }) }, ...(state.cart.size ? [{ label: 'Revisar pedido', solid: true, action: () => runFlow(review) }] : [])]));
    }
    say('Hmm, não encontrei isso por aqui. Posso mostrar o cardápio por categoria ou chamar a equipe no WhatsApp.');
    after(() => chips([
      { label: 'Ver cardápio', action: () => runFlow(() => { say('Por onde começamos?', 380); after(() => categoryChips()); }) },
      { label: 'Falar com a equipe', action: () => { window.open(`https://wa.me/${WHATSAPP}`, '_blank', 'noopener'); } }
    ]));
  }

  /* =========================================================
     Notificações contextuais no modo flutuante
     ========================================================= */
  const HINTS = {
    about: { msg: 'Oi, eu sou o Ahlan. Monto seu pedido aqui e mando pronto para o WhatsApp do Suud.', cta: 'Começar pedido', intent: 'delivery' },
    menu: { msg: 'Gostou de algum prato? Toque no <strong>+</strong> que eu guardo no seu pedido e vou somando.', cta: 'Me indica algo', intent: 'suggest' },
    mezze: { msg: 'O <strong>Mezze Capadócia</strong> traz três kaftas, três kibes e três falafels, com hummus e tabule.', cta: 'Pedir o Capadócia', add: 'mezze-capadocia' },
    delivery: { msg: 'Quer testar? Em 1 minuto o pedido fica pronto para enviar.', cta: 'Montar pedido', intent: 'delivery' },
    moments: { msg: 'Vai vir com a turma? Eu reservo a mesa com você em quatro toques.', cta: 'Reservar mesa', intent: 'reserva' },
    culture: { msg: 'Pensando em aniversário ou confraternização? Eu levo seu pedido para a equipe.', cta: 'Falar sobre eventos', intent: 'evento' },
    faq: { msg: 'Não achou a resposta? Pode me perguntar.', cta: 'Perguntar', intent: null },
    visit: { msg: 'Vai passar aqui? Reservo sua mesa agora.', cta: 'Reservar mesa', intent: 'reserva' }
  };
  const toast = { shown: 0, last: 0, dismissed: 0, seen: new Set(), timer: null, cartHinted: false, floatingSince: 0 };
  const toastMsg = $('.ahlan__toast-msg', toastEl);
  const toastCta = $('.ahlan__toast-cta', toastEl);
  let toastAction = null;

  function showToast({ msg, cta, action, ttl = 9000, force = false }) {
    const now = Date.now();
    if (box.dataset.state === 'open') return false;
    if (!force) {
      if (!root.classList.contains('is-floating')) return false;
      if (now - toast.last < (isMobile() ? 28000 : 20000) || now - toast.floatingSince < 1400) return false;
      toast.shown++;
    }
    toast.last = now;
    toastMsg.innerHTML = msg;
    toastCta.textContent = cta;
    toastAction = action;
    toastEl.hidden = false;
    requestAnimationFrame(() => toastEl.classList.add('is-in'));
    clearTimeout(toast.timer);
    toast.timer = setTimeout(hideToast, ttl);
    return true;
  }
  function hideToast() {
    clearTimeout(toast.timer);
    toastEl.classList.remove('is-in');
    setTimeout(() => { if (!toastEl.classList.contains('is-in')) toastEl.hidden = true; }, 500);
  }
  toastCta.addEventListener('click', () => { const a = toastAction; hideToast(); a && a(); });
  $('.ahlan__toast-x', toastEl).addEventListener('click', () => { toast.dismissed++; hideToast(); });

  function hintFor(zone) {
    const { qty, total } = cartInfo();
    if (qty && !toast.cartHinted && zone !== 'menu' && !isMobile()) {
      toast.cartHinted = true;
      return { msg: `Seu pedido tem <strong>${qty === 1 ? '1 item' : qty + ' itens'}</strong> · ${brl(total)}. Quando quiser, finalizo pelo WhatsApp.`, cta: 'Finalizar pedido', action: () => open('launcher', 'review') };
    }
    const h = HINTS[zone];
    if (!h) return null;
    return {
      msg: h.msg, cta: h.cta,
      action: () => {
        if (h.add) { add(h.add, 'hint'); open('launcher', () => afterPageAdd(h.add)); }
        else open('launcher', h.intent);
      }
    };
  }

  let currentZone = null;
  if ('IntersectionObserver' in window) {
    const zo = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        currentZone = e.target.dataset.ahlanZone;
        setTimeout(() => {
          const z = e.target.dataset.ahlanZone;
          if (z !== currentZone || z === 'hero') return;
          const h = hintFor(z);
          if (h && showToast(h)) toast.seen.add(z);
        }, 1600);
      });
    }, { rootMargin: '-35% 0px -45% 0px' });
    $$('[data-ahlan-zone]').forEach(s => zo.observe(s));
  }
  // marca quando entrou no modo flutuante
  let wasFloating = root.classList.contains('is-floating');
  new MutationObserver(() => {
    const floating = root.classList.contains('is-floating');
    if (floating === wasFloating) return;
    wasFloating = floating;
    if (floating) toast.floatingSince = Date.now();
    else { toast.floatingSince = 0; hideToast(); }
  }).observe(root, { attributes: true, attributeFilter: ['class'] });

  /* Barra "Pergunte ao Ahlan" dentro das páginas */
  function ask(text) {
    const anchor = root.classList.contains('is-floating') ? 'launcher' : 'header';
    open(anchor, text ? () => { userSay(text); runFlow(understand, text); } : null);
  }
  $$('[data-ahlan-ask]').forEach(f => f.addEventListener('submit', e => {
    e.preventDefault();
    const inp = $('input', f); const t = inp.value.trim(); inp.value = '';
    ask(t);
  }));
  $$('[data-ahlan-say]').forEach(b => b.addEventListener('click', () => ask(b.dataset.ahlanSay)));

  if (embed()) start();
  updateCart();
  window.Ahlan = { open, close, add, ask };
})();
