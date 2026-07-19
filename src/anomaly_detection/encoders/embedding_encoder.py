from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin

import pandas as pd


class EmbeddingEncoder(BaseEstimator, TransformerMixin):
    """Embeds and reduces string attributes."""

    def __init__(self, model_path, n_components=32):
        self.model_path = model_path
        self.n_components = n_components

    def fit(self, X, y=None):
        self.model = SentenceTransformer(self.model_path)

        texts = pd.Series(X.squeeze()).fillna("").tolist()

        embeddings = self.model.encode(texts, convert_to_numpy=True)

        self.scaler = StandardScaler()
        embeddings = self.scaler.fit_transform(embeddings)

        self.pca = PCA(self.n_components)
        self.pca.fit(embeddings)

        return self

    def transform(self, X):
        texts = pd.Series(X.squeeze()).fillna("").tolist()

        embeddings = self.model.encode(texts)
        embeddings = self.scaler.transform(embeddings)
        return self.pca.transform(embeddings)
