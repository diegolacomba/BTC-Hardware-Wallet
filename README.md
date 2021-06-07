# BTC-Hardware-Wallet
Development of a BTC cold wallet, that is, a hardware device with the ability to create and manage your private keys associated with your BTC in an offline environment.

## Entrono de desarrollo
El microcontrolador escogido es la ESP-32 TTGO y el lenguaje de programación Micropython.

## Propósito
Dispositivo hardware para almacenamiento y gestión de las claves privadas asociadas a los Bitcoin del usuario. Para ello debe ser capaz de establecer una conexión segura con un medio online y realizar transacciones sin poner en riesgo las claves privadas, además de hacer inaccesible la información almacenada al realizar una conexión con un dispositivo conectado a Internet.

## Entradas
- Entrada USB: Su función es alimentar al dispositivo y establecer una conexión segura, con el PC o móvil que proporciona la alimentación, para realizar las transacciones de BTC.
- Tres botones: Habilitan la navegación por el menú.

## Salidas
- Pantalla 23 mm * 60 mm aprox. : Display del menú y todas las acciones posibles a realizar con el dispositivo. Debe ser un menú sencillo e intuitivo para el usuario.
- Tarjeta SD: La función de la tarjeta SD es almacenar un clave privada “maestra”, llamada semilla de recuperación, a partir de la cual se pueden obtener todas las claves privadas asociadas a los BTC del usuario y por lo tanto las claves públicas también. Y por lo tanto proporcionar una recuperación completa del dispositivo extraviado o inutilizado. Además de almacenar la semilla de recuperación, obviamente se puede cargar esta para el proceso de recuperación. Ambas opciones están disponibles desde el menú mostrado por pantalla.
- Salida USB: Como se ha explicado en el apartado de entradas, la salida USB se emplea para realizar la conexción con el medio online.

## Funciones
La función principal del dispositivo es almacenar de forma segura las claves privadas de los BTC del usuario. El dispositivo debe ser capaz de generar tanto la semilla de recuperación como las claves privadas y públicas. Además de emplear una semilla de recuperación para la restauración del dispositivo. ( Explicar brevemente los mecanismos de generación y cifrado ).

También debe ser reconocido por una plataforma online, como por ejemplo Electrum, para realizar las transferencias, desde nuestro dispositivo que almacena las claves en un entorno offline, a la billetera caliente ( Electrum ) que almacena las claves en un entorno online ( servidor ) o viceversa. Para operar con Electrum es necesario darse de alta en la plataforma, como en cualquier otra. La decisión de la plataforma online para realizar las transferencias está sujeta a cambios.

Como se ha explicado anteriormente también debe ser capaz de almacenar la semilla de recuperación en una tarjeta SD, se pueden realizar tantas copias como el usuario desee, esta semilla se almacena cifrada. Para realizar una transacción de BTC se envía la clave pública al emisor ( este no puede obtener tu clave privada a partir de esta ), esta clave pública hace la función de dirección de envío. La transacción debe realizarse mediante la red blockchain de BTC y de esta forma quedar registrada. De la misma forma se realiza un envío, en este caso el usuario necesita la clave pública del receptor.

## Prestaciones
- Posibilidad de generar aleatoriedad (entropía) de calidad, para así generar una semilla y tu clave privada de - forma segura.
- Posibilidad de poder demostrar la legitimidad o incorruptibilidad del dispositivo con algún mecanismo de integridad.
- Garantizar la confidencialidad de tus claves y la semilla, aunque tengan ataques físicos o remotos.

