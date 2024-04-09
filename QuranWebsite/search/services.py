# services.py in your Django app 'search'

from sentence_transformers import SentenceTransformer, util
import joblib
import numpy as np
import pandas as pd

def load_model_and_embeddings(model_path, embeddings_path):
    model = SentenceTransformer(model_path)
    df = joblib.load(embeddings_path)
    return model, df

def find_top_related_verses(input_text, model, df, top_k=5):
    input_embedding = model.encode(input_text, convert_to_tensor=True)
    similarities = df['embedding'].apply(lambda emb: util.pytorch_cos_sim(input_embedding, emb).item())
    top_indices = np.argsort(-similarities)[:top_k]
    return df.iloc[top_indices]
