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

Perfecto, aquí tienes un resumen claro y completo de **todo lo que hemos implementado en tu app**, listo para añadir al `README.md` del proyecto.

---

## 🧾 Descripción del proyecto

Esta aplicación permite visualizar y analizar transacciones simuladas en la red Ethereum, con un enfoque especial en la **detección de posibles comportamientos fraudulentos** usando reglas heurísticas y visualizaciones interactivas. 
ATENCION! He usado otro dataset, generado aleatoriamente por mí llamado "Transacciones_Simuladas_Ethereum.csv", ya que nos faltaban datos como irección del emisor, cantidad, tipo, gas usado, fecha, etc... Mi intención es usar también el original pero por la falta de tiempo, opté por una versión más comoda

## 🧩 Funcionalidades principales

### 🔍 Explorador de bloques

* Visualiza transacciones por bloque.
* Filtros avanzados: bloque, tipo de transacción (por EIP), emisor.
* Muestra información detallada: emisor, receptor, valor (ETH), gas, tipo, contrato, hash, fecha.

### ⚠️ Análisis de riesgo

* Detecta posibles transacciones fraudulentas basándose en:

  * Valor alto transferido (> 5 ETH)
  * Gas utilizado muy alto (> 250,000)
  * Despliegue de contratos
  * Tipos avanzados de transacción (EIP-4844: `0x3`, EIP-7702: `0x4`)
* Clasificación de riesgo: Ninguno, Bajo, Medio, Alto.
* Muestra justificación matemática de cada caso.
* Visualizaciones:

  * Gráfico de barras por nivel de riesgo
  * Gráfico de pastel por tipo de transacción

---

## 🧠 Análisis de Riesgo con IA

Este proyecto también incorpora un sistema de inteligencia artificial para analizar automáticamente el riesgo de fraude en las transacciones de Ethereum.

### 🔍 ¿Cómo funciona?

Se entrenó un modelo de clasificación basado en Random Forest con datos simulados. Las etiquetas de fraude fueron generadas usando reglas heurísticas, como:

- Transacciones con más de 2 ETH.
- Uso de más de 200,000 unidades de gas.
- Despliegue de contratos inteligentes.

El modelo considera variables como `value`, `gasUsed`, `contract_deploy`, codificaciones de direcciones y la hora de la transacción.

### 📦 Integración en la App

La app web muestra ahora dos evaluaciones de riesgo:

- **Riesgo (Reglas):** Basado en condiciones fijas interpretables.
- **Clasificación IA:** Basado en el modelo entrenado que generaliza patrones de riesgo.

Esto permite comparar el juicio humano basado en reglas con las predicciones automáticas del modelo de IA.

---

## ▶️ Cómo ejecutar

1. Clona o descarga este repositorio.
2. Instala dependencias:

```bash
pip install streamlit pandas matplotlib
```

3. Ejecuta la app:

```bash
streamlit run app.py
```

---

## 📚 Recursos y documentación

- [Documentación oficial de Alchemy: Understanding Transactions](https://www.alchemy.com/docs/understanding-transactions)[1]
- [Guía para enviar transacciones en Ethereum con Alchemy](https://docs.alchemy.com/docs/how-to-send-transactions-on-ethereum)[2]
- [Ethereum.org: Enviar transacciones usando Web3 y Alchemy](https://ethereum.org/es/developers/tutorials/sending-transactions-using-web3-and-alchemy/)[3]
- [Bit2Me Academy: ¿Qué es Alchemy?](https://academy.bit2me.com/que-es-alchemy/)[7]
