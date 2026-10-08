# Gera as páginas do site do Suud a partir de um layout comum.
# Uso: python _build/build.py   (a partir da pasta site/)
import json, re, html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, '_build')
SPRITE = open(os.path.join(B, 'sprite.html'), encoding='utf-8').read()
PANELS = open(os.path.join(B, 'panels.html'), encoding='utf-8').read()
DOMAIN = 'https://www.SEUDOMINIO.com.br/'  # TROCAR pelo domínio definitivo
V = '41'

EXTRA_ICONS = '''
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
  <symbol id="s-menu" viewBox="0 0 24 24"><path fill="currentColor" d="M5 3h11a3 3 0 0 1 3 3v15l-3-2-3 2-3-2-3 2-2-1.4V5a2 2 0 0 1 2-2Zm2 5v2h8V8H7Zm0 4v2h8v-2H7Zm0 4v2h5v-2H7Z"/></symbol>
  <symbol id="s-sum" viewBox="0 0 24 24"><path fill="currentColor" d="M6 2h12a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2Zm1 3v4h10V5H7Zm0 7v2h2v-2H7Zm4 0v2h2v-2h-2Zm4 0v6h2v-6h-2Zm-8 4v2h2v-2H7Zm4 0v2h2v-2h-2Z"/></symbol>
  <symbol id="s-check" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.7 14.9L2 22l5.2-1.3A10 10 0 1 0 12 2Zm-1.2 13.8-3.6-3.6 1.4-1.4 2.2 2.2 5-5 1.4 1.4-6.4 6.4Z"/></symbol>
  <symbol id="s-question" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm1 16h-2v-2h2v2Zm1.6-6.6-.9.9c-.6.6-.9 1.1-.9 2.2h-1.9v-.5c0-1.1.4-2 1.1-2.7l1.2-1.2a1.7 1.7 0 0 0 .5-1.3 1.8 1.8 0 0 0-3.6 0H8.3a3.7 3.7 0 0 1 7.4 0c0 1-.4 1.9-1.1 2.6Z"/></symbol>
  <symbol id="s-insta" viewBox="0 0 24 24"><path fill="currentColor" d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3Zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6Zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0ZM12 4.6c2.4 0 2.7 0 3.6.1 2.4.1 3.6 1.3 3.7 3.7.1 1 .1 1.2.1 3.6s0 2.7-.1 3.6c-.1 2.4-1.3 3.6-3.7 3.7-1 .1-1.2.1-3.6.1s-2.7 0-3.6-.1c-2.4-.1-3.6-1.3-3.7-3.7-.1-1-.1-1.2-.1-3.6s0-2.7.1-3.6C4.8 6 6 4.8 8.4 4.7c1-.1 1.2-.1 3.6-.1ZM12 3c-2.4 0-2.8 0-3.7.1C5 3.2 3.2 5 3.1 8.3 3 9.2 3 9.6 3 12s0 2.8.1 3.7c.1 3.3 1.9 5.1 5.2 5.2.9.1 1.3.1 3.7.1s2.8 0 3.7-.1c3.3-.1 5.1-1.9 5.2-5.2.1-.9.1-1.3.1-3.7s0-2.8-.1-3.7C20.8 5 19 3.2 15.7 3.1 14.8 3 14.4 3 12 3Z"/></symbol>
  <symbol id="s-whats" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2.2A9.8 9.8 0 0 0 3.6 17l-1.4 4.9 5-1.3A9.8 9.8 0 1 0 12 2.2Zm5.7 13.9c-.2.7-1.4 1.3-2 1.4-.5.1-1.2.1-1.9-.1-.4-.1-1-.3-1.7-.6-3-1.3-4.9-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3s.8-2.2 1-2.5c.3-.3.6-.4.8-.4h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.3.5-.4.5c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.7-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.1.1.7-.1 1.3Z"/></symbol>
  <symbol id="s-chevron-l" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M15 5l-7 7 7 7"/></symbol>
  <symbol id="s-chevron-r" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></symbol>
</defs></svg>'''

NAV = [('index.html', 'Início'), ('#opcoes', 'Opções'), ('cardapio.html', 'Cardápio'), ('delivery.html', 'Delivery'), ('index.html#mezze', 'Mezze'), ('nossa-historia.html', 'Nossa história')]
NAV_R = [('eventos.html', 'Eventos'), ('index.html#visite', 'Visite')]

def cedar_lines(width):
    return f'''<g fill="none" stroke="currentColor" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">
          <path pathLength="1" style="--d:0" d="M627 765V262"/>
          <polyline pathLength="1" style="--d:1" points="627,260 517,192 410,263"/><polyline pathLength="1" style="--d:1" points="627,260 737,192 845,263"/>
          <polyline pathLength="1" style="--d:2" points="627,372 517,303 410,372 358,337"/><polyline pathLength="1" style="--d:2" points="627,372 737,303 845,372 897,337"/>
          <polyline pathLength="1" style="--d:3" points="627,475 517,405 410,475 310,410"/><polyline pathLength="1" style="--d:3" points="627,475 737,405 845,475 942,410"/>
          <polyline pathLength="1" style="--d:4" points="627,572 517,505 410,572 305,505 250,540"/><polyline pathLength="1" style="--d:4" points="627,572 737,505 845,572 947,505 1005,540"/>
          <polyline pathLength="1" style="--d:5" points="627,675 513,607 405,675 297,605 195,670"/><polyline pathLength="1" style="--d:5" points="627,675 742,607 852,680 960,607 1058,670"/>
        </g>'''

def head(title, desc, path, schema_extra='', preload=''):
    url = DOMAIN + ('' if path == 'index.html' else path)
    restaurant = {
        "@context": "https://schema.org", "@type": "Restaurant", "@id": DOMAIN + "#restaurante",
        "name": "Suud Culinária Árabe",
        "description": "Restaurante de culinária árabe em Icaraí, Niterói, com mezzes para dividir, pastas, kibes, esfihas, falafel, doces árabes e café turco. Salão, delivery pelo WhatsApp e encomendas.",
        "url": DOMAIN, "image": DOMAIN + "assets/img/og-suud.jpg", "logo": DOMAIN + "assets/img/apple-touch-icon.png",
        "telephone": "+55-21-96771-7717",
        "address": {"@type": "PostalAddress", "streetAddress": "Rua Otávio Carneiro, 8", "addressLocality": "Niterói", "addressRegion": "RJ", "addressCountry": "BR"},
        "areaServed": [{"@type": "City", "name": "Niterói"}, {"@type": "Place", "name": "Icaraí, Niterói"}],
        "servesCuisine": ["Árabe", "Libanesa", "Síria", "Turca", "Mediterrânea"], "priceRange": "$$",
        "acceptsReservations": True, "hasMenu": DOMAIN + "cardapio.html",
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "11:00", "closes": "22:00"}],
        "sameAs": ["https://www.instagram.com/suud.restaurante/"]
    }
    return f'''<!doctype html>
<html lang="pt-BR" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#914B3C">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Suud Culinária Árabe">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}assets/img/og-suud.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@300..600&display=swap" rel="stylesheet">
{preload}<link rel="stylesheet" href="assets/css/style.css?v={V}">
<script>document.documentElement.classList.replace('no-js','js')</script>
<script type="application/ld+json">{json.dumps(restaurant, ensure_ascii=False)}</script>
{schema_extra}
</head>
<body class="page-{path.replace('.html','')}">
{SPRITE}
{EXTRA_ICONS}
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
'''

