import numpy as np
import pandas as pd

from gensim.models import Word2Vec
from gensim.matutils import unitvec
from sklearn.metrics.pairwise import cosine_similarity

class Word2VecVectorizer:

    def __init__(self, size=100, window=50, min_count=1, workers=20, epochs=50):
        self.size = size
        self.window = window
        self.min_count = min_count
        self.workers = workers
        self.epochs = epochs
        self.model = None

    def fit(self, X, y=None):
        self.model = Word2Vec(X, vector_size=self.size, window=self.window, min_count=self.min_count,
                              workers=self.workers, epochs=self.epochs, compute_loss=True)
        return self

    def transform(self, X):
        vectors = []
        for tokens in X:
            vec = np.zeros(self.size)
            n_words = 0
            for token in tokens:
                if token in self.model.wv:
                    vec += self.model.wv[token]
                    n_words += 1
            if n_words > 0:
                vec /= n_words
            vectors.append(vec)
        return np.array(vectors)

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

    def main(self):
        try:
            resume_df = pd.read_csv('./Back/bd/tp_one_resume.csv')
            vacancies_df = pd.read_csv('./Back/bd/tp_all_vacancies.csv')
            vacancies_df = vacancies_df[:2000]
        except:
            print('Error : Ошибка при чтении file.csv.')
            return -1

        vacancy_desc_w2v = self.fit_transform(vacancies_df['description'])
        resume_desc_w2v = self.transform(resume_df['INF'])

        alpha = 0.7
        desc_vectors = unitvec(vacancy_desc_w2v)
        title_vectors = unitvec(self.transform(vacancies_df['name']))
        vacancy_w2v = alpha * desc_vectors + (1 - alpha) * title_vectors

        desc_vectors = unitvec(resume_desc_w2v)
        title_vectors = unitvec(self.transform(resume_df['name']))
        resume_w2v = alpha * desc_vectors + (1 - alpha) * title_vectors

        cos_sim = cosine_similarity(resume_w2v, vacancy_w2v)
        top_vacancy_indices = cos_sim.argsort()[0][::-1][:10]

        top_vacancies = vacancies_df.loc[top_vacancy_indices].reset_index(drop=True)
        top_vacancies = top_vacancies.assign(similarity=cos_sim[0][top_vacancy_indices])

        print("Top 10 vacancies:")
        top_vacancies['resume_url'] = resume_df.get('link')[0]
        top_vacancies['tittle_resume'] = resume_df.get('name')[0]
        top_vacancies = top_vacancies[['id', 'name', 'similarity', 'tittle_resume', 'alternate_url', 'resume_url']]
        print(top_vacancies)
        top_vacancies = top_vacancies[['name', 'similarity', 'tittle_resume', 'alternate_url', 'resume_url']]
        # top_vacancies.to_csv('./AnalysisVR/bd_bot/word2vec.csv')
        top_vacancies.to_csv('./Front/bd/word2vec.csv')
        return top_vacancies