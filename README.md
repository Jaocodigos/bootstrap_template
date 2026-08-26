# Modelo de Arquitetura para Automações Python

Este documento define um modelo simples e padronizado para o desenvolvimento e a execução de automações em Python.

O modelo foi pensado para permitir a participação de pessoas com diferentes níveis de experiência técnica, mantendo responsabilidades claras, configurações personalizáveis e um fluxo de execução previsível.

Os principais elementos são:

- um bootstrap técnico compartilhado;
- uma estrutura de projeto organizada por etapas;
- dependências isoladas por automação;
- configurações próprias por meio de variáveis de ambiente;
- entrada e saída estruturadas para integração com o Automation Anywhere.

---

## Estrutura do repositório

~~~text
repositorio/
│
├── bootstrap.py
├── .gitignore
├── README.md
│
└── automacoes/
    │
    └── automacao_pedidos/
        ├── main.py
        ├── config.py
        ├── requirements.txt
        ├── .env
        ├── .env.example
        │
        ├── etapas/
        │   ├── etapa_01_extrair_dados.py
        │   ├── etapa_02_validar_dados.py
        │   ├── etapa_03_atualizar_sistema.py
        │   ├── etapa_04_gerar_relatorio.py
        │   └── etapa_05_enviar_email.py
        │
        ├── funcoes/
        │   ├── excel.py
        │   ├── banco.py
        │   ├── navegador.py
        │   └── email.py
        │
        ├── arquivos/
        ├── logs/
        └── README.md
~~~

A pasta automacoes pode conter uma ou mais automações. Cada automação mantém suas próprias etapas, configurações, dependências e arquivos auxiliares.

O arquivo .env existe apenas no ambiente de execução e não deve ser versionado.

---

## Visão geral da execução

~~~text
Automation Anywhere
        ↓
bootstrap.py
        ↓
Atualização e preparação do ambiente
        ↓
automacao/main.py
        ↓
Etapas da automação
        ↓
Resposta estruturada
        ↓
Automation Anywhere
~~~

O Automation Anywhere inicia o bootstrap e envia um único parâmetro em formato JSON.

O bootstrap prepara o ambiente, inicia a automação em um novo processo, aguarda sua conclusão e devolve ao Automation Anywhere a resposta e o código de saída recebidos.

---

## Responsabilidade do bootstrap

O bootstrap é o inicializador técnico das automações.

Suas responsabilidades são:

1. receber o parâmetro enviado pelo Automation Anywhere;
2. atualizar o repositório;
3. reiniciar utilizando sua versão atualizada;
4. interpretar o envelope JSON;
5. identificar a automação solicitada;
6. preparar o ambiente virtual da automação;
7. sincronizar as dependências declaradas;
8. iniciar a automação em um novo processo;
9. aguardar sua conclusão;
10. repassar a saída e o código de retorno ao Automation Anywhere.

O bootstrap não deve:

- conter regras de negócio;
- executar etapas do processo;
- validar os parâmetros funcionais da automação;
- decidir se itens devem ser reprocessados;
- interpretar ou modificar o resultado de negócio;
- montar comandos de shell diretamente a partir de valores recebidos.

Ele apenas prepara, inicia, aguarda e transporta o resultado.

---

## Autoatualização do bootstrap

O bootstrap está localizado no mesmo repositório que será atualizado. Por isso, a atualização deve ocorrer em duas fases.

~~~text
Bootstrap carregado inicialmente
        ↓
Atualiza o repositório
        ↓
Inicia novamente o bootstrap
        ↓
Bootstrap atualizado identifica o reinício
        ↓
Continua a preparação
~~~

O primeiro processo permanece aguardando o processo atualizado. Dessa forma, toda a cadeia continua vinculada à mesma execução iniciada pelo Automation Anywhere.

Um marcador interno deve indicar que o bootstrap já foi reiniciado. Isso impede que a nova versão atualize o repositório e se reinicie indefinidamente.

Regras:

