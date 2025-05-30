
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

# Cargar el dataset
df = pd.read_csv("C:/Users/diego/Downloads/analisis-transacciones-ethereum/data/Transacciones_Simuladas_Ethereum.csv")

# Etiquetado por reglas heurísticas
def etiquetar_fraude(df):
    condiciones = [
        (df['value'] > 2),
        (df['gasUsed'] > 200000),
        (df['contract_deploy'] == 1),
    ]
    puntajes = [2, 1, 1]
    df['riesgo_score'] = sum(cond.astype(int) * peso for cond, peso in zip(condiciones, puntajes))
    df['fraude'] = (df['riesgo_score'] >= 2).astype(int)
    return df

df = etiquetar_fraude(df)

# Preprocesamiento
le_from = LabelEncoder()
le_to = LabelEncoder()
df['from_enc'] = le_from.fit_transform(df['from'])
df['to_enc'] = le_to.fit_transform(df['to'])
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour

# Variables predictoras y etiqueta
features = ['value', 'gasUsed', 'contract_deploy', 'from_enc', 'to_enc', 'hour']
X = df[features]
y = df['fraude']

# Modelo
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Validación cruzada
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(clf, X, y, cv=cv, scoring='f1')

print("F1-score promedio:", scores.mean())
print("Desviación estándar:", scores.std())

# Entrenamiento final y guardado del modelo
clf.fit(X, y)
joblib.dump(clf, "modelo_riesgo_fraude.pkl")
print("Modelo entrenado y guardado como modelo_riesgo_fraude.pkl")
