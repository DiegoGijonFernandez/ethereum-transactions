
# 📦 Ethereum Transaction Tracker

Este proyecto proporciona una herramienta para monitorear y analizar el ciclo de vida de las transacciones en la red de Ethereum, incluyendo estados como pendientes, minadas, descartadas y reemplazadas. Utiliza la API de Alchemy y su herramienta Mempool Watcher para ofrecer una visión detallada del estado de las transacciones.

---

## 🚀 Características

* Seguimiento en tiempo real de transacciones pendientes y minadas.
* Detección de transacciones descartadas y reemplazadas.
* Interfaz de usuario intuitiva para visualizar el estado de las transacciones.
* Integración con Alchemy Notify para recibir notificaciones.([docs.alchemy.com][1])

---

## 🧠 Fundamentos de las Transacciones en Ethereum

### ¿Qué es una transacción en Ethereum?

Una transacción en Ethereum es una instrucción firmada digitalmente enviada desde una cuenta para actualizar el estado de la red. Puede ser una transferencia de ETH, una interacción con un contrato inteligente o una implementación de contrato.

### Estados de las transacciones

1. **Pendiente (Pending):** La transacción ha sido enviada a la red pero aún no ha sido incluida en un bloque.
2. **Minada (Mined):** La transacción ha sido incluida en un bloque y confirmada por la red.
3. **Descartada (Dropped):** La transacción fue eliminada del mempool, posiblemente debido a una tarifa de gas insuficiente o un nonce incorrecto.
4. **Reemplazada (Replaced):** Una nueva transacción con el mismo nonce y una tarifa de gas más alta ha reemplazado a una anterior.

### ¿Qué es el mempool?

El mempool (memory pool) es el conjunto de transacciones pendientes que cada nodo mantiene antes de que sean incluidas en un bloque. Las transacciones con tarifas de gas más altas tienen prioridad para ser minadas.

### ¿Qué es un nonce?

El nonce es un contador que representa el número de transacciones enviadas desde una dirección. Asegura que cada transacción sea única y se procese en orden.

---

## 🛠️ Instalación y Uso

### Requisitos previos

* Node.js v14 o superior.
* Cuenta en Alchemy con una clave API.
* Cuenta en GitHub.

### Pasos de instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu_usuario/ethereum-transaction-tracker.git
   cd ethereum-transaction-tracker
   ```



2. **Instalar dependencias:**

   ```bash
   npm install
   ```



3. **Configurar variables de entorno:**

   Crea un archivo `.env` y añade tu clave API de Alchemy:

   ```env
   ALCHEMY_API_KEY=tu_clave_api
   ```



4. **Iniciar la aplicación:**

   ```bash
   npm start
   ```



---

## 📊 Ejemplo de Datos

Aquí tienes un conjunto de datos de ejemplo para probar la aplicación:

```json
[
  {
    "hash": "0xabc123...",
    "from": "0xSenderAddress",
    "to": "0xReceiverAddress",
    "value": "1000000000000000000",
    "gas": "21000",
    "gasPrice": "5000000000",
    "nonce": 1,
    "status": "pending"
  },
  {
    "hash": "0xdef456...",
    "from": "0xSenderAddress",
    "to": "0xReceiverAddress",
    "value": "2000000000000000000",
    "gas": "21000",
    "gasPrice": "6000000000",
    "nonce": 2,
    "status": "mined"
  }
]
```



