import pandas as pd 
from web3 import Web3
from collections import Counter
from tqdm import tqdm
import time

# CONFIGURACIÓN
ALCHEMY_API_KEY = "DiSaYeAziqFt_zi7tutYIdHaYgQZSrFE"  # Sustituye si en tu caso usas otra clave
INPUT_FILE = "C:/Users/diego/Downloads/analisis-transacciones-ethereum/data/data.txt"
OUTPUT_FILE = "ETFD_Dataset_enriched.csv"

# CONEXIÓN A ETHEREUM 
w3 = Web3(Web3.HTTPProvider(f"https://eth-mainnet.g.alchemy.com/v2/DiSaYeAziqFt_zi7tutYIdHaYgQZSrFE"))

# DATASET ORIGINAL 
df = pd.read_csv(INPUT_FILE, sep="\t")

# FUNCIÓN PARA OBTENER FEATURES DEL BLOQUE
def get_block_features(block_number):
    try:
        block = w3.eth.get_block(int(block_number), full_transactions=True)
        txs = block.transactions
        total = len(txs)

        # Tipos de transacción (como enteros)
        tx_types = [tx.type if tx.type is not None else 0 for tx in txs]
        type_counts = Counter(tx_types)

        # Conteo de despliegues de contrato
        deploy_count = sum(1 for tx in txs if tx.to is None)

        # DEBUG 
        print(f"Bloque {block_number} → tipos: {dict(type_counts)}, contract deploys: {deploy_count}")

        return {
            "tx_type_0x0_ratio": type_counts.get(0, 0) / total,
            "tx_type_0x1_ratio": type_counts.get(1, 0) / total,
            "tx_type_0x2_ratio": type_counts.get(2, 0) / total,
            "tx_type_0x3_ratio": type_counts.get(3, 0) / total,
            "tx_type_0x4_ratio": type_counts.get(4, 0) / total,
            "contract_deploy_tx_count": deploy_count,
            "contract_deploy_tx_ratio": deploy_count / total
        }

    except Exception as e:
        print(f"Error en bloque {block_number}: {e}")
        return {
            "tx_type_0x0_ratio": None,
            "tx_type_0x1_ratio": None,
            "tx_type_0x2_ratio": None,
            "tx_type_0x3_ratio": None,
            "tx_type_0x4_ratio": None,
            "contract_deploy_tx_count": None,
            "contract_deploy_tx_ratio": None
        }

#  APLICAR A TODOS LOS BLOQUES 
print("Consultando bloques de Ethereum...")
features = []
for block_number in tqdm(df["blockNumber"]):
    features.append(get_block_features(block_number))
    time.sleep(0.2)  # Para evitar rate limit

# CREAR DATAFRAME DE FEATURES 
features_df = pd.DataFrame(features)

# UNIR AL DATASET ORIGINAL 
df_enriched = pd.concat([df.reset_index(drop=True), features_df], axis=1)

# GUARDAR RESULTADO FINAL 
df_enriched.to_csv(OUTPUT_FILE, index=False)
print(f"Dataset enriquecido guardado como: {OUTPUT_FILE}")
