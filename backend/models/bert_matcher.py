from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class BERTMatcher:
    def __init__(self):
        print("Loading BERT model... (this may take a minute on first run)")
        # Using a smaller, faster model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("BERT model loaded successfully!")
        
    def get_embedding(self, text: str) -> np.ndarray:
        """Generate BERT embedding for text"""
        # Truncate long text
        if len(text) > 5000:
            text = text[:5000]
        return self.model.encode(text)
    
    def calculate_similarity(self, job_desc: str, resume_text: str) -> float:
        """Calculate cosine similarity between JD and resume"""
        try:
            job_embedding = self.get_embedding(job_desc)
            resume_embedding = self.get_embedding(resume_text)
            
            similarity = cosine_similarity(
                [job_embedding], 
                [resume_embedding]
            )[0][0]
            
            # Ensure value is between 0 and 1
            return max(0.0, min(1.0, float(similarity)))
        except Exception as e:
            print(f"Error in similarity calculation: {e}")
            return 0.0