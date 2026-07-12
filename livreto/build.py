#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o livreto do atendeaqui -> livreto/index.html (rota /livreto).

    python3 livreto/build.py     (mas voce NAO precisa: o CI faz — ver livreto/CLAUDE.md)

Pipeline portado do livreto do baterponto, que herda a doutrina do SeuCondominio
(~/workspace/seucondominio/livreto/CLAUDE.md). Marca: coral #FF5A36.

NUNCA editar livreto/index.html na mao — e gerado, e o CI sobrescreve.

PEGADINHAS DO PRINT (custaram correcao; nao mexa sem entender):
  - @media print PRECISA forcar .rev{opacity:1} — senao o PDF sai EM BRANCO.
  - print-color-adjust:exact — senao hero/CTA/fotos saem sem cor.
  - break-inside:avoid so nas unidades atomicas. NUNCA por capitulo.
  - @page{size:A4} — senao o Chrome imprime em Letter.
  - Traco de SVG: stroke explicito no elemento.
"""
import pathlib, importlib.util, datetime, hashlib

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
OUT  = REPO / "livreto" / "index.html"

sp = importlib.util.spec_from_file_location("content", str(ROOT / "content.py"))
C = importlib.util.module_from_spec(sp); sp.loader.exec_module(C)

WA = C.WA + C.WA_TXT

# --------------------------------------------------------------------- cenas
# Line-art dos storyboards. `stroke="currentColor"` explícito e fill="none" —
# nada de classe utilitária que possa zerar o traço.
SCENES = {
 "msg":     '<rect x="10" y="10" width="30" height="22" rx="4"/><path d="M16 30l-3 7 9-7"/><path d="M17 18h16M17 24h10"/>',
 "robo":    '<rect x="16" y="12" width="24" height="20" rx="4"/><circle cx="24" cy="21" r="2"/><circle cx="32" cy="21" r="2"/><path d="M28 12V7"/><circle cx="28" cy="5" r="2"/><path d="M24 27h8"/>',
 "passa":   '<path d="M10 22h26"/><path d="M30 15l7 7-7 7"/><rect x="38" y="12" width="10" height="20" rx="3"/>',
 "humano":  '<circle cx="28" cy="15" r="6"/><path d="M16 36c1.8-6.4 6.2-9.6 12-9.6s10.2 3.2 12 9.6"/><path d="M8 12h8M8 18h5"/>',
 "fila":    '<rect x="8" y="9" width="18" height="12" rx="3"/><rect x="8" y="25" width="18" height="12" rx="3"/><rect x="32" y="17" width="16" height="12" rx="3"/><path d="M26 15h6M26 31h6"/>',
 "distrib": '<circle cx="28" cy="22" r="5"/><path d="M28 17V8M28 27v9M23 22H10M33 22h13"/><circle cx="8" cy="22" r="2.5"/><circle cx="48" cy="22" r="2.5"/><circle cx="28" cy="6" r="2.5"/><circle cx="28" cy="38" r="2.5"/>',
 "relogio": '<circle cx="28" cy="22" r="13"/><path d="M28 14v8l6 3.5"/><path d="M28 3v4"/>',
 "tag":     '<path d="M34 8 46 20 28 38 16 26 22 8Z" stroke-linejoin="round"/><circle cx="26" cy="14" r="2"/><path d="M8 30l6 6"/>',
}
def scene(n):
    return ('<svg class="scene" viewBox="0 0 56 44" aria-hidden="true">'
            f'<g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            f'stroke-linejoin="round">{SCENES[n]}</g></svg>')

# ---------------------------------------------------------------- componentes
_CHAP = [0]
def chapter(cid, eyebrow, h2, lead, *blocks):
    bg = "nevoa" if _CHAP[0] % 2 else ""   # alterna sozinho — não passe bg
    _CHAP[0] += 1
    return f'''<section class="cap {bg}" id="{cid}" aria-label="{eyebrow}">
  <div class="cap-in">
    <div class="cap-head rev"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2>
      {f'<p class="lead">{lead}</p>' if lead else ''}</div>
    {"".join(blocks)}
  </div>
</section>'''

def tag(t):
    return f'<span class="tg">{t}</span>' if t else ''

def cards(items, cor):
    cs = "".join(f'<article class="fc"><span class="fc-mk"></span><h3>{t}{tag(g)}</h3><p>{d}</p></article>'
                 for t, d, g in items)
    return f'<div class="fgrid c-{cor} rev">{cs}</div>'

def board(key):
    cor, titulo, panels = C.BOARDS[key]
    cells = []
    for i, (sc, h, cap) in enumerate(panels):
        cells.append(f'<li class="bp"><span class="bp-n">{i+1}</span>'
                     f'<span class="bp-art">{scene(sc)}</span><b>{h}</b><i>{cap}</i></li>')
        if i < len(panels) - 1:
            cells.append('<li class="bp-arr" aria-hidden="true">→</li>')
    return (f'<figure class="board c-{cor} rev"><figcaption class="board-cap">'
            f'<span class="eyebrow">Como funciona</span><b>{titulo}</b></figcaption>'
            f'<ol class="board-strip">{"".join(cells)}</ol></figure>')

def foto(slug, alt, extra=""):
    return (f'<figure class="shot{extra}"><img src="/assets/{slug}.jpg" alt="{alt}" '
            f'loading="lazy" decoding="async"></figure>')

def mrow(media, h, p, flip=False):
    return (f'<div class="mrow{" flip" if flip else ""} rev"><div class="m-media">{media}</div>'
            f'<div class="m-copy"><h3>{h}</h3><p>{p}</p></div></div>')

def lista(items):
    return ('<ul class="check rev">' +
            "".join(f'<li><span class="ck"></span>{t}</li>' for t in items) + '</ul>')

# ---------------------------------------------------------------------- CSS
CSS = """
:root{
  --branco:#fff;--nevoa:#f5f5f7;--preto:#000;
  --tinta:#1d1d1f;--tinta-2:#6e6e73;--claro:#f5f5f7;--claro-2:#a1a1a6;
  --coral:#FF5A36;--coral-vivo:#FF8563;--coral-esc:#D93B18;--coral-leve:#FFEEE9;
  --roxo:#7C3AED;--verde:#1E9E63;--ambar:#B45309;
  --linha:rgba(0,0,0,.12);--maxw:1120px;
  --sec:var(--coral);
  --ease:cubic-bezier(.45,0,.55,1);
}
.c-coral{--sec:#FF5A36;--soft:#FFEEE9}
.c-roxo{--sec:#7C3AED;--soft:#F1EBFE}
.c-verde{--sec:#1E9E63;--soft:#E4F5EC}
.c-ambar{--sec:#B45309;--soft:#FBF0E2}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--branco);color:var(--tinta);
  font-family:-apple-system,BlinkMacSystemFont,'SF Pro Text','Inter',system-ui,sans-serif;
  font-size:17px;line-height:1.4705882353;letter-spacing:-.022em;-webkit-font-smoothing:antialiased}
h1,h2,h3{margin:0;font-weight:600;line-height:1.06;letter-spacing:-.015em;text-wrap:balance}
p{margin:0}ul,ol{margin:0;padding:0;list-style:none}
a{color:var(--coral);text-decoration:none}
img{display:block;max-width:100%}
:focus-visible{outline:3px solid var(--coral-vivo);outline-offset:3px;border-radius:6px}
.eyebrow{display:block;font-size:21px;font-weight:600;letter-spacing:.011em;color:var(--sec);margin-bottom:8px}
.lead{font-size:21px;line-height:1.381;letter-spacing:.011em;color:var(--tinta-2);margin-top:14px}

.nav{position:sticky;top:0;z-index:50;height:52px;display:flex;align-items:center;justify-content:space-between;
  padding:0 clamp(20px,4vw,40px);background:rgba(255,255,255,.72);
  backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);
  border-bottom:1px solid rgba(0,0,0,.08)}
.nav .brand{display:flex;align-items:center;gap:8px;font-weight:600;font-size:17px;color:var(--tinta);letter-spacing:-.02em}
.nav .brand img{width:24px;height:24px;border-radius:6px}
.nav .brand .tld{color:var(--coral)}
.nav-r{display:flex;align-items:center;gap:clamp(14px,3vw,26px);font-size:13px}
/* os <a> vivem DENTRO de .nav-links — sem display:flex aqui eles saem colados
   ("A batidaA prova"), porque o gap do .nav-r só separa os filhos diretos. */
.nav-links{display:inline-flex;align-items:center;gap:clamp(14px,2.2vw,24px)}
.nav-r a{color:var(--tinta);opacity:.85}
.nav-r a:hover{opacity:1;color:var(--coral)}
.nav-cta{background:var(--coral);color:#fff!important;padding:6px 14px;border-radius:980px;font-weight:500}
@media(max-width:760px){.nav-links{display:none}}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--coral);color:#fff;
  padding:12px 22px;border-radius:980px;font-weight:400;font-size:17px;letter-spacing:-.022em;
  transition:background-color .1s linear}
.btn:hover{background:var(--coral-esc)}
.btn-branco{background:#fff;color:var(--tinta)}
.btns{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:32px}

/* hero */
.hero{background:var(--preto);color:var(--claro);text-align:center;padding:clamp(64px,9vh,104px) 24px 0;overflow:hidden;
  background-image:radial-gradient(900px 500px at 50% -10%,rgba(255,90,54,.5),transparent 62%)}
.hero .eyebrow{color:var(--coral-vivo)}
.hero h1{font-size:clamp(40px,4.4vw+14px,76px);color:#fff;max-width:16ch;margin:0 auto}
.hero .sub{margin:22px auto 0;max-width:56ch;font-size:21px;line-height:1.4;color:var(--claro-2);letter-spacing:.011em}
.hero-stage{margin:56px auto 0;max-width:900px}
/* banner: a foto sobe do hero e é cortada pelo fim da seção (o corte é de propósito).
   Sem aspect-ratio ela entra inteira e o corte cai em lugar aleatório. */
.hero-stage img{width:100%;aspect-ratio:16/8;object-fit:cover;object-position:60% 16%;
  border-radius:24px 24px 0 0;box-shadow:0 -10px 60px rgba(255,90,54,.3)}

.credo{max-width:960px;margin:0 auto;padding:clamp(80px,10vw,130px) 24px;text-align:center}
.credo h2{font-size:clamp(30px,3.4vw+10px,52px);letter-spacing:-.02em}
.credo .g{color:var(--coral)}

/* capítulos */
.cap{padding:clamp(72px,9vw,120px) 0}
.cap.nevoa{background:var(--nevoa)}
.cap-in{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.cap-head{max-width:760px}
.cap-head h2{font-size:clamp(30px,2.4vw+14px,48px);letter-spacing:-.01em;margin-top:2px}

.fgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:44px}
.fc{background:var(--branco);border:1px solid var(--linha);border-radius:20px;padding:26px 24px;break-inside:avoid}
.cap.nevoa .fc{background:#fff;border-color:rgba(0,0,0,.06)}
.fc-mk{display:block;width:26px;height:3px;border-radius:3px;background:var(--sec);margin-bottom:16px}
.fc h3{font-size:20px;letter-spacing:-.01em}
.fc p{margin-top:8px;color:var(--tinta-2);font-size:16px;line-height:1.5}
.tg{display:inline-block;margin-left:8px;font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  color:var(--sec);background:var(--soft);padding:3px 8px;border-radius:980px;vertical-align:middle}

/* storyboard */
.board{margin:48px 0 0;padding:30px;border-radius:24px;background:var(--soft);break-inside:avoid}
.board-cap{margin-bottom:22px}
.board-cap b{display:block;font-size:22px;font-weight:600;letter-spacing:-.01em}
.board-strip{display:flex;align-items:stretch;gap:10px;flex-wrap:wrap}
.bp{flex:1 1 180px;background:#fff;border-radius:16px;padding:20px 18px;position:relative;break-inside:avoid}
.bp-n{position:absolute;top:14px;right:16px;font-size:12px;font-weight:700;color:var(--sec)}
.bp-art{display:block;color:var(--sec)}
.scene{width:56px;height:44px}
.bp b{display:block;margin-top:12px;font-size:17px;font-weight:600;letter-spacing:-.01em}
.bp i{display:block;margin-top:6px;font-style:normal;font-size:14.5px;line-height:1.45;color:var(--tinta-2)}
.bp-arr{display:flex;align-items:center;color:var(--sec);font-size:20px;opacity:.55}
@media(max-width:860px){.bp-arr{display:none}}

/* media row */
.mrow{display:grid;grid-template-columns:1.05fr .95fr;gap:44px;align-items:center;margin-top:48px}
.mrow.flip .m-media{order:2}
@media(max-width:860px){.mrow{grid-template-columns:1fr}.mrow.flip .m-media{order:0}}
.m-copy h3{font-size:26px;letter-spacing:-.012em}
.m-copy p{margin-top:12px;color:var(--tinta-2);font-size:17px;line-height:1.5}
.shot img{width:100%;border-radius:20px}

/* checklist */
.check{margin-top:36px;display:grid;gap:14px}
.check li{display:flex;gap:12px;align-items:flex-start;font-size:17px;line-height:1.45;break-inside:avoid}
.ck{flex:0 0 auto;width:20px;height:20px;margin-top:2px;border-radius:50%;background:var(--coral-leve);position:relative}
.ck::after{content:"";position:absolute;left:6px;top:5px;width:5px;height:9px;border:2px solid var(--coral-esc);
  border-top:0;border-left:0;transform:rotate(42deg)}

/* setores */
.setores{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:44px}
@media(max-width:860px){.setores{grid-template-columns:repeat(2,1fr)}}
.setor{break-inside:avoid}
.setor img{width:100%;aspect-ratio:2/3;object-fit:cover;border-radius:18px}
.setor b{display:block;margin-top:12px;font-size:18px;font-weight:600;letter-spacing:-.01em}
.setor span{display:block;margin-top:4px;font-size:14.5px;line-height:1.45;color:var(--tinta-2)}

/* preço */
.planos{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:44px}
@media(max-width:860px){.planos{grid-template-columns:1fr}}
.plano{border:1px solid var(--linha);border-radius:24px;padding:30px 26px;background:#fff;break-inside:avoid}
.plano .nome{font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--tinta-2)}
.plano .v{margin-top:14px;font-size:46px;font-weight:600;letter-spacing:-.03em;line-height:1}
.plano .u{margin-top:6px;font-size:14px;color:var(--tinta-2)}
.plano p{margin-top:14px;font-size:15.5px;line-height:1.5;color:var(--tinta-2)}
.plano.hi{background:var(--preto);border-color:var(--preto);color:var(--claro)}
.plano.hi .nome{color:var(--coral-vivo)}
.plano.hi .v{color:#fff}
.plano.hi .u,.plano.hi p{color:var(--claro-2)}
.naos{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:20px}
@media(max-width:860px){.naos{grid-template-columns:1fr}}
.nao{border-radius:20px;padding:24px;background:#fff;border:1px solid var(--linha);break-inside:avoid}
.nao h4{margin:0;font-size:18px;font-weight:600;letter-spacing:-.01em}
.nao p{margin-top:8px;font-size:15.5px;line-height:1.5;color:var(--tinta-2)}

/* lineup */
.lineup{background:var(--preto);color:var(--claro);padding:clamp(80px,10vw,130px) 0}
.lineup-in{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.lineup h2{font-size:clamp(30px,2.4vw+14px,48px);color:#fff}
.lineup .lead{color:var(--claro-2)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:44px}
.tile{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:20px;padding:24px;break-inside:avoid}
.tile h3{font-size:18px;color:#fff}
.tile p{margin-top:8px;font-size:15px;line-height:1.5;color:var(--claro-2)}
.tile-mk{display:block;width:26px;height:3px;border-radius:3px;background:var(--sec);margin-bottom:14px}

/* cta / download / rodapé */
.cta{text-align:center;padding:clamp(88px,11vw,140px) 24px;background:
  radial-gradient(1100px 560px at 50% 0%,rgba(255,90,54,.5),transparent 65%),#0b0a0e;color:var(--claro)}
.cta h2{font-size:clamp(30px,3vw+12px,52px);color:#fff;max-width:18ch;margin:0 auto}
.cta p{margin:20px auto 0;max-width:52ch;font-size:19px;line-height:1.5;color:var(--claro-2)}
.dl{text-align:center;padding:clamp(64px,8vw,96px) 24px;background:var(--nevoa)}
.dl h2{font-size:30px}
.dl p{margin-top:12px;color:var(--tinta-2)}
.foot{border-top:1px solid var(--linha);padding:36px 24px;background:var(--nevoa)}
.foot-in{max-width:var(--maxw);margin:0 auto;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;
  color:var(--tinta-2);font-size:13px}

/* reveal */
.rev{opacity:0;transform:translateY(30px);transition:opacity .9s var(--ease),transform .9s var(--ease)}
.rev.vis{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.rev{opacity:1;transform:none}html{scroll-behavior:auto}}

/* ======================= IMPRESSÃO / PDF =======================
   As três travas do playbook. Mexer aqui quebra o PDF em silêncio. */
@media print{
  /* 1. sem isto o PDF sai EM BRANCO (o reveal nunca dispara sem scroll) */
  .rev{opacity:1!important;transform:none!important}
  /* 2. sem isto hero/CTA/fotos saem sem cor */
  *{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}
  /* 3. só nas unidades atômicas — NUNCA por capítulo (gera página quase vazia) */
  .fc,.bp,.plano,.nao,.tile,.setor,.board,.check li{break-inside:avoid}
  .nav,.dl,.btns{display:none!important}
  .cap{padding:28px 0}
  .hero{padding-top:36px}
  .credo{padding:44px 24px}
  body{font-size:11.5pt}
  a{color:inherit;text-decoration:none}
  /* sem isto o Chrome imprime em Letter (padrão americano) — no Brasil é A4 */
  @page{size:A4;margin:14mm}
}
"""

SCRIPT = """<script>
(function(){
  if(matchMedia("(prefers-reduced-motion: reduce)").matches){
    document.querySelectorAll(".rev").forEach(function(e){e.classList.add("vis")});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){e.target.classList.add("vis");io.unobserve(e.target)}})},
    {threshold:0,rootMargin:"0px 0px -12% 0px"});
  document.querySelectorAll(".rev").forEach(function(e){io.observe(e)});
})();
</script>"""

# --------------------------------------------------------------------- montagem
def build():
    _CHAP[0] = 0
    wa_svg = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" style="width:18px;height:18px">'
              '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.6 0-3.1-.4-4.4-1.2'
              'l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>')

    nav = f'''<nav class="nav">
  <a class="brand" href="/"><img src="/assets/brand-mark.png" width="24" height="24" alt="">
    <span>atendeaqui<span class="tld">.app</span></span></a>
  <span class="nav-r"><span class="nav-links">
    <a href="#caixa">A caixa</a><a href="#robo">Robô e humano</a>
    <a href="#preco">Preço</a><a href="#limites">O que não faz</a></span>
  <a class="nav-cta" href="{WA}">Falar no WhatsApp</a></span>
</nav>'''

    hero = f'''<header class="hero">
  <span class="eyebrow">{C.HERO["eyebrow"]}</span>
  <h1>{C.HERO["h1"]}</h1>
  <p class="sub">{C.HERO["sub"]}</p>
  <div class="btns"><a class="btn btn-branco" href="{WA}">{wa_svg} Falar no WhatsApp</a></div>
  <div class="hero-stage rev"><img src="/assets/hero.jpg" width="1600" height="1067"
    alt="Atendente respondendo clientes na caixa de entrada do atendeaqui."></div>
</header>'''

    credo = f'<section class="credo rev"><h2>{C.CREDO}</h2></section>'

    cap_caixa = chapter("caixa", "A caixa", "Uma caixa, o time inteiro.",
        "WhatsApp (quantos números você quiser), chat do site e Telegram caem no mesmo lugar. "
        "A conversa entra no setor certo e cai em quem está livre.",
        board("fila"), cards(C.CAIXA, "coral"))

    cap_robo = chapter("robo", "Robô e humano", "O cliente não repete nada.",
        "O robô atende primeiro e resolve o que é repetido. Quando o assunto exige gente, ele "
        "passa a conversa — e o histórico inteiro vai junto, já na tela do atendente.",
        board("bastao"),
        mrow(foto("bento-copiloto", "Atendente lendo a sugestão do copiloto na tela."),
             "A terceira frase é onde os outros fazem recomeçar.",
             "“Quero falar com uma pessoa.” Aqui, a conversa do robô é a mesma conversa do "
             "humano — o atendente entra lendo o que já foi dito.", True),
        cards(C.ROBO, "coral"))

    cap_cresce = chapter("cresce", "Recursos", "O que o time liga quando cresce.",
        "Nada disso é obrigatório. Cada setor decide o que usar.",
        mrow(foto("bento-audio", "Áudio do cliente transcrito em texto embaixo do player."),
             "O áudio de três minutos vira texto.",
             "A transcrição aparece embaixo do player — dá pra ler no meio de uma reunião. E ela "
             "entra na busca."),
        cards(C.CRESCE, "roxo"))

    cap_painel = chapter("painel", "Painel", "O fim do “como foi o atendimento hoje?”",
        "Quanto o cliente esperou, quanto durou e quantas conversas cada pessoa encerrou — por "
        "atendente e por setor, no período que você escolher.",
        mrow(foto("bento-fila", "Painel do supervisor com fila e tempos de espera."),
             "A nota vem com o comentário — e com o nome de quem atendeu.",
             "Não é uma média solta no fim do mês: é a satisfação do cliente ao lado da pessoa "
             "que respondeu.", True),
        cards(C.PAINEL, "ambar"))

    setores = "".join(
        f'<figure class="setor rev"><img src="/assets/{s}.jpg" alt="{r}" loading="lazy" decoding="async">'
        f'<b>{r}</b><span>{d}</span></figure>' for s, r, d in C.SETORES)
    cap_quem = chapter("quem", "Para quem é", "Se o cliente manda mensagem, serve.",
        "Muda o assunto, não a caixa.",
        f'<div class="setores">{setores}</div>',
        '<div class="cap-head rev" style="margin-top:64px"><h2 style="font-size:30px">'
        'O que dói hoje.</h2></div>',
        lista(C.DORES))

    planos = "".join(
        f'<div class="plano{" hi" if i == 1 else ""}"><div class="nome">{n}</div>'
        f'<div class="v">{v}</div><div class="u">{u}</div><p>{d}</p></div>'
        for i, (n, v, u, d) in enumerate(C.PRECO))
    naos = "".join(f'<div class="nao"><h4>{t}</h4><p>{d}</p></div>' for t, d in C.NAOS)
    cap_preco = chapter("preco", "Preço", "R$ 49 por atendente. Só isso.",
        "Não cobramos por conversa, nem por número de WhatsApp, nem por mensagem que o robô mandou.",
        f'<div class="planos rev">{planos}</div>',
        f'<div class="naos rev">{naos}</div>')

    cap_limites = chapter("limites", "Honestidade", "O que a gente ainda não faz.",
        "Todo material de software mostra só o que sabe fazer. Isto aqui é o que a caixa "
        "<b>não</b> resolve — melhor você saber agora do que na segunda semana.",
        cards(C.NAO_FAZ, "ambar"))

    tiles = "".join(f'<article class="tile c-{c}"><span class="tile-mk"></span>'
                    f'<h3>{n}{tag(g)}</h3><p>{d}</p></article>' for n, d, c, g in C.TILES)
    lineup = f'''<section class="lineup" id="modulos">
  <div class="lineup-in">
    <h2 class="rev">Tudo o que ela faz.</h2>
    <p class="lead rev">Cada setor liga o que precisa. Nada aqui é opcional pago.</p>
    <div class="tiles rev">{tiles}</div>
  </div>
</section>'''

    h2, p = C.CTA
    cta = f'''<section class="cta">
  <h2 class="rev">{h2}</h2>
  <p class="rev">{p}</p>
  <div class="btns rev"><a class="btn btn-branco" href="{WA}">{wa_svg} Falar no WhatsApp</a></div>
</section>'''

    dl = '''<section class="dl">
  <h2>Leve o livreto com você.</h2>
  <p>Baixe o PDF para apresentar offline ou mandar por e-mail.</p>
  <div class="btns"><a class="btn" href="/livreto.pdf" download="livreto-atendeaqui.pdf">
    Baixar o livreto (PDF)</a></div>
</section>'''

    body = "\n".join([nav, hero, credo, cap_caixa, cap_robo, cap_cresce, cap_painel,
                      cap_quem, cap_preco, cap_limites, lineup, cta, dl])

    hoje = datetime.date.today().strftime("%d/%m/%Y")
    sha = hashlib.sha1(body.encode()).hexdigest()[:7]
    foot = (f'<footer class="foot"><div class="foot-in">'
            f'<span>atendeaqui · atendimento no WhatsApp para empresas · '
            f'<a href="/privacidade">Privacidade</a></span>'
            f'<span>Livreto v{hoje} · {sha}</span></div></footer>')

    desc = ("Livreto do atendeaqui: WhatsApp, chat do site e Telegram numa caixa só. O robô "
            "resolve o repetido e passa o resto pro time com o histórico junto. Copiloto de IA, "
            "transcrição de áudio e painel. R$ 49 por atendente/mês, grátis com 1.")
    url = f"{C.SITE}/livreto"
    head = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Livreto do atendeaqui — atendimento no WhatsApp numa caixa só</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="atendeaqui">
<meta property="og:locale" content="pt_BR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="Livreto do atendeaqui">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{C.SITE}/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600&display=swap" rel="stylesheet">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication",
"name":"atendeaqui","applicationCategory":"BusinessApplication","operatingSystem":"Web",
"url":"{url}","inLanguage":"pt-BR","description":"{desc}",
"offers":{{"@type":"Offer","price":"49.00","priceCurrency":"BRL"}},
"featureList":["Caixa de entrada única (WhatsApp, chat do site, Telegram)",
"Robô que resolve o repetido e passa o histórico ao atendente",
"Copiloto de IA que redige a resposta a partir da base do setor",
"Transcrição de áudio","Assunto automático por IA","Chat interno",
"Distribuição automática de conversas","Painel e pesquisa de satisfação"]}}</script>
<style>{CSS}</style>
</head>
<body>
'''
    doc = head + body + "\n" + foot + "\n" + SCRIPT + "\n</body>\n</html>\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc)
    print(f"[livreto] {OUT} — {len(doc)//1024} KB · v{hoje} · {sha}")

build()
