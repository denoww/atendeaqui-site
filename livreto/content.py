# -*- coding: utf-8 -*-
"""Conteúdo do livreto do atendeaqui — 95% das mudanças acontecem AQUI.

VOCÊ SÓ PRECISA EDITAR ESTE ARQUIVO. O HTML e o PDF se regeneram sozinhos no CI
(.github/workflows/livreto.yml) assim que você der push — o PDF é um ESPELHO
automático. Não rode build.py nem build_pdf.sh na mão.

FONTE DA VERDADE, nesta ordem:
  1. o site https://www.atendeaqui.app (é o mais novo e o que o cliente vê)
  2. ~/workspace/atendeaqui-app/ROADMAP.md  ← o que está PRONTO vs o que falta
  3. o backend, no ERP SeuCondomínio (módulo `atendimento_humano`)

REGRA DE OURO DO CONTEÚDO: **nunca vender roadmap como pronto.**
O ROADMAP (2026-07-11) diz: ondas 0,1,2,3,5 ✅ feitas e deployadas; falta a Onda 4
(push), e o app do atendente NÃO está publicado na loja. Por isso:
  - a caixa é vendida como ela é: abre no NAVEGADOR (inclusive do celular)
  - o app na loja fica no capítulo "O que a gente ainda não faz"
  - nada de prometer Instagram/Messenger (não existe hoje)

REGRAS DE COPY (herdadas do playbook dos livretos):
  - PROIBIDO prova social inventada: nada de "X empresas", "Y mil conversas".
  - Nunca citar concorrente pelo nome.
  - O atendente não é o problema — a peça vende ALÍVIO pra ele, não vigilância.
  - O robô NÃO "resolve tudo": ele resolve o repetido e passa o resto. É de propósito.
"""

WA = "https://wa.me/5562996701278"
WA_TXT = "?text=Ol%C3%A1%21%20Vi%20o%20livreto%20do%20atendeaqui%20e%20quero%20conhecer."
SITE = "https://www.atendeaqui.app"

# ---------------------------------------------------------------- hero / credo
HERO = {
    "eyebrow": "Livreto",
    "h1": "Ninguém fica sem resposta.",
    "sub": "WhatsApp, chat do site e Telegram numa caixa de entrada só. O robô resolve o "
           "repetido. O time assume o resto — com a conversa inteira já lida.",
}

CREDO = ('O cliente não repete nada. <span class="g">Nem para o robô, nem para o humano.</span>')

# ---------------------------------------------------------------- storyboards
BOARDS = {
    "bastao": ("coral", "A passagem de bastão que não faz o cliente recomeçar", [
        ("msg",    "O cliente escreve",   "WhatsApp, chat do site ou Telegram — tudo cai na mesma caixa."),
        ("robo",   "O robô resolve",      "O que é repetido ele responde pela base de conhecimento do setor."),
        ("passa",  "Passa o bastão",      "Saiu do roteiro, vira conversa humana — e o histórico vai junto."),
        ("humano", "O atendente entra lendo", "Ele já sabe o que foi dito. Ninguém pede pra “explicar de novo”."),
    ]),
    "fila": ("verde", "Da mensagem nova ao encerramento", [
        ("fila",     "Cai na fila",        "A conversa entra no setor certo — financeiro, comercial, suporte."),
        ("distrib",  "Cai em quem está livre", "Rodízio, menos carregado ou puxar na mão. O time escolhe."),
        ("relogio",  "O relógio corre",    "Quem espera demais fica vermelho — antes de virar reclamação."),
        ("tag",      "Encerra com assunto","A IA marca o assunto no fim. O painel do mês se escreve sozinho."),
    ]),
}

# ---------------------------------------------------------------- capítulos
# (título, descrição, selo)  — selo "" = produção. NUNCA vender roadmap como pronto.
CAIXA = [
    ("Um número, uma caixa",
     "O WhatsApp que a sua empresa já usa vira a entrada. Não troca de número. Tem mais de um? "
     "Todos entram na mesma caixa, e o filtro por conta separa.", ""),
    ("Três canais, a mesma tela",
     "WhatsApp (quantos números quiser), chat do site e Telegram. O atendente não pula de "
     "aplicativo — e o cliente não escolhe por onde falar.", ""),
    ("Setores de verdade",
     "Financeiro, comercial, suporte. Cada setor tem seu time, sua forma de distribuir e seu "
     "tempo-alvo de resposta.", ""),
    ("A conversa cai sozinha",
     "Rodízio, menos carregado ou puxar na mão. Quem fica disponível recebe o que estava parado "
     "desde a madrugada.", ""),
    ("Abre no navegador",
     "Inclusive no do celular. Nada pra instalar, nada pra aprovar na loja.", ""),
]

ROBO = [
    ("O robô resolve o repetido",
     "Segunda via, horário, status. O que se responde igual todo dia, ele responde — pela base "
     "de conhecimento do setor.", ""),
    ("E passa o que exige gente",
     "Quando o assunto sai do roteiro, vira conversa humana. O histórico inteiro vai junto, já "
     "na tela do atendente.", ""),
    ("Fora do horário ele segue",
     "Em vez de deixar no vácuo, o robô responde pela base. A aba “Bot ao vivo” mostra o que ele "
     "está atendendo agora — e você assume com um clique.", ""),
    ("Ele não resolve tudo — de propósito",
     "Um robô que insiste em resolver o que não sabe é um robô que faz o cliente repetir. "
     "Aqui ele entrega cedo.", ""),
]