MORE = '''      <div class="nav-more">
        <button class="nav-more__btn" type="button" aria-expanded="false" aria-controls="nav-more-list">Opções<svg aria-hidden="true"><use href="#s-chevron-r"/></svg></button>
        <div class="nav-more__panel" id="nav-more-list">
          <a href="cardapio.html">Cardápio completo</a><a href="eventos.html">Eventos e cultura</a><a href="delivery.html">Delivery pelo WhatsApp</a>
          <a href="index.html#mezze">Mezze para dividir</a><a href="nossa-historia.html">Nossa história</a><a href="eventos.html">Eventos e cultura</a>
          <a href="index.html#perguntas">Perguntas frequentes</a><a href="index.html#visite">Como chegar</a>
          <button type="button" data-ahlan-open data-ahlan-intent="reserva">Reservar mesa</button>
        </div>
      </div>'''

def header(active):
    def link(h, t):
        cur = ' aria-current="page"' if h == active else ''
        return f'<a href="{h}"{cur}>{t}</a>'
    left = '\n      '.join(MORE if h == '#opcoes' else link(h, t) for h, t in NAV)
    right = '\n      '.join(link(h, t) for h, t in NAV_R)
    mob = '\n      '.join(f'<li><a href="{h}">{t}</a></li>' for h, t in [n for n in NAV if n[0] != '#opcoes'] + NAV_R + [('index.html#perguntas', 'Perguntas frequentes')])
    return f'''
<header class="site-header">
  <div class="topbar">
    <p class="topbar__text">
      <span class="topbar__live" aria-hidden="true"></span>
      <span class="topbar__long"><strong>Ahlan</strong>, o atendente do Suud no WhatsApp: escolha os pratos aqui, veja o total e envie o pedido pronto para a cozinha.</span>
      <span class="topbar__short"><strong>Ahlan</strong>: seu pedido pelo WhatsApp em 1 minuto</span>
    </p>
    <button class="topbar__cta" type="button" data-ahlan-open data-ahlan-intent="delivery">Pedir agora<svg aria-hidden="true"><use href="#i-arrow"/></svg></button>
  </div>
  <div class="navbar">
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu"><span class="sr-only">Abrir menu</span><span class="menu-toggle__lines" aria-hidden="true"></span></button>
    <nav class="nav nav--left" aria-label="Principal">
      {left}
    </nav>
    <a class="brand" href="index.html" aria-label="Suud Culinária Árabe, página inicial">
      <svg class="brand-cedar" viewBox="170 170 920 615" aria-hidden="true">{cedar_lines(40)}</svg>
      <svg class="brand-word" aria-hidden="true"><use href="#wordmark"/></svg>
    </a>
    <div class="nav nav--right">
      <a class="social-btn" href="https://www.instagram.com/suud.restaurante/" target="_blank" rel="noopener" aria-label="Instagram do Suud"><svg aria-hidden="true"><use href="#s-insta"/></svg></a>
      <a class="social-btn" href="https://wa.me/5521967717717" target="_blank" rel="noopener" aria-label="WhatsApp do Suud"><svg aria-hidden="true"><use href="#s-whats"/></svg></a>
      <button class="order-chip" type="button" data-ahlan-open aria-haspopup="dialog" aria-controls="ahlan">
        <span class="order-chip__avatar" aria-hidden="true"><svg><use href="#cedar"/></svg></span>
        <span class="order-chip__label">Fazer pedido</span>
        <span class="order-chip__count" data-cart-count hidden>0</span>
      </button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
  <nav aria-label="Menu mobile"><ol>
      {mob}
  </ol></nav>
  <div class="mobile-menu__foot"><p>Rua Otávio Carneiro, 8 · Icaraí, Niterói</p><p>Todos os dias, das 11h às 22h</p><a href="tel:+5521967717717">(21) 96771-7717</a></div>
  <svg class="mobile-menu__cedar" aria-hidden="true"><use href="#cedar"/></svg>
</div>
<main id="conteudo" tabindex="-1">
'''

FOOTER = f'''
</main>
<footer class="site-footer">
  <div class="site-footer__bg" aria-hidden="true"></div>
  <div class="wrap footer__inner">
    <div class="footer__brand">
      <svg class="footer__logo" viewBox="170 170 920 960" role="img" aria-label="Suud"><use href="#cedar" x="170" y="170" width="920" height="615"/><use href="#wordmark" x="185" y="710" width="870" height="420"/></svg>
      <p class="footer__tag">Culinária árabe · Icaraí, Niterói</p>
    </div>
    <nav class="footer__nav" aria-label="Rodapé"><h2>Navegue</h2><ul>
      <li><a href="cardapio.html">Cardápio árabe</a></li><li><a href="delivery.html">Delivery pelo WhatsApp</a></li><li><a href="index.html#mezze">Mezze para dividir</a></li>
      <li><a href="nossa-historia.html">Nossa história</a></li><li><a href="eventos.html">Eventos e cultura</a></li><li><a href="index.html#perguntas">Perguntas frequentes</a></li>
    </ul></nav>
    <div class="footer__contact"><h2>Contato</h2>
      <address>Rua Otávio Carneiro, 8<br>Icaraí, Niterói · RJ</address>
      <p><a href="tel:+5521967717717">(21) 96771-7717</a></p><p>Todos os dias, 11h–22h</p>
      <p class="footer__social"><a href="https://www.instagram.com/suud.restaurante/" target="_blank" rel="noopener">Instagram</a><a href="https://wa.me/5521967717717" target="_blank" rel="noopener">WhatsApp</a></p>
    </div>
    <div class="footer__base"><svg aria-hidden="true"><use href="#ornament"/></svg><p>© <span data-year>2026</span> Suud Culinária Árabe. Quer abrir um Suud? <a href="https://suudfranquia.com.br" target="_blank" rel="noopener">suudfranquia.com.br</a></p></div>
  </div>
</footer>
<nav class="dock" aria-label="Atalhos">
  <span class="dock__progress" aria-hidden="true"></span>
  <a class="dock__item" href="cardapio.html"><svg aria-hidden="true"><use href="#i-list"/></svg><span>Cardápio</span></a>
  <a class="dock__item" href="index.html#mezze"><svg aria-hidden="true"><use href="#i-plate"/></svg><span>Mezze</span></a>
  <button class="dock__item" type="button" data-ahlan-open data-ahlan-intent="reserva"><svg aria-hidden="true"><use href="#i-calendar"/></svg><span>Reservar</span></button>
  <a class="dock__item" href="index.html#visite"><svg aria-hidden="true"><use href="#i-pin"/></svg><span>Visite</span></a>
  <button class="dock__ahlan" type="button" data-ahlan-open aria-label="Fazer pedido com o Ahlan"><svg aria-hidden="true"><use href="#cedar"/></svg><span class="dock__badge" data-cart-count hidden>0</span></button>
</nav>
<button class="minicart" type="button" data-ahlan-open data-ahlan-intent="review" hidden>
  <svg aria-hidden="true"><use href="#i-bag"/></svg>
  <span class="minicart__text"><b data-mini-qty>0 itens</b><span data-mini-total>R$ 0,00</span></span>
  <span class="minicart__cta">Ver pedido</span>
</button>
<div class="ahlan" id="ahlan" data-state="closed">
  <div class="ahlan__backdrop" data-ahlan-close></div>
  <section class="ahlan__panel" role="dialog" aria-modal="false" aria-labelledby="ahlan-title" tabindex="-1">
    <span class="ahlan__grip" aria-hidden="true"></span>
    <header class="ahlan__head">
      <span class="ahlan__avatar" aria-hidden="true"><svg><use href="#cedar"/></svg></span>
      <div class="ahlan__id"><h2 id="ahlan-title">Ahlan</h2><p><span class="ahlan__online" aria-hidden="true"></span>Atendente do Suud · online</p></div>
      <button class="ahlan__icon-btn" type="button" data-ahlan-restart aria-label="Recomeçar conversa" title="Recomeçar"><svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3M4.5 4.5v3.7h3.7"/></svg></button>
      <button class="ahlan__icon-btn" type="button" data-ahlan-close aria-label="Fechar atendente"><svg><use href="#i-close"/></svg></button>
    </header>
    <div class="ahlan__band" aria-hidden="true"></div>
    <div class="ahlan__log" role="log" aria-live="polite" data-lenis-prevent></div>
    <div class="ahlan__cart" data-ahlan-cartbar hidden>
      <svg aria-hidden="true"><use href="#i-bag"/></svg>
      <span class="ahlan__cart-text"><b data-cart-qty>0 itens</b><span data-cart-total>R$ 0,00</span></span>
      <button type="button" data-ahlan-review>Revisar pedido</button>
    </div>
    <form class="ahlan__composer" autocomplete="off">
      <label class="sr-only" for="ahlan-input">Mensagem para o Ahlan</label>
      <input id="ahlan-input" name="msg" type="text" placeholder="Pergunte ou peça: hummus, horário, vegano…" enterkeyhint="send">
      <button type="submit" aria-label="Enviar mensagem"><svg><use href="#i-send"/></svg></button>
    </form>
  </section>
  <div class="ahlan__toast" role="status" aria-live="polite" hidden>
    <button class="ahlan__toast-x" type="button" aria-label="Dispensar notificação"><svg><use href="#i-close"/></svg></button>
    <div class="ahlan__toast-head"><span class="ahlan__avatar ahlan__avatar--xs" aria-hidden="true"><svg><use href="#cedar"/></svg></span><b>Ahlan</b><span>agora</span></div>
    <p class="ahlan__toast-msg"></p>
    <button class="ahlan__toast-cta" type="button"></button>
  </div>
  <button class="ahlan__launcher" type="button" aria-label="Abrir atendente de pedidos do Suud" aria-controls="ahlan" data-ahlan-open>
    <span class="ahlan__launcher-ring" aria-hidden="true"></span>
    <svg class="ahlan__launcher-cedar" aria-hidden="true"><use href="#cedar"/></svg>
    <svg class="ahlan__launcher-close" aria-hidden="true"><use href="#i-close"/></svg>
    <span class="ahlan__badge" data-cart-count hidden>0</span>
  </button>
</div>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="assets/js/menu-data.js?v={V}" defer></script>
<script src="assets/js/main.js?v={V}" defer></script>
<script src="assets/js/ahlan.js?v={V}" defer></script>
</body>
</html>
'''

