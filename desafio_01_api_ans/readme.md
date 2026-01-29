🔎 Visão Geral

Esta solução foi desenvolvida para realizar a coleta, consolidação e análise crítica das despesas das operadoras de planos de saúde, utilizando exclusivamente os dados públicos disponibilizados pela Agência Nacional de Saúde Suplementar (ANS).

O processo contempla:

Download automático do cadastro de operadoras da ANS

Download dos arquivos trimestrais de demonstrações contábeis

Extração e leitura de arquivos CSV

Consolidação dos dados dos últimos 3 trimestres disponíveis

Integração com o cadastro oficial de operadoras

Análise e tratamento de inconsistências

Geração de arquivo final compactado

🧩 Estrutura da Solução

Linguagem: Python

Bibliotecas utilizadas:

pandas — manipulação e consolidação dos dados

requests — download dos arquivos disponibilizados pela ANS

zipfile — extração e compactação dos arquivos

os / pathlib — gerenciamento de diretórios

📁 Estrutura de Pastas

desafio_01_api_ans/
│
├── src/
│   └── main.py
│
├── data/
│   ├── raw/        # Dados brutos (ZIP e CSV trimestrais + cadastro ANS)
│   └── processed/ # CSV consolidado
│
├── output/
│   └── consolidado_despesas.zip
│
└── README.md


⚙️ Pré-requisitos

Python 3.10 ou superior

Instalação das dependências:

pip install pandas requests


▶️ Instalação e Execução

Na raiz do projeto, execute:

python src/main.py


O script executa automaticamente as seguintes etapas:

Download do cadastro de operadoras da ANS

Download dos arquivos dos últimos 3 trimestres disponíveis

Extração dos arquivos ZIP

Leitura e padronização dos dados

Consolidação das despesas

Geração do CSV final

Compactação do arquivo consolidado em ZIP

📄 Arquivo Consolidado

O arquivo final consolidado contém exatamente as colunas solicitadas no desafio:

CNPJ

RazaoSocial

Trimestre

Ano

ValorDespesas

O arquivo gerado encontra-se no caminho:

output/consolidado_despesas.zip


🔍 Consolidação e Análise de Inconsistências

Durante o processo de consolidação, foram identificadas e tratadas as seguintes inconsistências:

1️⃣ CNPJs duplicados com razões sociais diferentes

Tratamento adotado:
Foi utilizada a razão social proveniente do cadastro oficial da ANS, vinculada pelo identificador da operadora (REG_ANS).

Justificativa:
O cadastro da ANS é a fonte oficial e mais confiável, refletindo alterações societárias, incorporações ou mudanças cadastrais ao longo do tempo.

2️⃣ Valores de despesas zerados ou negativos

Tratamento adotado:
Os registros com valores iguais a zero ou negativos foram mantidos no conjunto final de dados.

Justificativa:
Esses valores podem representar estornos, ajustes contábeis ou ausência de movimentação financeira no período. A exclusão desses registros poderia comprometer análises financeiras futuras ou auditorias.

3️⃣ Inconsistências no formato do trimestre

Tratamento adotado:
O trimestre foi inferido a partir da estrutura dos arquivos e padronizado no formato:

1T, 2T, 3T


Justificativa:
A padronização garante consistência temporal, facilita análises comparativas e mantém a rastreabilidade da origem dos dados.

📦 Saída Final

Arquivo gerado: consolidado_despesas.zip

Conteúdo: consolidado_despesas.csv

Localização: pasta output/

O arquivo final está pronto para uso em análises estatísticas, auditorias, visualizações ou integrações com outros sistemas.

📝 Observações Importantes

O script verifica automaticamente a existência de arquivos antes de realizar downloads, evitando duplicações

O cadastro de operadoras é baixado apenas uma vez e reutilizado nas execuções seguintes

Todo o processo é reprodutível, bastando executar o arquivo main.py