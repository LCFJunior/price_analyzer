# PriceAnalyzer

Monitor inteligente de preços, promoções e oportunidades para marketplaces, desenvolvido em Python.

O PriceMonitor coleta anúncios do Mercado Livre, normaliza e classifica os produtos, registra histórico próprio de preços, compara anúncios equivalentes e utiliza diferentes mecanismos de análise para identificar promoções reais e possíveis anomalias de preço.

O objetivo do projeto é ir além do percentual de desconto informado pelo marketplace, utilizando dados históricos e comparação entre produtos equivalentes para decidir se uma oferta realmente representa uma oportunidade.

> **Status atual:** sistema funcional de monitoramento e análise de preços para o Mercado Livre, com classificação técnica de produtos, histórico próprio, comparação hierárquica entre anúncios equivalentes, deduplicação comercial por vendedor e detecção inteligente de oportunidades.

---

# 🎯 Objetivo

Marketplaces frequentemente exibem descontos calculados a partir de preços anteriores que podem não representar o valor real de mercado.

O PriceMonitor busca construir sua própria referência de preço.

Para isso, o sistema considera diferentes fontes de informação:

- histórico real coletado pelo próprio monitor;
- preço atual do anúncio;
- preço anterior informado pelo marketplace;
- anúncios do mesmo modelo;
- produtos tecnicamente equivalentes;
- categoria e características do produto;
- vendedor;
- loja oficial;
- logística do marketplace;
- frete;
- origem nacional ou internacional;
- confiança na identificação do produto.

A partir dessas informações, o sistema calcula uma pontuação e decide se determinado anúncio representa uma oportunidade relevante.

---

# 🚀 Funcionalidades atuais

## Coleta de anúncios

- Navegação automatizada com Playwright;
- utilização do Google Chrome;
- perfil persistente para manter cookies e sessão;
- pesquisa automática no Mercado Livre;
- coleta de dezenas de anúncios por busca;
- suporte a múltiplos alvos de monitoramento.

Entre os dados coletados estão:

- ID do anúncio;
- título;
- preço atual;
- preço anterior;
- desconto;
- parcelamento;
- vendedor;
- loja oficial;
- envio pela logística do marketplace;
- frete;
- link;
- imagem;
- origem nacional ou internacional.

---

## 🔎 Filtro e validação inicial

Cada monitoramento possui regras próprias de relevância.

Atualmente podem ser utilizados:

- termos obrigatórios;
- termos excluídos;
- preço mínimo;
- preço máximo;
- exigência de loja oficial;
- exigência de logística FULL;
- ativação/desativação do monitoramento;
- ativação/desativação de notificações.

Isso evita que acessórios, kits ou produtos diferentes sejam analisados como se fossem o produto pesquisado.

---

# 🧠 Classificação inteligente de produtos

O projeto possui uma camada específica para identificar e normalizar produtos.

Atualmente existem classificadores dedicados para:

- GPUs;
- CPUs;
- SSDs;
- produtos genéricos/desconhecidos.

O coordenador `ProductClassifier` seleciona automaticamente o classificador adequado.

```text
Product
   ↓
ProductClassifier
   ↓
┌────────────────────┐
│ GPUClassifier      │
│ CPUClassifier      │
│ SSDClassifier      │
│ GenericClassifier  │
└────────────────────┘
   ↓
ProductProfile
```

A classificação não serve apenas para organizar os produtos.

Ela é utilizada diretamente pelo sistema de comparação de preços para determinar quais anúncios podem ser considerados equivalentes.

---

# 🪪 ProductProfile

Após a classificação, cada produto recebe um perfil normalizado.

O perfil pode conter:

- categoria;
- fabricante/marca;
- modelo;
- variante;
- capacidade;
- memória;
- interface;
- geração;
- características técnicas;
- nível de confiança da identidade;
- chaves de comparação.

Exemplo conceitual:

```text
Produto:
Samsung 9100 Pro 1TB NVMe Gen5

Categoria:
ssd

Marca:
SAMSUNG

Modelo:
9100 PRO

BROAD:
ssd_interno_nvme_1tb

TIER:
ssd_interno_nvme_gen5_1tb

STRICT:
samsung_9100_pro_1tb_nvme
```

---

# 🧩 Sistema BROAD / TIER / STRICT

Uma das principais partes do PriceMonitor é a comparação hierárquica entre produtos.

