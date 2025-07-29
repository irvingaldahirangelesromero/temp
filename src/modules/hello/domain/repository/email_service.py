class EmailService:
    def send_email(self, recipient: str, subject: str, body: str):
        return f"Sending email to {recipient} with subject '{subject}'"
