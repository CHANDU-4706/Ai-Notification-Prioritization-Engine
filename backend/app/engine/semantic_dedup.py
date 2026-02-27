from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from app.models import NotificationEvent
from typing import List, Optional

class SemanticDeduplicator:
    def __init__(self):
        # Using a small, fast model for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384 # Dimension for all-MiniLM-L6-v2
        self.index = faiss.IndexFlatL2(self.dimension)
        self.history_ids = []
        self.history_texts = []

    def is_duplicate(self, event: NotificationEvent, threshold: float = 0.6) -> Optional[str]:
        if not self.history_texts:
            return None
        
        # Encode and Normalize new embedding
        new_embedding = self.model.encode([event.message])
        faiss.normalize_L2(np.array(new_embedding).astype('float32'))
        
        # FAISS search
        distances, indices = self.index.search(np.array(new_embedding).astype('float32'), 1)
        
        if len(indices[0]) > 0 and indices[0][0] != -1:
            best_idx = indices[0][0]
            dist = distances[0][0]
            
            # Since vectors are normalized, L2 dist squared is 2(1-cos_sim)
            # A distance < 0.6 is quite similar.
            if dist < threshold:
                return self.history_texts[best_idx]
                
        return None

    def add_to_history(self, event: NotificationEvent):
        embedding = self.model.encode([event.message])
        faiss.normalize_L2(np.array(embedding).astype('float32'))
        self.index.add(np.array(embedding).astype('float32'))
        self.history_ids.append(event.id)
        self.history_texts.append(event.message)
