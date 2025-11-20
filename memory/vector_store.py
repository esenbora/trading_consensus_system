import faiss
import numpy as np
import os
import pickle
from config import Config

class VectorStore:
    def __init__(self):
        self.index_path = Config.VECTOR_DB_PATH
        self.dimension = 768 # Assuming standard embedding size
        self.index = None
        self.metadata = [] # To store actual text/context associated with vectors
        self._load_or_create_index()

    def _load_or_create_index(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            # Load metadata if exists (simplified for now)
            if os.path.exists(self.index_path + ".meta"):
                with open(self.index_path + ".meta", 'rb') as f:
                    self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)

    def add_memory(self, vector, text_context):
        """Adds a new memory vector and its context."""
        if len(vector) != self.dimension:
            raise ValueError("Vector dimension mismatch")
        
        np_vector = np.array([vector], dtype='float32')
        self.index.add(np_vector)
        self.metadata.append(text_context)
        self._save_index()

    def search_memory(self, query_vector, k=3):
        """Searches for similar memories."""
        if self.index.ntotal == 0:
            return []
            
        np_vector = np.array([query_vector], dtype='float32')
        distances, indices = self.index.search(np_vector, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append({
                    "context": self.metadata[idx],
                    "distance": float(distances[0][i])
                })
        return results

    def _save_index(self):
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + ".meta", 'wb') as f:
            pickle.dump(self.metadata, f)
