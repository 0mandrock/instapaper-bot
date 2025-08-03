# Instapaper Bot

Telegram bot that saves links to Instapaper.

## Local setup

1. Copy `.env.example` to `.env` and fill in:
   - `telegram_token` – Telegram Bot API token
   - `app_url` – public URL for webhook (e.g. `http://localhost:5000` or tunnel)
   - `DATABASE_URL` – PostgreSQL connection string
2. Install dependencies: `pip install -r requirements.txt`
3. Run the bot: `python -m src.bot`

## Heroku deployment

1. Create an app and add a Postgres add-on.
2. Set config vars:
   ```bash
   heroku config:set telegram_token=<token> app_url=https://<app>.herokuapp.com
   ```
   `DATABASE_URL` is provided by the add-on.
3. Deploy: `git push heroku main`
