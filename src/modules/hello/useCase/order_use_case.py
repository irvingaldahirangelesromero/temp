class OrderUseCase:
    def __init__(self, email_service, payment_service):
        self.email_service = email_service
        self.payment_service = payment_service

    def execute_order(self, recipient: str, amount: float):
        self.payment_service.process_payment(amount)
        return self.email_service.send_email(recipient, "Order Confirmation", f"Your payment of ${amount} was successful.")