Existem três níveis principais.

## STRICT

Representa o mesmo modelo específico.

Exemplo:

```text
Samsung 9100 Pro 1TB
Samsung 9100 Pro 1TB
```

Chave:

```text
samsung_9100_pro_1tb_nvme
```

Essa comparação possui prioridade máxima.

Quando existem anúncios suficientes do mesmo produto, eles são utilizados como principal referência de mercado.

---

## TIER

Representa produtos tecnicamente semelhantes.

Exemplo:

```text
Samsung 9100 Pro 1TB Gen5
WD SN8100 1TB Gen5
Crucial T705 1TB Gen5
```

Podem pertencer ao mesmo grupo:

```text
ssd_interno_nvme_gen5_1tb
```

Isso impede, por exemplo, que um SSD NVMe Gen5 topo de linha seja comparado diretamente com SSDs NVMe Gen4 básicos apenas porque ambos possuem 1 TB.

O mesmo conceito é aplicado a CPUs e GPUs.

---

## BROAD

Representa um grupo mais amplo de produtos.

Exemplo:

```text
ssd_interno_nvme_1tb
```

É utilizado como último fallback quando não existem observações suficientes nos níveis mais específicos.

O uso de BROAD é propositalmente mais conservador, pois grupos amplos podem possuir diferenças significativas de desempenho e preço.

---

## Prioridade de comparação

```text
STRICT
   ↓
TIER
   ↓
BROAD
```

O sistema sempre tenta utilizar a referência mais específica disponível.

Caso não existam observações suficientes, ele pode avançar para o próximo nível de comparação.

---

# 💾 Classificação de SSDs

O classificador de SSDs identifica características como:

- marca;
- modelo;
- capacidade;
- SATA/NVMe/USB;
- geração PCIe;
- SSD interno ou externo;
- formato;
- confiança da identidade.

Exemplos já reconhecidos:

```text
Kingston NV3
WD Black SN850X
Samsung 990 PRO
Samsung 9100 PRO
Crucial P3 Plus
Kingston A400
Lexar NM790
ADATA Legend 800
SanDisk externos
```

O sistema também consegue normalizar determinados SKUs e títulos menos padronizados.

Exemplo:

```text
Disco Sólido Interno Ssd Plus Sa400s37480g Kingston
```

é reconhecido como:

```text
Kingston A400 480GB SATA
```

Produtos que são apenas acessórios, como:

```text
Case Externo USB para SSD NVMe
```

não são classificados como SSD.

---

## Hierarquia de SSDs

Exemplo:

```text
Produto:
Samsung 9100 Pro 1TB NVMe Gen5

BROAD:
ssd_interno_nvme_1tb

TIER:
ssd_interno_nvme_gen5_1tb

STRICT:
samsung_9100_pro_1tb_nvme
```

Isso permite comparar primeiro o mesmo modelo e, caso não existam referências suficientes, utilizar SSDs tecnicamente semelhantes.

---

# 🖥️ Classificação de CPUs

O sistema possui classificação dedicada para processadores AMD Ryzen e Intel Core.

## AMD

São identificados:

- família;
- série;
- modelo;
- variante;
- classe da variante;
- produto desktop/mobile quando aplicável.

Exemplos:

```text
Ryzen 7 5700X
Ryzen 7 5700X3D
Ryzen 5 5600
Ryzen 5 5600G
Ryzen 7 7800X3D
Ryzen 9 9950X
```

Exemplo de hierarquia:

```text
BROAD:
cpu_amd_ryzen_7

TIER:
cpu_amd_ryzen_7_5000_x

STRICT:
amd_ryzen_7_5700x
```

Variantes como:

```text
standard
X
X3D
APU
```

podem ser separadas no nível TIER.

Dessa forma, processadores de classes diferentes não precisam ser tratados automaticamente como equivalentes apenas por pertencerem à mesma família.

---

## Intel

São identificados processadores de diferentes gerações e variantes.

Exemplos:

```text
Core i5-10400
Core i7-11700
Core i5-12400F
Core i5-13600KF
Core i7-14700K
Core i9-14900KS
Core i9-9900K
```

Exemplo:

```text
BROAD:
cpu_intel_core_i7

TIER:
cpu_intel_core_i7_gen14_performance

STRICT:
intel_core_i7_14700k
```

Sufixos como:

```text
F
K
KF
KS
```

