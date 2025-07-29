class OrderAdapter:
    def __init__(self, order_use_case):
        self.order_use_case = order_use_case

    def process_order(self, recipient: str, amount: float):
        value = self.order_use_case.execute_order(recipient, amount)
        return value
