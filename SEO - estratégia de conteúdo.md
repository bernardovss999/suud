# Suud — pesquisa de SEO e estratégia de conteúdo

Pesquisa feita em 08/10/2026 com buscas no Google sobre culinária árabe em Niterói.

## O que a pesquisa mostrou

- **Pouca concorrência com conteúdo próprio.** Para "restaurante árabe Niterói / Icaraí", os resultados são quase todos diretórios (Telelistas, magicpin, apps de delivery) e listas de São Paulo ou do Rio. Nenhum restaurante árabe de Niterói tem uma página bem escrita e focada no tema.
- **"Mezze em Niterói" não tem dono.** Nenhuma casa da cidade aparece explicando ou vendendo mezze. Por isso o site dedica uma seção inteira ao assunto ("O que é mezze").
- **As buscas de delivery caem em apps** (99Food, iFood, Rappi). O site disputa essas buscas com uma página própria e um caminho de pedido direto pelo WhatsApp, sem a comissão do app.
- **Perguntas informativas** ("o que é babaganoush", "o que é kibe cru", "diferença entre hummus e babaganoush") aparecem em respostas de IA e em blocos de perguntas do Google. O FAQ do site responde cada uma em 1 ou 2 frases, que é o formato que essas respostas usam.

## Palavras-chave e onde estão no site

| Intenção | Termo principal | Onde está |
|---|---|---|
| Achar o restaurante | restaurante árabe em Niterói / Icaraí | title ("Restaurante árabe em Niterói: mezze, kibe e esfiha"), H1 da faixa de abertura, meta description, schema Restaurant |
| Conhecer a casa | culinária árabe em Icaraí | seção "Sobre o Suud" (texto do media kit) |
| Ver o cardápio | cardápio árabe | H2 "Cardápio árabe do Suud" e pratos em HTML (indexáveis) |
| Mezze | mezze em Niterói, o que é mezze | H2 "Mezze em Niterói: a mesa árabe para dividir" + FAQ |
| Delivery | delivery de comida árabe em Niterói / pedido pelo WhatsApp | seção Delivery ("Comida árabe em casa, com o pedido pronto em 1 minuto"), FAQ "Como funciona o pedido pelo Ahlan?" |
| Sem carne | falafel, opções vegetarianas e veganas | pilar "Muita opção sem carne", tags "vegetariano", FAQ |
| Pratos | kibe cru (nayee), hummus, babaganoush, esfiha | descrições do cardápio, FAQ e glossário do Ahlan |
| Eventos | espaço para eventos em Icaraí | cartão de eventos + FAQ |
| Visita | como chegar, endereço, horário | H2 "Como chegar ao Suud em Icaraí", mapa, schema |

## Regras de escrita aplicadas

1. Um prato concreto ligado a um momento ("um mezze no centro, kaftas no pau de canela e um Caipiarak"), em vez de adjetivos vagos.
2. Termos locais (Icaraí, Niterói) entram no texto de forma natural, sem repetir à exaustão: hoje são cerca de 6 menções de Niterói e 5 de Icaraí no texto visível.
3. Cada resposta do FAQ começa pela resposta direta. O schema FAQPage repete o texto visível palavra por palavra.
4. Nada inventado: preços vêm do cardápio público do delivery (marcados como "valores de referência"). Não entram avaliações, prêmios, data de fundação, área de entrega nem taxas.

## Pendências antes de publicar

- **Domínio:** trocar `https://www.SEUDOMINIO.com.br` em `index.html`, `robots.txt` e `sitemap.xml`.
- **CEP e coordenadas:** as fontes divergem (24230-052 no Google/Waze, 24230-191 no Rappi). Confirmar com o Suud e adicionar `postalCode` e `geo` ao schema.
- **Google Business Profile:** colocar a URL em `sameAs` e conferir se nome, endereço e telefone estão idênticos aos do site.
- **Preços:** os valores do site são do Rappi, que costuma ser mais caro que o salão. Confirmar com a casa e atualizar os `data-price` no HTML. O bot lê os preços direto do HTML, então basta editar em um lugar.
- **Kebab Bodrum, chá e café turco:** sem preço público. Hoje aparecem como "consulte".

## O diferencial do Ahlan (argumento de venda)

1. Sem esperar o cardápio chegar: pratos, descrições e preços estão no site.
2. Total na tela antes de enviar, com ajuste de quantidades.
3. Pedido que chega certo: itens, endereço, pagamento e observações numa mensagem só.
4. Pergunte antes de pedir: o bot explica pratos (nayee, labanie, babaganoush, mamul…), horário, endereço e opções sem carne.
5. Direto com o Suud, sem intermediário.

## Próximos passos de conteúdo (fase 2)

- Páginas dedicadas para **Delivery**, **Eventos** e **Mezze**, cada uma com URL própria no sitemap.
- Um guia curto "Comida árabe para iniciantes", com hummus, babaganoush, nayee, mamul e café turco, linkando para o cardápio.
- Agenda cultural com data, horário e condições, publicada só quando estiver confirmada. Eventos passados ficam marcados como histórico.