são preservados.

O classificador também evita interpretar acessórios como processadores.

Exemplos bloqueados:

```text
Caixa vazia Ryzen 7 5700X
Kit Upgrade Ryzen 7 5700X + B550
Cooler para Ryzen 7 5700X
Placa-mãe B550 para Ryzen 7 5700X
```

---

# 🎮 Classificação de GPUs

O sistema possui classificação dedicada para placas de vídeo NVIDIA e AMD.

O classificador identifica e normaliza informações como:

- fabricante da placa;
- fabricante da GPU;
- modelo da GPU;
- quantidade de VRAM;
- variante comercial;
- família;
- geração;
- características relevantes para comparação;
- nível de confiança da identidade;
- chaves BROAD / TIER / STRICT.

O objetivo é impedir que placas tecnicamente diferentes sejam utilizadas como referência umas das outras apenas por possuírem nomes semelhantes.

---

## Famílias NVIDIA

O classificador possui suporte para diferentes famílias GeForce, incluindo modelos das linhas:

```text
RTX
GTX
GT
```

Entre os modelos trabalhados durante o desenvolvimento estão placas de diferentes gerações, incluindo exemplos como:

```text
RTX 5060
RTX 5060 Ti
RTX 5070
RTX 5070 Ti
RTX 5080
RTX 5090

RTX 4070
RTX 4070 Super
RTX 4070 Ti
RTX 4070 Ti Super

GTX e GT de gerações anteriores
```

O classificador continua sendo expandido conforme novos títulos reais são encontrados no marketplace.

---

## Famílias AMD

Também existe suporte para diferentes placas Radeon RX.

Exemplos trabalhados durante o desenvolvimento incluem:

```text
RX 580
RX 7600
RX 7700 XT
RX 7800 XT
RX 7900 XT
RX 7900 XTX
RX 9070
RX 9070 XT
```

AMD e NVIDIA permanecem separadas nas referências técnicas.

---

## Fabricantes e variantes

O classificador consegue utilizar informações comerciais presentes no título.

Entre os fabricantes e variantes encontradas durante o desenvolvimento estão exemplos como:

```text
ASUS
MSI
Gigabyte
Zotac
Galax
PNY
Sapphire
PowerColor
XFX
ASRock
Soyo
Revenger
PCYes
```

E variantes como:

```text
Ventus
Shadow
Windforce
Gaming OC
TUF Gaming
ROG Strix
Aero
Eagle
Hellhound
Red Devil
Nitro+
Pulse
Merc
```

A presença de uma variante pode ser utilizada para construir uma identidade mais específica do anúncio.

---

## Hierarquia de GPUs

Exemplo conceitual:

```text
Produto:
MSI RTX 5060 Ventus 2X 8GB

TIER:
gpu_nvidia_rtx_5060_8gb

STRICT:
msi_rtx_5060_ventus_2x_8gb
```

O nível STRICT representa uma identidade comercial mais específica.

O nível TIER permite comparar diferentes implementações da mesma GPU quando não existem observações suficientes do modelo exato.

Por exemplo:

```text
MSI RTX 5060 Ventus 2X 8GB
MSI RTX 5060 Shadow 2X 8GB
outra RTX 5060 8GB equivalente
```

podem compartilhar um grupo técnico TIER quando apropriado.

Ao mesmo tempo:

```text
RTX 5060
≠
RTX 5060 Ti
≠
RTX 5070
```

permanecem isoladas.

Isso reduz significativamente o risco de gerar uma falsa oportunidade comparando placas de níveis diferentes.

---

## Títulos reais e normalização

Títulos de marketplace podem ser incompletos, inconsistentes ou escritos de maneiras diferentes.

Por isso, o classificador tenta normalizar variações antes de criar a identidade do produto.

Ao mesmo tempo, o sistema mantém uma estratégia conservadora:

> se não houver informações suficientes para determinar a identidade com confiança, é preferível não criar uma identidade específica falsa.

Esse comportamento é importante principalmente para placas antigas, anúncios genéricos e produtos com títulos pouco informativos.

---

# 📊 Histórico próprio de preços

Cada coleta válida gera uma nova observação no banco SQLite.

O sistema mantém histórico individual por anúncio.

As estatísticas disponíveis incluem:

- número de observações;
- menor preço;
- maior preço;
- média;
- mediana;
- desvio padrão;
- preço anterior/mais recente.

