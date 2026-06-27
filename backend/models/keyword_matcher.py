from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

class KeywordMatcher:
    def __init__(self):
        self.tech_skills = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node.js', 'express', 'django', 'flask', 'spring', 'asp.net', 'c#', 'c++',
            'go', 'rust', 'ruby', 'php', 'sql', 'postgresql', 'mysql', 'mongodb',
            'firebase', 'redis', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'jenkins', 'git', 'github', 'gitlab', 'machine learning', 'deep learning',
            'nlp', 'computer vision', 'tensorflow', 'pytorch', 'scikit-learn',
            'pandas', 'numpy', 'tableau', 'power bi', 'excel', 'agile', 'scrum'
        ]
        self.vectorizer = CountVectorizer(vocabulary=self.tech_skills, lowercase=True)
        
    def calculate_keyword_score(self, job_desc: str, resume_text: str) -> float:
        """Calculate keyword matching score"""
        try:
            # Vectorize both texts
            job_lower = job_desc.lower()
            resume_lower = resume_text.lower()
            
            job_vector = self.vectorizer.transform([job_lower]).toarray()
            resume_vector = self.vectorizer.transform([resume_lower]).toarray()
            
            # Count matching keywords
            job_keywords = set(np.where(job_vector[0] > 0)[0])
            resume_keywords = set(np.where(resume_vector[0] > 0)[0])
            
            if len(job_keywords) == 0:
                return 0.0
                
            matches = len(job_keywords.intersection(resume_keywords))
            total = len(job_keywords)
            
            return matches / total
        except Exception as e:
            print(f"Error in keyword matching: {e}")
            return 0.0