- a atualização deve utilizar uma operação segura, como git pull --ff-only;
- alterações locais não devem ser descartadas automaticamente;
- uma falha na atualização deve impedir o início da automação;
- o commit anterior e o novo commit devem ser registrados nos logs;
- o marcador de reinício deve permanecer estável entre versões;
- o bootstrap deve utilizar apenas recursos da biblioteca padrão do Python;
- caminhos devem ser resolvidos a partir da localização do bootstrap, e não do diretório atual do terminal.

Ao ser reiniciado, o bootstrap atualizado passa a ser utilizado ainda na execução atual.

---

## Parâmetro recebido do Automation Anywhere

Como o Automation Anywhere envia apenas um parâmetro, as informações devem ser agrupadas em um único JSON.

Exemplo:

~~~json
{
  "versao": 1,
  "automacao": "automacao_pedidos",
  "execucao_id": "AA-20260818-0001",
  "parametros": {
    "ambiente": "producao",
    "data_referencia": "2026-08-18",
    "reprocessar": false
  }
}
~~~

### Campos do envelope

| Campo | Finalidade |
|---|---|
| versao | Identifica a versão do contrato de entrada |
| automacao | Identifica qual automação deve ser executada |
| execucao_id | Relaciona os registros do Automation Anywhere, bootstrap e automação |
| parametros | Contém os dados específicos da automação |

O JSON inteiro deve ser enviado como um único argumento.

O campo automacao nunca deve ser utilizado diretamente como caminho de arquivo. O bootstrap deve comparar o valor recebido com uma lista de automações permitidas e resolver internamente o diretório correspondente.

---

## Divisão da validação

A validação é dividida entre o bootstrap e a automação.

### Validação do bootstrap

O bootstrap verifica apenas o contrato técnico necessário para iniciar a execução:

- existência do argumento;
- JSON sintaticamente válido;
- formato de objeto;
- versão de contrato suportada;
- identificador de automação permitido;
- diretório, arquivo principal e requirements da automação existentes.

### Validação da automação

A automação é responsável por validar:

- campos obrigatórios dentro de parametros;
- tipos dos valores;
- formatos de datas, códigos e identificadores;
- combinações permitidas;
- regras de negócio;
- valores disponíveis no ambiente.

Um JSON pode ser tecnicamente válido e ainda ser funcionalmente inválido. Essa segunda validação pertence à automação.

---

## Dependências por automação

Cada automação deve possuir seu próprio requirements.txt.

~~~text
automacoes/
└── automacao_pedidos/
    └── requirements.txt
~~~

O bootstrap deve criar ou reutilizar um ambiente virtual exclusivo para a automação e sincronizar nele as dependências declaradas.

Atualizar dependências significa deixar o ambiente de execução compatível com as versões declaradas pelo projeto. Não significa instalar indiscriminadamente as versões mais recentes disponíveis.

Regras:

- preferir versões explicitamente definidas;
- não instalar dependências no Python global da máquina;
- não compartilhar o mesmo ambiente virtual entre automações com requisitos diferentes;
- não versionar a pasta do ambiente virtual;
- iniciar a automação utilizando o interpretador Python do ambiente virtual preparado;
- interromper a execução quando a sincronização das dependências falhar.

Como o bootstrap prepara as dependências, ele próprio deve depender apenas da biblioteca padrão do Python.

---

## Variáveis de ambiente

Cada automação deve disponibilizar seu próprio sistema de variáveis de ambiente.

~~~text
automacao_pedidos/
├── config.py
├── .env
└── .env.example
~~~

### .env

Contém os valores específicos da instalação atual.

Exemplos:

~~~env
AMBIENTE=producao
CAMINHO_ENTRADA=C:\Automacao\Entrada
CAMINHO_SAIDA=C:\Automacao\Saida
TIMEOUT=30
TENTATIVAS=3
~~~

O arquivo .env:

- não deve entrar no Git;
- pode conter valores diferentes em cada máquina;
- não deve ser incluído nos logs;
- deve ser carregado pela própria automação.

### .env.example

