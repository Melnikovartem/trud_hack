from selenium import webdriver
from parsel import Selector
import time

driver = webdriver.Chrome('C:\chromedriver\chromedriver')
sel = Selector(text=driver.page_source)


def enter(user_id):
    global driver, sel
    url = f'https://www.linkedin.com/in/{user_id}/'
    driver.get('https://www.linkedin.com')
    driver.find_element_by_class_name('nav__button-secondary').click()
    time.sleep(1)
    driver.find_element_by_id('username').send_keys('ch00p.228@gmail.com')
    driver.find_element_by_id('password').send_keys('575000lush')
    driver.find_element_by_class_name('login__form_action_container').click()
    driver.get(url)
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
    name = sel.xpath("//*[starts-with(@class, 'inline t-24 t-black t-normal break-words')]/text()").extract_first()
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
    time.sleep(2)
    sel = Selector(text=driver.page_source)
    skills = sel.xpath("/html/body//main//section//ol//following-sibling::span/text()").getall()
    skills = [e.strip() for e in skills]
    return skills


def close():
    global driver
    driver.close()


def parse_from_linkedin(user_id):
    res = dict()
    enter(user_id)
    time.sleep(1)
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


def main():
    user_adil = 'adilkhan-kussidenov-4163841b2'
    user_oleg = 'oleg-nagaev-112a4392'
    user_female = 'elena-caymaz-57b88937'
    information = parse_from_linkedin(user_female)
    print(information)


if __name__ == '__main__':
    main()


