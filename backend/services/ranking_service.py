from models.bert_matcher import BERTMatcher
from models.keyword_matcher import KeywordMatcher
from utils.ner_extractor import ResumeNER

class ResumeRanker:
    def __init__(self):
        print("Initializing Resume Ranker...")
        try:
            self.bert_matcher = BERTMatcher()
            self.keyword_matcher = KeywordMatcher()
            self.ner_extractor = ResumeNER()
            print("Resume Ranker ready!")
        except Exception as e:
            print(f"Error initializing: {e}")
            self.bert_matcher = None
            self.keyword_matcher = None
            self.ner_extractor = None
        
    def rank_resume(self, job_description: str, resume_text: str) -> dict:
        """Rank a single resume against job description"""
        try:
            # Default values in case of errors
            semantic_score = 0.5
            keyword_score = 0.5
            
            # 1. Semantic similarity (70% weight)
            if self.bert_matcher:
                try:
                    semantic_score = self.bert_matcher.calculate_similarity(
                        job_description, resume_text
                    )
                except Exception as e:
                    print(f"BERT error: {e}")
                    semantic_score = 0.5
            
            # 2. Keyword matching (30% weight)
            if self.keyword_matcher:
                try:
                    keyword_score = self.keyword_matcher.calculate_keyword_score(
                        job_description, resume_text
                    )
                except Exception as e:
                    print(f"Keyword error: {e}")
                    keyword_score = 0.5
            
            # 3. Combined score
            total_score = (0.7 * semantic_score) + (0.3 * keyword_score)
            
            # 4. Extract structured info
            extracted_info = {'SKILLS': [], 'NAME': ['Candidate']}
            if self.ner_extractor:
                try:
                    extracted_info = self.ner_extractor.extract_entities(resume_text)
                except Exception as e:
                    print(f"NER error: {e}")
            
            # Get candidate name
            candidate_name = "Candidate"
            if extracted_info.get('NAME') and len(extracted_info['NAME']) > 0:
                candidate_name = extracted_info['NAME'][0]
            
            return {
                'total_score': round(total_score * 100, 2),
                'semantic_score': round(semantic_score * 100, 2),
                'keyword_score': round(keyword_score * 100, 2),
                'extracted_skills': extracted_info.get('SKILLS', [])[:10],
                'extracted_experience': extracted_info.get('ORG', []),
                'candidate_name': candidate_name
            }
        except Exception as e:
            print(f"Error ranking resume: {e}")
            return {
                'total_score': 50.0,
                'semantic_score': 50.0,
                'keyword_score': 50.0,
                'extracted_skills': [],
                'extracted_experience': [],
                'candidate_name': 'Error'
            }
    
    def rank_multiple_resumes(self, job_description: str, resumes: list) -> list:
        """Rank multiple resumes and return sorted list"""
        results = []
        for resume in resumes:
            result = self.rank_resume(job_description, resume['text'])
            result['resume_id'] = resume['id']
            result['filename'] = resume['filename']
            results.append(result)
        
        return sorted(results, key=lambda x: x['total_score'], reverse=True)