def faq_schema(html_text):
    qas = re.findall(r'<summary><h3>(.*?)</h3>.*?<div class="qa__body"><p>(.*?)</p></div>', html_text, re.S)
    ent = [{"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub('<[^>]+>', '', a))}} for q, a in qas]
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ent}, ensure_ascii=False) + '</script>'

def crumbs(name, path):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": DOMAIN},
        {"@type": "ListItem", "position": 2, "name": name, "item": DOMAIN + path}]}, ensure_ascii=False) + '</script>'

def qa(q, a, opened=False):
    return f'''      <details class="qa reveal"{" open" if opened else ""}>
        <summary><h3>{q}</h3><span class="qa__icon" aria-hidden="true"></span></summary>
        <div class="qa__body"><p>{a}</p></div>
      </details>'''

def page_hero(kicker, title, lede, img, alt):
    return f'''
<section class="page-hero">
  <figure class="page-hero__media"><img src="assets/img/{img}" alt="{alt}" width="1774" height="887" fetchpriority="high"></figure>
  <div class="wrap page-hero__inner">
    <p class="eyebrow">{kicker}</p>
    <h1>{title}</h1>
    <p class="page-hero__lede">{lede}</p>
  </div>
</section>'''

# ---------- Blocos reutilizados ----------
REASONS = '''
      <ul class="reasons">
        <li class="reason reveal"><svg class="reason__icon" aria-hidden="true"><use href="#s-menu"/></svg><div><h3>Cardápio inteiro, sem esperar</h3><p>Pratos, descrições e preços na tela. Ninguém precisa mandar foto do cardápio.</p></div></li>
        <li class="reason reveal"><svg class="reason__icon" aria-hidden="true"><use href="#s-sum"/></svg><div><h3>Total antes de enviar</h3><p>Cada prato entra com o preço e a soma atualiza enquanto você escolhe.</p></div></li>
        <li class="reason reveal"><svg class="reason__icon" aria-hidden="true"><use href="#s-check"/></svg><div><h3>Pedido que chega certo</h3><p>Itens, endereço, pagamento e observações numa única mensagem para a cozinha.</p></div></li>
        <li class="reason reveal"><svg class="reason__icon" aria-hidden="true"><use href="#s-question"/></svg><div><h3>Dúvidas resolvidas na hora</h3><p>O que é nayee? Tem opção sem carne? Até que horas abre? O Ahlan responde.</p></div></li>
      </ul>'''

DEMO = '''
      <div class="demo reveal" aria-hidden="true">
        <div class="phone">
          <div class="phone__notch"></div>
          <div class="phone__head"><span class="phone__avatar"><svg><use href="#cedar"/></svg></span><div><b>Ahlan</b><small>Atendente do Suud · online</small></div></div>
          <div class="phone__band"></div>
          <div class="phone__log" data-demo-log></div>
          <div class="phone__cart" data-demo-cart><svg><use href="#i-bag"/></svg><span>1 item · R$ 107,90</span><b>Revisar</b></div>
        </div>
        <p class="demo__caption">Prévia do Ahlan. O de verdade está a um toque: “Fazer pedido”.</p>
      </div>'''

ASK = '''
    <form class="ask" data-ahlan-ask role="search" aria-label="Pergunte ao Ahlan">
      <span class="ask__avatar" aria-hidden="true"><svg><use href="#cedar"/></svg></span>
      <label class="sr-only" for="ask-{id}">Pergunte ou peça ao Ahlan</label>
      <input id="ask-{id}" type="text" placeholder="{ph}" autocomplete="off" enterkeyhint="send">
      <button type="submit" aria-label="Enviar ao Ahlan"><svg aria-hidden="true"><use href="#i-send"/></svg></button>
    </form>
    <div class="ask__chips">
      <button type="button" data-ahlan-open data-ahlan-intent="delivery">Pedir delivery</button>
      <button type="button" data-ahlan-open data-ahlan-intent="reserva">Reservar mesa</button>
      <button type="button" data-ahlan-say="o que é nayee?">O que é nayee?</button>
      <button type="button" data-ahlan-open data-ahlan-intent="suggest">Me indica algo</button>
    </div>'''

