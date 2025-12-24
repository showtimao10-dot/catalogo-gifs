# Catálogo de GIFs (somente visualização)

Este projeto cria uma página moderna para exibir GIFs animados do fornecedor (steamartworkdesigns.com/shop).
Ele NÃO faz upload de imagens: apenas lista links públicos de GIF (hotlink).

## Como publicar (mínimo de passos)
1) Crie um repositório no GitHub e envie TODO o conteúdo deste zip.
2) No GitHub: Settings → Pages → Deploy from a branch → main / (root) → Save.
3) Aguarde o link aparecer em Pages (vai ser algo como https://SEUUSUARIO.github.io/NOME-DO-REPO/)

## Atualização automática
- Vá em Actions e permita workflows (se o GitHub pedir).
- O bot roda 1x por dia e atualiza o arquivo `gifs.json` automaticamente.
- Você também pode rodar manualmente em Actions → "Update GIF list" → Run workflow.

Pronto: seu link fica sempre atualizado e seus clientes só visualizam.
