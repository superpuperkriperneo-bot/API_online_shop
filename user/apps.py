from django.apps import AppConfig
import sys
import os


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        import user.signals
        if 'runserver' in sys.argv:
            self.set_telegram_webhook()

    def set_telegram_webhook(self):
        import requests
        from django.conf import settings

        token = settings.TELEGRAM_BOT_TOKEN
        webhook_url = settings.TELEGRAM_WEBHOOK_URL

        if not token or not webhook_url:
            print("Telegram token or Webhook URL not found in settings, webhook not set")
            return
        
        url = f"https://api.telegram.org/bot{token}/setWebhook"
        try:
            response = requests.post(url, json={"url": webhook_url})
            if response.status_code == 200:
                print(f"Telegram webhook successfully set to: {webhook_url}")
            else:
                print(f"Failed to set Telegram Webhook: {response.text}")
        except Exception as e:
            print(f"Error setting Telegram Webhook: {e}")