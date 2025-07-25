import telebot
import re
import threading
from command_runner.CommandRunner import CommandRunner
import os
import logging
from dotenv import load_dotenv

load_dotenv()  # Carrega do arquivo .env

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")
USER_ID = str(USER_ID)

# Configura o logging para salvar em arquivo
logging.basicConfig(
    filename='meulog.log',       # Nome do arquivo de log
    level=logging.ERROR,           # Nível mínimo de log
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato da linha
)


bot = telebot.TeleBot(BOT_TOKEN)

user_states = {}
users_data = {}
regex_PIN = re.compile(r'^\d{6}$')

@bot.message_handler(commands=['start'])
def handle_start(message):
    if str(message.chat.id) == USER_ID:
        user_states[USER_ID] = 'aguardando PIN'
        bot.reply_to(message, "Digite seu PIN")
        return
    bot.reply_to(message, "Acesso Negado !!")
    logging.error("Acesso Negado - Chat Id não corresponde")

@bot.message_handler(commands=['cancelar'])
def handle_cancelar(message):
    if user_states.get(USER_ID) != "comando iniciado":
        user_states.clear()
        bot.reply_to(message, "Cancelado")
    else:
        bot.reply_to(message, "Comando já iniciado!!")

@bot.message_handler(commands=['help'])
def handle_help(message):
    with open("help.txt", "r", encoding="utf-8") as f:
        ajuda = f.read()
    bot.reply_to(message, ajuda)

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    estado = user_states.get(USER_ID)
    if estado == "aguardando PIN":
        if regex_PIN.match(message.text):
            users_data[str(USER_ID)+":user_PIN"]=message.text
            user_states[USER_ID] = 'aguardando senha'
            bot.reply_to(message, "Digite sua senha")
        else:
            bot.reply_to(message, "Digite um PIN válido")
        return

    if estado == "aguardando senha":
        users_data[str(USER_ID)+":user_password"]=message.text
        user_states[USER_ID] = 'aguardando comando'
        bot.reply_to(message, "Digite o comando Google")
        return

    if estado == "aguardando comando":
        comando_inicial = """sudo -S """
        usuario = " --user-name=matheus"
        comando_google = message.text
        comando_cmd = comando_inicial + comando_google + usuario
        user_PIN = users_data[str(USER_ID)+":user_PIN"]
        user_password = users_data[str(USER_ID)+":user_password"]
        comandos = [
            {
                "comando": comando_cmd,
                "interacoes": [
                    {"prompt": r"senha para .*:", "resposta": user_password},
                    {"prompt": "Enter a PIN of at least six digits:", "resposta": user_PIN},
                    {"prompt": "Enter the same PIN again:", "resposta": user_PIN},
                ]
            }
        ]
        bot.reply_to(message, "Iniciando comando")
        user_states[USER_ID] = 'comando iniciado'
        thread = threading.Thread(target=chamar_comando, args=(USER_ID,comandos))
        thread.start()
        return

    if estado == "comando iniciado":
        bot.reply_to(message, "Aguarde")
        return

    # Nenhum estado definido:
    bot.reply_to(message, "Use /start para iniciar.")


def chamar_comando(chat_id,comando):
    env = os.environ.copy()
    runner = CommandRunner(timeout=10,env=env)
    sucesso, log = runner.run_commands(comando)
    if sucesso:
        bot.send_message(chat_id,"Ambiente configurado com sucesso !!")
        comando_cmd = "gnome-session-quit --logout --no-prompt"
        comando = [{"comando": comando_cmd,"interacoes": []}]
        runner.run_commands(comando)

    else:
        bot.send_message(chat_id,"ERRO: "+str(log))
        logging.error("Erro:"+str(log))
    




bot.infinity_polling()