import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics.pairwise import cosine_similarity
# import joblib
import warnings
warnings.filterwarnings('ignore')

class TfidfVectorizerCustom(BaseEstimator, TransformerMixin,):

    def __init__(self, max_features=2200):
        self.vectorizer = TfidfVectorizer(max_features=max_features)

    def fit(self, X, y=None):
        self.vectorizer.fit(X)
        return self

    def transform(self, X):
        return self.vectorizer.transform(X)

    def fit_transform(self, X, y=None):
        return self.vectorizer.fit_transform(X)

    def main(self):
        try:
            resume_df = pd.read_csv('./Back/bd/tp_one_resume.csv')
            vacancies_df = pd.read_csv('./Back/bd/tp_all_vacancies.csv')
        except:
            print('Error : Ошибка при чтении file.csv.')
            return -1

        # TF-IDF векторизатор с настройкой весов
        vacancy_desc_tfidf = self.fit_transform(vacancies_df['description'])
        resume_desc_tfidf = self.transform(resume_df['INF'])

        vacancy_title_tfidf = self.fit_transform(vacancies_df['name'])
        resume_title_tfidf = self.transform(resume_df['name'])

        # настройка веса для названия резюме и вакансий
        alpha = 0.5
        vacancy_tfidf = alpha * vacancy_desc_tfidf + (1 - alpha) * vacancy_title_tfidf
        resume_tfidf = alpha * resume_desc_tfidf + (1 - alpha) * resume_title_tfidf

        # косинусная близость между резюме и вакансиями
        cos_sim = cosine_similarity(resume_tfidf, vacancy_tfidf)

        top_vacancy_indices = cos_sim.argsort()[0][::-1][:10]
        top_vacancies = vacancies_df.loc[top_vacancy_indices].reset_index(drop=True)
        top_vacancies = top_vacancies.assign(similarity=cos_sim[0][top_vacancy_indices])

        # вычисление схожести названий вакансии и резюме
        title_cos_sim = cosine_similarity(resume_title_tfidf, vacancy_title_tfidf)
        top_vacancies['title_similarity'] = title_cos_sim[0][top_vacancy_indices]

        print("Top 10 vacancies:")
        top_vacancies['resume_url'] = resume_df.get('link')[0]
        top_vacancies['tittle_resume'] = resume_df.get('name')[0]
        top_vacancies = top_vacancies[['id', 'name', 'similarity', 'tittle_resume','title_similarity', 'alternate_url', 'resume_url']]
        print(top_vacancies)
        top_vacancies = top_vacancies[['name', 'similarity', 'tittle_resume', 'alternate_url', 'resume_url']]
        # top_vacancies.to_csv('./AnalysisVR/bd_bot/tfidf.csv')
        top_vacancies.to_csv('./Front/bd/tfidf.csv')
        # joblib.dump(self,'../Models/tfidf_model.pkl')
        return top_vacancies

# if __name__ == "__main__":
#     tvp = TfidfVectorizerCustom()
#     top_vacancies=tvp.main()
#     print(top_vacancies)
    # joblib.dump(top_vacancies, '../Models/tfidf_model.pkl')
