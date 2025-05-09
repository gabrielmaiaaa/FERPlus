import os
import csv
import argparse
import numpy as np
from PIL import Image

# Mapeia usage para pasta principal
folder_names = {
    'Training': 'FER2013Train',
    'PublicTest': 'FER2013Valid',
    'PrivateTest': 'FER2013Test'
}

# Nomes das emoções em ordem (deve corresponder às colunas no CSV)
emotion_labels = [
    'neutral', 'happiness', 'surprise', 'sadness', 'anger',
    'disgust', 'fear', 'contempt', 'unknown', 'NF'
]

def str_to_image(image_blob):
    ''' Converte blob de string em imagem PIL '''
    image_string = image_blob.split(' ')
    image_data = np.asarray(image_string, dtype=np.uint8).reshape(48, 48)
    return Image.fromarray(image_data)

def main(base_folder, fer_path, ferplus_path):
    print("Start generating FER+ images with emotion folders.")

    # Verifica/Cria a estrutura de pastas completa
    for usage_folder in folder_names.values():
        for emotion in emotion_labels:
            folder_path = os.path.join(base_folder, usage_folder, emotion)
            try:
                os.makedirs(folder_path, exist_ok=True)
                print(f"Created directory: {folder_path}")
            except Exception as e:
                print(f"Error creating {folder_path}: {e}")

    # Carrega labels do FER+
    ferplus_dict = {}
    with open(ferplus_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Pega o header para verificar colunas
        
        # Verifica se as colunas estão na ordem esperada
        print("CSV Header:", header)
        
        for row in reader:
            if len(row) < 12:  # Verifica se tem todas as colunas
                continue
                
            filename = row[0]
            usage = row[1]
            
            # Pega os votos (colunas 3 a 12)
            votes = list(map(int, row[3:13]))  
            
            max_vote = max(votes)
            if max_vote == 0:
                continue  # nenhuma emoção clara
                
            emotion_index = votes.index(max_vote)
            emotion_label = emotion_labels[emotion_index]
            ferplus_dict[filename] = (usage, emotion_label)

    print(f"Total valid labels loaded: {len(ferplus_dict)}")

    # Gera imagens com base nas labels válidas
    with open(fer_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # pula header
        for i, row in enumerate(reader):
            if len(row) < 3:
                continue
                
            emotion, pixels, usage = row[0], row[1], row[2]
            filename = f"fer{i:07d}.png"
            
            if filename in ferplus_dict:
                usage, emotion_label = ferplus_dict[filename]
                folder = os.path.join(base_folder, folder_names[usage], emotion_label)
                
                try:
                    image = str_to_image(pixels)
                    image_path = os.path.join(folder, filename)
                    image.save(image_path, compress_level=0)
                    print(f"Saved: {image_path}")
                except Exception as e:
                    print(f"Error saving {filename}: {e}")

    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--base_folder", type=str, required=True,
                        help="Base folder containing training/validation/testing folders.")
    parser.add_argument("-fer", "--fer_path", type=str, required=True,
                        help="Path to the original fer2013.csv file.")
    parser.add_argument("-ferplus", "--ferplus_path", type=str, required=True,
                        help="Path to the new fer2013new.csv file.")
    args = parser.parse_args()
    main(args.base_folder, args.fer_path, args.ferplus_path)