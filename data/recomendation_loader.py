import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors

# 1. Adquisición de Datos
# Suponiendo que tienes un archivo CSV con el nombre 'Groceries_dataset.csv'
df = pd.read_csv('data/Groceries_dataset.csv')

# 2. Limpieza de Datos
# Visualiza los primeros registros
# print(df.head())

# Verifica la cantidad de valores nulos en cada columna
# print(df.isnull().sum())

# Elimina filas con valores nulos
df.dropna(inplace=True)

# Asegúrate de que la columna 'Date' sea del tipo datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

# 3. Análisis Exploratorio de Datos (EDA)
def print_graphics():
    # Distribución de productos comprados
    product_counts = df['itemDescription'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=product_counts.index[:10], y=product_counts.values[:10])
    plt.xticks(rotation=45)
    plt.title('Top 10 Productos Comprados')
    plt.xlabel('Producto')
    plt.ylabel('Cantidad Comprada')
    plt.show()

    # Distribución de compras por fecha
    df['Date'].dt.to_period('M').value_counts().sort_index().plot(kind='bar', figsize=(12, 6))
    plt.title('Compras por Mes')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad de Compras')
    plt.xticks(rotation=45)
    plt.show()

# 4. Preprocesamiento de Datos
# Convertir descripciones de productos en códigos numéricos
label_encoder = LabelEncoder()
df['itemEncoded'] = label_encoder.fit_transform(df['itemDescription'])

# 5. Modelado: Implementación de un modelo de recomendación
# Usando K-Nearest Neighbors para un sistema de recomendación basado en productos
# Creando una tabla de pivot para la matriz de compras
basket = (df.groupby(['Member_number', 'itemEncoded'])['itemEncoded']
          .count().unstack().reset_index().fillna(0)
          .set_index('Member_number'))

# Convertir a 1 (comprado) y 0 (no comprado)
basket = basket.applymap(lambda x: 1 if x > 0 else 0)

# Dividir el conjunto de datos
X_train, X_test = train_test_split(basket, test_size=0.2, random_state=42)

# Entrenar el modelo de K-Nearest Neighbors
model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(X_train)

# Función para hacer recomendaciones
def recommend_products(member_number, n_recommendations=5):
    # Verifica si el número de miembro existe en el índice
    if member_number not in basket.index:
        print(f"El número de miembro {member_number} no se encuentra en el índice.")
        return []
    
    member_index = basket.index.get_loc(member_number)
    distances, indices = model.kneighbors(X_train.iloc[member_index, :].values.reshape(1, -1), n_neighbors=n_recommendations + 1)
    
    # Recuperar productos comprados por el cliente
    recommended_indices = indices.flatten()[1:]  # Ignorar el primero, que es el mismo cliente
    recommendations = []
    for i in recommended_indices:
        product_indexes = X_train.iloc[i].to_numpy().nonzero()[0]
        recommended_products = label_encoder.inverse_transform(product_indexes)
        recommendations.extend(recommended_products)
    return recommendations[:n_recommendations]

# Ejemplo de uso de la función de recomendación
print(recommend_products(1808, 5))
