from sentence_transformers import SentenceTransformer
from pickle import dump as pkl_dump
from argparse import ArgumentParser
from datetime import datetime
from tqdm import tqdm
import json

# Initialize the faster Sentence-Transformer model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')  # 768 dimensions# 768 dimensions


def load_data(data_fl):
    """
    Load data from the JSON file into a list of conversations
    
    Args:
    data_fl: str, path to the JSON file containing the data
    
    Returns:
    iiitp_data_lst: list, list of conversation texts
    """
    with open(data_fl, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [entry['content'].replace('\n', ' ') for entry in data if entry.get('content')]

def generate_embeddings(data_lst, batch_size=32):
    """
    Generate embeddings for the list of conversation texts

    Args:
    data_lst: list, list of conversation texts
    batch_size: int, number of texts to process in each batch

    Returns:
    embeddings: list, list of embeddings
    """
    embeddings = []
    for i in tqdm(range(0, len(data_lst), batch_size)):
        batch_texts = data_lst[i:i + batch_size]
        
        # Encode texts with Sentence-Transformers model
        batch_embeddings = model.encode(batch_texts, batch_size=batch_size, show_progress_bar=True)
        
        # Append each embedding to the embeddings list
        embeddings.extend(batch_embeddings)
    return embeddings

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--data_fl', type=str, help='Path to the JSON file containing the translated data', default='translated_data.json')
    args = parser.parse_args()
    embeddings_fl = 'iiitp_embeddings.pkl'

    # Load data
    start1 = datetime.now()
    print(f"\n{'='*50}\nLoading data from {args.data_fl}...")
    iiitp_data_lst = load_data(args.data_fl)
    print('Data loaded successfully')

    # Generate embeddings
    print('\nGenerating embeddings...')
    embeddings = generate_embeddings(iiitp_data_lst, batch_size=32)
    print('Embeddings generated successfully')

    # Save embeddings as a pickle file
    with open(embeddings_fl, 'wb') as f:
        pkl_dump(embeddings, f)

    print(f'\nSuccessfully stored embeddings into {embeddings_fl} in {(datetime.now() - start1).seconds} seconds')
    print('='*50, '\n')
