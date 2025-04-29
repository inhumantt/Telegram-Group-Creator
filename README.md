# Telegram Group Creator Bot

A powerful script that automates the creation of Telegram groups using multiple accounts. It supports auto-login, group customization, and media upload for group photos. Ideal for marketing campaigns, community setups, or bulk testing environments.

---

## 🚀 Features

- ✅ Multi-account support (login with multiple Telegram accounts)
- ✅ Auto group creation with custom names, bios, emojis, and images
- ✅ Progress tracking per account using `progress.json`
- ✅ Handles Telegram rate limits (FloodWait)
- ✅ Custom welcome messages sent to each group
- ✅ Random image fetching and setting as group photo
- ✅ Automatic retry logic and 24-hour cooldown after reaching limits
- ✅ Colored terminal output with branding banner

---

## 🧰 Requirements

- Python 3.7 or higher
- A Telegram account for each bot session
- Telegram API credentials (API ID and API Hash)

---

## 🛠 Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/telegram-group-creator.git
cd telegram-group-creator
```

### Step 2: Run the script

On first run, it installs dependencies automatically.

```bash
python multi.py
```

You’ll be prompted to enter:

- Number of groups per account
- Telegram phone number
- API ID
- API Hash

Repeat account input as needed. The script will then create groups using the provided credentials.

---

## 📝 Notes

- Do not use for spamming or illegal activities. This is intended for educational and ethical automation only.
- Always respect Telegram’s rate limits and terms of service.
- Accounts may get banned if abused.

---

## 📬 Contact

Created by **INHUMANTT**. For collaboration or queries, reach out on Telegram.

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for more information.
