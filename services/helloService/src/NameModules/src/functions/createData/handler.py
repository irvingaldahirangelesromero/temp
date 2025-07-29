import json
from .inversify import Container

def main(event, context):
    # Inicializar el contenedor
    container = Container()

    # Obtener instancia del adaptador sin importar directamente
    order_adapter = container.order_adapter()

    # Extraer datos del evento (por ejemplo, en un API Gateway)
    elementary = json.loads(event['body'])
    recipient = elementary['recipient']
    amount = elementary['amount']

    # Usar el adaptador para procesar el pedido
    response1 = order_adapter.process_order(recipient, amount)
    response2 = {
        'statusCode': 200,
        'body': f"action: {response1}"
    }
    return response2