TRIO = '''
    <div class="trio-wrap">
      <button class="trio-arrow trio-arrow--prev" type="button" aria-label="Prato anterior"><svg aria-hidden="true"><use href="#s-chevron-l"/></svg></button>
      <ul class="trio" aria-label="Clássicos da casa">
        <li class="trio__panel trio__panel--hummus reveal"><a href="cardapio.html#cat-pastas" aria-label="Hummus: ver as pastas no cardápio">
          <img src="assets/img/trio-hummus.webp" srcset="assets/img/trio-hummus-sm.webp 345w, assets/img/trio-hummus.webp 557w" sizes="(max-width: 860px) 72vw, 32vw" width="557" height="760" loading="lazy" decoding="async" alt="Hummus com grão-de-bico e azeite em travessa dourada"><h3>Hummus</h3></a></li>
        <li class="trio__panel trio__panel--falafel reveal"><a href="cardapio.html#cat-entradas" aria-label="Falafel: ver as entradas no cardápio">
          <img src="assets/img/trio-falafel.webp" srcset="assets/img/trio-falafel-sm.webp 335w, assets/img/trio-falafel.webp 540w" sizes="(max-width: 860px) 72vw, 31vw" width="540" height="760" loading="lazy" decoding="async" alt="Três falafels com limão e salsinha sob a marca Suud"><h3>Falafel</h3></a></li>
        <li class="trio__panel trio__panel--esfihas reveal"><a href="cardapio.html#cat-entradas" aria-label="Esfihas: ver as entradas no cardápio">
          <img src="assets/img/trio-esfihas.webp" srcset="assets/img/trio-esfihas-sm.webp 384w, assets/img/trio-esfihas.webp 620w" sizes="(max-width: 860px) 72vw, 36vw" width="620" height="760" loading="lazy" decoding="async" alt="Esfihas fechadas douradas com limão"><h3>Esfihas</h3></a></li>
      </ul>
      <button class="trio-arrow trio-arrow--next" type="button" aria-label="Próximo prato"><svg aria-hidden="true"><use href="#s-chevron-r"/></svg></button>
    </div>'''

def mezze_card(n, name, desc, items, price, pid, featured=False, badge=''):
    lis = ''.join(f'<li>{i}</li>' for i in items)
    b = f'<span class="mezze-card__badge">{badge}</span>' if badge else ''
    btn = 'btn--light' if featured else 'btn--line-light'
    return f'''
        <li class="mezze-slide" role="group" aria-roledescription="slide" aria-label="{n} de 3: Mezze {name}">
          <article class="mezze-card{' mezze-card--featured' if featured else ''}">
            {b}<span class="mezze-card__n">{['I','II','III'][n-1]}</span>
            <h3>{name}</h3><p class="mezze-card__desc">{desc}</p>
            <ul class="mezze-card__list">{lis}</ul>
            <div class="mezze-card__foot"><data value="{price.replace(',','.')}">R$ {price}</data><button class="btn btn--sm {btn}" type="button" data-ahlan-add="{pid}">Pedir o {name}</button></div>
          </article>
        </li>'''

MEZZE = f'''
<section class="section mezze" id="mezze" aria-labelledby="mezze-title" data-ahlan-zone="mezze">
  <figure class="mezze__panorama reveal-fade">
    <img src="assets/img/mezze-mediterraneo-panorama.webp" srcset="assets/img/mezze-mediterraneo-panorama-900.webp 900w, assets/img/mezze-mediterraneo-panorama.webp 1774w" sizes="100vw" width="1774" height="487" loading="lazy" decoding="async" alt="Mezze com kaftas, kibes, falafels, charutos de folha de uva, tabule, coalhada, hummus e azeitonas" data-parallax="0.06">
  </figure>
  <div class="wrap mezze__inner">
    <header class="mezze__head mezze__head--center">
      <h2 id="mezze-title" class="h2 h2--light reveal">Mezze em Niterói: a mesa árabe para dividir</h2>
      <p class="prose prose--light reveal">Mezze é uma seleção de pequenas porções servidas ao mesmo tempo: pastas, salada, bolinhos e grelhados, com pão árabe para todos. No Suud são três montagens. Deslize para comparar.</p>
    </header>
    <div class="mezze-carousel reveal" aria-roledescription="carrossel" aria-label="Mezzes do Suud">
      <button class="mz-arrow mz-arrow--prev" type="button" aria-label="Mezze anterior"><svg aria-hidden="true"><use href="#s-chevron-l"/></svg></button>
      <ol class="mezze-track">{mezze_card(1,'Byblos','Os clássicos, em versão menor.',['<b>2</b> mini kaftas','<b>2</b> mini kibes','Hummus tahine','Tabule','Mix de azeitonas','Coalhada e pão árabe'],'80,30','mezze-byblos')}{mezze_card(2,'Capadócia','Três de cada, com hummus e tabule.',['<b>3</b> mini kaftas','<b>3</b> mini kibes','<b>3</b> falafels','Hummus tahine e tabule','Mix de azeitonas','Pão árabe e complemento'],'107,90','mezze-capadocia',True,'Kafta, kibe e falafel')}{mezze_card(3,'Mediterrâneo','O mais completo, com charutos de uva.',['<b>5</b> mini kaftas e <b>5</b> mini kibes','<b>5</b> falafels e <b>5</b> charutos de uva','Coalhada seca ou babaganoush','Hummus, tabule e azeitonas','Salada Beirute e cebola crocante','Pão árabe e complemento'],'184,80','mezze-mediterraneo')}
      </ol>
      <button class="mz-arrow mz-arrow--next" type="button" aria-label="Próximo mezze"><svg aria-hidden="true"><use href="#s-chevron-r"/></svg></button>
      <div class="mezze-dots" role="tablist" aria-label="Escolher mezze"><button type="button" aria-label="Byblos"></button><button type="button" aria-label="Capadócia"></button><button type="button" aria-label="Mediterrâneo"></button></div>
    </div>
  </div>
</section>'''

VISIT = '''
<section class="section visit" id="visite" aria-labelledby="visit-title" data-ahlan-zone="visit">
  <div class="wrap visit__grid">
    <div>
      <h2 id="visit-title" class="h2 h2--light reveal">Como chegar ao Suud em Icaraí</h2>
      <dl class="visit__info reveal">
        <div><dt><svg aria-hidden="true"><use href="#i-pin"/></svg>Endereço</dt><dd>Rua Otávio Carneiro, 8<br>Icaraí, Niterói · RJ</dd></div>
        <div><dt><svg aria-hidden="true"><use href="#i-clock"/></svg>Horário</dt><dd>Todos os dias, das 11h às 22h<br><small>Feriados podem ter horário especial</small></dd></div>
        <div><dt><svg aria-hidden="true"><use href="#i-phone"/></svg>Reservas e delivery</dt><dd><a href="tel:+5521967717717">(21) 96771-7717</a><br><a href="https://wa.me/5521967717717" target="_blank" rel="noopener">Chamar no WhatsApp</a></dd></div>
      </dl>
      <div class="visit__actions reveal">
        <a class="btn btn--light" href="https://www.google.com/maps/search/?api=1&amp;query=Suud+Culin%C3%A1ria+%C3%81rabe+Rua+Ot%C3%A1vio+Carneiro+8+Icara%C3%AD+Niter%C3%B3i" target="_blank" rel="noopener">Abrir no Google Maps<svg class="ico ico--arrow" aria-hidden="true"><use href="#i-arrow"/></svg></a>
        <button class="btn btn--ghost-light" type="button" data-ahlan-open data-ahlan-intent="reserva">Reservar mesa</button>
      </div>
    </div>
    <div class="visit__map reveal reveal--img">
      <iframe title="Mapa: Suud Culinária Árabe, Rua Otávio Carneiro, 8, Icaraí, Niterói" src="https://www.google.com/maps?q=Rua%20Ot%C3%A1vio%20Carneiro%2C%208%2C%20Icara%C3%AD%2C%20Niter%C3%B3i%20-%20RJ&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>'''

CTA_BOT = '''
<section class="cta-bot">
  <div class="wrap cta-bot__inner reveal">
    <span class="cta-bot__avatar" aria-hidden="true"><svg><use href="#cedar"/></svg></span>
    <div><h2>Com fome agora?</h2><p>O Ahlan monta seu pedido em 1 minuto e manda pronto para o WhatsApp do Suud.</p></div>
    <button class="btn btn--light" type="button" data-ahlan-open data-ahlan-intent="delivery"><svg class="ico" aria-hidden="true"><use href="#i-bag"/></svg>Fazer pedido</button>
  </div>
</section>'''