CRESCE = [
    ("Copiloto: a resposta já vem escrita",
     "A IA lê a pergunta, procura na base de conhecimento **do setor** e escreve o rascunho. "
     "Ela não inventa a partir da internet. Quem envia é sempre o atendente.", "IA"),
    ("O áudio de 3 minutos vira texto",
     "A transcrição aparece embaixo do player — dá pra ler no meio de uma reunião. E ela entra "
     "na busca.", "IA"),
    ("Assunto automático",
     "A IA marca o assunto ao encerrar. Sem isso, ninguém preenche — e o relatório do mês vira "
     "chute.", "IA"),
    ("Chat interno",
     "Canal por setor, mensagem direta e anotação privada dentro da própria conversa. O time "
     "combina sem abrir outro aplicativo.", ""),
    ("Dois relógios de espera",
     "O de quem está na fila sem ninguém, e o de quem já está em atendimento e ficou sem "
     "resposta. Quem espera demais fica vermelho.", ""),
    ("Pesquisa de satisfação",
     "A nota que o cliente deu, com o comentário dele, do lado do nome de quem atendeu.", ""),
]

PAINEL = [
    ("Quanto o cliente esperou",
     "Tempo até a primeira resposta, por atendente e por setor, no período que você escolher.", ""),
    ("Quanto durou e quantas encerraram",
     "Duração do atendimento e conversas encerradas por pessoa.", ""),
    ("A nota, com o comentário",
     "Satisfação do cliente ao lado do nome de quem atendeu — não uma média solta.", ""),
]

# Setores: (slug da foto, rótulo, dor concreta)
SETORES = [
    ("setor-administradora", "Administradoras", "Centenas de condôminos perguntando boleto e 2ª via no mesmo número."),
    ("setor-clinica",        "Clínicas",        "Agendamento, remarcação e confirmação — tudo por mensagem, o dia todo."),
    ("setor-imobiliaria",    "Imobiliárias",    "Lead que some se ninguém responde em minutos."),
    ("setor-loja",           "Lojas e serviços","Pedido, prazo e troca chegando junto no WhatsApp da loja."),
]

DORES = [
    "A mensagem chega no celular de uma pessoa só — e o resto do time não vê.",
    "O cliente explica tudo pro robô e explica tudo de novo pro humano.",
    "Fora do horário, a conversa fica no vácuo até alguém lembrar.",
    "Ninguém sabe quem está esperando há três horas até virar reclamação.",
    "O áudio de três minutos ninguém ouve — e a resposta atrasa mais.",
    "No fim do mês, “como foi o atendimento?” vira chute.",
]

# ---------------------------------------------------------------- preço
PRECO = [
    ("Começar", "Grátis", "com 1 atendente",
     "Para sempre — não é teste de 14 dias. Todos os canais, robô e copiloto inclusos, sem cartão."),
    ("Equipe", "R$ 49", "por atendente/mês",
     "Preço único, do segundo atendente ao vigésimo. Você paga por quem responde — não por "
     "quanta gente te procura."),
    ("Escala", "20+", "sob proposta",
     "Preço por volume abaixo de R$ 49, vários setores e integração com o sistema que você já usa."),
]

NAOS = [
    ("Não cobramos por conversa",
     "Nem por mensagem que o robô mandou. Uma campanha que dá certo não vira uma fatura que "
     "assusta."),
    ("Não cobramos por número",
     "Conecte quantos números de WhatsApp a empresa tiver. Todos caem na mesma caixa."),
    ("Sem fidelidade",
     "Mês a mês, sem carência e sem multa. O produto tem que segurar você — não o contrato."),
]

# ---------------------------------------------------------------- honestidade
# Vem do site (#honesto) + do ROADMAP do app. Se entrar em produção, sai daqui.
NAO_FAZ = [
    ("Instagram e Messenger: ainda não",
     "Hoje são WhatsApp (quantos números você quiser), chat do site e Telegram. Se o seu "
     "atendimento vive no Direct, a caixa ainda não te serve.", ""),
    ("O robô não resolve tudo",
     "Ele resolve o repetido; o resto vira conversa humana. Isso é decisão de produto, não "
     "limitação — robô que insiste faz o cliente repetir.", ""),
    ("O app do atendente não está na loja",
     "A caixa abre no navegador, inclusive no do celular. O aplicativo está pronto e já recebe "
     "notificação, mas ainda não foi publicado — e enquanto não estiver na loja, ele não é "
     "vendido aqui.", ""),

]

# ---------------------------------------------------------------- lineup
TILES = [
    ("Caixa única",         "WhatsApp, chat do site e Telegram na mesma tela.",        "coral",  ""),
    ("Robô que passa o bastão", "Resolve o repetido e entrega com o histórico junto.", "coral",  ""),
    ("Copiloto",            "Rascunho da resposta, da base do seu setor.",             "roxo",   "IA"),
    ("Distribuição",        "Rodízio, menos carregado ou puxar na mão.",               "verde",  ""),
    ("Transcrição de áudio","O áudio vira texto — e entra na busca.",                  "roxo",   "IA"),
    ("Assunto automático",  "A IA marca o assunto ao encerrar.",                       "roxo",   "IA"),
    ("Chat interno",        "Canal, DM e anotação privada na conversa.",               "verde",  ""),
    ("Tempo de espera",     "Dois relógios. Quem espera demais fica vermelho.",        "ambar",  ""),
    ("Painel e satisfação", "1ª resposta, encerradas e a nota com o comentário.",      "ambar",  ""),
]

CTA = ("Seu time atende na mesma caixa amanhã.",
       "Grátis com 1 atendente. R$ 49 por atendente depois disso. Conte como o seu atendimento "
       "funciona hoje e a gente mostra a caixa rodando com o seu cenário.")
