import os
import sys

# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../../../../../..'))
sys.path.append(project_root)

from dependency_injector import containers, providers
from src.modules.hello.domain.repository.email_service import EmailService
from src.modules.hello.domain.repository.payment_service import PaymentService
from src.modules.hello.useCase.order_use_case import OrderUseCase
from src.modules.hello.adapter.order_adapter import OrderAdapter


class Container(containers.DeclarativeContainer):
    # Proveedores de servicios
    email_service = providers.Singleton(EmailService)
    payment_service = providers.Singleton(PaymentService)

    # Caso de uso que depende de los servicios
    order_use_case = providers.Factory(
        OrderUseCase,
        email_service=email_service,
        payment_service=payment_service
    )

    # Adaptador que depende del caso de uso
    order_adapter = providers.Factory(
        OrderAdapter,
        order_use_case=order_use_case  # Aquí se inyecta la instancia del caso de uso
    )