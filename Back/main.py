import numpy as np
import pandas as pd
import argparse
import re
import os

from Vacancies.VacancyLoader import VacancyLoader
from Resume.ResumeOne import Resume as resume_one
from Resume.ResumeALL import Resume as resume_all

from Preprocessor.TextPreprocessor import TextPreprocessor

from AnalysisVR.TfidfVectorizer import TfidfVectorizerCustom
from AnalysisVR.BoWVectorizer import BoWVectorizerCustom
from AnalysisVR.Word2VecVectorizer import Word2VecVectorizer
from AnalysisVR.DistilBertVectorizer import DistilBertVectorizer

class Main:

    def __init__(self):
        self.str_help = "156 : BI-аналитик, аналитик данных,\n160 : DevOps-инженер,\n10  : Аналитик,\n12  : Арт-директор, креативный директор,\n150 : Бизнес-аналитик,\n25  : Гейм-дизайнер,\n\
165 : Дата-сайентист,\n34  : Дизайнер, художник,\n36  : Директор по информационным технологиям (CIO),\n73  : Менеджер продукта,\n96  : Программист, разработчик,\n164 : Продуктовый аналитик,\n\
104 : Руководитель группы разработки,\n157 : Руководитель отдела аналитики,\n107 : Руководитель проектов,\n112 : Сетевой инженер,\n113 : Системный администратор,\n148 : Системный аналитик,\n\
114 : Системный инженер,\n116 : Специалист по информационной безопасности,\n121 : Специалист технической поддержки',\n124 : Тестировщик,\n125 : Технический директор (CTO),\n126 : Технический писатель,\n\
16  : Аудитор,\n154 : Брокер,\n18  : Бухгалтер\nor 0 для выхода"
        self.vacancy_loader = np.nan
        self.vacancy_resume = np.nan
        self.vacancy_resume_all = np.nan
        self.args = np.nan

    def load_vacancy_all(self):
        try:
            while True:
                print("Введите номера категорий через запятую:")
                inp = input()
                numbers = inp.split(',')
                for num in numbers:
                    if not str(num).strip().isdigit():
                        print(
                            f"Ошибка! Введена неправильная строка чисел.\n Необходимо написать через запятую номера категорий из следующего списка:\n{self.str_help}")
                        return -20
                else:
                    num = list(map(int, numbers))
                    if 0 in num:
                        return 1
                    numeric_list = list(set(num))
                    numbers = re.findall(r'\d+', self.str_help)
                    numbers = [int(num) for num in numbers]
                    if all(elem in numbers for elem in numeric_list):
                        self.vacancy_loader = VacancyLoader(numeric_list)
                        self.vacancy_loader.main()
                        print('Вакансии успешно сохранились.')
                        return 1
                    else:
                        print(f"Ошибка! Введена неправильная строка чисел.")
        except:
            print('Error: Ошибка в load_vacancy_all.')

    def load_resume_one(self):
        try:
            while True:
                print('Введите ссылку на резюме с сайта gorodrabot.ru:')
                # https://gorodrabot.ru/resume/5334430 java
                url_str = str(input())
                if '-' in url_str:
                    return 0
                match = re.match(r'^(https?://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w.-]*)*/?$', url_str)
                if match:
                    self.vacancy_resume = resume_one(f'{url_str}')
                    self.vacancy_resume = self.vacancy_resume.main()
                    print('Резюме успешно сохранилось.')
                    return 1
                else:
                    print("\n\nError : Вы указали не корректную ссылку на резюме.\nВведите правильную ссылку или введите '-' для выхода.")
        except:
            print('Error: Ошибка в load_resume_one.')

    def load_resume_more(self):
        while True:
            try:
                print('Введите должность для сайта gorodrabot.ru:')
                str_job = str(input())
                print('Введите количество страниц сайта, с которых будет скачиваться резюме:')
                page_range_max = int(input())
                print('Введите количество потоков для скачивания:')
                max_workers = int(input())
                self.vacancy_resume_all = resume_all(str_job, page_range_max=page_range_max, max_workers=max_workers)
                self.vacancy_resume_all.main()
                print('Резюме успешно сохранились.')
                return 1
            except:
                print('Error: Ошибка в load_resume_more.')
                return 0

    def text_preprocessor(self):
        while True:
            try:
                print('Введите\n1-Для одного резюме\n2-Для обработки большого количества резюме в файле\n3-Для множества вакансий\nИли свой путь к файлу.')
                file_name = input()
                if file_name == '1':
                    file_name = 'one_resume.csv'
                elif file_name == '2':
                    file_name = 'all_resume.csv'
                elif file_name == '3':
                    file_name = 'all_vacancies.csv'
                file_path = os.path.join('./Back/bd/', file_name)
                if os.path.isfile(file_path):
                    if (file_name == 'one_resume.csv' or file_name == 'all_resume.csv'):
                        preprocessor = TextPreprocessor()
                        df = pd.read_csv('./Back/bd/'+file_name)
                        df1 = preprocessor.process_df(df, 'INF')
                        if file_name == 'one_resume.csv':
                            df1.to_csv('./Back/bd/tp_one_resume.csv', index=False)
                        else:
                            df1.to_csv('./Back/bd/tp_more_resume.csv', index=False)
                        print('Предобработка прошла успешно.')
                    elif file_name == 'all_vacancies.csv':
                        preprocessor = TextPreprocessor()
                        df = pd.read_csv('./Back/bd/' + file_name)
                        df['description'] = df[
                            ['area', 'experience', 'schedule', 'employment', 'description', 'skills']] \
                            .apply(lambda x: ', '.join(set(x.dropna().astype(str))), axis=1)
                        df1 = preprocessor.process_df(df, 'description')
                        df1.to_csv('./Back/bd/tp_all_vacancies.csv', index=False)
                elif (file_name != 'one_resume.csv' and file_name != 'all_resume.csv' and file_name != 'all_vacancies.csv'):
                    print('Будет реализовано в следующих версиях проекта.')
                else:
                    print("Файл не существует.")
                    pass
                return 1
            except:
                print('Error: Ошибка в text_preprocessor')

    def load_model(self):
        try:
            print('Выберете модель для обучения:\n1-TF-IDF\n2-BOW\n3-Word2Vec\n4-BERT\n')
            model = input()
            if model == '1':
                try:
                    tfdf = TfidfVectorizerCustom(max_features=2200)
                    tfdf.main()
                except:
                    print('Error: Допущена ошибка в модели tfidf.')
            elif model == '2':
                try:
                    bow = BoWVectorizerCustom(max_features=1000)
                    bow.main()
                except:
                    print('Error: Допущена ошибка в модели bow.')
            elif model == '3':
                try:
                    w2v = Word2VecVectorizer()
                    w2v.main()
                except:
                    print('Error: Допущена ошибка в модели w2v.')
            elif model == '4':
                try:
                    dbert = DistilBertVectorizer()
                    dbert.main()
                except:
                    print('Error: Допущена ошибка в модели dbert.')
        except:
            print('Error: Допущена ошибка в model.')

    def check_values(self):
        if self.args.load_vacancy == 'all':
            self.load_vacancy_all()
        if self.args.load_resume == 'one':
            self.load_resume_one()
        if self.args.load_resume == 'more':
            self.load_resume_more()
        if self.args.text_preprocessor == 'tp':
            self.text_preprocessor()
        if self.args.load_model == 'model':
            self.load_model()

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--load_vacancy', default='Null', type=str,
                            help="Command for downloading vacancies from the site hh.ru.")
        parser.add_argument('--load_resume', default='Null', type=str,
                            help="Command for downloading resumes from gorodrabot.ru.")
        parser.add_argument('--text_preprocessor', default='Null', type=str,help="Word processing.")
        parser.add_argument('--load_model', default='Null', type=str, help="Command for training a machine learning model.")
        self.args = parser.parse_args()
        self.check_values()

if __name__ == "__main__":
    try:
        main_instance = Main()
        main_instance.main()
    except:
        exit(-1)