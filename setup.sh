touch keys_tokens.py
touch telegram_id.py

cat > ./keys_tokens.py <<EOL
# Telegram
BOT_TOKEN = 'Your Telegram bot token'

# Twitter
TW_API_KEY = 'Your Twitter API key'
TW_API_SECRET_KEY = 'Your Twitter API secret key'
TW_ACCESS_TOKEN = 'Your Twitter Access Token'
TW_ACCESS_TOKEN_SECRET = 'Your Twitter Access Token Secret'
EOL

cat > ./telegram.py <<EOL
id = 'Your telegram ID'
EOL

