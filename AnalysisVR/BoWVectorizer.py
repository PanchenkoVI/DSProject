import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import normalize

import warnings
warnings.filterwarnings('ignore')

class BoWVectorizerCustom(BaseEstimator, TransformerMixin):
    def __init__(self, max_features=1000):
        self.max_features = max_features
        self.vectorizer = CountVectorizer(max_features=self.max_features)
        
    def fit(self, X, y=None):
        self.vectorizer.fit(X)
        return self

    def transform(self, X):
        return self.vectorizer.transform(X)

    def fit_transform(self, X, y=None):
        return self.vectorizer.fit_transform(X)

    def main(self):
        try:
            resume_df = pd.read_csv('./bd/tp_one_resume.csv')
            vacancies_df = pd.read_csv('./bd/tp_all_vacancies.csv')
        except:
            print('Error : Ошибка при чтении file.csv.')
            return -1

        vacancy_desc_bow = self.fit_transform(vacancies_df['description'])
        resume_desc_bow = self.transform(resume_df['description'])

        vacancy_title_bow = self.fit_transform(vacancies_df['name'])
        resume_title_bow = self.transform(resume_df['name'])

        alpha = 0.5
        vacancy_bow = alpha * normalize(vacancy_desc_bow) + (1 - alpha) * normalize(vacancy_title_bow)
        resume_bow = alpha * normalize(resume_desc_bow) + (1 - alpha) * normalize(resume_title_bow)

        cos_sim_bow = cosine_similarity(resume_bow, vacancy_bow)

        top_vacancy_indices_bow = cos_sim_bow.argsort()[0][::-1][:10]
        top_vacancies_bow = vacancies_df.loc[top_vacancy_indices_bow].reset_index(drop=True)
        top_vacancies_bow = top_vacancies_bow.assign(similarity=cos_sim_bow[0][top_vacancy_indices_bow])

        # вычисление схожести названий вакансии и резюме
        title_cos_sim_bow = cosine_similarity(resume_title_bow, vacancy_title_bow)
        top_vacancies_bow['title_similarity'] = title_cos_sim_bow[0][top_vacancy_indices_bow]

        print("Top 10 vacancies:")
        top_vacancies_bow['resume_url'] = resume_df.get('link')[0]
        top_vacancies_bow['tittle_resume'] = resume_df.get('name')[0]
        print(top_vacancies_bow[['id', 'name', 'similarity', 'tittle_resume','title_similarity', 'alternate_url', 'resume_url']])
        return top_vacancies_bow[['id', 'name', 'similarity', 'tittle_resume','title_similarity', 'alternate_url', 'resume_url']]
