# atendeaqui-site — playbook

Site institucional do **atendeaqui** (WhatsApp, chat do site e Telegram numa caixa de entrada
só). Estático, sem build de framework. Servido por **GitHub Pages** em
`https://www.atendeaqui.app`.

É um produto **fora do nicho condomínio** — o ERP SeuCondomínio é o motor, mas o cliente daqui
é qualquer empresa que atende no WhatsApp, e nada na copy pode lembrar condomínio. A fonte da
verdade do que pode ser prometido é `app/services/atendimento_humano/ROADMAP.md` **no repo do
ERP** (`denoww/seucondominio`). Nada entra na copy sem estar entregue lá.

> Este arquivo nasceu em 10/09/2026, na revisão do eixo multi-produto — era o único dos três
> sites irmãos sem playbook na raiz, e quem editasse aqui não recebia nada do que está abaixo.
> Mapa do eixo (os 5 produtos, o registry, a dívida): `ROADMAP_multi_produto.md` no repo do ERP.

## Deploy

> **Deploy = `git push`.** Não existe passo separado.

GitHub Pages publica o `main` direto (~40–60s + CDN). Para conferir que produção já serve o
seu commit — não confie no "subiu":

```bash
diff <(curl -s https://www.atendeaqui.app/index.html) index.html && echo "prod == HEAD"
```

**Domínio:** o `CNAME` do repo é `www.atendeaqui.app` (host canônico). ⚠️ **`.app` é um TLD com
HSTS preload**: sem certificado o navegador recusa a conexão, sem opção de prosseguir — `curl`
por HTTP responder 200 **não** significa "no ar".

⚠️ **Pages em `errored` não provisiona certificado** (cicatriz do `acompanhaobra-site`, 20/08/2026):
pushes concorrentes derrubaram um deploy e o site ficou horas sem cert, sem aviso. Diagnóstico:
`gh api repos/denoww/atendeaqui-site/pages`.

## Estrutura

| O quê | Onde |
|---|---|
| Landing (CSS + HTML + JS num arquivo) | `index.html` |
| Livreto de vendas (gerado) | `livreto/` → `content.py` é 95% das mudanças |
| Ponte de login | `entrar.html` |
| Política de privacidade | `privacidade.html` |
| Fotos (JPEG otimizado) | `assets/` |

**Fonte única de contato e login:** os dotfiles `.whatsapp` e `.login` na raiz. Dotfile não é
publicado pelo Pages, e o `guarda.yml` reprova o push se algum `wa.me` ou algum link de `/logar`
no HTML divergir. Trocou de número? Edite `.whatsapp` e mais nada.

O `.login` aponta pra `https://app.atendeaqui.app/logar?no_layout=true` — host próprio, que é um
**distribution tenant** da distribution CloudFront `erpsc` do ERP. O `?no_layout=true` já é
redundante desde 10/09/2026 (o ERP tira o chrome sozinho em host de marca), mas fica: é o
contrato que o `guarda.yml` valida.

## Design — padrão Apple

Herdado do `baterponto-site` (que tirou os números do CSS de produção da apple.com):

- **Tipografia**: tracking **não-monotônico** — `-.015em` em 80px, ~zero em 40px, **positivo**
  em 21px. Peso de título **600**, nunca 700.
- **Superfícies**: branco ↔ `#f5f5f7` ↔ preto, alternando. **Sem borda entre seções** — o
  divisor é o contraste de fundo.
- **Cards**: radius 28px e **`box-shadow: none`**. **Botões**: pill `border-radius: 980px`.
- **Movimento**: `opacity 0→1` + `translateY(30px)→0`, **900ms**, dispara **uma vez**.

⚠️ **Duas variáveis de coral, e trocá-las quebra acessibilidade.** `--coral` (`#FF5A36`) é
**botão e foco**; `--coral-esc` (`#D93B18`) é **link e eyebrow sobre fundo claro**. O motivo é
medido: `#FF5A36` com texto branco dá **3,10:1** e reprova o AA de 4,5:1 — é a única das três
marcas irmãs cuja primária não serve como superfície sólida. O ERP tem a mesma distinção no
registry (`cor` × `cor_solida`) e um spec que trava o contraste.

