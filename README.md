# Crea una aplicación de Video content moderation ⏯️ 🔫 🚬 en minutos usando [AWS CodeWhisperer](https://aws.amazon.com/es/pm/codewhisperer)


Soy fan de las películas de acción y quería probar Rekognition con el tráiler de Die Hard 1, así que creé esta aplicación y ¡guau! cada dataframe es pura violencia 🫣... Te invito a crearla y probarla con un tráiler de tu película favorita.

![Video content moderation](imagenes/diagrama.png) 

Te voy a guiar en un paso a paso de como crear esta aplicación con [AWS Cloud Development Kit (AWS CDK)](https://docs.aws.amazon.com/cdk/v2/guide/home.html) usando [AWS CodeWhisperer](https://aws.amazon.com/es/pm/codewhisperer)

### ¿Qué es CodeWhisperer?
Es un generador de código de uso general basado en el aprendizaje automático que le proporciona recomendaciones de código en tiempo real. A medida que escribe código, CodeWhisperer genera automáticamente sugerencias basadas en el código y los comentarios existentes. Sus recomendaciones personalizadas pueden variar en tamaño y alcance, desde un comentario de una sola línea hasta funciones completas.

CodeWhisperer también puede escanear tu código para resaltar y definir los problemas de seguridad.

## ¿Como funciona esta aplicación?

1. Sube un video en formato .mp4 a un [Bucket de S3](https://docs.aws.amazon.com/es_es/AmazonS3/latest/userguide/UsingBucket.html).
2. Una [Amazon Lambda Function](https://docs.aws.amazon.com/es_es/lambda/latest/dg/welcome.html) hace la llamada a la API de [Amazon Rekognition](https://aws.amazon.com/es/rekognition/).
3. Una vez finalizada la revisión del vídeo, una nueva función de Lambda recupera el resultado y lo almacena en un bucket de Amazon S3.

## Instrucciones para crearla con [AWS CodeWhisperer](https://aws.amazon.com/es/pm/codewhisperer): 

### Paso 1: configura [AWS CodeWhisperer](https://aws.amazon.com/es/pm/codewhisperer) en [VS Code](https://code.visualstudio.com/) para desarrolladores individuales:

Siguiendo los pasos en [Configuración de CodeWhisperer para desarrolladores individuales](https://docs.aws.amazon.com/codewhisperer/latest/userguide/whisper-setup-indv-devs.html) o ve el siguiente video: 

[![Install Amazon CodeWhisperer and Build Applications Faster Today (How To)](imagenes/video_1.jpeg)](https://www.youtube.com/watch?v=sFh3_cMUrMk&t=1s)

### Paso 2: Crear El Ambiente de [AWS Cloud Development Kit (AWS CDK)](https://docs.aws.amazon.com/cdk/v2/guide/home.html): 

Siguendo los pasos de [Tu primeraAWS CDK aplicación](https://docs.aws.amazon.com/es_es/cdk/v2/guide/hello_world.html)

- Crea la carpeta para la aplicación y luego ingresa a ella: 

```
mkdir scanvideo-with-codewhisperer 
cd scanvideo-with-codewhisperer 
```

- Inicializa la aplicación en el lenguaje python: 

```
cdk init app --language python
```
- Activa en ambiente virtual e instala las dependencias de AWS CDK principales. 

```
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Paso 3: Crear La Aplicación: 

En este paso le vamos a pedir a [AWS CodeWhisperer](https://aws.amazon.com/es/pm/codewhisperer) que nos sugiera el código que dará vida a nuestra aplicación. 

![Video content moderation](imagenes/diagrama.png) 

Volviendo a la arquitectura, necesitamos crear lo siguiente: 
1. Un bucket de Amazon S3, que se llamará `video-storage`. 
2. Dos Lambdas Functions:
    - lambda_invokes_Rekognition: Para invocar la API [start_content_moderation](https://boto3.amazonaws.com/v1/documentation/api/1.9.42/reference/services/rekognition.html#Rekognition.Client.start_content_moderation) de Amazon Rekognition.
    - lambda_process_Rekognition: Para procesar el resultado de Amazon Rekognition. 
3. Un Amazon SNS Topic para generar la notificación a `lambda_process_Rekognition` cuando se termine de procesar el video. 

Para empezar a generar el codigo ve al `/scanvideo-with-codewhisperer/scanvideo_with_codewhisperer/scanvideo_with_codewhisperer_stack.py` creado en el ambiente del paso anterior. 

Escribe las siguientes instrucciones, una a una, una vez escribas la intruccion presiona `enter`, luego las teclas `option + c` y la fechas `derecha` e `izquierda` para seleccionar la sugerencia de código más adecuado. 

En este video puedes ver un ejemplo: 

[![Who Did This? Track Code Recommendations With Amazon CodeWhisperer](imagenes/video_1.jpeg)](https://www.youtube.com/watch?v=qu67bvH2Y08)

> 🚨 **Atención** Amazon CodeWhisperer te entrega sugerencias de código que no necesariamente esten 100% correctos, debes revisarlo y si es necesario modificarlo. 

1 - Crear el Amazon s3 Bucket: 

`#cdk code to amazon s3 bucket named "video-storage"`

![crear amazon s3 bucket](imagenes/create-amazon-s3-bucket.gif)

2 - Crear el Amazon SNS Topic: 

`#cdk code to sns topic named "scan-video-topic"`

3 - Crear el Amazon IAM Role para ejecutar Amazon Rekognition: 

`#cdk code to role to grant to assume amazon rekognition`

4 - Crear agregar al Role anterior la politica que permite que Amazon Rekognition pueda publicar en el SNS Topic:

`#cdk code to add a policy to the role to allow rekognition to publish sns`

5 - Crear la Amazon Lambda Function encargada de invocar a rekogntion (el código de esta se crea aparte en `/lambdas_code/lambda_invokes_rekognition`)

`#cdk code to create a lambda function to scan the video`

6 - Permisos requeridos para lambda_invokes_rekognition Lambda Function

`#cdk code to add a permission to the lambda function to allow it to read from the video storage`


`#cdk code to add a permission to the lambda function to invoke amazon rekognition content moderation`

7 - Crear la Amazon Lambda Function encargada de procesar el resultado de amazon rekogntion (el código de esta se crea aparte en `/lambdas_code/lambda_process_rekognition`)

`#cdk code to create a lambda function to process result of content moderation`

6 - Permisos requeridos para lambda_process_rekognition Lambda Function

`#cdk code to add a permission to the lambda function to allow it to read from the video storage`

`#cdk code to add a permission to the lambda function to invoke amazon rekognition content moderation`

`#cdk code to add a LambdaSubscription`

Cuando finalices deberías ver algo como en [scanvideo_with_codewhisperer_stack.py](/scanvideo-with-codewhisperer/scanvideo_with_codewhisperer/scanvideo_with_codewhisperer_stack.py)


### Paso 4: Crear La Aplicación: 











---

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.


