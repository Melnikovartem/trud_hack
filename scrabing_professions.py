from selenium import webdriver
from parsel import Selector
import time

names = []
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
driver = webdriver.Chrome(options=options)
sel = Selector(text=driver.page_source)


def get_profiles_on_page():
    global driver, sel
    profile_pages = sel.xpath("/html/body//ul/li/div/div/div/a/@href").getall()
    temp = [profile_pages[i] for i in range(0, len(profile_pages), 2)]
    profile_pages = temp
    return profile_pages


def search_and_get(name, position):
    global driver, sel
    driver.get('https://www.linkedin.com')
    driver.find_element_by_class_name('nav__button-secondary').click()
    time.sleep(1)
    driver.find_element_by_id('username').send_keys('e_m_p_t_y_e@mail.ru')
    driver.find_element_by_id('password').send_keys('12121212EM')
    driver.find_element_by_class_name('login__form_action_container').click()
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
    print(all_profiles)
    driver.close()


search_and_get('василий', 'грузчик')