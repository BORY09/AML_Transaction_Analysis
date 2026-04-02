import sqlite3
import pandas as pd

#1 Ładowanie danych z CSV
df_tx = pd.read_csv('../data/transactions.csv')
df_customers = pd.read_csv('../data/customers.csv')

#2 Połączenie z bazą danych SQLite
conn = sqlite3.connect('../data/bank_data.db')

#3 Wysyłanie surowych danych do bazy
df_tx.to_sql('transactions', conn, if_exists='replace', index=False)
df_customers.to_sql('customers', conn, if_exists='replace', index=False)

#4 Czyszczenie i analiza danych w SQL
query = """
SELECT 
    tx_id,
    customer_id,
    COALESCE(merchant, 'Brak danych') AS merchant_status,
    category
FROM transactions
WHERE amount > 50000 OR merchant IS NULL
ORDER BY amount DESC
"""

podejrzane_df = pd.read_sql_query(query, conn)

print("Raport podejrzanych transakcji (Puste dane lub wysokie kwoty):")
print(podejrzane_df.head(10))

# Zamykamy połączenie
conn.close()

import numpy as np

#1 obliczamy średnią i odchylenie standardowe dla kwot transakcji
mean_amount = df_tx['amount'].mean()
std_amount = df_tx['amount'].std()

#2 Definiujemy próg jako średnia + 3*odchylenie standardowe
threshold = mean_amount + 3 * std_amount

print(f"Średnia kwota: {mean_amount:.2f}, Odchylenie standardowe: {std_amount:.2f}, Próg anomalii: {threshold:.2f}")

#3 Dodajemy kolumnę z flagą anomalii
df_tx['z_score'] = (df_tx['amount'] - mean_amount) / std_amount
df_tx['is_anomaly'] =df_tx['z_score'].abs() > 3

#4 Sprawdzamy ile transakcji zostało oznaczonych jako anomalie
anomalies = df_tx[df_tx['is_anomaly'] == True]
print(f"Liczba transakcji oznaczonych jako anomalie: {len(anomalies)}")
print(anomalies[['amount', 'z_score']].head())

final_report = df_tx.merge(df_customers, on='customer_id', how='left')

final_report.to_csv('../data/final_report.csv', index=False)
print("Ostateczny raport zapisany jako final_report.csv")