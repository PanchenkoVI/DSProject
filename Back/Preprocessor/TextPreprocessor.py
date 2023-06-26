import re
from typing import List
import pandas as pd
from pymystem3 import Mystem
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from html import unescape

import warnings
warnings.filterwarnings('ignore')

class TextPreprocessor:
    def __init__(self):
        self.mystem = Mystem()
        self.stop_words_ru = stopwords.words("russian")
        self.stop_words_en = stopwords.words("english")

    def preprocess_text(self, text: str) -> str:
        # удаление HTML-тегов
        text = unescape(text)
        text = re.sub(r"<.*?>", "", text)
        # удаление HTML-entities
        text = re.sub(r"&\w+;", "", text)
        # удаление ссылок
        text = re.sub(r"http\S+", "", text)
        # удаление специальных символов
        text = re.sub(r"[^a-zA-Zа-яА-Я0-9]+", " ", text)
        # токенизация и приведение к нижнему регистру
        tokens = word_tokenize(text.lower())
        # удаление стоп-слов
        tokens = self.remove_stop_words(tokens)
        # стемминг
        tokens = self.stem_words(tokens)
        # объединение токенов обратно в текст
        text = " ".join(tokens)
        return text

    def remove_stop_words(self, tokens: List[str]) -> List[str]:
        tokens_filtered = [token for token in tokens if token not in self.stop_words_ru and token not in self.stop_words_en]
        return tokens_filtered

    def stem_words(self, tokens: List[str]) -> List[str]:
        lemmas = [self.mystem.lemmatize(token)[0] for token in tokens]
        return lemmas

    def process_df(self, df: pd.DataFrame, text_col: str) -> pd.DataFrame:
        df_processed = df.copy()
        df_processed[text_col] = df_processed[text_col].apply(self.preprocess_text)
        return df_processed