Exemplo:

```text
Observações: 4
Menor preço: R$ 2.450
Maior preço: R$ 2.550
Média: R$ 2.500
Mediana: R$ 2.500
```

A análise de baseline é realizada antes de salvar a coleta atual, impedindo que o preço que está sendo analisado seja utilizado como referência de si próprio.

---

# 👥 Comparação entre anúncios equivalentes

O `PeerPriceAnalyzer` cria uma referência de mercado utilizando outros anúncios equivalentes.

A busca segue a prioridade:

```text
mesmo modelo
    ↓
mesmo tier
    ↓
grupo geral
```

Os grupos também podem separar:

```text
nacional
internacional
```

Isso reduz comparações inadequadas entre produtos com condições comerciais diferentes.

---

## Exemplo de fallback

Imagine um produto sem anúncios suficientes do mesmo modelo.

```text
STRICT:
1 observação
```

Caso o mínimo necessário não seja atingido, o sistema pode procurar:

```text
TIER:
5 observações
```

Se o TIER possuir quantidade suficiente de referências válidas, ele passa a ser utilizado.

Somente quando os níveis mais específicos não possuem referências suficientes o sistema considera um grupo BROAD.

---

# 🏪 Deduplicação por vendedor

Um marketplace pode possuir diversos anúncios do mesmo produto publicados pela mesma loja.

Sem tratamento, uma loja com muitos anúncios poderia dominar artificialmente a média e a mediana.

O PriceMonitor reduz esse problema consolidando anúncios equivalentes do mesmo vendedor antes de gerar as estatísticas comerciais.

Exemplo:

```text
Loja A
├── anúncio 1
├── anúncio 2
├── anúncio 3
├── anúncio 4
└── anúncio 5
```

não necessariamente recebe cinco vezes o peso de:

```text
Loja B
└── anúncio 1
```

Isso produz uma referência de mercado mais equilibrada.

A deduplicação é especialmente importante quando o sistema utiliza TIER ou BROAD, pois esses grupos podem conter uma quantidade maior de anúncios.

---

# 📈 Análise de oportunidades

O sistema possui mecanismos diferentes para analisar possíveis oportunidades.

Entre os sinais utilizados estão:

- diferença em relação ao histórico do próprio anúncio;
- diferença em relação ao mesmo modelo;
- diferença em relação ao mesmo tier;
- diferença em relação ao grupo geral;
- desconto anunciado;
- loja oficial;
- logística do marketplace;
- frete grátis;
- confiança na identidade do produto.

Esses sinais podem ser combinados para produzir uma pontuação.

---

# 🔥 PromotionEngine

O `PromotionEngine` procura promoções reais utilizando múltiplos sinais.

Exemplo de uma análise:

```text
Produto:
Samsung 9100 Pro 1TB

Preço atual:
R$ 1.850

Mediana histórica:
R$ 2.500

Mediana de anúncios equivalentes:
R$ 2.500
```

O sistema pode identificar:

```text
Preço abaixo do histórico: 26%
Preço abaixo do mesmo modelo: 26%
Desconto anunciado: 28,8%
Loja oficial
FULL
Frete grátis
```

e gerar uma pontuação.

Exemplo:

```text
Score: 80/100
Tipo: promocao
Confiança: alta
Notificar: True
```

---

# ⚠️ BugEngine

O projeto também possui uma análise específica para possíveis anomalias ou erros de preço.

O objetivo é diferenciar:

```text
promoção legítima
```

de situações extremamente fora do padrão que podem representar:

```text
erro de cadastro
erro de preço
produto diferente
identidade incorreta
anúncio suspeito
```

Quando diferentes mecanismos encontram sinais no mesmo produto, o sistema utiliza regras para decidir qual interpretação possui maior prioridade.

---

# 🛡️ Confiança da identidade

A classificação do produto possui níveis de confiança.

Exemplos:

```text
alta
media
baixa
muito_baixa
```

Produtos cuja identidade não pôde ser determinada de maneira confiável recebem tratamento mais conservador na análise.

Isso evita transformar automaticamente um produto genérico extremamente barato em uma "promoção imperdível".

A confiança da identidade é especialmente importante quando os dados vêm diretamente de títulos escritos pelos vendedores.

---

# 🔬 Validação profunda

O sistema possui uma etapa adicional antes de determinados alertas.

