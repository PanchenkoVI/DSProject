import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

class Resume:
    def __init__(self, url):
        self.url = url

    def get_resume_info(self):
        res = requests.get(self.url)
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
            skills = ""

        data = {'name': name,
                'achievements': achievements,
                'city': city,
                'experience': experience,
                'education': education,
                'schedule': schedule,
                'about': about,
                'skills': skills,
                'info': info,
                'link': self.url}
        return pd.DataFrame(data, index=[0])

    def main(self):
        one_resume = self.get_resume_info()
        one_resume = one_resume[one_resume['name'] != '']
        one_resume['ID'] = one_resume.get('link').apply(lambda row: re.search(r'\d+', row).group())
        one_resume.to_csv('./bd/one_resume.csv', index=False)
        return one_resume