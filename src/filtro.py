import pandas as pd

# Caminho do seu CSV
df = pd.read_csv("C:/Users/gmara/Documents/GitHub/FERPlus/data/fer2013new.csv")

# Emoções que você quer excluir
emotions_to_remove = ["happiness", "sadness", "contempt"]

# Força os dados das colunas pra int (caso haja texto ou NaN)
for col in emotions_to_remove:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# Limite de votos permitidos nas emoções indesejadas
tolerancia = 5

# Filtra as linhas
df_filtered = df[df[emotions_to_remove].sum(axis=1) <= tolerancia].copy()

# Remove as colunas indesejadas
df_filtered.drop(columns=emotions_to_remove, inplace=True)

# Salva o novo CSV
df_filtered.to_csv("fer2013_cleaned.csv", index=False)

print(f"Imagens mantidas: {len(df_filtered)} de {len(df)}")