Documenta todas as variáveis reconhecidas pela automação.

~~~env
AMBIENTE=
CAMINHO_ENTRADA=
CAMINHO_SAIDA=
TIMEOUT=30
TENTATIVAS=3
~~~

O arquivo .env.example:

- deve entrar no Git;
- não deve conter senhas, tokens ou credenciais reais;
- deve acompanhar qualquer alteração nas configurações disponíveis;
- deve informar valores padrão apenas quando forem seguros e válidos.

### Precedência

Quando uma variável existir tanto no sistema operacional quanto no arquivo .env, o valor do sistema operacional deve prevalecer.

O config.py é responsável por carregar as variáveis, convertê-las para os tipos necessários e validar as configurações obrigatórias.

Os caminhos do .env e dos demais arquivos devem ser calculados a partir do diretório da própria automação, evitando dependência do diretório em que o Automation Anywhere iniciou o processo.

---

## main.py

O main.py representa o fluxo principal da automação.

Ele deve permitir que uma pessoa entenda o processo lendo o arquivo de cima para baixo.

Exemplo:

~~~python
from etapas.etapa_01_extrair_dados import executar as extrair
from etapas.etapa_02_validar_dados import executar as validar
from etapas.etapa_03_atualizar_sistema import executar as atualizar
from etapas.etapa_04_gerar_relatorio import executar as gerar_relatorio
from etapas.etapa_05_enviar_email import executar as enviar_email


def main(parametros):
    dados = extrair(parametros)
    dados = validar(dados)
    atualizar(dados)
    gerar_relatorio(dados)
    enviar_email()
~~~

O main.py deve mostrar o que a automação faz, e não todos os detalhes de como cada atividade é executada.

O prefixo etapa_01, etapa_02 e assim por diante mantém os arquivos visualmente ordenados e, ao mesmo tempo, produz nomes de módulos válidos em Python.

---

## Pasta etapas

A pasta etapas contém as atividades principais do processo.

~~~text
etapas/
├── etapa_01_extrair_dados.py
├── etapa_02_validar_dados.py
├── etapa_03_atualizar_sistema.py
├── etapa_04_gerar_relatorio.py
└── etapa_05_enviar_email.py
~~~

Cada etapa deve:

- representar uma atividade clara;
- possuir, sempre que possível, uma função principal chamada executar;
- receber apenas as informações necessárias;
- devolver um resultado compreensível;
- gerar mensagens de erro que identifiquem a atividade e o item afetado.

A ordem real de execução continua sendo definida pelo main.py.

---

## Pasta funcoes

A pasta funcoes contém operações reutilizáveis.

~~~text
funcoes/
├── excel.py
├── banco.py
├── navegador.py
└── email.py
~~~

Exemplos:

~~~python
def ler_planilha(caminho):
    ...


def salvar_planilha(caminho, dados):
    ...
~~~

Se o mesmo trecho estiver sendo copiado em diferentes etapas, ele deve ser considerado para transformação em uma função reutilizável.

---

## Resposta para o Automation Anywhere

A automação deve produzir uma resposta estruturada em JSON.

Exemplo:

~~~json
{
  "status": "sucesso",
  "execucao_id": "AA-20260818-0001",
  "resultado": {
    "itens_processados": 120,
    "itens_com_erro": 3
  }
}
~~~

O contrato de saída é:

| Canal | Conteúdo |
|---|---|
| stdout | Resposta final estruturada em JSON |
| stderr | Mensagens de erro técnico |
| Código 0 | Execução concluída |
| Código diferente de 0 | Falha na execução |
| Arquivos de log | Detalhes do processamento e suporte |

O bootstrap deve iniciar a automação de forma síncrona, aguardar o término e repassar stdout, stderr e o código de saída sem interpretar o resultado de negócio.

Para preservar o JSON de resposta, mensagens de acompanhamento não devem ser escritas em stdout.

Na implementação atual, a função `executar()` devolve ao Automation Anywhere um envelope técnico. O JSON produzido pela automação é validado e inserido como objeto no campo `resposta`:

