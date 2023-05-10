import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures

class Resume:
    def __init__(self, params, page_range_max=10, max_workers=4):
        self.params = params
        self.resume_links = set()
        self.page_range_max = page_range_max
        self.max_workers = max_workers

    def get_resume_links(self, page_range=(1, 1)):
        def process_page(page_num):
            page_url = f"{self.url}&p={page_num}"
            response = requests.get(page_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            page_links = set()
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and "gorodrabot.ru/resume/" in href and href not in self.resume_links:
                    page_links.add(href)
            return page_links

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(process_page, page_num) for page_num in range(page_range[0], page_range[1] + 1)]
            for future in concurrent.futures.as_completed(futures):
                page_links = future.result()
                self.resume_links.update(page_links)
        return self.resume_links

    def get_links_for_params(self):
        all_resume = set()
        for param in self.params:
            self.url = f'https://moskva.gorodrabot.ru/resumes?q={param}'
            resume_links = self.get_resume_links(page_range=(1, self.page_range_max))
            all_resume = all_resume | resume_links
        return list(all_resume)

    def get_resume_info(self, link):
        res = requests.get(link)
        soup = BeautifulSoup(res.content, 'html.parser')
        try:
            name = soup.find('h1', {'class': 'resume-view__name content__title'}).text.strip()
        except:
            name = ""
        try:
            achievements = soup.find('li', {'class': 'section__list-item resume-view__list-item'}) \
                .find_next('div', {'class': 'content-minimizer__body'}).text.strip()
        except:
            achievements = ""
        try:
            city = soup.find_all('span', {'class': 'resume-view__title'})[3] \
                .find_next('span', {'class': 'resume-view__text'}).text.strip()
        except:
            city = ""
        try:
            experience = soup.find('h2', {'class': 'section__title'}) \
                .find_next('span', {'class': 'section__subtitle'}).text.strip()
        except:
            experience = ""
        try:
            education = soup.find('h2', {'class': 'section__title'}) \
                .find_next('span', {'class': 'section__subtitle'}) \
                .find_next('span', {'class': 'section__subtitle'}).text.strip()
        except:
            education = ""
        try:
            schedule = soup.find('li', {'class': 'section__list-item resume-view__list-item'}) \
                .find_next('span', {'class': 'resume-view__text'}).text.strip()
        except:
            schedule = ""
        try:
            about = soup.find('li', {'class': 'section__list-item'}) \
                .find_next('div', {'class': 'resume-view__text content-minimizer'}) \
                .find_next('div', {'class': 'resume-view__text content-minimizer'}).text.strip()
        except:
            about = ""
        try:
            skills = soup.find('li', {'class': 'section__list-item resume-view__tags-wrapper'}) \
                .find_next('span', {'class': 'resume-view__tags tags'}).text.strip()
        except:
            skills = ""
        try:
            info = soup.find_all('h2', {'class': 'section__title'})[2] \
                .find_next('div', {'class': 'content-minimizer__body'}) \
                .text.strip()
        except:
            info = ""
        data = {'name': name,
                'achievements': achievements,
                'city': city,
                'experience': experience,
                'education': education,
                'schedule': schedule,
                'about': about,
                'skills': skills,
                'info': info,
                'link': link}
        return pd.DataFrame(data, index=[0])

    def get_date_for_one_resume(self):
        return self.get_resume_info(link=self.url)

    def main(self):
        all_resume = self.get_links_for_params()
        resume_dataframes = []

        for link in all_resume:
            resume_dataframes.append(self.get_resume_info(link))
        all_resume_data = pd.concat(resume_dataframes, ignore_index=True)
        all_resume_data = all_resume_data[all_resume_data['name'] != '']
        all_resume_data['ID'] = all_resume_data.get('link').apply(lambda row: re.search(r'\d+', row).group())
        all_resume_data.to_csv('./bd/all_resume_test.csv',index=False)
        return all_resume_data