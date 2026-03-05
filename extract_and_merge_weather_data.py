import pandas as pd
import os
from pathlib import Path

data_dir = Path('data/dados_meteorologicos')

csv_files = sorted(data_dir.glob('*.csv'))

print(f"Encontrados {len(csv_files)} arquivos CSV")

all_data = []

for i, file_path in enumerate(csv_files, 1):
    print(f"Processando arquivo {i}/{len(csv_files)}: {file_path.name}")
    
    try:
        df = pd.read_csv(file_path, sep=';', skiprows=10, decimal=',')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            metadata = {}
            for line in lines[:9]:  
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        df['Estacao'] = metadata.get('Codigo Estacao', '')
        df['Nome_Estacao'] = metadata.get('Nome', '')
        df['Latitude'] = metadata.get('Latitude', '')
        df['Longitude'] = metadata.get('Longitude', '')
        df['Altitude'] = metadata.get('Altitude', '')
        
        all_data.append(df)
        
    except Exception as e:
        print(f"  Erro ao processar {file_path.name}: {e}")

if all_data:
    merged_df = pd.concat(all_data, ignore_index=True)
    
    merged_df.columns = merged_df.columns.str.strip()
    
    print(f"\nDados combinados com sucesso!")
    print(f"Dimensões finais: {merged_df.shape}")
    print(f"\nColunas: {list(merged_df.columns)}")
    print(f"\nPrimeiras linhas:\n{merged_df.head()}")
    
    output_file = 'data/dados_meteorologicos_completos.csv'
    merged_df.to_csv(output_file, sep=';', index=False, encoding='utf-8')
    print(f"\nArquivo salvo como: {output_file}")
    
    try:
        excel_file = 'data/dados_meteorologicos_completos.xlsx'
        merged_df.to_excel(excel_file, index=False)
        print(f"Arquivo Excel salvo como: {excel_file}")
    except ImportError:
        print("(Para salvar em Excel, instale openpyxl: pip install openpyxl)")
else:
    print("Nenhum arquivo foi processado com sucesso.")