# =========================================================
# HOME
# =========================================================
HOME_FAQ = '\n'.join([
    qa('Onde fica o Suud?', 'Na Rua Otávio Carneiro, 8, em Icaraí, Niterói (RJ), a poucas quadras da praia.', True) if False else qa('Onde fica o Suud?', 'Na Rua Otávio Carneiro, 8, em Icaraí, Niterói (RJ).', True),
    qa('Qual o horário de funcionamento?', 'O salão abre todos os dias, das 11h às 22h. Em feriados e nos aplicativos de delivery o horário pode mudar. Na dúvida, chame no WhatsApp (21) 96771-7717.'),
    qa('Como funciona o pedido pelo Ahlan?', 'Você escolhe os pratos no site e o Ahlan soma o pedido. Depois ele pergunta nome, endereço e forma de pagamento e abre o WhatsApp com a mensagem pronta para enviar ao Suud. A equipe confirma valores, taxa e prazo.'),
    qa('O Suud entrega em toda Niterói?', 'A área de entrega e a taxa dependem do endereço. Envie o pedido pelo WhatsApp e a equipe confirma se atende o seu bairro.'),
    qa('O que é mezze?', 'É uma seleção de pequenas porções servidas juntas, como pastas, salada, bolinhos e grelhados, com pão árabe para todos dividirem. O Suud tem três: Byblos, Capadócia e Mediterrâneo.'),
    qa('Tem opção vegetariana e vegana?', 'Sim. Falafel, hummus tahine, babaganoush, tabule, saladas e esfihas vegetarianas não levam carne. Para dieta vegana, restrições ou alergias, confirme os ingredientes com a equipe antes de pedir.'),
    qa('Qual a diferença entre hummus e babaganoush?', 'O hummus é uma pasta de grão-de-bico com tahine, que é a pasta de gergelim. No babaganoush, a estrela é a berinjela defumada, que no Suud vai misturada ao hummus tahine da casa.'),
    qa('O que é nayee?', 'É o kibe cru, um clássico da cozinha árabe. No Suud ele vem com cebola, hortelã e azeite. Também aparece na Torre de Nayee, em camadas com coalhada e cebola crocante.'),
    qa('Dá para reservar mesa ou fazer evento?', 'Sim. Reservas, aniversários, confraternizações, aulas, palestras e eventos de empresa são combinados pelo WhatsApp, de acordo com a disponibilidade do espaço.'),
])

HOME = f'''
<section class="hero" aria-label="Suud Culinária Árabe" data-ahlan-zone="hero">
  <picture class="hero__media">
    <source media="(max-width: 860px)" srcset="assets/img/capa-suud-mobile.webp" width="700" height="665">
    <img src="assets/img/capa-suud.webp" srcset="assets/img/capa-suud-1100.webp 1100w, assets/img/capa-suud.webp 1774w" sizes="100vw" width="1774" height="887" fetchpriority="high" alt="Mezze árabe com kibes, charutos de folha de uva, falafel, tabule, coalhada, hummus e azeitonas, ao lado de pão árabe e vinho tinto">
  </picture>
  <div class="hero__chat" data-ahlan-home aria-label="Atendimento do Suud"></div>
  <div class="hero__brand">
    <svg class="hero__logo" viewBox="170 170 920 960" role="img" aria-label="Suud">
      {cedar_lines(30)}
      <use class="hero__word" href="#wordmark" x="185" y="710" width="870" height="420"/>
    </svg>
    <p class="hero__label">Culinária árabe</p>
  </div>
</section>

<section class="intro" aria-labelledby="intro-title">
  <div class="wrap intro__grid">
    <div class="intro__copy">
      <h1 id="intro-title">Restaurante árabe em Icaraí, Niterói</h1>
      <p>Mezze para dividir, kibe cru, falafel, esfiha e café turco. Salão aberto todos os dias, das 11h às 22h. Em casa, o pedido sai pelo WhatsApp com o Ahlan.</p>
      <ul class="intro__facts">
        <li><svg aria-hidden="true"><use href="#i-pin"/></svg>Rua Otávio Carneiro, 8</li>
        <li><svg aria-hidden="true"><use href="#i-clock"/></svg>Todo dia, 11h–22h</li>
        <li><svg aria-hidden="true"><use href="#i-phone"/></svg><a href="tel:+5521967717717">(21) 96771-7717</a></li>
      </ul>
    </div>
    <div class="intro__actions">
      <a class="btn btn--light" href="cardapio.html"><svg class="ico" aria-hidden="true"><use href="#i-list"/></svg>Ver cardápio</a>
      <button class="btn btn--ghost-light" type="button" data-ahlan-open data-ahlan-intent="reserva">Reservar mesa</button>
    </div>
  </div>
</section>

<section class="section delivery" id="delivery" aria-labelledby="delivery-title" data-ahlan-zone="delivery">
  <div class="wrap">
    <div class="delivery__grid">
      <div class="delivery__copy">
        <p class="eyebrow reveal">Delivery pelo WhatsApp</p>
        <h2 id="delivery-title" class="h2 h2--light reveal">Comida árabe em casa, com o pedido pronto em 1 minuto</h2>
        <p class="delivery__lede reveal">O Ahlan é o atendente digital do Suud. Mostra o cardápio inteiro, soma tudo enquanto você escolhe e entrega o pedido organizado no WhatsApp da casa. Você só confirma.</p>
        {REASONS}
        <div class="delivery__actions reveal">
          <button class="btn btn--light" type="button" data-ahlan-open data-ahlan-intent="delivery"><svg class="ico" aria-hidden="true"><use href="#i-bag"/></svg>Montar meu pedido</button>
          <a class="btn btn--ghost-light" href="delivery.html">Como funciona<svg class="ico ico--arrow" aria-hidden="true"><use href="#i-arrow"/></svg></a>
        </div>
      </div>
      {DEMO}
    </div>
  </div>
</section>

<section class="section menu menu--home" id="cardapio" aria-labelledby="menu-title" data-ahlan-zone="menu">
  <div class="wrap">
    <header class="section-head section-head--center">
      <h2 id="menu-title" class="h2 reveal">Os clássicos da casa</h2>
      <p class="section-lede reveal">Hummus, falafel e esfiha abrem a mesa no Suud. Toque em um prato para ver a categoria inteira no cardápio.</p>
    </header>
    {TRIO}
    <p class="center reveal"><a class="btn btn--terra" href="cardapio.html">Ver o cardápio completo<svg class="ico ico--arrow" aria-hidden="true"><use href="#i-arrow"/></svg></a></p>
  </div>
</section>

{MEZZE}

<section class="section moments" id="momentos" aria-labelledby="moments-title" data-ahlan-zone="moments">
  <div class="moments__pin">
    <div class="wrap moments__head">
      <h2 id="moments-title" class="h2 reveal">Do almoço ao café turco</h2>
      <p class="section-lede reveal">Tem dia de almoço rápido, tem noite de mesa cheia. O cardápio acompanha.</p>
    </div>
    <div class="moments__stage">
    <button class="rail-arrow rail-arrow--prev" type="button" data-rail-prev aria-label="Momento anterior"><svg aria-hidden="true"><use href="#s-chevron-l"/></svg></button>
    <button class="rail-arrow rail-arrow--next" type="button" data-rail-next aria-label="Próximo momento"><svg aria-hidden="true"><use href="#s-chevron-r"/></svg></button>
    <ul class="moments__rail">
      <li class="moment"><figure class="moment__img"><img src="assets/img/bowl-delivery.webp" width="784" height="580" loading="lazy" decoding="async" alt="Bowl do Suud com frango grelhado, hummus, tabule e repolho roxo"></figure><span class="moment__time">Almoço</span><h3>Rápido e completo</h3><p>Shawarma no pão folha, Monte seu prato ou salada Istambul.</p></li>
      <li class="moment"><figure class="moment__img"><img src="assets/img/mezze-para-compartilhar-640.webp" width="640" height="601" loading="lazy" decoding="async" alt="Prato para dividir com falafel, kibes, grão-de-bico, tomate e hortelã"></figure><span class="moment__time">Fim de tarde</span><h3>Mesa para dividir</h3><p>Mezze no meio, mini kaftas no pau de canela e um Caipiarak.</p></li>
      <li class="moment"><figure class="moment__img moment__img--light"><img src="assets/img/cha-turco-520.webp" width="520" height="370" loading="lazy" decoding="async" alt="Chá turco servido em copo de vidro"></figure><span class="moment__time">Pausa</span><h3>Chá turco e doce</h3><p>Chá ou café turco com mamul ou merche de tâmara.</p></li>
    </ul>
    </div>
  </div>
</section>

<section class="section story-teaser" aria-labelledby="story-title">
  <div class="wrap story-teaser__grid">
    <figure class="story-teaser__img reveal reveal--img"><img src="assets/img/mesa-partilha-pao-tabule.webp" width="790" height="887" loading="lazy" decoding="async" alt="Mãos dividindo tabule e pão árabe à mesa"></figure>
    <div>
      <p class="eyebrow eyebrow--terra reveal">Nossa história</p>
      <h2 id="story-title" class="h2 reveal">Uma casa árabe que Icaraí adotou</h2>
      <p class="prose reveal">Primeiro numa loja da Moreira César, depois na Rua Otávio Carneiro, o Suud foi juntando clientes de almoço, famílias de domingo e plateia de sarau. A história de como uma cozinha de mezze virou ponto de encontro em Niterói.</p>
      <p class="reveal"><a class="btn btn--line" href="nossa-historia.html">Ler a história<svg class="ico ico--arrow" aria-hidden="true"><use href="#i-arrow"/></svg></a></p>
    </div>
  </div>
</section>

<section class="section faq" id="perguntas" aria-labelledby="faq-title" data-ahlan-zone="faq">
  <div class="wrap faq__grid">
    <header class="faq__head">
      <h2 id="faq-title" class="h2 reveal">Perguntas frequentes</h2>
      <p class="section-lede reveal">Não achou a resposta? O Ahlan responde na hora.</p>
      <button class="btn btn--line" type="button" data-ahlan-open>Perguntar ao Ahlan</button>
    </header>
    <div class="faq__list">
{HOME_FAQ}
    </div>
  </div>
</section>
{VISIT}
'''

