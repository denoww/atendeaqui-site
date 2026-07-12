# Livreto do atendeaqui — playbook

Peça de vendas do comercial: página pública (`/livreto`) + PDF baixável (`/livreto.pdf`).

Pipeline portado do livreto do **baterponto**, que herda a doutrina do **SeuCondomínio**
(`~/workspace/seucondominio/livreto/CLAUDE.md`). Marca: **coral `#FF5A36`**.

## A regra de ouro (o "espelho")

> **Edite `content.py` e dê push. Só isso.**
> O HTML e o PDF se regeneram sozinhos no CI e o bot commita o espelho.

- **NÃO rode `build.py` nem `build_pdf.sh` na mão.** Se rodar, o CI só confirma que já estava
  em dia.
- O espelho é [`.github/workflows/livreto.yml`](../.github/workflows/livreto.yml). Ele:
  1. gera o HTML; 2. compara um **fingerprint do conteúdo** (`.espelho.sha` = sha do HTML +
  todos os assets); 3. só refaz o PDF se mudou; 4. **barra o build se alguma página sair em
  branco**; 5. commita o espelho.

## Conteúdo é aterrado — e o app AINDA NÃO ESTÁ NA LOJA

Fonte da verdade, nesta ordem:
1. o site **https://www.atendeaqui.app** (é o que o cliente vê)
2. **`~/workspace/atendeaqui-app/ROADMAP.md`** ← o que está pronto vs o que falta
3. o backend, no ERP SeuCondomínio (módulo `atendimento_humano`)

**A regra que mais importa aqui: nunca vender roadmap como pronto.**
O ROADMAP (2026-07-11) diz: ondas 0, 1, 2, 3 e 5 ✅ feitas e deployadas; falta a **Onda 4
(push)**, e o **app do atendente não está publicado na loja**. Consequências para a copy:

- a caixa é vendida como ela é: **abre no navegador**, inclusive no do celular;
- **app na loja** e **push** ficam no capítulo *"O que a gente ainda não faz"*;
- **Instagram/Messenger não existem** hoje — não prometa. São WhatsApp (quantos números
  quiser), chat do site e Telegram.

Quando o app for publicado (ou o push sair), **tire do capítulo de honestidade e vire card** —
não antes.

## Regras de copy (não negociáveis)

- **Zero prova social inventada.** Nada de "X empresas", "Y mil conversas".
- **Nunca citar concorrente pelo nome.**
- **O atendente não é o problema.** A peça vende **alívio** para ele (a conversa chega lida,
  o rascunho já vem escrito), nunca vigilância.
- **O robô não "resolve tudo"** — ele resolve o repetido e passa o resto. É **decisão de
  produto**, e a peça diz isso com orgulho: robô que insiste faz o cliente repetir.

## Onde editar

| Quero mudar | Arquivo |
|---|---|
| Texto/dados (cards, storyboards, tiles, preço) — **95% das mudanças** | `content.py` |
| Capítulos, CSS, print CSS | `build.py` |
| Cenas dos storyboards (line-art SVG) | `build.py` → `SCENES` |

`livreto/index.html` e `livreto.pdf` são **gerados** — o CI sobrescreve.

## Pegadinhas (quebram em silêncio)

- **`@media print`**: sem `.rev{opacity:1}` o **PDF sai EM BRANCO**; sem
  `print-color-adjust:exact` sai sem cor; `break-inside:avoid` só nas unidades atômicas (nunca
  por capítulo); sem `@page{size:A4}` o Chrome imprime em **Letter**.
  → O CI mede o desvio-padrão das páginas 1 e 5 (branco = 0). **Mas só olha essas duas.**
- **Traço de SVG**: use `stroke` explícito no elemento.
- **O PDF do Chrome não é determinístico** (carimba `CreationDate`). Por isso o gate compara o
  **conteúdo**, não os bytes — senão o CI commitaria megabytes de binário a cada push.
- **O fingerprint tem que ser reproduzível.** Auditar:
  ```bash
  find livreto/index.html assets -type f | LC_ALL=C sort | xargs sha256sum | sha256sum | cut -c1-16
  # tem que bater com livreto/.espelho.sha
  ```