Quando uma oportunidade importante é detectada, uma validação mais profunda pode verificar novamente o anúncio antes da notificação.

Possíveis resultados incluem:

```text
valid
blocked
inconclusive
```

Somente oportunidades aprovadas pelo fluxo configurado seguem para notificação.

---

# 🔔 Controle de alertas duplicados

O PriceMonitor registra notificações já realizadas.

Isso permite impedir que o usuário receba repetidamente o mesmo alerta sem uma mudança relevante.

As decisões de notificação podem considerar:

- primeiro alerta;
- alertas anteriores;
- preço anteriormente notificado;
- nova queda relevante;
- estado atual do anúncio.

---

# 📱 Telegram

O projeto possui integração com Telegram para envio das oportunidades aprovadas.

Uma notificação pode incluir:

```text
Produto
Preço
Score
Tipo da oportunidade
Confiança
Motivos da decisão
Link do anúncio
```

O envio ocorre apenas quando o produto passa pelas regras configuradas.

Durante os testes, notificadores simulados também podem ser utilizados para validar o fluxo sem enviar mensagens reais.

---

# 🔄 Fluxo geral

```text
MonitoringTarget
       ↓
MercadoLivreCollector
       ↓
ProductFactory
       ↓
Filtro / Validação inicial
       ↓
ProductClassifier
       ↓
ProductProfile
       ↓
┌──────────────────────────┐
│ Histórico próprio        │
│ PeerPriceAnalyzer        │
└──────────────────────────┘
       ↓
PromotionEngine / BugEngine
       ↓
Seleção da oportunidade
       ↓
Validação profunda
       ↓
Controle de duplicidade
       ↓
TelegramNotifier
       ↓
Registro da notificação
```

---

# 🗃️ Banco de dados

O projeto utiliza SQLite.

O banco armazena informações como:

- produtos conhecidos;
- histórico de preços;
- observações;
- notificações enviadas.

Entre as principais estruturas estão:

```text
products
price_history
notifications
```

O banco é criado e atualizado localmente pelo projeto.

Arquivos `.db` não devem ser enviados ao GitHub.

---

# 🛠️ Tecnologias

Principais tecnologias utilizadas:

- Python;
- Playwright;
- Google Chrome;
- SQLite;
- Requests;
- python-dotenv;
- Telegram Bot API;
- Git;
- GitHub.

---

# 📁 Estrutura do projeto

A estrutura pode evoluir conforme novos módulos forem adicionados, mas atualmente segue aproximadamente esta organização:

```text
PriceMonitor/
│
├── analyzers/
│   ├── peer_price_analyzer.py
│   └── ...
│
├── browser/
│   └── browser.py
│
├── config/
│   ├── settings.py
│   └── monitoring_targets.py
│
├── database/
│   ├── database.py
│   └── repository.py
│
├── entities/
│   ├── product.py
│   ├── product_profile.py
│   ├── opportunity.py
│   ├── monitoring_target.py
│   └── search_rule.py
│
├── marketplaces/
│   └── mercadolivre/
│       └── collector.py
│
├── notifications/
│   └── telegram.py
│
├── services/
│   ├── classifiers/
│   │   ├── base.py
│   │   ├── text_utils.py
│   │   ├── gpu_classifier.py
│   │   ├── cpu_classifier.py
│   │   ├── ssd_classifier.py
│   │   └── generic_classifier.py
│   │
│   ├── product_classifier.py
│   ├── product_factory.py
│   ├── monitor_service.py
│   ├── batch_monitor_service.py
│   └── ...
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🧪 Testes

O projeto possui testes independentes para validar partes críticas da arquitetura.

Entre eles estão testes relacionados a:

```text
classificação de SSD
classificação de CPU
classificação de GPU

histórico de preços
baseline histórico

comparação entre equivalentes

STRICT / TIER / BROAD de SSD
STRICT / TIER / BROAD de CPU
STRICT / TIER / BROAD de GPU

deduplicação por vendedor

PromotionEngine
BugEngine

fluxo completo de promoção
controle de notificações
```

Exemplos:

```powershell
python test_ssd_classifier.py
python test_cpu_classifier.py
python test_gpu_classifier.py

python test_peer_tier.py
python test_cpu_peer_tier.py
python test_gpu_peer_tier.py
python test_peer_seller_dedup.py

python test_repository_baseline.py

