# master_profiles

## Estructura

Example:
```
my_project/
│
├── order_service/                    
│   ├── domain/                       
│   │   ├── models/                   
│   │   │   ├── order.py              # Entidad "Order"
│   │   │   ├── order_item.py         # Entidad "OrderItem"
│   │   │   ├── customer.py           # Entidad "Customer" (si aplica al dominio del pedido)
│   │   ├── repositories/             
│   │   │   ├── order_repository.py   # Interfaz del repositorio para "Order"
│   │   │   └── customer_repository.py# Interfaz del repositorio para "Customer"
│   │   └── services/                 
│   │       ├── order_domain_service.py # Servicio de dominio para lógica compleja de "Order"
│   │       └── payment_domain_service.py # Servicio de dominio para lógica de pagos (si aplica)
│   │
│   ├── application/                  
│   │   ├── use_cases/                
│   │   │   ├── place_order.py        # Caso de uso para colocar un pedido
│   │   │   ├── cancel_order.py       # Caso de uso para cancelar un pedido
│   │   │   └── get_order_details.py  # Caso de uso para obtener detalles de un pedido
│   │   └── dto/                      
│   │       ├── order_dto.py          # DTO para la entidad "Order"
│   │       ├── order_item_dto.py     # DTO para la entidad "OrderItem"
│   │       └── customer_dto.py       # DTO para la entidad "Customer"
│   │
│   ├── infrastructure/               
│   │   ├── persistence/              
│   │   │   ├── order_repository_impl.py # Implementación concreta de "OrderRepository" usando una base de datos
│   │   │   ├── customer_repository_impl.py # Implementación concreta de "CustomerRepository"
│   │   ├── external_apis/            
│   │   │   ├── payment_gateway_api.py # Adaptador para la integración con un gateway de pago externo
│   │   ├── config/                   
│   │   │   └── settings.py           # Configuración y parámetros de entorno
│   │   └── s3/                       
│   │       └── s3_file_handler.py    # Manejador específico para almacenamiento en S3
│   │
│   ├── interface/                    
│   │   ├── controllers/              
│   │   │   ├── order_controller.py   # Controlador para manejar endpoints relacionados con "Order"
│   │   │   └── customer_controller.py # Controlador para manejar endpoints relacionados con "Customer"
│   │   ├── serializers/              
│   │   │   ├── order_serializer.py   # Serializador para la validación de "Order"
│   │   │   └── customer_serializer.py # Serializador para la validación de "Customer"
│   │   └── mappers/                  
│   │       ├── order_mapper.py       # Mapper para convertir entre DTOs y entidades para "Order"
│   │       └── customer_mapper.py    # Mapper para convertir entre DTOs y entidades para "Customer"
│   │
│   └── serverless.yml                # Configuración del Serverless Framework para despliegue en AWS Lambda
│
├── shared_kernel/                    
│   ├── config/                       
│   │   └── shared_settings.py        # Configuraciones globales compartidas
│   ├── enums/                        
│   │   └── status_enum.py            # Enumeraciones de estados comunes
│   ├── events/                       
│   │   └── order_events.py           # Eventos relacionados con pedidos
│   ├── validators/                   
│   │   ├── common_validators.py      # Validadores comunes para payloads
│   └── utils.py                      
```

### DDD
Domain-Driven Design (DDD) es una metodología de diseño de software.

#### Entidad
Objetos que tienen identidad única dentro del dominio (ejemplo: un “Order” o “Customer”).

#### Value Objects
Objetos que no tienen identidad única y son definidos solo por sus atributos (ejemplo: una dirección o un rango de fechas).

#### Agregado
Un grupo de entidades y objetos de valor que se tratan como una unidad para fines de consistencia.

#### Repositorio
Abstracción para el acceso a datos que permite gestionar la persistencia de los agregados.

#### Servicio de Dominio
Contiene lógica de negocio que no pertenece a una sola entidad o agregado.

#### Bounded Contexts
Límites explícitos donde un modelo de dominio particular se aplica. En un sistema grande, hay múltiples bounded contexts.

### Clean Architecture
Se enfoca en mantener la lógica de negocio independiente de frameworks, bases de datos, interfaces de usuario y otros detalles externos.

#### Capa de Dominio
Representa el núcleo del sistema y contiene la lógica de negocio usando modelos, entidades y servicios de dominio. Esta capa es independiente de cualquier tecnología o infraestructura.

#### Capa de Aplicación
Implementa los casos de uso específicos (use cases). Esta capa orquesta la lógica del negocio, invocando los servicios y repositorios necesarios.

#### Infraestructura
Maneja detalles como la persistencia, acceso a APIs externas, manejadores de eventos, y configuración. En un entorno serverless, aquí es donde se definen los adaptadores para conectarse a servicios como DynamoDB, S3 o SNS.

#### Interfaces/Interacción
Aquí se ubican los controladores HTTP o los manejadores de eventos (como los Lambda handlers en AWS). Esta capa también puede contener validadores y mappers para convertir datos de entrada a objetos de dominio.

# ------------------------------------------



<!--
title: 'AWS Simple HTTP Endpoint example in Python'
description: 'This template demonstrates how to make a simple HTTP API with Python running on AWS Lambda and API Gateway using the Serverless Framework.'
layout: Doc
framework: v4
platform: AWS
language: python
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, Inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->

# Serverless Framework Python HTTP API on AWS

This template demonstrates how to make a simple HTTP API with Python running on AWS Lambda and API Gateway using the Serverless Framework.

This template does not include any kind of persistence (database). For more advanced examples, check out the [serverless/examples repository](https://github.com/serverless/examples/) which includes DynamoDB, Mongo, Fauna and other examples.

## Usage

### Deployment

```
serverless deploy
```

After deploying, you should see output similar to:

```
Deploying "aws-python-http-api" to stage "dev" (us-east-1)

✔ Service deployed to stack aws-python-http-api-dev (85s)

endpoint: GET - https://6ewcye3q4d.execute-api.us-east-1.amazonaws.com/
functions:
  hello: aws-python-http-api-dev-hello (2.3 kB)
```

_Note_: In current form, after deployment, your API is public and can be invoked by anyone. For production deployments, you might want to configure an authorizer. For details on how to do that, refer to [http event docs](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/).

### Invocation

After successful deployment, you can call the created application via HTTP:

```
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/
```

Which should result in response similar to the following (removed `input` content for brevity):

```json
{
  "message": "Go Serverless v4.0! Your function executed successfully!"
}
```

### Local development

You can invoke your function locally by using the following command:

```
serverless invoke local --function hello
```

Which should result in response similar to the following:

```json
{
  "statusCode": 200,
  "body": "{\n  \"message\": \"Go Serverless v4.0! Your function executed successfully!\"}"
}
```

Alternatively, it is also possible to emulate API Gateway and Lambda locally by using `serverless-offline` plugin. In order to do that, execute the following command:

```
serverless plugin install -n serverless-offline
```

It will add the `serverless-offline` plugin to `devDependencies` in `package.json` file as well as will add it to `plugins` in `serverless.yml`.

After installation, you can start local emulation with:

```
serverless offline
```

To learn more about the capabilities of `serverless-offline`, please refer to its [GitHub repository](https://github.com/dherault/serverless-offline).

### Bundling dependencies

In case you would like to include 3rd party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).

# sls offline start





> // copiar tus credenciales aws
> python -m venv .venv
> source .venv/bin/activate
> cd service/sampleService
> ln -s ../../package-lock.json
> ln -s ../../package.json
> ln -s ../../node_modules
> serverless offline