⚠️ **As variáveis de borda aqui são `--fio` / `--fio-esc`** — nas irmãs são `--linha`. Não é
descuido a corrigir sem motivo; é só divergência de nome. Ao copiar bloco de CSS de outro site
da família, confira o nome antes.

**Sem Google Fonts de propósito.** A stack começa em `-apple-system`/`BlinkMacSystemFont`: era
CSS de terceiro no caminho crítico por quase nada, e entregava o IP do visitante a um terceiro
que a política de privacidade teria de declarar.

## A regra que manda em tudo: só o que roda

O guard `.github/scripts/seo.py` reprova o push. As proibições que são **específicas deste
produto** (as outras — prova social inventada, concorrente pelo nome, marcador de rascunho —
valem nos três sites):

- ⛔ **"API oficial" do WhatsApp.** O canal roda via **Z-API**. Dizer oficial é declaração falsa
  sobre a natureza da integração — e é o que o cliente cobra quando descobre.
- ⛔ **Instagram, Direct e Messenger** não existem no produto. Não prometer canal que não está
  ligado.
- ⛔ **"baixe o app" / "disponível na Play Store".** O app do atendente existe
  (`~/workspace/atendeaqui-app`, autenticando por OAuth com o scope `app_atendimento`), mas
  **não está publicado em loja** — e o `flavors.yaml` dele ainda é cópia byte-a-byte do
  baterponto, sem flavor `atendeaqui` próprio.
- ⛔ **Métrica de acurácia/uptime** (99,9%, "X% de precisão") e garantia absoluta.

## Medição — GA4 `G-6MP19GRPQ7`

Existe por um motivo só: o lead deste site é um **clique para fora** (`wa.me`), e sem isso não
dá pra saber se o blog e as páginas novas trazem cliente. O evento é `contato_whatsapp`, por
listener **delegado no document** — pega os CTAs de hoje e os das páginas que ainda vão nascer.

⚠️ **Nenhum sinal de anúncio.** `ad_storage`/`ad_user_data`/`ad_personalization` nascem `denied`
e `allow_google_signals:false`. O opt-out de `/privacidade` grava `localStorage['sem-analytics']`
e o `window['ga-disable-…']` precisa vir **antes** do `gtag.js`, senão a primeira medição já saiu.

## Cicatrizes (bugs reais desta base e das irmãs)

- **`git diff --quiet` não vê arquivo untracked.** O `livreto.yml` decidia assim se commitava o
  espelho; num repo novo o `livreto.pdf` nasce untracked, então o job gerava as páginas, passava
  no guard de página em branco e dizia "nada mudou" — `/livreto.pdf` respondia 404 sem nenhum
  workflow vermelho. Corrigido aqui em 10/09/2026 (`git status --porcelain`).
- **Referenciar foto que não existe não quebra nada visível** — vira `<img>` 404 dentro do PDF, e
  o guard de página em branco não pega porque a página tem texto. Ao adicionar `foto("x")` no
  livreto, confira `assets/x.jpg`.
- **Foto de fundo atrás de texto no mobile** vira borrão. Texto em campo sólido, foto inteira
  embaixo. Não "resolva" com opacidade.
- **Escopo de CSS vaza**: um `.ft a{text-decoration:underline}` grifou o logotipo do rodapé.
- **Crop central decapita.** As fotos saem 3:2 do gerador e o hero é 16:9 — o corte tira topo e
  base, e é no topo que estão as cabeças.

## Imagens

**Doutrina: foto = gerador de imagem, UI = HTML/CSS.** Nunca peça interface ao gerador — ele
alucina texto e borra a tipografia. Print de conversa é HTML/CSS à mão, e leva `<figcaption>`
dizendo que é exemplo: sem isso, um diálogo inventado ao lado de um nome de empresa lê como
cliente real.

## Como verificar

- **Layout**: screenshot em **1440px e 412px**. Vários bugs só existem no mobile.
- **Guard**: `python3 .github/scripts/seo.py` local, e force uma violação de propósito para ver
  o vermelho — "um workflow que nunca foi executado não vale nada".
- **Login**: o `guarda.yml` faz `curl` no `.login` esperando 200, mas como **aviso** — deploy do
  ERP não pode travar push de site. Se o login quebrou, o site não fica vermelho: confira à mão.
- **Produção**: compare o artefato local com o que o servidor entrega (o `diff` do topo).
