from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from parsel import Selector
import time
import json
from pathlib import Path


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
driver = webdriver.Chrome(options=options)
sel = Selector(text=driver.page_source)


def enter():
    global driver
    driver.get('https://www.linkedin.com')
    driver.find_element_by_class_name('nav__button-secondary').click()
    time.sleep(1)
    driver.find_element_by_id('username').send_keys('va_no_10@mail.ru')
    driver.find_element_by_id('password').send_keys('12121212EM')
    driver.find_element_by_class_name('login__form_action_container').click()


def switch_to_page(user_id):
    global driver, sel
    url = f'https://www.linkedin.com/in/{user_id}/'
    driver.get(url)
    time.sleep(1)
    sel = Selector(text=driver.page_source)


def scroll():
    # Скролим
    global driver, sel
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    sel = Selector(text=driver.page_source)


def get_about():
    global driver
    # Разворачиваем поле about
    time.sleep(4)
    try:
        driver.find_element_by_xpath('/html/body//main//section/p/span/span/a').click()
    except Exception:
        pass
    time.sleep(1)
    sel = Selector(text=driver.page_source)
    about = sel.xpath("/html/body//main//section/p/span[1]/text()").getall()
    return about


def get_fullname():
    global sel
    name = sel.xpath("/html/body//main//section/div/div/div/ul/li/text()").getall()[0]
    return name.strip()


def get_organisations():
    global sel
    organisations = sel.xpath(
        "//*[starts-with(@class, 'pv-top-card--experience-list')]//following-sibling::span/text()").getall()
    organisations = [e.strip() for e in organisations]
    return organisations


def get_experience():
    global sel
    experience_1 = sel.xpath("//*[starts-with(@class, 't-16 t-black t-bold')]/text()").getall()
    experience_2 = sel.xpath("//*[starts-with(@class, 't-14 t-black t-bold')]//following-sibling::span/text()").getall()
    experience = experience_1 + experience_2
    temp = []
    for e in experience:
        if e.strip() != 'Title' and e.strip() != '' and e.strip() != 'Keep in touch with your network':
            temp.append(e.strip())
    experience = temp
    return experience


def get_languages():
    global sel
    languages = sel.xpath("/html/body//main//section/div/section/div/div/ul//following-sibling::li/text()").getall()
    languages = [e.strip() for e in languages]
    return languages


def get_interests():
    global sel, driver
    # Разворачиваем интересы
    try:
        driver.find_element_by_xpath('/html/body//main//section/a').click()
    except Exception:
        pass
    time.sleep(2)
    sel = Selector(text=driver.page_source)
    interests = sel.xpath("//*[starts-with(@class, 'pv-entity__summary-title-text')]/text()").getall()
    interests = [e.strip() for e in interests]
    return interests


def get_skills():
    global sel, driver
    # Разворачиваем
    try:
        driver.find_element_by_xpath('/html/body//main//section/div[2]/button').click()
    except Exception:
        pass
    sel = Selector(text=driver.page_source)
    skills = sel.xpath("//*[@class='pv-profile-section pv-skill-categories-section artdeco-container-card ember-view']//following-sibling::span/text()").getall()
    skills = [e.strip() for e in skills]
    return skills


def close():
    global driver
    driver.close()


def parse_from_linkedin(user_id):
    res = dict()
    enter()
    switch_to_page(user_id)
    res['fullname'] = get_fullname()
    res['about'] = get_about()
    scroll()
    res['organisations'] = get_organisations()
    res['experience'] = get_experience()
    res['languages'] = get_languages()
    res['skills'] = get_skills()
    res['interests'] = get_interests()
    close()
    return res


def parse_next_page(user_id):
    res = dict()
    switch_to_page(user_id)
    res['fullname'] = get_fullname()
    res['about'] = get_about()
    scroll()
    res['organisations'] = get_organisations()
    res['experience'] = get_experience()
    res['languages'] = get_languages()
    res['skills'] = get_skills()
    res['interests'] = get_interests()
    return res


def get_profiles_on_page():
    global driver, sel
    profile_pages = sel.xpath("/html/body//ul/li/div/div/div/a/@href").getall()
    temp = [profile_pages[i] for i in range(0, len(profile_pages), 2)]
    profile_pages = temp
    return profile_pages


def search_and_get(name, position):
    global driver, sel
    sel = Selector(text=driver.page_source)
    page = 1
    all_profiles = []
    while True:
        url = f'https://www.linkedin.com/search/results/people/?firstName={name}&origin=FACETED_SEARCH&page={page}&title={position}/'
        driver.get(url)
        sel = Selector(text=driver.page_source)
        try:
            sel.xpath('/html/body//h1/text()').getall()[0]
        except Exception:
            all_profiles += get_profiles_on_page()
        else:
            break
        page += 1
    all_profiles = [e.split('/')[-2] for e in all_profiles]
    return all_profiles


def main():
    path = Path('users_id_workers.txt')
    users_ids = json.loads(path.read_text(encoding='utf-8'))
    enter()
    res = []
    for user_id in users_ids:
        print(user_id)
        res += [parse_next_page(user_id)]
        _path = Path('information_about_managers.txt')
        _path.write_text(json.dumps(res))
    close()

def _main():
    print(parse_from_linkedin('em-em-20829b1b2'))

if __name__ == '__main__':
    _main()