python test_promotion_engine.py
python test_promotion_flow.py
```

Os testes utilizam verificações automáticas com `assert` para impedir regressões durante a evolução do sistema.

Os testes de equivalência são particularmente importantes porque garantem, por exemplo, que:

```text
RTX 5060 != RTX 5060 Ti
AMD != NVIDIA
Gen4 != Gen5 quando o tier exige geração
5700X != 5700X3D
```

e que diferentes variantes comerciais possam compartilhar TIER sem necessariamente compartilhar STRICT.

---

# ⚙️ Requisitos

Para executar o projeto:

- Python;
- Google Chrome;
- Git;
- Playwright;
- conta no Telegram para notificações;
- bot do Telegram configurado.

---

# 📥 Instalação

Clone o repositório:

```bash
git clone https://github.com/LCFJunior/price_analyzer.git
cd price_analyzer
```

Crie o ambiente virtual.

## Windows PowerShell

```powershell
python -m venv .venv
```

Ative:

```powershell
.\.venv\Scripts\Activate.ps1
```

Atualize o pip:

```powershell
python -m pip install --upgrade pip
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Instale os navegadores necessários ao Playwright:

```powershell
python -m playwright install
```

---

# 🌐 Configuração do Chrome

O projeto pode utilizar um perfil exclusivo do Chrome para persistir:

- cookies;
- login;
- sessão do marketplace.

Exemplo de configuração local:

```text
Executável:
C:\Program Files\Google\Chrome\Application\chrome.exe

Perfil:
C:\ChromePriceMonitor
```

O perfil pode ser criado manualmente:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\ChromePriceMonitor"
```

Faça login no Mercado Livre utilizando esse perfil.

Depois feche o Chrome antes de executar o monitor.

> O perfil do navegador não deve ser enviado ao GitHub, pois pode conter cookies, sessões e outras informações privadas.

---

# 🔐 Variáveis de ambiente

Crie um arquivo:

```text
.env
```

na raiz do projeto.

Exemplo:

```env
TELEGRAM_BOT_TOKEN=SEU_TOKEN
TELEGRAM_CHAT_ID=SEU_CHAT_ID
TELEGRAM_ENABLED=true
```

Nunca publique tokens reais.

O arquivo `.env` deve permanecer ignorado pelo Git.

---

# ▶️ Execução

Com o ambiente virtual ativado:

```powershell
python app.py
```

O sistema executará aproximadamente o seguinte fluxo:

1. carrega os alvos de monitoramento;
2. abre o navegador;
3. pesquisa os produtos;
4. coleta os anúncios;
5. normaliza os dados;
6. aplica filtros de relevância;
7. classifica os produtos;
8. recupera o histórico anterior;
9. cria referências entre anúncios equivalentes;
10. analisa promoções e anomalias;
11. executa validações adicionais quando necessário;
12. decide se deve notificar;
13. envia oportunidades aprovadas;
14. registra preços e notificações no banco.

---

# 🎯 Alvos de monitoramento

O sistema suporta múltiplos produtos monitorados.

Exemplos utilizados durante o desenvolvimento:

```text
NVIDIA RTX 5070 12GB
AMD Ryzen 7 5700X
SSD NVMe 1TB
```

Cada alvo pode possuir:

```text
search_query
required_terms
excluded_terms
minimum_price
maximum_price
require_official_store
require_full
enabled
notifications_enabled
```

Isso permite desenvolver e testar novas categorias sem necessariamente habilitar alertas imediatamente.

---

# 📊 Exemplo de resultado

Uma oportunidade pode gerar uma análise semelhante a:

```text
Produto:
SSD Samsung 9100 Pro 1TB NVMe Gen5 X4

Preço:
R$ 1.850,00

Classificação geral:
ssd_interno_nvme_1tb

Tier:
ssd_interno_nvme_gen5_1tb

Classificação específica:
samsung_9100_pro_1tb_nvme

Marca:
SAMSUNG

Modelo:
9100 PRO

Confiança da identidade:
alta

Score:
80/100

Tipo:
promocao

Confiança:
alta

Notificar:
Sim

Mediana histórica:
R$ 2.500,00

Escopo dos equivalentes:
modelo_exato_nacional