BANNERS = {'cat-pastas': 'hummus-tahine.webp', 'cat-entradas': 'esfihas.webp', 'cat-mezzes': 'mezze-mediterraneo-panorama-900.webp', 'cat-pratos': 'bowl-delivery.webp', 'cat-doces': 'cha-turco-520.webp'}
def _banner(m):
    cid = m.group(1)
    img = BANNERS.get(cid, 'hummus-tahine.webp')
    return m.group(0) + f'\n          <figure class="menu-cat__banner"><img src="assets/img/{img}" alt="" loading="lazy" decoding="async"></figure>'
PANELS_VISUAL = re.sub(r'<section class="menu-cat[^"]*" id="(cat-[a-z]+)"[^>]*>', _banner, PANELS)

# =========================================================
# CARDÁPIO
# =========================================================
CARDAPIO = page_hero('Cardápio', 'Cardápio árabe do Suud, em Icaraí', 'Das pastas ao mamul, tudo o que sai da cozinha, com preço de referência. Toque no + e o prato entra no seu pedido pelo WhatsApp.', 'capa-suud-1100.webp', 'Mezze árabe do Suud') + f'''
<section class="section menu" id="cardapio" aria-labelledby="menu-title" data-ahlan-zone="menu">
  <div class="wrap">
    <h2 id="menu-title" class="sr-only">Pratos do cardápio</h2>
    {TRIO}
    <div class="menu-board reveal">
      <div class="menu-tools">
        <label class="menu-search"><svg aria-hidden="true"><use href="#i-list"/></svg><span class="sr-only">Buscar no cardápio</span><input type="search" placeholder="Buscar prato: kibe, hummus, doce…" data-menu-search autocomplete="off"></label>
        <button class="menu-veg" type="button" aria-pressed="false" data-menu-veg><svg aria-hidden="true"><use href="#i-sprout"/></svg>Só vegetarianos</button>
      </div>
      <p class="menu-empty" data-menu-empty hidden>Nenhum prato encontrado. Tente outro nome ou pergunte ao Ahlan.</p>
      <div class="menu-tabs" role="tablist" aria-label="Categorias do cardápio">
        <button type="button" role="tab" id="tab-pastas" aria-controls="cat-pastas" aria-selected="true"><img src="assets/img/trio-hummus-sm.webp" alt="" width="120" height="120" loading="lazy" decoding="async"><span>Pastas</span></button>
        <button type="button" role="tab" id="tab-entradas" aria-controls="cat-entradas" aria-selected="false" tabindex="-1"><img src="assets/img/falafel.webp" alt="" width="120" height="120" loading="lazy" decoding="async"><span>Entradas</span></button>
        <button type="button" role="tab" id="tab-mezzes" aria-controls="cat-mezzes" aria-selected="false" tabindex="-1"><img src="assets/img/mezze-para-compartilhar-640.webp" alt="" width="120" height="120" loading="lazy" decoding="async"><span>Mezzes &amp; torres</span></button>
        <button type="button" role="tab" id="tab-pratos" aria-controls="cat-pratos" aria-selected="false" tabindex="-1"><img src="assets/img/bowl-delivery.webp" alt="" width="120" height="120" loading="lazy" decoding="async"><span>Pratos &amp; saladas</span></button>
        <button type="button" role="tab" id="tab-doces" aria-controls="cat-doces" aria-selected="false" tabindex="-1"><img src="assets/img/cha-turco-520.webp" alt="" width="120" height="120" loading="lazy" decoding="async"><span>Sobremesas &amp; bebidas</span></button>
        <span class="menu-tabs__ink" aria-hidden="true"></span>
      </div>
      <p class="menu-swipe-hint" aria-hidden="true">Deslize para trocar de categoria</p>
      {PANELS_VISUAL}
      <p class="menu-disclaimer">Preços de referência do delivery, sujeitos a alteração. A equipe confirma valores, disponibilidade e taxa de entrega ao fechar o pedido. Tem alergia ou restrição? Pergunte sobre os ingredientes antes de pedir.</p>
    </div>
  </div>
</section>

<section class="section article-block">
  <div class="wrap article">
    <h2 class="h2 reveal">Como ler o cardápio de um restaurante árabe</h2>
    <p class="reveal">Quem chega pela primeira vez a uma mesa árabe costuma travar nos nomes. Não precisa. As <strong>pastas</strong> são o ponto de partida: hummus de grão-de-bico com tahine, babaganoush de berinjela defumada e labanie, a coalhada seca. Vêm com pão árabe e servem a mesa toda.</p>
    <p class="reveal">Nas <strong>entradas</strong> estão os fritos e assados que todo mundo conhece por outro nome: o maklie é o kibe frito, o il feren é o kibe assado e o nayee é o kibe cru, servido com cebola, hortelã e azeite. Falafel e esfiha completam o time.</p>
    <p class="reveal">Se a ideia é provar um pouco de tudo, o atalho é o <strong>mezze</strong>. O Byblos é a porta de entrada, o Capadócia junta kafta, kibe e falafel e o Mediterrâneo chega com charutos de folha de uva e salada Beirute. Para fechar, mamul ou merche de tâmara com café turco.</p>
    <p class="reveal">Ainda em dúvida? Escreva para o Ahlan “o que é labanie?” ou “tem opção sem carne?”. Ele responde e já mostra o prato.</p>
  </div>
</section>
{CTA_BOT}
'''

