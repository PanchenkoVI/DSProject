# import string
# import ast
# import re
# import pandas as pd
# from nltk import SnowballStemmer, word_tokenize
# from nltk.corpus import stopwords
# from sklearn.metrics import precision_score, recall_score
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split, GridSearchCV
#
# snowball = SnowballStemmer(language="russian")
# russian_stop_words = stopwords.words("russian")
# english_stop_words = stopwords.words("english")
#
# import warnings
# warnings.filterwarnings('ignore')
#
# class TfidfVectorizerPipe:
#
#     def remove_html_tags(self, text):
#         clean = re.compile('<.*?>')
#         cleaned_text = re.sub(clean, '', text)
#         cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)
#         cleaned_text = re.sub(r'\b\w{1,2}\b', '', cleaned_text)
#         if cleaned_text.strip():
#             return cleaned_text
#         else:
#             return None
#         return cleaned_text
#
#     def token_sentence(self, sentence: str, remove_stop_words: bool = True):
#
#         tokens = word_tokenize(sentence, language="russian")
#         tokens = [self.remove_html_tags(item) for item in tokens if self.remove_html_tags(item)]
#         tokens = [i.lower() for i in tokens]
#         tokens = [i for i in tokens if i not in string.punctuation]
#         if remove_stop_words:
#             tokens = [i for i in tokens if i not in russian_stop_words and i not in english_stop_words]
#         tokens = [snowball.stem(i) for i in tokens]
#         return tokens
#
#     def main(self):
#         df = pd.read_csv('../bd/all_vacancies_old.csv')
#         df = df.fillna('')
#         df['description'] = df[['area', 'experience', 'schedule', 'employment', 'description', 'skills']] \
#             .apply(lambda x: ', '.join(set(x.dropna().astype(str))), axis=1)
#         df['professional_roles'] = df['professional_roles'].apply(ast.literal_eval)
#         df['CATEGORY'] = df['professional_roles'].apply(lambda x: x[0]['id'] if x else None)
#         df1 = df[['description', 'CATEGORY']].copy()
#         train_df, test_df = train_test_split(df1, test_size=500)
#
#         # print(test_df.shape)
#         # print(train_df.shape)
#         # print(test_df['CATEGORY'].value_counts())
#         # print(train_df['CATEGORY'].value_counts())
#
#         vectorizer = TfidfVectorizer(tokenizer=lambda x: self.token_sentence(x, remove_stop_words=True))
#         features = vectorizer.fit_transform(train_df["description"])
#         model = LogisticRegression(random_state=42)
#         model.fit(features, train_df["CATEGORY"])
#
#         model_pipline = Pipeline([
#             ("vectorizer", TfidfVectorizer(tokenizer=lambda x: self.token_sentence(x, remove_stop_words=True))),
#             ("model", LogisticRegression(random_state=42))
#         ])
#         model_pipline.fit(train_df['description'],train_df['CATEGORY'])
#         model_pipline.predict([''])
#
#         # precision_score(y_true=test_df["CATEGORY"], y_pred=model_pipeline.predict(test_df["description"]))
#         # recall_score(y_true=test_df["CATEGORY"], y_pred=model_pipeline.predict(test_df["description"]))
#
#         # prec, rec, thresholds = precision_recall_curve(y_true=test_df['CATEGORY'], probas_pred=model.pipline.predict_proba(test_df["description"])[:,1])
#
#         grid_pipeline = Pipeline ([
#             ("vectorizer",  TfidfVectorizer(tokenizer=lambda x: self.token_sentence(x, remove_stop_words=True))),
#             ("model",
#              GridSearchCV(
#                  LogisticRegression(random_state=42),
#                  param_grid={'C': [0.1,1.,10.]},
#                  cv=3,
#                  verbose=4))])
#         grid_pipeline.fit(train_df['description'], train_df['CATEGORY'])
#
#         return model.predict(features[0]), train_df["description"].iloc[0]
#
# if __name__ == "__main__":
#     tvp = TfidfVectorizerPipe()
#     print(tvp.main())
