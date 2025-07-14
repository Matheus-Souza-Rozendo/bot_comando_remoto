
## ✅ Etapas da Análise de Requisitos

### 📌 1. **Levantamento de objetivos (Requisitos de negócio)**

**Objetivo principal:**

> Permitir que o usuário inicialize remotamente o Chrome Remote Desktop no Ubuntu de forma automatizada, usando o Telegram, para que a máquina esteja pronta para acesso remoto sem necessidade de intervenção manual.

---

### 📌 2. **Requisitos Funcionais (o que o sistema deve fazer)**

| ID  | Descrição                                                               |
| --- | ----------------------------------------------------------------------- |
| RF1 | O sistema deve receber comandos via bot do Telegram.                    |
| RF2 | O sistema deve rodar comandos do terminal Linux no Ubuntu.              |
| RF3 | O sistema deve configurar o Chrome Remote Desktop via código do Google. |
| RF4 | O sistema deve fornecer o PIN e senha de sudo de forma automática.      |
| RF5 | O sistema deve encerrar a sessão local do Ubuntu após configurar o CRD. |

---

### 📌 3. **Requisitos Não Funcionais (como o sistema deve se comportar)**

| ID   | Descrição                                                                                                 |
| ---- | --------------------------------------------------------------------------------------------------------- |
| RNF1 | O sistema deve ser seguro e armazenar dados sensíveis (senhas, PINs) com criptografia ou acesso restrito. |
| RNF2 | O bot deve ter autenticação mínima (ex: aceitar comandos apenas de um ID específico).                     |
| RNF3 | O sistema deve ser compatível com Ubuntu 20.04 ou superior.                                               |
| RNF4 | O tempo entre o comando do Telegram e a execução dos scripts deve ser inferior a 10 segundos.             |

---

### 📌 5. **Fluxo de uso resumido (caso de uso)**

1. Usuário envia `/preparar_crd` via Telegram.
2. Bot valida se o usuário tem permissão.
3. Bot executa:

   * Comando de inicialização do CRD com o código do Google.
   * PIN e autenticação sudo.
   * Encerramento da sessão atual.
4. Usuário acessa remotamente via CRD do trabalho.
5. Quando termina, encerra a sessão remota no CRD.
6. Ao voltar pra casa, notebook pode ser acessado normalmente localmente.