# =========================================================
# DELIVERY
# =========================================================
DELIV_FAQ = '\n'.join([
    qa('Como funciona o pedido pelo Ahlan?', 'Você escolhe os pratos no site e o Ahlan soma o pedido. Depois ele pergunta nome, endereço e forma de pagamento e abre o WhatsApp com a mensagem pronta para enviar ao Suud. A equipe confirma valores, taxa e prazo.', True),
    qa('Preciso baixar algum aplicativo?', 'Não. O Ahlan funciona aqui no site, no celular ou no computador. O pedido é enviado pelo WhatsApp que você já usa.'),
    qa('O Suud entrega em toda Niterói?', 'A área de entrega e a taxa dependem do endereço. Envie o pedido pelo WhatsApp e a equipe confirma se atende o seu bairro.'),
    qa('Dá para retirar no restaurante?', 'Sim. Escolha “Retirar no Suud” no Ahlan e busque o pedido na Rua Otávio Carneiro, 8, em Icaraí.'),
    qa('Vocês vendem congelados?', 'Sim. As opções variam ao longo da semana. Pergunte ao Ahlan ou à equipe pelo WhatsApp o que está disponível.'),
])
DELIVERY = page_hero('Delivery pelo WhatsApp', 'Delivery de comida árabe em Niterói, pedido pelo Ahlan', 'Sem aplicativo, sem esperar alguém mandar o cardápio. Você escolhe, o Ahlan soma e o pedido chega pronto no WhatsApp do Suud.', 'capa-suud-1100.webp', 'Mezze árabe do Suud') + f'''
<section class="section delivery" aria-labelledby="delivery-title" data-ahlan-zone="delivery">
  <div class="wrap">
    <div class="delivery__grid">
      <div class="delivery__copy">
        <h2 id="delivery-title" class="h2 h2--light reveal">Por que pedir pelo Ahlan</h2>
        {REASONS}
        <div class="delivery__actions reveal">
          <button class="btn btn--light" type="button" data-ahlan-open data-ahlan-intent="delivery"><svg class="ico" aria-hidden="true"><use href="#i-bag"/></svg>Montar meu pedido</button>
          <a class="btn btn--ghost-light" href="tel:+5521967717717"><svg class="ico" aria-hidden="true"><use href="#i-phone"/></svg>Prefiro ligar</a>
        </div>
        <p class="delivery__note reveal">Direto com o Suud, sem intermediário. A casa também atende pelos aplicativos de delivery.</p>
      </div>
      {DEMO}
    </div>
  </div>
</section>

<section class="section steps-sec">
  <div class="wrap">
    <h2 class="h2 reveal">Do clique à mesa em três passos</h2>
    <ol class="steps3">
      <li class="reveal"><span>1</span><h3>Escolha</h3><p>Navegue pelo cardápio ou peça uma sugestão ao Ahlan. Cada prato entra no pedido com um toque.</p></li>
      <li class="reveal"><span>2</span><h3>Revise</h3><p>Ajuste quantidades, veja o total e diga se é entrega ou retirada, além da forma de pagamento.</p></li>
      <li class="reveal"><span>3</span><h3>Envie</h3><p>O WhatsApp abre com a mensagem pronta. A equipe do Suud confirma valores, taxa e prazo.</p></li>
    </ol>
  </div>
</section>

<section class="section extras-sec">
  <div class="wrap extras">
    <article class="extra reveal"><figure><img src="assets/img/congelados-bandejas-800.webp" width="800" height="316" loading="lazy" decoding="async" alt="Bandejas de congelados com tampa terracota do Suud"></figure><div><h3>Congelados para ter em casa</h3><p>Para resolver o jantar ou receber visitas sem correr para a cozinha. Pergunte ao Ahlan o que tem hoje.</p></div></article>
    <article class="extra reveal"><figure><img src="assets/img/potes-de-pastas-520.webp" width="520" height="366" loading="lazy" decoding="async" alt="Pote de hummus com cinta terracota do Suud"></figure><div><h3>Encomendas para festas</h3><p>Ceia de fim de ano, aniversário, confraternização. Diga a data e o número de pessoas que a equipe monta a encomenda.</p></div></article>
  </div>
</section>

<section class="section faq" aria-labelledby="faq-title">
  <div class="wrap faq__grid">
    <header class="faq__head"><h2 id="faq-title" class="h2 reveal">Dúvidas sobre o delivery</h2><button class="btn btn--line" type="button" data-ahlan-open>Perguntar ao Ahlan</button></header>
    <div class="faq__list">
{DELIV_FAQ}
    </div>
  </div>
</section>
'''

# =========================================================
# NOSSA HISTÓRIA
# =========================================================
HISTORIA = page_hero('Nossa história', 'Suud: a casa de mezze que virou ponto de encontro em Icaraí', 'Uma cozinha árabe, uma rua tranquila de Niterói e o hábito, antigo como o Levante, de pôr tudo no meio da mesa.', 'capa-suud-1100.webp', 'Mesa árabe do Suud') + '''
<article class="section article-block">
  <div class="wrap article">
    <p class="article__lead reveal">Há restaurantes que se explicam pelo prato principal. O Suud se explica pelo centro da mesa. É ali que chegam, todos juntos, o hummus, a coalhada seca, o tabule, as kaftas no pau de canela e o pão árabe ainda quente. Ninguém tem prato próprio por muito tempo. É assim na tradição árabe, e é assim numa esquina de Icaraí.</p>

    <h2 class="reveal">Da Moreira César à Otávio Carneiro</h2>
    <p class="reveal">O nome já circulava em Niterói antes do endereço atual. Em 2019, uma reportagem de O Globo registrava o Suud numa loja da Rua Moreira César, com um mezze no cardápio que custava R$ 55. A casa cresceu e se mudou para a Rua Otávio Carneiro, 8, no mesmo bairro, onde funciona hoje, todos os dias, das 11h às 22h.</p>
    <p class="reveal">A ficha do restaurante no Google o descreve como uma cozinha síria comandada por um chef vindo da Síria. A apresentação da rede de franquias fala em herança libanesa. As duas pistas apontam para o mesmo mapa: o Levante, região onde o mezze é menos um prato do que um modo de comer.</p>

    <figure class="article__figure reveal reveal--img"><img src="assets/img/mezze-mediterraneo-panorama.webp" width="1774" height="487" loading="lazy" decoding="async" alt="Mezze com kaftas, kibes, falafels e charutos de folha de uva"><figcaption>O mezze, servido para dividir, é o retrato da casa.</figcaption></figure>

    <h2 class="reveal">Uma cozinha que explica o que serve</h2>
    <p class="reveal">Quem acompanha o Suud nas redes sociais percebe um hábito raro: a casa explica a comida. Conta que o babaganoush é berinjela defumada, que o falafel é grão-de-bico com ervas, que as folhas de uva usadas na cozinha vêm da Vinícola Famiglia Maioli. O pão árabe, diz o próprio restaurante, é artesanal.</p>
    <p class="reveal">O cardápio passeia entre a tradição e alguns desvios bem-vindos. Há o kibe cru, servido com cebola, hortelã e azeite, e há o Kebab Bodrum, inspirado na Riviera Turca, com filé-mignon, batata palha, coalhada seca e molho turco. Para o fim da refeição, chá ou café turco e doces como o mamul, recheado com tâmaras.</p>
    <p class="reveal">Esse impulso didático chegou ao site. O <strong>Ahlan</strong>, atendente digital do Suud, responde o que é nayee ou labanie, monta o pedido de delivery e entrega a mensagem pronta no WhatsApp da casa. O nome vem da saudação árabe de boas-vindas, a mesma que abre a conversa.</p>

    <h2 class="reveal">Mesa, palco e sala de aula</h2>
    <p class="reveal">Com o tempo, o salão ganhou outros usos. Recebeu noites de Julio Morgado cantando Vinicius de Moraes, Tom Jobim, Milton Nascimento e Fagner; cafés-concerto que misturam literatura e música; apresentações de dança oriental com Aaminah Al Abdalla. Também abriu as portas para aulas, palestras, aniversários e confraternizações de empresa.</p>
    <p class="reveal">Nas datas importantes, o Suud vai até a casa dos clientes. Já preparou ceias de fim de ano com hummus, tabule, cordeiro e arroz maklub, e mantém uma linha de congelados para quem quer a cozinha árabe na geladeira.</p>

    <h2 class="reveal">O que não mudou</h2>
    <p class="reveal">Endereço, cardápio e programação mudaram ao longo dos anos. O gesto continua o mesmo: pratos no centro, pão passando de mão em mão e uma conversa que não tem pressa de acabar. O resto é detalhe, e cabe num mezze.</p>
    <p class="article__note reveal">Fontes: reportagens de O Globo (2019, 2023 e 2024), ficha pública do restaurante no Google, perfil @suud.restaurante e apresentação da rede de franquias. Informações históricas não representam cardápio ou preços atuais.</p>
  </div>
</article>
''' + CTA_BOT

