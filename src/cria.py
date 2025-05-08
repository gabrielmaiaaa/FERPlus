import os
import shutil
import pandas as pd

# Caminho pro CSV filtrado
csv_path = "C:/Users/gmara/Documents/GitHub/FERPlus/src/fer2013_cleaned.csv"
# Caminho das imagens já geradas
original_images_dir = "C:/Users/gmara/Documents/GitHub/FERPlus/images"
# Novo diretório de saída
output_dir = "C:/Users/gmara/Documents/GitHub/FERPlus/FER2013Cleaned"

# Emoções correspondentes (ajuste se necessário)
emotion_labels = [
    "neutral", "surprise", "anger", "disgust", "fear", "unknown", "NF"
]

# Lê o CSV filtrado
df = pd.read_csv(csv_path)

# Garante que a pasta de saída exista
os.makedirs(output_dir, exist_ok=True)

def get_emotion_label(row):
    """Retorna a emoção com mais votos na linha."""
    votes = row[emotion_labels].values
    max_index = votes.argmax()
    return emotion_labels[max_index]

# Cria as subpastas e move as imagens
for idx, row in df.iterrows():
    emotion = get_emotion_label(row)
    usage = row["usage"].lower()  # Deve ser "train", "publictest" ou "privatetest"

    # Padroniza o nome da pasta de destino
    if usage == "publictest":
        split = "valid"
    elif usage == "privatetest":
        split = "test"
    else:
        split = "train"

    dest_folder = os.path.join(output_dir, split, emotion)
    os.makedirs(dest_folder, exist_ok=True)

    # Nome do arquivo da imagem (já está no CSV)
    filename = row["filename"]
    source_path = os.path.join(original_images_dir, split.upper(), filename)
    dest_path = os.path.join(dest_folder, filename)

    if os.path.exists(source_path):
        shutil.copy2(source_path, dest_path)
    else:
        print(f"Imagem não encontrada: {source_path}")

print("Organização finalizada com sucesso!")
