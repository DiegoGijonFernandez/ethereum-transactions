# 📦 Ethereum Transaction Tracker

Ethereum Transaction Tracker es una herramienta diseñada para monitorear, analizar y visualizar el ciclo de vida de las transacciones en la red de Ethereum. Permite identificar el estado de cada transacción (pendiente, minada, descartada o reemplazada), evaluar su riesgo y visualizar explicaciones claras sobre cada caso. Utiliza la API de Alchemy y su Mempool Watcher para ofrecer información en tiempo real y una experiencia de usuario intuitiva.

---

## 🚀 Características principales

- **Seguimiento en tiempo real** de transacciones pendientes y minadas.
- **Detección de transacciones descartadas y reemplazadas** en la red.
- **Interfaz visual sencilla** para explorar el estado y los detalles de cada transacción.
- **Integración con Alchemy Notify** para recibir alertas automáticas sobre cambios de estado.
- **Evaluación de riesgo** de cada transacción (bajo, medio, alto) y explicación de los criterios utilizados.
- **Soporte para datasets simulados o reales**, facilitando pruebas y análisis personalizados.

---

## 🧠 Fundamentos de las transacciones en Ethereum

### ¿Qué es una transacción en Ethereum?

Una transacción en Ethereum es una instrucción firmada digitalmente enviada desde una cuenta, que puede transferir ETH, interactuar con contratos inteligentes o desplegar nuevos contratos. Cada transacción es fundamental para modificar el estado de la blockchain y puede contener datos adicionales para ejecutar funciones específicas en contratos inteligentes[1][2].

### Estados posibles de una transacción

- **Pendiente (Pending):** Enviada a la red, esperando inclusión en un bloque.
- **Minada (Mined):** Confirmada e incluida en un bloque.
- **Descartada (Dropped):** Eliminada del mempool, generalmente por errores de nonce o gas insuficiente.
- **Reemplazada (Replaced):** Sustituida por otra transacción con el mismo nonce y mayor tarifa de gas[1].

### Campos clave de una transacción

- **from:** Dirección del emisor.
- **to:** Dirección del destinatario (o contrato).
- **value:** Cantidad transferida (en Wei).
- **gas y gasPrice:** Recursos y coste de ejecución.
- **nonce:** Número de transacciones previas del emisor, garantiza unicidad y orden[1][2].
- **data:** Información adicional, especialmente relevante en interacciones con contratos inteligentes.

### El mempool y el ciclo de vida

El mempool es el espacio donde las transacciones esperan antes de ser minadas. Los mineros priorizan aquellas con mayores tarifas de gas. El ciclo de vida de una transacción puede consultarse y analizarse en tiempo real usando herramientas como las APIs de Alchemy[1][2][7].

---

## 📊 Sobre el dataset utilizado

Para el análisis y clasificación de riesgo, este proyecto emplea un dataset estructurado con variables agregadas por dirección y periodo temporal, que incluye:

- **blockNumber, confirmations, fecha y hora**
- **mean_value_received, variance_value_received, total_received:** Estadísticas sobre los valores recibidos.
- **total_tx_sent, total_tx_sent_malicious, total_tx_sent_unique:** Totales y unicidad de transacciones enviadas, incluyendo aquellas marcadas como maliciosas.
- **total_tx_received_malicious_unique:** Número de transacciones maliciosas recibidas.
- **Fraud:** Etiqueta binaria que indica si la actividad está asociada a fraude.

Este tipo de dataset, con variables agregadas y etiqueta de fraude, es ideal para la detección de patrones, entrenamiento de modelos de clasificación de riesgo y visualización clara en la interfaz. Permite mostrar, por ejemplo, si una dirección presenta alta varianza en valores recibidos, actividad inusual o historial de transacciones maliciosas, facilitando la explicación de cada nivel de riesgo.

---

## 🛠️ Instalación y uso

### Requisitos previos

- Node.js v14 o superior.
- Cuenta en Alchemy con clave API.
- Cuenta en GitHub.

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

## 📚 Recursos y documentación

- [Documentación oficial de Alchemy: Understanding Transactions](https://www.alchemy.com/docs/understanding-transactions)[1]
- [Guía para enviar transacciones en Ethereum con Alchemy](https://docs.alchemy.com/docs/how-to-send-transactions-on-ethereum)[2]
- [Ethereum.org: Enviar transacciones usando Web3 y Alchemy](https://ethereum.org/es/developers/tutorials/sending-transactions-using-web3-and-alchemy/)[3]
- [Bit2Me Academy: ¿Qué es Alchemy?](https://academy.bit2me.com/que-es-alchemy/)[7]

---

## 📝 Notas adicionales

- Alchemy no almacena tus claves privadas, por lo que siempre debes firmar tus transacciones antes de enviarlas[2][3].
- El sistema de evaluación de riesgo puede personalizarse mediante reglas o modelos de machine learning, usando las variables del dataset.
- La aplicación es apta tanto para pruebas con datos simulados como para monitoreo en tiempo real de la red principal de Ethereum.

