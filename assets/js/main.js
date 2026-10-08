/* SUUD — interações do site */
(() => {
  const root = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = () => matchMedia('(max-width: 860px)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const navH = () => parseInt(getComputedStyle(root).getPropertyValue('--nav-h')) || 72;

  /* ---------- Scroll suave (Lenis) ---------- */
  let lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new window.Lenis({ duration: 1.15, easing: t => 1 - Math.pow(1 - t, 4), smoothWheel: true });
    const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }
  window.SuudScroll = {
    to(target, offset = 0) {
      const el = typeof target === 'string' ? $(target) : target;
      if (!el) return;
      const off = -navH() - 8 + offset;
      if (lenis) lenis.scrollTo(el, { offset: off, duration: 1.4 });
      else window.scrollTo({ top: el.getBoundingClientRect().top + scrollY + off, behavior: reduce ? 'auto' : 'smooth' });
    },
    top() { lenis ? lenis.scrollTo(0, { duration: 1.4 }) : scrollTo({ top: 0, behavior: 'smooth' }); },
    stop() { lenis && lenis.stop(); },
    start() { lenis && lenis.start(); }
  };

  /* ---------- Entrada ---------- */
  const ready = () => requestAnimationFrame(() => root.classList.add('is-loaded'));
  Promise.race([document.fonts ? document.fonts.ready : Promise.resolve(), new Promise(r => setTimeout(r, 1200))]).then(ready);

  /* ---------- Revelação no scroll ---------- */
  const revealEls = $$('.reveal');
  const groups = new Map();
  revealEls.forEach(el => {
    const p = el.parentElement;
    const idx = groups.get(p) || 0;
    el.style.setProperty('--i', Math.min(idx, 6));
    groups.set(p, idx + 1);
  });
  const fadeEls = $$('.reveal-fade');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        const el = e.target;
        if (e.isIntersecting) { el.classList.add('is-in'); el.classList.remove('is-past'); }
        else if (e.boundingClientRect.top < 0) { el.classList.remove('is-in'); el.classList.add('is-past'); }
        else { el.classList.remove('is-in', 'is-past'); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    revealEls.concat(fadeEls).forEach(el => io.observe(el));
  } else revealEls.concat(fadeEls).forEach(el => el.classList.add('is-in'));

  /* ---------- Header, dock e modo flutuante ---------- */
  const hero = $('.hero');
  const intro = $('.intro');
  const dockProgress = $('.dock__progress');
  let lastY = scrollY, ticking = false;
  const onScroll = () => {
    const y = scrollY;
    const heroEnd = (hero ? hero.offsetHeight : 400) + (intro ? intro.offsetHeight : 0) - 80;
    root.classList.toggle('is-scrolled', y > 12);
    root.classList.toggle('is-floating', y > heroEnd);
    if (!root.classList.contains('menu-open') && !root.classList.contains('ahlan-open')) {
      if (y > lastY + 6 && y > heroEnd) root.classList.add('is-hidden-header');
      else if (y < lastY - 6 || y < heroEnd) root.classList.remove('is-hidden-header');
    }
    if (dockProgress) {
      const max = document.documentElement.scrollHeight - innerHeight;
      dockProgress.style.setProperty('--p', max > 0 ? (y / max).toFixed(4) : 0);
    }
    lastY = y;
    parallax();
    ticking = false;
  };
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });

  const pEls = reduce ? [] : $$('[data-parallax]');
  function parallax() {
    const vh = innerHeight;
    pEls.forEach(el => {
      const r = el.parentElement.getBoundingClientRect();
      if (r.bottom < -100 || r.top > vh + 100) return;
      const k = parseFloat(el.dataset.parallax) || 0;
      el.style.transform = `translate3d(0, ${((r.top + r.height / 2 - vh / 2) * k).toFixed(1)}px, 0)`;
    });
  }
  onScroll();

  /* ---------- Link ativo (header e dock) ---------- */
  const navLinks = $$('.nav a[href^="#"], .dock__item[href^="#"]');
  const sections = [...new Set(navLinks.map(a => a.getAttribute('href')))].map(h => $(h)).filter(Boolean);
  if ('IntersectionObserver' in window) {
    const so = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        navLinks.forEach(a => {
          const on = a.getAttribute('href') === '#' + e.target.id;
          a.setAttribute('aria-current', on ? 'true' : 'false');
          a.classList.toggle('is-active', on);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(s => so.observe(s));
  }

  /* ---------- Âncoras internas ---------- */
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute('href');
    if (id.length < 2) return;
    const target = $(id);
    if (!target) return;
    e.preventDefault();
    closeMenu();
    if (a.dataset.menuTab) {
      window.SuudMenuTabs && window.SuudMenuTabs.selectByPanel(a.dataset.menuTab);
      window.SuudScroll.to('.menu-board', 0);
      return;
    }
    if (id === '#topo') window.SuudScroll.top(); else window.SuudScroll.to(target);
    history.replaceState(null, '', id);
  });

  /* ---------- Menu mobile ---------- */
  const toggle = $('.menu-toggle');
  const mobileMenu = $('#mobile-menu');
  function closeMenu() {
    if (!root.classList.contains('menu-open')) return;
    root.classList.remove('menu-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.querySelector('.sr-only').textContent = 'Abrir menu';
    mobileMenu.setAttribute('aria-hidden', 'true');
    window.SuudScroll.start();
  }
  toggle && toggle.addEventListener('click', () => {
    const open = !root.classList.contains('menu-open');
    root.classList.toggle('menu-open', open);
    root.classList.remove('is-hidden-header');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.sr-only').textContent = open ? 'Fechar menu' : 'Abrir menu';
    mobileMenu.setAttribute('aria-hidden', String(!open));
    open ? window.SuudScroll.stop() : window.SuudScroll.start();
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
  window.SuudMenu = { close: closeMenu };

  /* ---------- Abas do cardápio (com swipe no mobile) ---------- */
  const tabs = $$('.menu-tabs [role="tab"]');
  const ink = $('.menu-tabs__ink');
  const tabBar = $('.menu-tabs');
  const current = () => tabs.findIndex(t => t.getAttribute('aria-selected') === 'true');
  const moveInk = tab => {
    if (!ink || !tab) return;
    ink.style.width = tab.offsetWidth + 'px';
    ink.style.transform = `translateX(${tab.offsetLeft}px)`;
  };
  const select = (tab, { focus = false, dir = 0 } = {}) => {
    tabs.forEach(t => {
      const on = t === tab;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      const panel = document.getElementById(t.getAttribute('aria-controls'));
      panel.classList.toggle('is-active', on);
      panel.classList.toggle('from-right', on && dir > 0);
      panel.classList.toggle('from-left', on && dir < 0);
      panel.hidden = !on;
    });
    moveInk(tab);
    if (focus) tab.focus();
    if (tabBar.scrollWidth > tabBar.clientWidth) tabBar.scrollTo({ left: tab.offsetLeft - tabBar.clientWidth / 2 + tab.offsetWidth / 2, behavior: 'smooth' });
  };
  $$('.menu-cat').forEach(panel => $$('.dish', panel).forEach((d, i) => d.style.setProperty('--n', i)));
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(tab, { dir: i - current() }));
    tab.addEventListener('keydown', e => {
      const k = e.key;
      if (!['ArrowRight', 'ArrowLeft', 'Home', 'End'].includes(k)) return;
      e.preventDefault();
      const n = k === 'Home' ? 0 : k === 'End' ? tabs.length - 1 : (i + (k === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
      select(tabs[n], { focus: true, dir: n - i });
    });
  });
  if (tabs.length) select(tabs[0]);
  window.addEventListener('resize', () => moveInk(tabs[current()]));
  if (document.fonts) document.fonts.ready.then(() => moveInk(tabs[current()]));
  window.SuudMenuTabs = { selectByPanel(id) { const t = tabs.find(t => t.getAttribute('aria-controls') === id); t && select(t, { dir: tabs.indexOf(t) - current() }); } };

  const panels = $('.menu-panels');
  if (panels) {
    let x0 = null, y0 = null;
    panels.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
    panels.addEventListener('touchend', e => {
      if (x0 == null) return;
      const dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      x0 = null;
      if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.4) return;
      const i = current(), n = i + (dx < 0 ? 1 : -1);
      if (n < 0 || n >= tabs.length) return;
      select(tabs[n], { dir: dx < 0 ? 1 : -1 });
      if (navigator.vibrate && navigator.userActivation && navigator.userActivation.hasBeenActive) navigator.vibrate(8);
    }, { passive: true });
  }

  /* ---------- Trio: destaque do card central no carrossel mobile ---------- */
  const trio = $('.trio');
  if (trio && 'IntersectionObserver' in window) {
    const cards = $$('.trio__panel', trio);
    const to = new IntersectionObserver(entries => {
      entries.forEach(e => e.target.classList.toggle('is-center', e.intersectionRatio > .5));
      if (isMobile() && cards.some(c => c.classList.contains('is-center'))) trio.classList.add('trio--ready');
    }, { root: trio, threshold: [0, .6, 1] });
    cards.forEach(c => to.observe(c));
    const centerFalafel = () => { if (isMobile()) { const f = cards[1]; trio.scrollLeft = f.offsetLeft - (trio.clientWidth - f.offsetWidth) / 2; } };
    if (document.readyState === 'complete') centerFalafel(); else window.addEventListener('load', centerFalafel);
  }

  /* ---------- Prévia do Ahlan no celular ---------- */
  const demoLog = $('[data-demo-log]');
  const demoCart = $('[data-demo-cart]');
  if (demoLog && !reduce) {
    const W = ms => new Promise(r => setTimeout(r, ms));
    const add = (cls, html) => { const d = document.createElement('div'); d.className = cls; d.innerHTML = html; demoLog.appendChild(d); while (demoLog.children.length > 7) demoLog.firstChild.remove(); return d; };
    const typing = async ms => { const t = add('dm-typing', '<i></i><i></i><i></i>'); await W(ms); t.remove(); };
    let running = false, visible = false;
    const play = async () => {
      if (running) return; running = true;
      while (visible) {
        demoLog.innerHTML = ''; demoCart.classList.remove('is-on');
        await W(500);
        add('dm dm--user', 'Oi! Quero pedir um mezze para hoje à noite');
        await typing(1100);
        add('dm dm--bot', '<b>Ahlan!</b> Delivery ou retirada aqui no Suud?');
        const ch = add('dm dm--chips', '<i>Delivery</i><i>Retirada</i><i>Reservar mesa</i>');
        await W(1100); ch.firstElementChild.classList.add('is-on');
        await typing(900);
        add('dm dm--bot', 'Perfeito. Estes são os mezzes:');
        const card = add('dm dm--card', '<small>Mezzes &amp; torres</small><b>Mezze Capadócia</b><span>R$ 107,90 <i>Adicionar</i></span>');
        await W(1300); card.querySelector('i').classList.add('is-added'); card.querySelector('i').textContent = '1 no pedido';
        demoCart.classList.add('is-on');
        await typing(1000);
        add('dm dm--bot', 'Anotado! Nome, endereço e pagamento e eu monto a mensagem.');
        await W(1200);
        add('dm dm--send', '<pre>*Pedido — delivery*\n1x Mezze Capadócia — R$ 107,90\nPagamento: Pix</pre><em>Enviar pelo WhatsApp</em>');
        await W(4200);
      }
      running = false;
    };
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) play(); }, { threshold: .35 }).observe(demoLog.closest('.demo'));
  } else if (demoLog) {
    demoLog.innerHTML = '<div class="dm dm--user">Oi! Quero pedir um mezze</div><div class="dm dm--bot"><b>Ahlan!</b> Delivery ou retirada?</div><div class="dm dm--send"><pre>*Pedido — delivery*\n1x Mezze Capadócia — R$ 107,90</pre><em>Enviar pelo WhatsApp</em></div>';
  }

  /* ---------- Carrossel de mezze ---------- */
  const mz = $('.mezze-carousel');
  if (mz) {
    const slides = $$('.mezze-slide', mz), dots = $$('.mezze-dots button', mz);
    let idx = 1;
    const show = n => {
      idx = (n + slides.length) % slides.length;
      slides.forEach((sl, i) => {
        const d = (i - idx + slides.length) % slides.length;
        sl.dataset.pos = d === 0 ? 'active' : d === 1 ? 'next' : 'prev';
        sl.setAttribute('aria-hidden', String(d !== 0));
        $$('button', sl).forEach(b => b.tabIndex = d === 0 ? 0 : -1);
      });
      dots.forEach((b, i) => b.setAttribute('aria-selected', String(i === idx)));
    };
    show(idx);
    $('.mz-arrow--prev', mz).addEventListener('click', () => show(idx - 1));
    $('.mz-arrow--next', mz).addEventListener('click', () => show(idx + 1));
    dots.forEach((b, i) => b.addEventListener('click', () => show(i)));
    mz.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') show(idx - 1); if (e.key === 'ArrowRight') show(idx + 1); });
    let x0 = null, dx = 0;
    mz.addEventListener('pointerdown', e => { if (e.target.closest('button')) return; x0 = e.clientX; dx = 0; mz.classList.add('is-drag'); });
    window.addEventListener('pointermove', e => {
      if (x0 == null) return; dx = e.clientX - x0;
      const a = slides[idx]; a.style.transform = `translateX(${dx}px) rotate(${dx / 40}deg)`;
    });
    window.addEventListener('pointerup', () => {
      if (x0 == null) return; mz.classList.remove('is-drag'); slides[idx].style.transform = '';
      if (Math.abs(dx) > 60) show(idx + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  }

  /* ---------- Setas do trio e dos momentos ---------- */
  const scrollByCard = (track, dir) => {
    const card = track.firstElementChild; if (!card) return;
    track.scrollBy({ left: dir * (card.getBoundingClientRect().width + 16), behavior: reduce ? 'auto' : 'smooth' });
  };
  $$('.trio-wrap').forEach(w => {
    const t = $('.trio', w);
    $('.trio-arrow--prev', w).addEventListener('click', () => scrollByCard(t, -1));
    $('.trio-arrow--next', w).addEventListener('click', () => scrollByCard(t, 1));
  });
  const mom = $('.moments');
  if (mom) {
    const rail = $('.moments__rail', mom);
    $$('.moment', mom).forEach((m, i) => m.style.setProperty('--k', i));
    $('[data-rail-prev]', mom).addEventListener('click', () => scrollByCard(rail, -1));
    $('[data-rail-next]', mom).addEventListener('click', () => scrollByCard(rail, 1));
    if ('IntersectionObserver' in window && !reduce) {
      new IntersectionObserver(([e]) => mom.classList.toggle('is-in', e.isIntersecting), { threshold: .2 }).observe(mom);
    } else mom.classList.add('is-in');
  }

  /* ---------- Abas do cardápio pelo endereço (#cat-...) ---------- */
  const openTabFromHash = () => {
    const h = location.hash.slice(1);
    if (h.startsWith('cat-') && window.SuudMenuTabs) { window.SuudMenuTabs.selectByPanel(h); setTimeout(() => window.SuudScroll.to('.menu-board'), 300); }
  };
  openTabFromHash();
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="cardapio.html#cat-"]');
    if (a && $('.menu-board')) { e.preventDefault(); history.replaceState(null, '', a.hash); openTabFromHash(); }
  });

  /* ---------- Menu "Opções" (desktop) ---------- */
  $$('.nav-more').forEach(m => {
    const btn = $('.nav-more__btn', m);
    btn.addEventListener('click', e => { e.stopPropagation(); const o = !m.classList.contains('is-open'); m.classList.toggle('is-open', o); btn.setAttribute('aria-expanded', String(o)); });
    document.addEventListener('click', e => { if (!m.contains(e.target) || e.target.closest('.nav-more__panel a, .nav-more__panel button')) { m.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); } });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') { m.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); } });
  });

  /* ---------- Cardápio: busca e filtro vegetariano ---------- */
  const search = $('[data-menu-search]'), veg = $('[data-menu-veg]'), empty = $('[data-menu-empty]');
  if (search && veg) {
    const norm = t => t.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    const apply = () => {
      const q = norm(search.value.trim()), onlyVeg = veg.getAttribute('aria-pressed') === 'true';
      const filtering = q || onlyVeg;
      let shown = 0;
      $$('.menu-cat').forEach(cat => {
        let n = 0;
        $$('.dish', cat).forEach(d => {
          const ok = (!q || norm(d.textContent).includes(q)) && (!onlyVeg || (d.dataset.tags || '').includes('veg'));
          d.classList.toggle('is-hidden', !ok); if (ok) n++;
        });
        if (filtering) { cat.hidden = n === 0; cat.classList.toggle('is-active', n > 0); }
        shown += n;
      });
      if (!filtering) { const t = $('.menu-tabs [aria-selected="true"]'); window.SuudMenuTabs.selectByPanel(t.getAttribute('aria-controls')); }
      $('.menu-tabs').style.display = filtering ? 'none' : '';
      empty.hidden = shown > 0;
    };
    search.addEventListener('input', apply);
    veg.addEventListener('click', () => { veg.setAttribute('aria-pressed', String(veg.getAttribute('aria-pressed') !== 'true')); apply(); });
  }

  /* ---------- Ano no rodapé ---------- */
  $$('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
})();