Mediana dos equivalentes:
R$ 2.500,00
```

Motivos:

```text
- Preço bem abaixo do histórico do próprio anúncio
- Preço muito abaixo de anúncios do mesmo modelo
- Desconto anunciado relevante
- Produto vendido por loja oficial
- Produto enviado pela logística do marketplace
- Frete grátis
```

---

# 🛣️ Roadmap

O projeto continua em desenvolvimento.

Algumas evoluções planejadas são:

- ampliar a quantidade de categorias suportadas;
- melhorar continuamente os classificadores;
- ampliar a cobertura de GPUs NVIDIA e AMD;
- adicionar mais modelos conhecidos;
- melhorar o reconhecimento de títulos reais e pouco padronizados;
- melhorar detecção de produtos genéricos;
- expandir os níveis de equivalência comercial;
- análise estatística mais avançada;
- aumentar cobertura de testes;
- migração progressiva para `pytest`;
- execução agendada;
- monitoramento contínuo;
- integração com Amazon;
- suporte a outros marketplaces;
- análise de preço efetivo com cupom;
- validação opcional de cupons;
- painel web;
- API para consulta dos dados;
- métricas e observabilidade;
- configuração dinâmica dos produtos monitorados.

---

# ⚠️ Limitações atuais

O projeto ainda possui algumas limitações:

- foco atual no Mercado Livre;
- classificadores precisam evoluir conforme novos produtos aparecem;
- alguns títulos reais ainda podem não possuir informações suficientes para classificação segura;
- títulos de anúncios podem conter informações incorretas;
- produtos antigos e pouco padronizados podem exigir novas regras de identificação;
- mudanças no HTML do marketplace podem exigir atualização dos seletores;
- CAPTCHA pode exigir intervenção manual;
- sessão do marketplace pode expirar;
- quantidade pequena de anúncios equivalentes reduz a confiança estatística;
- produtos novos podem não possuir histórico suficiente;
- cupons ainda não fazem parte integral do cálculo do preço efetivo;
- o sistema não realiza compras automaticamente.

O sistema prioriza evitar falsos positivos.

Por isso, quando um anúncio não possui informações suficientes para uma classificação confiável, ele pode permanecer sem uma identidade técnica específica em vez de ser agrupado incorretamente.

---

# 📚 Objetivo educacional

Além de sua aplicação prática, o PriceMonitor também funciona como projeto de estudo e portfólio envolvendo:

- automação web;
- scraping;
- modelagem de dados;
- arquitetura de software;
- orientação a objetos;
- classificação de produtos;
- processamento e normalização de texto;
- análise estatística;
- SQLite;
- sistemas de pontuação;
- detecção de anomalias;
- integração com APIs;
- testes;
- Git e GitHub.

O desenvolvimento busca evoluir progressivamente de um simples coletor de preços para um sistema capaz de construir suas próprias referências de mercado.

---

# 📌 Estado do desenvolvimento

Atualmente o projeto já possui um fluxo funcional envolvendo:

```text
Coleta
   ↓
Filtro
   ↓
Classificação
   ↓
Histórico
   ↓
Comparação com equivalentes
   ↓
Detecção de oportunidades
   ↓
Validação
   ↓
Controle de duplicidade
   ↓
Notificação
```

A arquitetura atual já permite trabalhar separadamente com:

```text
SSD
CPU
GPU
```

utilizando classificadores específicos e referências hierárquicas.

O sistema também já possui testes específicos para verificar o isolamento correto entre grupos de produtos e impedir que referências inadequadas sejam utilizadas na análise.

A prioridade atual do desenvolvimento é:

1. aumentar a cobertura dos classificadores;
2. melhorar o reconhecimento de títulos reais do marketplace;
3. aumentar a qualidade das referências de mercado;
4. reduzir falsos positivos;
5. fortalecer os testes;
6. somente depois expandir o monitoramento para novos marketplaces.

---

# 🔒 Segurança e uso responsável

- não publique tokens;
- não publique arquivos `.env`;
- não versione perfis do navegador;
- não publique cookies ou sessões;
- mantenha credenciais fora do código;
- respeite os termos de uso dos marketplaces;
- utilize intervalos razoáveis entre coletas;
- trate alertas como indícios, não como garantia de estoque, preço ou entrega;
- mantenha intervenção humana para decisões de compra.

---

# 👨‍💻 Autor

Desenvolvido por **Luiz Carlos F. Junior**.

Projeto pessoal voltado ao estudo e aplicação prática de:

**Python, automação, análise de dados, monitoramento de preços e engenharia de software.**
