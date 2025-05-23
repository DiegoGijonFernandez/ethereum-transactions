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

## 🧠 Enriquecimiento del Dataset Ethereum Transactions

He estado trabajando con un **dataset de transacciones de Ethereum**, específicamente un conjunto de datos **agregados por bloque**. Pero ese dataset original **no incluía detalles técnicos clave** que nos pueden ayudar a entender mejor el comportamiento de las transacciones en esos bloques.

Quería detectar o analizar comportamientos maliciosos o sospechosos en Ethereum. Para eso, necesitabas enriquecer el dataset con **características técnicas** más modernas, como: 

* **Tipos de transacciones**: Diferentes versiones como legacy (`0x0`), EIP-1559 (`0x2`), etc.
* **Despliegues de contratos inteligentes**: Si en ese bloque se ha creado un nuevo contrato (`tx.to is None`).

Esto es útil porque algunos tipos de fraude (como scam tokens) implican desplegar contratos sospechosos, o usar nuevas formas de transacción para ocultar actividad.


###  Escribimos un script en Python llamado "modifificardataset.py" que:

1. **Lee el dataset original** (`data.txt`).
2. **Conecta a Ethereum** usando la API de Alchemy.
3. Por cada bloque (`blockNumber`):

   * Descarga todas las transacciones completas.
   * Detecta el tipo de cada transacción (`tx.type`).

     * Si es `None` → legacy (`0x0`)
     * Si es `2` → EIP-1559 (`0x2`), etc (y así sumando).
   * Detecta si despliega un contrato (`tx.to is None`).
4. Calcula proporciones por tipo y cuántas crean contratos.
5. Añade esas columnas nuevas al dataset.
6. Guarda el resultado en un nuevo archivo CSV.

---

## 📄 ¿Qué hace el código exactamente?


### 🔹 Conectar con Ethereum

```python
w3 = Web3(Web3.HTTPProvider(f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"))
```

Nos conectamos a Ethereum a través del nodo de Alchemy usando tu API key. Yo usé la que me generó mi proyecto personal.

---

### 🔹 Leer el dataset original

```python
df = pd.read_csv(INPUT_FILE, sep="\t")
```

Leemos el archivo `.txt` que contiene los bloques y sus estadísticas.

---

### 🔹 Para cada bloque, obtener nuevas características

```python
block = w3.eth.get_block(block_number, full_transactions=True)
```

Conseguimos todas las transacciones de ese bloque.

---

### 🔹 Detectar tipos de transacción

```python
tx_types = [tx.type if tx.type is not None else 0 for tx in txs]
type_counts = Counter(tx_types)
```

Cada transacción puede ser de tipo `0` (legacy), `1` (access list), `2` (EIP-1559), etc. Contamos cuántas hay de cada tipo.

---

### 🔹 Detectar creación de contratos

```python
deploy_count = sum(1 for tx in txs if tx.to is None)
```

Si `tx.to` es `None`, es un contrato nuevo.

---

### 🔹 Calcular proporciones y añadirlas al dataset

```python
return {
    "tx_type_0x0_ratio": type_counts.get(0, 0) / total,
    ...
    "contract_deploy_tx_ratio": deploy_count / total
}
```

Creamos columnas nuevas con esa información.

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
