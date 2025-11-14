# Relatório MiniCoin — Hugo

O arquivo-fonte do relatório continua sendo `report.md`. No momento do build copiamos esse conteúdo para o diretório `content/` que o Hugo espera e geramos o site estático em `public/`.

## Estrutura

```
docs/report/
├── report.md          # Markdown original editado manualmente
├── build.sh           # Script auxiliar para builds locais
├── hugo.toml          # Configuração principal do site
├── assets/css/        # Estilos customizados
├── layouts/           # Templates base/single/list
└── public/            # Saída (gerada automaticamente)
```

## Como gerar localmente

Requisitos: [Hugo Extended](https://gohugo.io/installation/) e Python (opcional para o restante do projeto).

```bash
cd docs/report
bash build.sh
python3 -m http.server --directory public
```

O GitHub Actions executa o mesmo script para publicar em GitHub Pages.