# =========================================================
# EVENTOS
# =========================================================
EVENTOS = page_hero('Eventos e cultura', 'Espaço para eventos em Icaraí, com cozinha árabe', 'Aniversários, confraternizações, aulas e noites de música. O salão do Suud recebe gente desde o almoço até o fim da noite.', 'capa-suud-1100.webp', 'Mesa árabe do Suud') + '''
<section class="section culture" id="experiencias" aria-labelledby="culture-title" data-ahlan-zone="culture">
  <div class="wrap culture__grid">
    <div>
      <h2 id="culture-title" class="h2 reveal">Música, poesia e dança oriental em Icaraí</h2>
      <div class="prose reveal">
        <p>De vez em quando o salão vira palco. Já passaram por aqui as noites de Julio Morgado cantando Vinicius de Moraes, Tom Jobim, Milton Nascimento e Fagner, cafés-concerto que misturam literatura e música e a dança oriental de Aaminah Al Abdalla.</p>
        <p>A agenda muda ao longo do ano. Para saber da próxima, pergunte no WhatsApp ou siga o <a href="https://www.instagram.com/suud.restaurante/" target="_blank" rel="noopener">@suud.restaurante</a>.</p>
      </div>
    </div>
    <aside class="event-card reveal" aria-labelledby="event-title">
      <p class="eyebrow eyebrow--terra">Espaço para eventos em Icaraí</p>
      <h3 id="event-title">Faça a sua festa no Suud</h3>
      <p>Aniversário, confraternização, aula, palestra ou reunião de empresa. Diga a data e o número de pessoas e a equipe responde com as opções do espaço.</p>
      <button class="btn btn--terra" type="button" data-ahlan-open data-ahlan-intent="evento">Falar sobre meu evento<svg class="ico ico--arrow" aria-hidden="true"><use href="#i-arrow"/></svg></button>
    </aside>
  </div>
</section>
<section class="section steps-sec">
  <div class="wrap">
    <h2 class="h2 reveal">O que cabe no salão</h2>
    <ol class="steps3">
      <li class="reveal"><span>1</span><h3>Festas e aniversários</h3><p>Mezzes no centro da mesa, pratos para dividir e doces árabes no fim.</p></li>
      <li class="reveal"><span>2</span><h3>Empresas e grupos</h3><p>Confraternizações, reuniões, aulas e palestras, com almoço ou jantar.</p></li>
      <li class="reveal"><span>3</span><h3>Noites culturais</h3><p>Música, poesia e dança oriental quando a agenda da casa permitir.</p></li>
    </ol>
  </div>
</section>
''' + CTA_BOT

PAGES = [
    ('index.html', 'Restaurante árabe em Niterói: mezze, kibe e esfiha | Suud', 'Mezze para dividir, kibe cru, falafel e esfiha em Icaraí. Peça pelo WhatsApp em 1 minuto com o Ahlan ou reserve sua mesa. Todo dia, das 11h às 22h.', HOME, '', ''),
    ('cardapio.html', 'Cardápio árabe em Icaraí, Niterói: preços e pratos | Suud', 'Cardápio do Suud: hummus, babaganoush, kibe cru, esfihas, mezzes, shawarma, saladas e doces árabes. Monte o pedido e envie pelo WhatsApp.', CARDAPIO, 'Cardápio', ''),
    ('delivery.html', 'Delivery de comida árabe em Niterói pelo WhatsApp | Suud', 'Peça comida árabe em Niterói sem aplicativo: o Ahlan mostra o cardápio, soma o pedido e envia pronto para o WhatsApp do Suud.', DELIVERY, 'Delivery', ''),
    ('nossa-historia.html', 'Nossa história: o restaurante árabe de Icaraí | Suud', 'Da Rua Moreira César à Otávio Carneiro: como o Suud virou ponto de encontro da culinária árabe em Niterói, entre mezzes, música e dança oriental.', HISTORIA, 'Nossa história', ''),
    ('eventos.html', 'Espaço para eventos em Icaraí com comida árabe | Suud', 'Aniversários, confraternizações, aulas e noites de música no salão do Suud, em Icaraí, Niterói. Consulte datas e formatos pelo WhatsApp.', EVENTOS, 'Eventos', ''),
]

for path, title, desc, body, crumb, _ in PAGES:
    extra = faq_schema(body) if 'class="qa' in body else ''
    if crumb: extra += crumbs(crumb, path)
    if path == 'nossa-historia.html':
        extra += '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": "Suud: a casa de mezze que virou ponto de encontro em Icaraí", "inLanguage": "pt-BR", "about": {"@id": DOMAIN + "#restaurante"}, "image": DOMAIN + "assets/img/og-suud.jpg", "publisher": {"@type": "Organization", "name": "Suud Culinária Árabe"}}, ensure_ascii=False) + '</script>'
    pre = '<link rel="preload" as="image" href="assets/img/capa-suud.webp" media="(min-width: 861px)">\n<link rel="preload" as="image" href="assets/img/capa-suud-mobile.webp" media="(max-width: 860px)">\n' if path == 'index.html' else ''
    active = {'cardapio.html': 'cardapio.html', 'delivery.html': 'delivery.html', 'nossa-historia.html': 'nossa-historia.html', 'eventos.html': 'eventos.html'}.get(path, '')
    out = head(title, desc, path, extra, pre) + header(active) + body + FOOTER
    open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(out)
    print('ok', path, len(out))

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'  <url><loc>{DOMAIN}{"" if p == "index.html" else p}</loc><lastmod>2026-10-08</lastmod></url>\n' for p, *_ in PAGES) + '</urlset>\n'
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
