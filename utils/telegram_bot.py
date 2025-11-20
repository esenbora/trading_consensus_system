class TelegramBot:
    def __init__(self):
        self.enabled = True

    def send_alert(self, message):
        """
        Sends an alert to the configured Telegram channel.
        Mock implementation.
        """
        if self.enabled:
            print(f"[TELEGRAM ALERT]: {message}")
            # In real implementation: requests.post(f"https://api.telegram.org/bot{token}/sendMessage", ...)
