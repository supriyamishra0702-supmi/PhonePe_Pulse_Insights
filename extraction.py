import os
import json
import pandas as pd
import sqlite3

# Define the root path to your cloned data
root_path = "phonepe_pulse_data/data/aggregated"

def extract_all():
    conn = sqlite3.connect("phonepe_pulse.db")
    
    # --- 1. TRANSACTIONS ---
    print("🚀 Processing Transactions...")
    path_t = os.path.join(root_path, "transaction/country/india/state")
    t_cols = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [], 'Transaction_amount': []}
    for state in os.listdir(path_t):
        s_path = os.path.join(path_t, state)
        for yr in os.listdir(s_path):
            y_path = os.path.join(s_path, yr)
            for file in os.listdir(y_path):
                with open(os.path.join(y_path, file), 'r') as f:
                    data = json.load(f)
                    for z in data['data']['transactionData']:
                        t_cols['State'].append(state.replace('-', ' ').title())
                        t_cols['Year'].append(int(yr))
                        t_cols['Quarter'].append(int(file.strip('.json')))
                        t_cols['Transaction_type'].append(z['name'])
                        t_cols['Transaction_count'].append(z['paymentInstruments'][0]['count'])
                        t_cols['Transaction_amount'].append(z['paymentInstruments'][0]['amount'])
    pd.DataFrame(t_cols).to_sql('aggregated_transaction', conn, if_exists='replace', index=False)

    # --- 2. USERS (CASE STUDY 2) ---
    print("📱 Processing User Device Data...")
    path_u = os.path.join(root_path, "user/country/india/state")
    u_cols = {'State': [], 'Year': [], 'Quarter': [], 'Brand': [], 'Count': [], 'Percentage': []}
    for state in os.listdir(path_u):
        s_path = os.path.join(path_u, state)
        for yr in os.listdir(s_path):
            y_path = os.path.join(s_path, yr)
            for file in os.listdir(y_path):
                with open(os.path.join(y_path, file), 'r') as f:
                    data = json.load(f)
                    # Some files might have empty device data
                    device_data = data['data'].get('usersByDevice')
                    if device_data:
                        for entry in device_data:
                            u_cols['State'].append(state.replace('-', ' ').title())
                            u_cols['Year'].append(int(yr))
                            u_cols['Quarter'].append(int(file.strip('.json')))
                            u_cols['Brand'].append(entry['brand'])
                            u_cols['Count'].append(entry['count'])
                            u_cols['Percentage'].append(entry['percentage'])
    pd.DataFrame(u_cols).to_sql('aggregated_user', conn, if_exists='replace', index=False)

    # --- 3. INSURANCE (CASE STUDY 3) ---
    print("🛡️ Processing Insurance...")
    path_i = os.path.join(root_path, "insurance/country/india/state")
    i_cols = {'State': [], 'Year': [], 'Quarter': [], 'Count': [], 'Amount': []}
    for state in os.listdir(path_i):
        s_path = os.path.join(path_i, state)
        for yr in os.listdir(s_path):
            y_path = os.path.join(s_path, yr)
            for file in os.listdir(y_path):
                with open(os.path.join(y_path, file), 'r') as f:
                    data = json.load(f)
                    for z in data['data']['transactionData']:
                        i_cols['State'].append(state.replace('-', ' ').title())
                        i_cols['Year'].append(int(yr))
                        i_cols['Quarter'].append(int(file.strip('.json')))
                        i_cols['Count'].append(z['paymentInstruments'][0]['count'])
                        i_cols['Amount'].append(z['paymentInstruments'][0]['amount'])
    pd.DataFrame(i_cols).to_sql('aggregated_insurance', conn, if_exists='replace', index=False)
    
    conn.close()
    print("✅ SUCCESS: All 3 tables are now populated!")

if __name__ == "__main__":
    extract_all()
