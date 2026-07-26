from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin

import pandas as pd
import numpy as np


class EmbeddingEncoder(BaseEstimator, TransformerMixin):
    """Embeds and reduces string attributes."""

    def __init__(self, model_path, n_components=32):
        self.model_path = model_path
        self.n_components = n_components

    def fit(self, X, y=None):
        self.model = SentenceTransformer(self.model_path)

        texts = pd.Series(X.squeeze()).fillna("").astype(str)
        unique_texts = texts.unique()

        embeddings = self.model.encode(
            unique_texts.tolist(),
            convert_to_numpy=True,
            show_progress_bar=True,
            batch_size=256,
        )

        self.scaler = StandardScaler()
        embeddings = self.scaler.fit_transform(embeddings)

        self.pca = PCA(self.n_components)
        self.pca.fit(embeddings)

        return self

    def transform(self, X):
        texts = pd.Series(X.squeeze()).fillna("").astype(str)

        unique_texts = texts.unique()

        unique_embeddings = self.model.encode(
            unique_texts.tolist(), convert_to_numpy=True
        )

        unique_embeddings = self.scaler.transform(unique_embeddings)
        unique_embeddings = self.pca.transform(unique_embeddings)

        lookup = dict(zip(unique_texts, unique_embeddings))

        return np.array([lookup[t] for t in texts])
