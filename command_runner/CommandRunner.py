import pexpect

class CommandRunner:
    def __init__(self, timeout=60, encoding='utf-8', env = None):
        self.timeout = timeout
        self.encoding = encoding
        self.env = env

    def run_commands(self, commands):
        """
        Executa uma sequência de comandos interativos.

        commands: lista de dicts:
          [
            {
              "comando": "sudo apt update",
              "interacoes": [
                  {"prompt": r"password for .*:", "resposta": "<senha>"},
                  {"prompt": r"Press ENTER to continue", "resposta": ""}
              ]
            },
            ...
          ]
        Retorna: (success: bool, log: str)
        """
        log = ""

        for cmd_obj in commands:
            cmd = cmd_obj["comando"]
            interacoes = cmd_obj.get("interacoes", [])

            log += f"\n>>> EXECUTANDO: {cmd}\n"

            try:
                child = pexpect.spawnu(cmd,env=self.env, encoding=self.encoding, timeout=self.timeout)
            except Exception as e:
                log += f"\n❌ Erro ao executar comando: {e}\n"
                return False, log

            erro = False

            for step in interacoes:
                prompt = step["prompt"]
                resposta = step["resposta"]

                try:
                    idx = child.expect([prompt, pexpect.TIMEOUT, pexpect.EOF])
                    log += child.before

                    if idx == 0:
                        child.sendline(resposta)
                    elif idx == 1:
                        log += f"\n⚠️ Timeout ao aguardar prompt: {prompt}\n"
                        erro = True
                    else:
                        log += f"\n❌ Processo terminou antes do prompt: {prompt}\n"
                        erro = True

                except Exception as e:
                    log += f"\n❌ Erro durante interação: {e}\n"
                    erro = True

                if erro:
                    child.close(force=True)
                    return False, log

            # Espera até o fim do processo
            try:
                child.expect(pexpect.EOF)
                log += child.before
            except Exception as e:
                log += f"\n❌ Erro ao aguardar fim do comando: {e}\n"
                child.close(force=True)
                return False, log

            child.close()
            # Pega código de saída
            exit_code = child.exitstatus
            if exit_code is None:
                exit_code = child.signalstatus
            if exit_code is None:
                exit_code = -1

            log += f"\n→ Exit code: {exit_code}\n"


            if exit_code != 0:
                return False, log

        return True, log
