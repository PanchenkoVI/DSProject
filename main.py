import numpy as np
import pandas as pd
import argparse
import re

from Vacancies.VacancyLoader import VacancyLoader
from Resume.ResumeOne import Resume as resume_one
from Resume.ResumeALL import Resume as resume_all

from Preprocessor.TextPreprocessor import TextPreprocessor

from AnalysisVR.TfidfVectorizer import TfidfVectorizerCustom
from AnalysisVR.BoWVectorizer import BoWVectorizerCustom
from AnalysisVR.Word2VecVectorizer import Word2VecVectorizer
# from AnalysisVR.DistilBertVectorizer import DistilBertVectorizer

from RESTService import RESTService

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
                num = map(int, numbers)
                if 0 in num:
                    exit(1)
                numeric_list = set(num)
                numbers = re.findall(r'\d+', self.str_help)
                numbers = [int(num) for num in numbers]
                if numeric_list == set(numbers):
                    self.vacancy_loader = VacancyLoader(numeric_list)
                    self.vacancy_loader.main()
                    return 1
                else:
                    print(
                        f'Таких категорий вакансий нет. {self.str_help}\n\nНеобходимо написать через запятую номера категорий из вышеуказанного списка.')
                    continue

    def load_resume_one(self):
        while True:
            print('Введите ссылку на резюме с сайта gorodrabot.ru:')
            # https://gorodrabot.ru/resume/5334430 java
            url_str = str(input())
            if 'exit' in url_str:
                exit(1)
            match = re.match(r'^(https?://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w.-]*)*/?$', url_str)
            if match:
                self.vacancy_resume = resume_one(f'{url_str}')
                self.vacancy_resume = self.vacancy_resume.main()
                print('Резюме успешно сохранилось.')
                return 1
            else:
                print(
                    "Вы указали не корректную ссылку на резюме.\nВведите правильную ссылку или введите\'exit\' для выхода.")
                # return -20

    def load_resume_more(self):
        while True:
            try:
                print('Введите должности через запятую для сайта gorodrabot.ru:')
                str_job = list(set(input().split(',')))
                print('Введите количество страниц с которых скачивать резюме:')
                max_workers = int(input())
                print(max_workers, str_job)
                self.vacancy_resume_all = resume_all(str_job, page_range_max=2, max_workers=max_workers)
                self.vacancy_resume_all.main()
                print('Резюме успешно сохранились.')
                return 1
                break
            except:
                print('Error: Ошибка в load_resume_more.')
                return -20

    def text_preprocessor_one_resume(self):
        while True:
            try:
                preprocessor = TextPreprocessor()
                df_one = pd.read_csv('./bd/one_resume.csv')
                df_one['description'] = df_one[
                    ['achievements', 'city', 'experience', 'education', 'schedule', 'about', 'info']] \
                    .apply(lambda x: ', '.join(set(x.dropna().astype(str))), axis=1)
                df_one_res = preprocessor.process_df(df_one, 'description')
                df_one_res.to_csv('./bd/tp_one_resume.csv', index=False)
                df_one_res['description'][0]
                print('Предобработка прошла успешно.')
                return 1
            except:
                print('Error: Ошибка в text_preprocessor_one_resume.')
                return -20

    def text_preprocessor_more_resumes(self):
        while True:
            try:
                preprocessor = TextPreprocessor()
                df1 = pd.read_csv('./bd/all_resume.csv')
                df1['description'] = df1[
                    ['name', 'achievements', 'city', 'experience', 'education', 'schedule', 'about', 'info']] \
                    .apply(lambda x: ', '.join(set(x.dropna().astype(str))), axis=1)
                df_all_res = preprocessor.process_df(df1, 'description')
                df_all_res.to_csv('./bd/tp_all_resume.csv', index=False)
                print('Предобработка прошла успешно.')
                return 1
            except:
                print('Error: Ошибка в text_preprocessor_more_resumes.')
                return -20

    def text_preprocessor_vacancyes(self):
        while True:
            try:
                preprocessor = TextPreprocessor()
                df = pd.read_csv('./bd/all_vacancies.csv')
                df['description'] = df[['area', 'experience', 'schedule', 'employment', 'description', 'skills']] \
                    .apply(lambda x: ', '.join(set(x.dropna().astype(str))), axis=1)
                df_all_vacancies = preprocessor.process_df(df, 'description')
                df_all_vacancies.to_csv('./bd/tp_all_vacancies.csv', index=False)
                print('Предобработка прошла успешно.')
                return 1
            except:
                print('Error: Ошибка в text_preprocessor_vacancyes.')
                return -20

    def check_values(self):
        flag = 0
        if self.args.load_vacancy == 'all':
            flag = flag + self.load_vacancy_all()
        if self.args.load_resume == 'one':
            flag = flag + self.load_resume_one()
        if self.args.load_resume == 'more':
            flag = flag + self.load_resume_more()
        if self.args.text_preprocessor == 'one_resume':
            flag = flag + self.text_preprocessor_one_resume()
        if self.args.text_preprocessor == 'more_resumes':
            flag = flag + self.text_preprocessor_more_resumes()
        if self.args.text_preprocessor == 'vacancyes':
            flag = flag + self.text_preprocessor_vacancyes()
        if self.args.load_model == 'tfidf':
            try:
                tfdf = TfidfVectorizerCustom(max_features=2200)
                tfdf.main()
                flag = flag + 1
            except:
                print('Error: Допущена ошибка в модели tfidf.')
                flag = -20
        if self.args.load_model == 'bow':
            try:
                bow = BoWVectorizerCustom(max_features=1000)
                bow.main()
                flag = flag + 1
            except:
                print('Error: Допущена ошибка в модели bow.')
                flag = -20
        if self.args.load_model == 'w2v':
            try:
                w2v = Word2VecVectorizer()
                w2v.main()
                flag = flag + 1
            except:
                print('Error: Допущена ошибка в модели w2v.')
                flag = -20
        # if self.args.load_model == 'dbert':
        #     try:
        #         dbert = DistilBertVectorizer()
        #         dbert.main()
        #         flag = flag + 1
        #     except:
        #         print('Error: Допущена ошибка в модели dbert.')
        #         flag = -20

        # if self.args.rest_api == 'now':
            # try:
            # rest_api = RESTService()
                # rest_api.run()
                # flag = flag + 1
            # except:
            #     print('Error: Была допущена ошибка в rest_api.')
            #     flag = -20
        if flag == 0:
            print("Неверный аргумент командной строки.")
            print("Введите:\n\t'python3 main.py --load_vacancy all' - если хотете скачать вакансии с сайта hh.ru.")
            print("\t'python3 main.py --load_resume one' - если хотите скачать только одно резюме.")
            print("\t'python3 main.py --load_resume more' - если хотите скачать больше одного резюме.")
            print("\t'python3 main.py --text_preprocessor one_resume' - если хотите скачать больше одного резюме.")
            print("\t'python3 main.py --text_preprocessor more_resumes' - если хотите скачать больше одного резюме.")
            print("\t'python3 main.py --text_preprocessor vacancyes' - если хотите скачать больше одного резюме.")
        elif flag < 0:
            print('Ранее была допущена ошибка. Не все вызванные шаги были выполнены. Необходимо исправить ошибки.')

    def parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--load_vacancy', default='Null', type=str, help="Specify the category of the vacancy from the site hh.ru.")
        parser.add_argument('--load_resume', default='Null', type=str, help="Enter 'one' or 'more' depending on how many summary you want to see.")
        parser.add_argument('--text_preprocessor', default='Null', type=str, help="Word processing. You must select a flag: 'one_resume', 'more_resumes' or 'vacancyes'.")
        parser.add_argument('--load_model', default='Null', type=str, help="You must select a model: 'tfidf', 'bow' or 'w2v'.")
        parser.add_argument('--rest_api', default='Null', type=str, help="You must select a model for api: 'tfidf', 'bow' or 'w2v'.")
        self.args = parser.parse_args()

    def main(self):
        self.parser() # парсер флагов в командной строке
        self.check_values() # обработка флагов и вызов сторонних команд/классов

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()