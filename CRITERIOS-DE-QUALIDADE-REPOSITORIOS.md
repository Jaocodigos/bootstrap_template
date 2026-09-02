# Diretrizes de Desenvolvimento e Code Review (Python -> Automation Anywhere)

Guia prático para desenvolvimento e submissão de scripts Python destinados à execução em runners controlados do Automation Anywhere.

---

## 1. Logs Obrigatórios
* **Início e Término:** Registre mensagens claras indicando quando o script iniciou e quando finalizou com sucesso.
* **Progresso do Negócio:** Inclua logs em etapas-chave intermediárias (ex.: leitura de arquivos, iterações em lotes, chamadas de API).
* **Detalhamento de Erros:** Capture e registre o traceback completo da exceção em caso de falha.
* **Privacidade e Conformidade:** Proibido registrar senhas, tokens de acesso, dados pessoais sensíveis ou CPFs nos logs.
* **Biblioteca Padrão:** Utilize a biblioteca `logging` configurada para saída padrão (`sys.stdout`/`sys.stderr`) em vez de `print()`.

---

## 2. Controle de Execução e Códigos de Saída (Exit Codes)
* **Status Explícito:**
  * Utilize `sys.exit(0)` para indicar conclusão com sucesso ao runner.
  * Utilize `sys.exit(1)` (ou código > 0) em exceções críticas para que o Automation Anywhere identifique o erro e acione a rota de contingência.
* **Tratamento Controlado:** Proibido o uso de blocos `except: pass` vazios que ocultem falhas silenciosas.
* **Liberação de Recursos:** Utilize gerenciadores de contexto (`with open(...) as f:`) e garanta o fechamento de conexões de banco ou sessões HTTP.

---

## 3. Segurança e Gestão de Segredos
* **Sem Credenciais Hardcoded:** Proibido armazenar senhas, tokens de API, connection strings ou chaves de acesso diretamente no código.
* **Parâmetros Dinâmicos:** Segredos e parâmetros variáveis devem ser injetados via argumentos de linha de comando (`argparse`/`sys.argv`) ou variáveis de ambiente gerenciadas pelo Automation Anywhere.

---

## 4. Gerenciamento de Caminhos e Arquivos
* **Sem Caminhos Absolutos Locais:** Proibido referenciar caminhos específicos de máquinas de desenvolvedores (ex.: `C:\Users\nome.sobrenome\...`).
* **Caminhos Parametrizados ou Relativos:** Utilize argumentos de entrada ou a biblioteca `pathlib.Path` para referenciar pastas de entrada, saída e diretórios temporários.
* **Validação Prévia:** Valide a existência de arquivos e diretórios de entrada antes de iniciar o processamento.

---

## 5. Dependências (`requirements.txt`)
* **Arquivo Obrigatório:** Todo repositório/script deve incluir um arquivo `requirements.txt` com as dependências e versões compatíveis com o ambiente do runner.
* **Sem Privilégios Administrativos:** Não utilize bibliotecas que demandem permissões de administrador local para instalação ou execução.

---

## 6. Estrutura do Código e Boas Práticas
* **Ponto de Entrada Definido:** Utilize a estrutura padrão de inicialização:
  ```python
  def main():
      # Execução do fluxo principal
      pass

  if __name__ == "__main__":
      main()
  ```
* **Prevenção de Loops Infinitos:** Estruturas `while` devem conter critérios claros de parada, contadores máximos de repetição ou timeouts configurados.

---

## Checklist Rápido Pré-Submissão (Code Review)

- [ ] As etapas principais e eventuais erros geram log estruturado via `logging`?
- [ ] Não há senhas, tokens ou dados sensíveis expostos no código?
- [ ] O script utiliza `sys.exit(0)` no encerramento normal e `sys.exit(1)` em falhas críticas?
- [ ] Foram removidos todos os caminhos absolutos locais (`C:\Users\...`)?
- [ ] O arquivo `requirements.txt` está atualizado e sem bibliotecas que exijam privilégios de admin?
- [ ] Há proteção contra loops infinitos e travamento de recursos?
