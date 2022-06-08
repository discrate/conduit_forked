import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from test_conduit.input_test_data import *
import random
import string

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.implicitly_wait(10)
browser.get("http://localhost:1667/#/")
browser.maximize_window()


# // Teszteset 02 \\ Regisztráció helyes adatokkal

def name_gen(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


name_gen(1)
random_name = name_gen(10)


def email_gen(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


email_gen(1)
random_email = email_gen(10) + "@gmail.com"


def registration_valid():
    sign_up_btn = browser.find_element_by_xpath('//a[@href="#/register"]')
    sign_up_btn.click()
    username_input = browser.find_element_by_xpath('//input[@placeholder="Username"]')
    email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
    password_input = browser.find_element_by_xpath('//input[@placeholder="Password"]')
    sign_up_send_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    username_input.send_keys(random_name)
    email_input.send_keys(random_email)
    password_input.send_keys(user["password"])
    time.sleep(1)
    sign_up_send_btn.click()
    time.sleep(2)
    result_message = browser.find_element_by_xpath('//div[@class="swal-title"]')
    result_reason = browser.find_element_by_xpath('//div[@class="swal-text"]')
    try:
        assert result_message.text == "Welcome!"
        assert result_reason.text == "Your registration was successful!"
        print('Sikeres regisztráció')
    except AssertionError:
        print('Sikertelen regisztráció')

    ok_btn = browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
    ok_btn.click()


# // Teszteset 03 \\ Bejelentkezés

def sign_in():
    home_sign_in_btn = browser.find_elements_by_xpath('//a[@href="#/login"]')[0]
    home_sign_in_btn.click()
    email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
    email_input.send_keys(random_email)
    password_input = browser.find_element_by_xpath('//input[@placeholder="Password"]')
    password_input.send_keys(user["password"])
    sign_in_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    sign_in_btn.click()
    time.sleep(2)
    # user_profile = browser.find_elements_by_xpath('//a[@class="nav-link"]')[2]
    user_profile = browser.find_element_by_xpath('//a[@href="#/@szgteszt1/" and @class="nav-link"]')
    print(user_profile.text)

    try:
        assert user_profile.text == user1["name"]  # helyes felhasználónév megjelenítésének ellenőrzése
        print('Sikeres bejelentkezés')
    except AssertionError:
        print('Nem sikerült bejelentkezni')


# // Teszteset 05 \\ Adatok listázása

# def popular_tag_list():
#     popular_tags = browser.find_elements_by_xpath('//div[@class="sidebar"]//a[@class="tag-pill tag-default"]')
#     list_of_tags = []
#     for i, j in enumerate(popular_tags):
#         list_of_tags.append(f'{i + 1}. elem: {j.text}')
#     print(f'Popular Tags: {list_of_tags}')
#     try:
#         assert len(list_of_tags) == len(popular_tags)
#         print(f'Helyes lista, elemek száma: {len(list_of_tags)}')
#     except AssertionError:
#         print('Helytelen lista')
#
#
# popular_tag_list()

# // Teszteset 06 \\ Több oldalas lista bejárása

# def page_navigation():
#     index_page_list = browser.find_elements_by_xpath('//a[@class="page-link"]')
#     for i in range(len(index_page_list)):
#         page_button = index_page_list[i]
#         page_button.click()
#
#     assert index_page_list[- 1].text == f'{len(index_page_list)}'
#
#
# sign_in()
# page_navigation()
# // Teszteset 07 \\ Új adatbevitel

# def adding_new_input():
#     new_article_btn = browser.find_element_by_xpath('//a[@href="#/editor"]')
#     new_article_btn.click()
#     time.sleep(2)
#     article_title = browser.find_element_by_xpath('//input[@placeholder ="Article Title"]')
#     article_title.send_keys(article['title'])
#     article_about = browser.find_element_by_xpath('//input[contains(@placeholder, "this article about?")]')
#     article_about.send_keys(article['about'])
#     article_body = browser.find_element_by_xpath('//textarea[@placeholder ="Write your article (in markdown)"]')
#     article_body.send_keys(article['body'])
#     article_tag = browser.find_element_by_xpath('//input[@placeholder ="Enter tags"]')
#     article_tag.send_keys(article['tag'])
#     publish_article_btn = browser.find_element_by_xpath('//button[@type="submit"]')
#     publish_article_btn.click()
#     time.sleep(2)
#     created_body = browser.find_element_by_xpath('//p')
#     try:
#         assert created_body.text == article['body']
#         print('Helyesen létrehozva')
#     except AssertionError:
#         print('Helytelen cikk')

# sign_in()
# adding_new_input()

# try:
#     assert result_message.text == "Registration failed!"
#     assert result_reason.text == "Email must be a valid email."
#     print('Helyes hibaüzenet')
# except AssertionError:
#     print('Helytelen validáció')

# browser.quit()


# // Teszteset 12 \\ Kijelentkezés

def logout():
    logout_btn = browser.find_element_by_xpath('//a[@active-class="active"]')
    logout_btn.click()
    home_sign_in_btn = browser.find_elements_by_xpath('//a[@href="#/login"]')[0]
    try:
        assert home_sign_in_btn.text == "Sign in"
        print('Sikeres kijelentkezés')
    except AssertionError:
        print('Nem sikerült kijelentkezni')


registration_valid()
logout()
sign_in()
