import numpy as np
import pandas as pd
import requests
from tqdm.auto import tqdm
import time
from collections import defaultdict
import random

import warnings
warnings.filterwarnings('ignore')

class VacancyLoader:
    def __init__(self, role):
        self.vacancy_df = None
        self.vacancies_ids = []
        self.page = 1
        self.num_per_page = 100
        self.moscow = 1
        self.tabdict = defaultdict(list)
        self.period = 1
        self.role = role

    def get_ids(self):
        for role in tqdm(self.role):
            try:
                res = 0
                url = f'https://api.hh.ru/vacancies?page={self.page}&per_page={self.num_per_page}&area={self.moscow}&professional_role={role}&search_period={self.period}'
                res = requests.get(url)
                if res.status_code == 200:
                    vacancies = res.json()
                    num_pages = vacancies.get('pages')
                    for i in range(num_pages):
                        try:
                            url = f'https://api.hh.ru/vacancies?page={i}&per_page={self.num_per_page}&area={self.moscow}&professional_role={role}&search_period={self.period}'
                            res = requests.get(url)
                            vacancies = res.json()
                            vacancy_ids = [el.get('id') for el in vacancies.get('items')]
                            self.vacancies_ids.extend(vacancy_ids)
                            time.sleep(0.25)
                            # break
                        except:
                            print(f"ERROR: Role = {role} and i = {i}!")
                            time.sleep(random.randint(2, 3))
                            continue
                else:
                    print(f"Request failed with code {res.status_code} and role = {role}!")
                    time.sleep(random.randint(2, 3))
                    continue
            except:
                print(f"ERROR: Role = {role}!")
                time.sleep(random.randint(2, 3))
                continue
        self.vacancies_ids = list(set(self.vacancies_ids))
        return self.vacancies_ids

    def get_vacancies(self):
        for i in range(0, len(self.vacancies_ids), 499):
            batch = self.vacancies_ids[i:i + 499]
            for vac_id in tqdm(batch):
                try:
                    url = f'https://api.hh.ru/vacancies/{vac_id}'
                    res = requests.get(url)
                    if res.status_code == 200:
                        vacancy = res.json()
                        self.tabdict['id'].append(vacancy.get('id'))
                        self.tabdict['name'].append(vacancy.get('name'))
                        self.tabdict['area'].append(vacancy.get('area'))
                        self.tabdict['experience'].append(vacancy.get('experience'))
                        self.tabdict['schedule'].append(vacancy.get('schedule'))
                        self.tabdict['employment'].append(vacancy.get('employment'))
                        self.tabdict['description'].append(vacancy.get('description'))
                        self.tabdict['skills'].append(vacancy.get('key_skills'))
                        self.tabdict['published_at'].append(vacancy.get('published_at'))
                        self.tabdict['professional_roles'].append(vacancy.get('professional_roles'))
                        self.tabdict['alternate_url'].append(vacancy.get('alternate_url'))
                        time.sleep(0.25)
                        # break
                    else:
                        print(f"Request failed with code {res.status_code} and vac_id = {vac_id}!")
                        time.sleep(random.randint(2, 3))
                        continue
                    time.sleep(random.randint(0, 2))
                except:
                    print(f"ERROR: Step = {i} and vac_id = {vac_id}!")
                    time.sleep(random.randint(2, 3))
                    continue
            time.sleep(random.randint(2, 3))
        self.tabdict = pd.DataFrame(self.tabdict)

    def data_transformation(self):
        self.tabdict["area"] = self.tabdict.get("area").map(
            lambda x: x.get("name", np.nan) if isinstance(x, dict) else np.nan)
        self.tabdict["experience"] = self.tabdict.get("experience").map(
            lambda x: x.get("name", np.nan) if isinstance(x, dict) else np.nan)
        self.tabdict["schedule"] = self.tabdict.get("schedule").map(
            lambda x: x.get("name", np.nan) if isinstance(x, dict) else np.nan)
        self.tabdict["employment"] = self.tabdict.get("employment").map(
            lambda x: x.get("name", np.nan) if isinstance(x, dict) else np.nan)
        self.tabdict['skills'] = self.tabdict.get('skills').apply(lambda lst: ', '.join([d['name'] for d in lst]))
        self.tabdict['published_at'] = pd.to_datetime(self.tabdict.get('published_at')).dt.date
        # self.tabdict.to_csv('./bd/all_vacancies.csv', index=False)
        self.tabdict.to_csv('./bd/test.csv', index=False)
        return self.tabdict

    def main(self):
        self.get_ids()
        self.get_vacancies()
        return self.data_transformation()