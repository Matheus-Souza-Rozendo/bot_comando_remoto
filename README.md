# 🖥️ Chrome Remote Desktop Starter via Telegram
This project allows you to automatically start Chrome Remote Desktop (CRD) on a Ubuntu machine by sending commands through Telegram, enabling remote access without manual intervention.

## 🚀 Objective
Allow the user to remotely initialize CRD on Ubuntu automatically using Telegram, so the machine is ready for remote access securely and quickly.

## ✅ Prerequisites
A Telegram account with a bot created via BotFather.

A computer running Ubuntu 20.04 or higher.

Chrome Remote Desktop installed.

A valid and updated CRD registration code from Google.

Certainly! Here's the English version of the `README.md`:

--- 

## 🔧 Quick Setup

```bash
# Clone the repository
git clone https://github.com/Matheus-Souza-Rozendo/bot_comando_remoto
cd bot_comando_remoto

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  

# Install dependencies
pip install -r requirements.txt

# Create a .env file with your bot credentials
cat <<EOF > .env
BOT_TOKEN=<YOUR_BOT_TOKEN>
USER_ID=<YOUR_USER_ID_TELEGRAM>
EOF

# Run the bot
python bot.py
```

--

## 🤝 Contributing

Contributions are welcome! If you’d like to suggest improvements or fixes, feel free to open an issue or pull request.

---

