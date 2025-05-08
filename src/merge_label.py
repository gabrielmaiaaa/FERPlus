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

# Nomes das emoções em ordem (usado como subpastas)
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

    # Cria pastas de destino por usage e emoção
    for usage_folder in folder_names.values():
        for emotion in emotion_labels:
            os.makedirs(os.path.join(base_folder, usage_folder, emotion), exist_ok=True)

    # Carrega labels do FER+
    ferplus_dict = {}
    with open(ferplus_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # pula header
        for row in reader:
            filename = row[0]
            usage = row[1]
            votes = list(map(int, row[3:]))  # colunas de voto
            if len(votes) != len(emotion_labels):
                continue  # segurança contra entradas incompletas
            max_vote = max(votes)
            if max_vote == 0:
                continue  # nenhuma emoção clara
            emotion_index = votes.index(max_vote)
            emotion_label = emotion_labels[emotion_index]
            ferplus_dict[filename] = (usage, emotion_label)

    # Gera imagens com base nas labels válidas
    with open(fer_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # pula header
        for i, row in enumerate(reader):
            emotion, pixels, usage = row
            filename = f"fer{i:07d}.png"
            if filename in ferplus_dict:
                usage, emotion_label = ferplus_dict[filename]
                folder = os.path.join(base_folder, folder_names[usage], emotion_label)
                image = str_to_image(pixels)
                image.save(os.path.join(folder, filename), compress_level=0)

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
