import pandas as pd
from faker import Faker
import random
import numpy as np

fake = Faker('pl_PL')

# 1. Tworzenie klientów
def create_customers(n=1000):
    customers = []
    for _ in range(n):
        customers.append({
            'customer_id': fake.unique.random_int(min=100000, max=999999),
            'name': fake.name(),
            'age': random.randint(18, 85),
            'city': fake.city(),
            'account_type': random.choice(['Standard', 'Premium', 'Gold'])
        })
    return pd.DataFrame(customers)

# 2. Tworzenie transakcji
def create_transactions(customers_df, n=10000):
    transactions = []
    customer_ids = customers_df['customer_id'].values
    
    for _ in range(n):
        # Normalna transakcja
        amount = round(random.uniform(5.0, 5000.0), 2)
        timestamp = fake.date_time_this_year()
        
        # WSTRZYKIWANIE ANOMALII (Celowe błędy do wykrycia)
        rand_val = random.random()
        if rand_val < 0.02:  # 2% to skrajnie wysokie kwoty
            amount = round(random.uniform(50000, 1000000), 2)
        elif rand_val < 0.05: # 3% to transakcje bez nazwy odbiorcy
            merchant = None
        else:
            merchant = fake.company()

        transactions.append({
            'tx_id': fake.unique.uuid4(),
            'customer_id': random.choice(customer_ids),
            'amount': amount,
            'timestamp': timestamp,
            'merchant': merchant,
            'category': random.choice(['Food', 'Tech', 'Travel', 'Health', 'Finance'])
        })
    return pd.DataFrame(transactions)

# Generowanie i zapis
df_customers = create_customers()
df_tx = create_transactions(df_customers)

df_customers.to_csv('../data/customers.csv', index=False)
df_tx.to_csv('../data/transactions.csv', index=False)

print("Pliki wygenerowane: customers.csv oraz transactions.csv")