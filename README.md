# PriceMonitor

Monitor inteligente de preços e oportunidades para marketplaces, desenvolvido em Python.

O projeto coleta anúncios do Mercado Livre, normaliza os dados, registra o histórico de preços em SQLite, analisa possíveis oportunidades e envia alertas pelo Telegram quando uma oferta atinge a pontuação mínima configurada.

> Status atual: MVP funcional para o Mercado Livre. A integração com a Amazon está planejada para uma etapa futura.

## Objetivo

O PriceMonitor foi criado para identificar:

- promoções reais;
- quedas de preço sem desconto anunciado;
- possíveis erros de cadastro;
- descontos artificiais baseados em preços anteriores inflados;
- anúncios confiáveis com loja oficial, frete grátis e envio FULL.

A proposta é não confiar apenas no percentual de desconto exibido pelo marketplace. O sistema constrói um histórico próprio e compara o preço atual com valores realmente observados.

## Funcionalidades atuais

- Navegação automatizada com Google Chrome e Playwright;
- perfil persistente para manter sessão e cookies;
- pesquisa automática no Mercado Livre;
- coleta de até dezenas de anúncios por busca;
- extração de:
  - ID do anúncio;
  - título;
  - preço atual;
  - preço anterior anunciado;
  - desconto;
  - parcelamento;
  - vendedor;
  - loja oficial;
  - envio FULL;
  - frete;
  - link;
- normalização de preços e textos;
- filtros por:
  - termos obrigatórios;
  - termos excluídos;
  - preço mínimo e máximo;
  - loja oficial;
  - envio FULL;
- armazenamento em SQLite;
- histórico individual por anúncio;
- cálculo de:
  - média histórica;
  - menor preço observado;
  - maior preço observado;
  - último preço;
  - número de observações;
- sistema de pontuação de oportunidades;
- alertas via Telegram;
- testes isolados dos principais componentes.

## Arquitetura

```text
PriceMonitor/
├── analyzers/
│   ├── price_analyzer.py
│   └── product_filter.py
├── browser/
│   └── browser.py
├── config/
│   └── settings.py
├── database/
│   ├── database.py
│   └── repository.py
├── entities/
│   ├── opportunity.py
│   ├── product.py
│   └── search_rule.py
├── marketplaces/
│   └── mercadolivre/
│       └── collector.py
├── notifications/
│   └── telegram.py
├── services/
│   └── product_factory.py
├── utils/
│   ├── money.py
│   └── text.py
├── app.py
├── requirements.txt
└── .env
```

Também podem existir arquivos de teste na raiz, como:

```text
test_money.py
test_text.py
test_factory.py
test_opportunity.py
test_product_filter.py
test_price_analyzer.py
test_historical_analyzer.py
test_repository.py
test_telegram.py
```

## Fluxo do sistema

```text
Playwright / Chrome
        ↓
MercadoLivreCollector
        ↓
ProductFactory
        ↓
ProductFilter
        ↓
SQLite / ProductRepository
        ↓
PriceAnalyzer
        ↓
Opportunity
        ↓
TelegramNotifier
```

## Tecnologias

- Python;
- Playwright;
- Google Chrome;
- SQLite;
- Requests;
- python-dotenv;
- Telegram Bot API.

## Requisitos

- Python instalado;
- Google Chrome instalado;
- Git;
- conta no Telegram;
- bot criado com o BotFather.

## Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
cd PriceMonitor
```

Crie o ambiente virtual:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install
```

## Configuração do Chrome

O projeto utiliza um perfil exclusivo do Chrome para persistir cookies e sessão.

Caminhos usados atualmente:

```text
Executável:
C:\Program Files\Google\Chrome\Application\chrome.exe

Perfil:
C:\ChromePriceMonitor
```

O perfil pode ser criado manualmente com:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\ChromePriceMonitor"
```

Faça login no Mercado Livre nesse perfil e feche o navegador antes de executar o projeto.

> Não envie a pasta `C:\ChromePriceMonitor` para o GitHub. Ela pode conter cookies, sessões e informações privadas.

## Configuração do Telegram

Crie um arquivo `.env` na raiz:

```env
TELEGRAM_BOT_TOKEN=SEU_TOKEN
TELEGRAM_CHAT_ID=SEU_CHAT_ID
TELEGRAM_ENABLED=true
```

Nunca publique o `.env` nem o token do bot.

Teste a integração:

```powershell
python test_telegram.py
```

## Execução

```powershell
python app.py
```

O programa:

1. abre o Chrome;
2. pesquisa os produtos;
3. coleta e filtra os anúncios;
4. registra os preços no banco;
5. compara os preços com o histórico;
6. calcula a pontuação;
7. envia ao Telegram apenas as oportunidades aprovadas.

## Banco de dados

O banco é criado automaticamente em:

```text
database/price_monitor.db
```

Tabelas principais:

- `products`: informações atuais e estáveis do anúncio;
- `price_history`: observações de preço ao longo do tempo.

O banco local não deve ser versionado, pois cresce a cada execução e contém dados específicos do ambiente de monitoramento.

## Testes

Os testes atuais podem ser executados individualmente:

```powershell
python test_money.py
python test_text.py
python test_factory.py
python test_product_filter.py
python test_price_analyzer.py
python test_historical_analyzer.py
python test_repository.py
python test_telegram.py
```

## Situação atual do analisador

O sistema já diferencia:

- preço anterior anunciado pelo vendedor;
- histórico real coletado pelo próprio bot;
- média histórica;
- menor preço anterior;
- preço da última coleta.

A pontuação histórica só é aplicada depois de uma quantidade mínima de observações, reduzindo falsos positivos.

O preço riscado pelo marketplace possui peso menor, pois pode estar artificialmente inflado.

## Limitações atuais

- suporta apenas Mercado Livre;
- monitora uma busca configurada diretamente no código;
- ainda não valida cupons no carrinho;
- ainda não agrupa anúncios diferentes do mesmo modelo;
- ainda não possui execução agendada definitiva;
- seletores do marketplace podem mudar;
- CAPTCHA ou expiração de sessão podem exigir intervenção manual;
- o sistema não realiza compras automaticamente.

## Próximas etapas

- comparação entre anúncios equivalentes;
- identificação de marca, modelo, capacidade e categoria;
- preço efetivo com cupom;
- validação opcional de cupom no carrinho;
- prevenção de alertas duplicados;
- serviço central de monitoramento;
- execução agendada;
- integração com Amazon;
- painel web;
- testes automatizados com pytest;
- análise estatística avançada de anomalias.

## Segurança e uso responsável

- não publique tokens, cookies ou arquivos `.env`;
- não versione perfis do navegador;
- respeite os termos de uso dos marketplaces;
- use intervalos razoáveis entre coletas;
- mantenha intervenção humana para compras;
- trate alertas como indícios, não como garantia de estoque, preço ou entrega.

## Autor

Desenvolvido por Luiz Carlos F. Junior como projeto de automação, monitoramento de preços e análise de oportunidades.