~~~json
{
  "status": "sucesso",
  "bot": "R00X",
  "ambiente": "DEV",
  "mensagem": "Bootstrap concluido com sucesso.",
  "resposta": {
    "status": "sucesso",
    "automacao": "R00X",
    "parametros_recebidos": {
      "identificador_teste": "AA-R00X-001"
    }
  }
}
~~~

Assim, o Automation Anywhere precisa interpretar apenas o JSON retornado pelo bootstrap; não existe um segundo JSON serializado dentro do campo `resposta`.

---

## Logs

Os logs do bootstrap e da automação devem permitir relacionar toda a execução por meio do execucao_id.

Devem registrar, quando aplicável:

- início e fim da execução;
- automação solicitada;
- commit anterior e commit atualizado;
- preparação do ambiente virtual;
- sincronização das dependências;
- início e fim de cada etapa;
- itens processados;
- erros técnicos e funcionais;
- código final de saída.

Não devem registrar:

- senhas;
- tokens;
- credenciais;
- conteúdo completo do .env;
- JSON completo de entrada quando puder conter informações sensíveis.

Mensagens de erro devem informar a etapa e o item afetado sempre que possível.

---

## Segurança

O modelo deve seguir estas regras mínimas:

- automações permitidas são definidas internamente;
- parâmetros não podem selecionar caminhos arbitrários;
- comandos devem ser executados com argumentos separados, sem composição livre de comandos de shell;
- credenciais não ficam no código;
- arquivos .env não são versionados;
- dados sensíveis não são registrados;
- atualizações não descartam alterações locais automaticamente;
- falhas na preparação interrompem a execução;
- o retorno do processo filho é propagado ao Automation Anywhere.

---

## Concorrência

A primeira versão do modelo considera que não haverá duas execuções preparando simultaneamente o mesmo repositório ou ambiente virtual.

Essa limitação deve ser documentada.

Caso execuções concorrentes passem a ser necessárias, será preciso revisar o modelo e implementar uma das seguintes estratégias:

- bloqueio durante atualização e preparação;
- ambientes de execução isolados;
- cópias de trabalho separadas;
- preparação antecipada das dependências.

A concorrência fica registrada como evolução futura e não faz parte do escopo inicial.

---

## Regras principais

| Regra | Motivo |
|---|---|
| O bootstrap cuida apenas da preparação e inicialização técnica | Evita mistura com regras de negócio |
| O fluxo principal fica no main.py | Facilita entender a automação |
| Cada automação possui seu próprio requirements.txt | Isola dependências |
| Cada automação possui seu próprio .env.example | Documenta configurações |
| O .env real não entra no Git | Protege informações do ambiente |
| A automação valida seus parâmetros funcionais | Mantém a responsabilidade no lugar correto |
| O bootstrap valida apenas o contrato técnico | Evita acoplamento com cada processo |
| O stdout contém somente a resposta final | Facilita a integração com o Automation Anywhere |
| Logs utilizam o execucao_id | Permite rastrear toda a execução |
| Falhas de preparação impedem a automação | Evita executar em um ambiente inconsistente |
| Nomes devem explicar o que fazem | Facilita manutenção e suporte |

---

## Resumo das responsabilidades

~~~text
Automation Anywhere
    → inicia a execução e envia um JSON

bootstrap.py
    → atualiza, reinicia, prepara e inicia a automação

requirements.txt
    → declara as dependências da automação

.env e config.py
    → personalizam e validam o ambiente

main.py
    → descreve o fluxo principal

etapas/
    → contém as atividades do processo

funcoes/
    → contém operações reutilizáveis

stdout e código de saída
    → devolvem o resultado ao Automation Anywhere
~~~

O objetivo deste modelo não é criar uma arquitetura complexa. Ele estabelece um caminho previsível para criar, configurar, atualizar, executar e dar suporte a automações Python sem exigir que todas as pessoas envolvidas dominem uma arquitetura tradicional de software.
