from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

class ResumeNER:
    def __init__(self):
        print("Loading NER model... (this may take a minute on first run)")
        self.model_name = "dslim/bert-base-NER"  # Simpler model that works well
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_name)
        print("NER model loaded successfully!")
        
    def extract_entities(self, text: str):
        """Extract entities from resume text"""
        # Truncate long text
        if len(text) > 1000:
            text = text[:1000]
            
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=2)
        
        entities = {
            'SKILLS': [],
            'EXPERIENCE': [],
            'NAME': [],
            'ORG': []  # Organizations/Companies
        }
        
        current_entity = None
        
        for i, pred in enumerate(predictions[0]):
            label = self.model.config.id2label[pred.item()]
            token = self.tokenizer.convert_ids_to_tokens([inputs['input_ids'][0][i].item()])[0]
            
            # Skip special tokens
            if token in ['[CLS]', '[SEP]', '[PAD]']:
                continue
                
            if label.startswith('B-'):
                if current_entity:
                    if current_entity['type'] == 'PER':
                        entities['NAME'].append(current_entity['text'])
                    elif current_entity['type'] == 'ORG':
                        entities['ORG'].append(current_entity['text'])
                current_entity = {
                    'type': label[2:],
                    'text': token
                }
            elif label.startswith('I-') and current_entity:
                current_entity['text'] += ' ' + token
            else:
                if current_entity:
                    if current_entity['type'] == 'PER':
                        entities['NAME'].append(current_entity['text'])
                    elif current_entity['type'] == 'ORG':
                        entities['ORG'].append(current_entity['text'])
                current_entity = None
        
        # Add some common tech skills detection (simple keyword matching)
        tech_skills = ['python', 'java', 'javascript', 'react', 'node', 'sql', 
                      'mongodb', 'aws', 'docker', 'kubernetes', 'tensorflow',
                      'pytorch', 'flask', 'django', 'git', 'linux']
        
        text_lower = text.lower()
        for skill in tech_skills:
            if skill in text_lower:
                entities['SKILLS'].append(skill)
        
        # Remove duplicates
        entities['SKILLS'] = list(set(entities['SKILLS']))
        entities['NAME'] = list(set(entities['NAME']))
        entities['ORG'] = list(set(entities['ORG']))
        
        return entities