from selenium import webdriver
from parsel import Selector
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
sel = Selector(text=driver.page_source)


def enter(user_id):
    global driver, sel
    url = f'https://ok.ru/profile/{user_id}'
    driver.get('https://ok.ru/')
    driver.find_element_by_id('field_email').send_keys('e_m_p_t_y_e@mail.ru')
    driver.find_element_by_id('field_password').send_keys('12121212EM')
    driver.find_element_by_xpath(
        "/html/body/div[7]/div[4]/div[3]/div[1]/div/div[2]/div/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[3]/form/div[5]/div[1]/input").click()
    driver.get(url)
    sel = Selector(text=driver.page_source)


def get_fullname():
    global sel
    name = sel.xpath(
        "/html/body/div[7]/div[4]/div[5]/div[1]/div/div[5]/div/div[1]/div[2]/div/div[1]/div[2]/div/div/a/h1").extract_first()
    return name.strip('</h1>')


def get_groups():
    global driver, sel
    driver.find_element_by_xpath(
        '/html/body/div[7]/div[4]/div[5]/div[1]/div/div[5]/div/div[1]/div[2]/div/div[2]/div[2]/div/div/a[4]').click()
    time.sleep(1)
    sel = Selector(text=driver.page_source)
    groups = sel.xpath("//*[starts-with(@class, 'o two-lines group-name-link')]/text()").getall()
    driver.back()
    sel = Selector(text=driver.page_source)
    return groups


def get_about():
    global driver, sel
    cur_url = driver.current_url
    driver.get(cur_url + '/about')
    sel = Selector(text=driver.page_source)
    about = sel.xpath('/html/body/div[7]/div[4]/div[5]/div[1]/div/div[5]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div[2]/div[4]/div[1]/div[2]/div[1]/div/a/span/text()').getall()
    about += sel.xpath('/html/body/div[7]/div[4]/div[5]/div[1]/div/div[5]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div[2]/div[4]/div[2]/div[2]/div[1]/div/a/span/text()').getall()
    about += sel.xpath('/html/body/div[7]/div[4]/div[5]/div[1]/div/div[5]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div[2]/div[4]/div[3]/div[2]/div[1]/div/a/span/text()').getall()
    about += sel.xpath('/html/body/div[7]/div[4]/div[5]/div[1]/div/div[5]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div[2]/div[6]/div/div[2]/div[1]/div/a/span/text()').getall()
    about += sel.xpath('/html/body/div[7]/div[4]/div[5]/div[1]/div/div[5]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/a/span/text').getall()
    about += sel.xpath('/html/body/div[7]/div[4]/div[5]/div[1]/div/div[5]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/a/span/text').getall()
    about += sel.xpath('/html/body/div[7]/div[4]/div[5]/div[1]/div/div[5]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/div[1]/div/a/span/text').getall()
    driver.get(cur_url)
    sel = Selector(text=driver.page_source)
    return about


def close():
    global driver
    driver.close()


def parse_from_ok(user_id):
    res = dict()
    enter(user_id)
    res['fullname'] = get_fullname()
    res['groups'] = get_groups()
    res['about'] = get_about()
    return res


def main():
    user_id = '146045361339'
    user_ivan = '566557903095'
    user_notivan = '536698071337'
    information = parse_from_ok(user_notivan)
    print(information)
    close()


if __name__ == '__main__':
    main()