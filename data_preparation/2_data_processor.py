import pandas as pd
import numpy as np

def main():
    print("Loading data/raw_bbm_data.csv...")
    df = pd.read_csv('data/raw_bbm_data.csv')
    df = df.sort_values('Tahun').reset_index(drop=True)
    
    df['Tahun'] = df['Tahun'].astype(int)
    df['Harga_Premium_Nominal'] = pd.to_numeric(df['Harga_Premium_Nominal'], errors='coerce')
    df['Harga_Solar_Nominal'] = pd.to_numeric(df['Harga_Solar_Nominal'], errors='coerce')
    df['Harga_Pertamax_Nominal'] = pd.to_numeric(df['Harga_Pertamax_Nominal'], errors='coerce')
    
    idx_2025 = df.index[df['Tahun'] == 2025]
    if not idx_2025.empty:
        df.loc[idx_2025, 'Ringkasan_Event'] = "Harga subsidi dipertahankan stabil selama masa transisi pemerintahan baru."
        df.loc[idx_2025, 'Harga_Premium_Nominal'] = 10000
        df.loc[idx_2025, 'Harga_Solar_Nominal'] = 6800
        df.loc[idx_2025, 'Harga_Pertamax_Nominal'] = 12950
        
    idx_2026 = df.index[df['Tahun'] == 2026]
    if not idx_2026.empty:
        df.loc[idx_2026, 'Ringkasan_Event'] = "Stabilitas harga BBM subsidi di tengah dinamika geopolitik global."
        df.loc[idx_2026, 'Harga_Premium_Nominal'] = 10000
        df.loc[idx_2026, 'Harga_Solar_Nominal'] = 6800
        df.loc[idx_2026, 'Harga_Pertamax_Nominal'] = 12950
    
    df['CPI'] = df['CPI'].interpolate(method='linear').ffill()
    
    anchor_cpi = df.loc[df['Tahun'] == df['Tahun'].max(), 'CPI'].values[0]
    
    df['Harga_Premium_Real'] = df['Harga_Premium_Nominal'] * (anchor_cpi / df['CPI'])
    df['Harga_Solar_Real'] = df['Harga_Solar_Nominal'] * (anchor_cpi / df['CPI'])
    df['Harga_Pertamax_Real'] = df['Harga_Pertamax_Nominal'] * (anchor_cpi / df['CPI'])
    
    df['Harga_Premium_Real'] = df['Harga_Premium_Real'].round(2)
    df['Harga_Solar_Real'] = df['Harga_Solar_Real'].round(2)
    df['Harga_Pertamax_Real'] = df['Harga_Pertamax_Real'].round(2)
    
    output_path = 'data/clean_bbm_data.csv'
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()
