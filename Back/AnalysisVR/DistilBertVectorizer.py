import pandas as pd
import numpy as np
import torch

from sklearn.metrics.pairwise import cosine_similarity
from transformers import DistilBertTokenizer, DistilBertModel
from sklearn.preprocessing import normalize

class DistilBertVectorizer:
    model_cache = {}

    def __init__(self):
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-multilingual-cased')
        self.model = self.get_model()
        self.batch_size = 128

    def transform(self, texts):
        try:
            tokens = [self.tokenizer.encode(text, max_length=512, truncation=True) for text in texts]
            embeddings = [self.model(torch.tensor([token]).to(self.device))[0][0][0].detach().cpu().numpy() for token in tokens]
            return np.array(embeddings)
        except:
            print('Error in transform.')

    def process_batches(self, texts, batch_size):
        try:
            num_batches = len(texts) // batch_size + 1
            embeddings = []
            for i in range(num_batches):
                batch = texts[i * batch_size: (i + 1) * batch_size]
                batch_embeddings = self.transform(batch)
                embeddings.append(batch_embeddings)
        except:
            print('Error in process_batches.')
        return np.concatenate(embeddings)

    def get_model(self):
        try:
            model_name = 'distilbert-base-multilingual-cased'
            if model_name in self.model_cache:
                return self.model_cache[model_name]
            else:
                model = DistilBertModel.from_pretrained(model_name)
                self.model_cache[model_name] = model
                return model
        except:
            print('Error in get_model.')

    def generate_embeddings(self, texts):
        try:
            tokens = [self.tokenizer.encode(text, max_length=512, truncation=True) for text in texts]
            embeddings = []
            for token in tokens:
                token_tensor = torch.tensor([token]).to(self.device)
                with torch.no_grad():
                    outputs = self.model(token_tensor)
                embedding = outputs.last_hidden_state[:, 0, :].detach().cpu().numpy()
                embeddings.append(embedding)
            return np.array(embeddings)
        except:
            print('Error in generate_embeddings.')

    def main(self):
        try:
            try:
                resume_df = pd.read_csv('./Back/bd/tp_one_resume.csv')
                vacancies_df = pd.read_csv('./Back/bd/tp_all_vacancies.csv')
                vacancies_df = vacancies_df[:2000]
            except:
                print('Error : Ошибка при чтении file.csv.')
                return -1

            # на тот случай если мало мощностей
            vacancy_desc_embeddings = self.process_batches(vacancies_df['description'].tolist(), self.batch_size)
            resume_desc_embeddings = self.process_batches(resume_df['INF'].tolist(), self.batch_size)
            vacancy_title_embeddings = self.process_batches(vacancies_df['name'].tolist(), self.batch_size)
            resume_title_embeddings = self.process_batches(resume_df['name'].tolist(), self.batch_size)

            # на тот случай если достаточно мощностей и маленький сет
            # vacancy_desc_embeddings = self.generate_embeddings(vacancies_df['description'].tolist())
            # resume_desc_embeddings = self.generate_embeddings(resume_df['description'].tolist())
            # vacancy_title_embeddings = self.generate_embeddings(vacancies_df['name'].tolist())
            # resume_title_embeddings = self.generate_embeddings(resume_df['name'].tolist())

            alpha = 0.2
            vacancy_embeddings = alpha * normalize(vacancy_desc_embeddings) + (1 - alpha) * normalize(vacancy_title_embeddings)
            resume_embeddings = alpha * normalize(resume_desc_embeddings) + (1 - alpha) * normalize(resume_title_embeddings)
            cos_sim = cosine_similarity(resume_embeddings, vacancy_embeddings)
            top_vacancy_indices = cos_sim.argsort()[0][::-1][:10]
            top_vacancies = vacancies_df.loc[top_vacancy_indices].reset_index(drop=True)
            top_vacancies = top_vacancies.assign(similarity=cos_sim[0][top_vacancy_indices])

            print("Top 10 vacancies:")
            top_vacancies['resume_url'] = resume_df.get('link')[0]
            top_vacancies['tittle_resume'] = resume_df.get('name')[0]
            top_vacancies = top_vacancies[['id', 'name', 'similarity', 'tittle_resume', 'alternate_url', 'resume_url']]
            print(top_vacancies)
            top_vacancies = top_vacancies[['name', 'similarity', 'tittle_resume', 'alternate_url', 'resume_url']]
            # top_vacancies.to_csv('./AnalysisVR/bd_bot/distilbert.csv')
            top_vacancies.to_csv('./Front/bd/distilbert.csv')
            return top_vacancies
        except:
            print('Error : Ошибка при чтении main.')