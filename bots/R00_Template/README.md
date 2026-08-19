# Modelo de Automação Python por Etapas

Modelo para padronizar o desenvolvimento de automações em Python de forma **simples, organizada e fácil de entender**, inclusive para pessoas com pouca experiência em desenvolvimento de software.

A ideia central é dividir a automação de acordo com as **etapas do processo**, permitindo que o fluxo seja compreendido apenas observando a estrutura do projeto e o arquivo `main.py`.

---

## Índice

- [Estrutura do projeto](#estrutura-do-projeto)
- [Como funciona](#como-funciona)
- [main.py](#mainpy)
- [config.py](#configpy)
- [Pasta etapas](#pasta-etapas)
- [Numeração das etapas](#numeração-das-etapas)
- [Pasta funcoes](#pasta-funcoes)
- [Pasta arquivos](#pasta-arquivos)
- [Pasta logs](#pasta-logs)
- [Boas práticas](#boas-práticas)
- [Exemplo completo](#exemplo-completo)
- [Resumo](#resumo)

---

## Estrutura do projeto

```text
automacao/
│
├── main.py
├── config.py
├── requirements.txt
│
├── etapas/
│   ├── 01_extrair_dados.py
│   ├── 02_validar_dados.py
│   ├── 03_atualizar_sistema.py
│   ├── 04_gerar_relatorio.py
│   └── 05_enviar_email.py
│
├── funcoes/
│   ├── excel.py
│   ├── banco.py
│   └── navegador.py
│
├── arquivos/
├── logs/
│
└── README.md
```

---

## Como funciona

A automação deve ser organizada seguindo o fluxo natural do processo. Exemplo:

```text
Extrair dados
     ↓
Validar dados
     ↓
Atualizar sistema
     ↓
Gerar relatório
     ↓
Enviar e-mail
     ↓
Fim
```

Cada etapa importante do processo deve possuir seu próprio arquivo dentro da pasta `etapas`.

---

## main.py

O arquivo `main.py` representa o **fluxo principal da automação**. Ele deve ser simples e permitir que qualquer pessoa consiga entender o processo lendo o arquivo de cima para baixo.

```python
from etapas.extrair_dados import executar as extrair
from etapas.validar_dados import executar as validar
from etapas.atualizar_sistema import executar as atualizar
from etapas.gerar_relatorio import executar as gerar_relatorio
from etapas.enviar_email import executar as enviar_email


def main():

    dados = extrair()

    dados = validar(dados)

    atualizar(dados)

    gerar_relatorio(dados)

    enviar_email()


if __name__ == "__main__":
    main()
```

> O `main.py` deve mostrar **o que a automação faz**, e não todos os detalhes de como cada atividade é executada.

---

## config.py

Concentra as informações configuráveis da automação.

```python
CAMINHO_ENTRADA = r"C:\Automacao\Entrada"

CAMINHO_SAIDA = r"C:\Automacao\Saida"

URL_API = "https://api.exemplo.com"

TIMEOUT = 30

TENTATIVAS = 3
```

### Regra

Se um valor pode mudar sem alterar a lógica da automação, ele deve preferencialmente ficar no `config.py`. Exemplos:

- caminhos
- URLs
- quantidade de tentativas
- tempos de espera
- nomes de arquivos
- nomes de filas
- parâmetros de execução

> ⚠️ Senhas, tokens e outras informações sensíveis **não devem ser armazenados diretamente no código**.

---

## Pasta etapas

Contém as principais etapas do processo:

```text
etapas/
├── 01_extrair_dados.py
├── 02_validar_dados.py
├── 03_atualizar_sistema.py
├── 04_gerar_relatorio.py
└── 05_enviar_email.py
```

Cada arquivo deve representar uma atividade clara do processo. Sempre que possível, cada etapa deve possuir uma função principal chamada `executar()`:

```python
def executar():

    dados = buscar_dados()

    return dados
```

O objetivo é manter um padrão simples entre todas as etapas.

---

## Numeração das etapas

Quando fizer sentido, os arquivos podem ser numerados:

```text
01_extrair_dados.py
02_validar_dados.py
03_processar_dados.py
04_gerar_relatorio.py
```

Isso facilita a visualização da ordem do processo diretamente pela estrutura das pastas. A numeração deve representar a **ordem lógica do processo**, e não necessariamente obrigar a execução automática nessa sequência — o `main.py` continua sendo responsável por definir a ordem real de execução.

---

## Pasta funcoes

Contém códigos reutilizáveis, utilizados por diferentes etapas:

```text
funcoes/
├── excel.py
├── banco.py
├── navegador.py
└── email.py
```

```python
# funcoes/excel.py

def ler_planilha(caminho):
    ...


def salvar_planilha(caminho):
    ...
```

Uso em uma etapa:

```python
from funcoes.excel import ler_planilha


def executar():

    dados = ler_planilha("entrada.xlsx")

    return dados
```

### Regra

Se um mesmo código estiver sendo copiado em vários lugares, considere transformá-lo em uma função reutilizável.

---

## Pasta arquivos

Pode armazenar arquivos utilizados pela automação:

```text
arquivos/
├── modelos/
├── entrada/
└── saida/
```

Exemplos: modelos Excel, arquivos de configuração auxiliares, arquivos temporários, arquivos gerados pela automação.

> Quando os arquivos estiverem armazenados em rede, SharePoint ou outro serviço externo, essa pasta pode não ser necessária.

---

## Pasta logs 

``
Utilizar biblioteca nativo logging conforme abaixo:
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
``
Armazena os registros de execução da automação quando os logs forem gravados localmente:

```text
logs/
├── automacao_2026-08-13.log
└── automacao_2026-08-14.log
```

Os logs devem permitir identificar:

- início da execução
- fim da execução
- etapas executadas
- itens processados
- erros encontrados
- informações importantes para suporte

Evite:

```python
print("deu erro")
```

Prefira mensagens que expliquem o problema:

```text
Erro ao atualizar item 1254 no SAP.
```

---

## Boas práticas

### 1. O fluxo principal deve ficar no main.py
Evite colocar códigos muito grandes diretamente nele.

### 2. Uma etapa deve ter uma responsabilidade clara
Prefira `03_atualizar_sap.py` em vez de `03_fazer_varias_coisas.py`. Se uma etapa ficar muito grande, considere dividi-la.

### 3. Utilize nomes claros
Prefira `buscar_pedidos()` em vez de `buscar()`, e `quantidade_tentativas` em vez de `qtd`. O código deve ser fácil de entender por outra pessoa.

### 4. Evite repetir código
Se o mesmo trecho aparecer várias vezes, transforme-o em uma função.

### 5. Configurações não devem ficar espalhadas
Evite repetir caminhos como `\\servidor01\pasta\arquivo.xlsx` em vários arquivos diferentes. Centralize esse tipo de informação no `config.py`.

### 6. Nunca coloque senhas diretamente no código
Credenciais devem ser armazenadas utilizando os mecanismos definidos pela organização.

### 7. Erros devem ser compreensíveis
Prefira `Erro ao atualizar pedido 4500012345 no SAP.` em vez de `Erro ao processar item.`. Sempre que possível, informe qual item estava sendo processado e em qual etapa ocorreu o problema.

---

## Exemplo completo

```text
automacao_pedidos/
│
├── main.py
├── config.py
│
├── etapas/
│   ├── 01_buscar_pedidos.py
│   ├── 02_validar_pedidos.py
│   ├── 03_atualizar_sap.py
│   ├── 04_gerar_relatorio.py
│   └── 05_enviar_email.py
│
├── funcoes/
│   ├── banco.py
│   ├── sap.py
│   ├── excel.py
│   └── email.py
│
├── arquivos/
├── logs/
└── README.md
```

```python
from etapas.buscar_pedidos import executar as buscar_pedidos
from etapas.validar_pedidos import executar as validar_pedidos
from etapas.atualizar_sap import executar as atualizar_sap
from etapas.gerar_relatorio import executar as gerar_relatorio
from etapas.enviar_email import executar as enviar_email


def main():

    pedidos = buscar_pedidos()

    pedidos = validar_pedidos(pedidos)

    atualizar_sap(pedidos)

    gerar_relatorio(pedidos)

    enviar_email()


if __name__ == "__main__":
    main()
```

---

## Resumo

| Item | Função |
|---|---|
| `main.py` | Mostra o fluxo da automação |
| `config.py` | Contém informações configuráveis |
| `etapas/` | Contém as etapas do processo |
| `funcoes/` | Contém códigos reutilizáveis |
| `arquivos/` e `logs/` | Armazenam arquivos utilizados e registros da execução |

O objetivo deste modelo não é criar uma arquitetura complexa, mas garantir que as automações desenvolvidas em Python sejam **fáceis de criar, entender, manter e dar suporte**.
