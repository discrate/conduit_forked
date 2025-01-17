import csv
import random
import string
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from function import *
from input_test_data import *


class TestConduit(object):
    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        self.browser.implicitly_wait(10)
        URL = "http://localhost:1667/"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown(self):
        self.browser.quit()

    # ------------------------------------------------------------------------------------------------------------------
    # // Teszteset 01 \\ Regisztráció helytelen adatokkal (helytelen email címmel)
    def test_registration_invalid(self):
        registration(self.browser, user["name"], user["email"], user["password"])
        time.sleep(2)
        result_message = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        result_reason = self.browser.find_element_by_xpath('//div[@class="swal-text"]')
        assert result_message.text == messages["failed"]
        assert result_reason.text == messages["valid"]

    # ------------------------------------------------------------------------------------------------------------------
    # // Teszteset 02 \\ Regisztráció helyes adatokkal (létrehozott random felhasználónévvel és random email címmel)
    def name_gen(y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))

    name_gen(1)
    random_name = name_gen(10)

    def email_gen(y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))

    email_gen(1)
    random_email = email_gen(10) + "@gmail.com"

    def test_registration_valid(self):
        registration(self.browser, self.random_name, self.random_email, user["password"])
        time.sleep(2)
        result_message = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        result_reason = self.browser.find_element_by_xpath('//div[@class="swal-text"]')
        assert result_message.text == messages["welcome"]
        assert result_reason.text == messages["success"]
        ok_btn = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
        ok_btn.click()

    # ------------------------------------------------------------------------------------------------------------------
    # // Teszteset 03 \\ Bejelentkezés (felhasználó bejelentkezése helyes email cím és jelszó megadásával)
    def test_sign_in(self):
        home_sign_in_btn = self.browser.find_elements_by_xpath('//a[@href="#/login"]')[0]
        home_sign_in_btn.click()
        email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
        email_input.send_keys(self.random_email)
        password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"]')
        password_input.send_keys(user1["password"])
        sign_in_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        sign_in_btn.click()
        time.sleep(2)
        user_profile = self.browser.find_elements_by_xpath('//a[@class="nav-link"]')[2]
        assert user_profile.text == self.random_name

    # ------------------------------------------------------------------------------------------------------------------
    # // Teszteset 04 \\ Adatkezelési nyilatkozat használata (cookiek elfogadása)

    def test_accept_cookies(self):
        accept_btn = self.browser.find_element_by_xpath('//div[normalize-space()="I accept!"]')
        accept_btn.click()
        time.sleep(1)
        decline_btn_list = self.browser.find_elements_by_xpath('//div[normalize-space()="I decline!"]')
        assert len(decline_btn_list) == 0

    # ------------------------------------------------------------------------------------------------------------------
    # # // Teszteset 05 \\ Adatok listázása ("Popular tag"-ek listázása)
    def test_popular_tag_list(self):
        popular_tags = self.browser.find_elements_by_xpath('//a[@class="tag-pill tag-default"]')
        list_of_tags = []
        for i, j in enumerate(popular_tags):
            list_of_tags.append(f'{i + 1}. elem: {j.text}')
        assert len(list_of_tags) == len(popular_tags)

    # ------------------------------------------------------------------------------------------------------------------
    # # // Teszteset 06 \\ Több oldalas lista bejárása (főoldal alján levő navigációs sáv bejárása)
    def test_page_navigation(self):
        TestConduit.test_sign_in(self)
        index_page_list = self.browser.find_elements_by_xpath('//a[@class="page-link"]')
        for i in range(len(index_page_list)):
            page_button = index_page_list[i]
            page_button.click()
        time.sleep(1)
        assert index_page_list[-1].text == f'{len(index_page_list)}'

    # ------------------------------------------------------------------------------------------------------------------
    # # // Teszteset 07 \\ Új adatbevitel (új cikk létrehozása)
    def test_adding_new_input(self):
        TestConduit.test_sign_in(self)
        new_article_btn = self.browser.find_element_by_xpath('//a[@href="#/editor"]')
        new_article_btn.click()
        time.sleep(2)
        article_title = self.browser.find_element_by_xpath('//input[@placeholder ="Article Title"]')
        article_title.send_keys(article['title'])
        article_about = self.browser.find_element_by_xpath('//input[contains(@placeholder, "this article about?")]')
        article_about.send_keys(article['about'])
        article_body = self.browser.find_element_by_xpath('//textarea[@placeholder ="Write your article (in markdown)"]')
        article_body.send_keys(article['body'])
        article_tag = self.browser.find_element_by_xpath('//input[@placeholder ="Enter tags"]')
        article_tag.send_keys(article['tag'])
        publish_article_btn = self.browser.find_element_by_xpath('//button[@type="submit"]')
        publish_article_btn.click()
        time.sleep(2)
        created_body = self.browser.find_element_by_xpath('//p')
        assert created_body.text == article['body']

    # ------------------------------------------------------------------------------------------------------------------
    # // Teszteset 08 \\ Ismételt és sorozatos adatbevitel adatforrásból
    def test_add_comments_from_input(self):
        TestConduit.test_sign_in(self)
        first_article = self.browser.find_elements_by_xpath('//h1')[1]
        first_article.click()
        time.sleep(1)
        comment_box = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write a comment..."]')))
        with open('test_conduit/input_comments.csv', 'r', encoding='UTF-8') as input_f:
            text = csv.reader(input_f, delimiter=',')
            counter = 0
            for row in text:
                comment_box.send_keys(row[1])
                post_comment_btn = self.browser.find_element_by_xpath('//button[text()="Post Comment"]')
                post_comment_btn.click()
                counter += 1
                time.sleep(0.3)
        comments_list = self.browser.find_elements_by_xpath('//div[@class="card"]')
        assert len(comments_list) == counter

    # ------------------------------------------------------------------------------------------------------------------
    # # // Teszteset 09 \\ Meglevő adat módosítás (profilkép cseréje input fileban megadott elérési útvonal alapján)
    def test_change_profile_pic(self):
        TestConduit.test_sign_in(self)
        settings_btn = self.browser.find_element_by_xpath('//a[@href="#/settings"]')
        settings_btn.click()
        image_path = self.browser.find_element_by_xpath('//input[@placeholder="URL of profile picture"]')
        image_path.clear()
        image_path.send_keys(profile_pic['Rick1'])
        update_settings_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        update_settings_btn.click()
        ok_btn = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
        ok_btn.click()
        user_profile = self.browser.find_elements_by_xpath('//a[@class="nav-link"]')[2]
        user_profile.click()
        time.sleep(1)
        img_source = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH,
                                                                                          '//img[@class="user-img"]'))).get_attribute(
            "src")
        assert img_source == profile_pic['Rick1']

    # ------------------------------------------------------------------------------------------------------------------
    # # // Teszteset 10 \\ Adat vagy adatok törlése (komment hozzáadása, majd eltávolítása)
    def test_delete_data(self):
        TestConduit.test_sign_in(self)
        first_article = self.browser.find_elements_by_xpath('//h1')[1]
        first_article.click()
        comment_box = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write a comment..."]')))
        comments_list_before = self.browser.find_elements_by_xpath('//div[@class="card"]')
        comment_box.send_keys(comment["comment1"])
        post_comment_btn = self.browser.find_element_by_xpath('//button[text()="Post Comment"]')
        post_comment_btn.click()
        delete_btn = self.browser.find_element_by_xpath('//i[@class="ion-trash-a"]')
        delete_btn.click()
        time.sleep(1)
        comments_list_after = self.browser.find_elements_by_xpath('//div[@class="card"]')
        assert len(comments_list_after) == len(comments_list_before)

    # ------------------------------------------------------------------------------------------------------------------
    # // Teszteset 11 \\ Adatok lementése felületről (Popular tag-ek kimentése .txt file-ba)

    def test_export_data(self):
        with open("exported.txt", "w", encoding="UTF-8") as output_f:
            popular_tags = self.browser.find_elements_by_xpath('//div[@class="sidebar"]//a[@class="tag-pill tag-default"]')
            output_f.write("Tag-ek listája:" "\n" "_______________" "\n")
            count = 0
            for i, j in enumerate(popular_tags):
                output_f.write(f'{i + 1}. tag: {j.text}' "\n")
                count += 1
        assert count == len(popular_tags)

    # ------------------------------------------------------------------------------------------------------------------
    # # // Teszteset 12 \\ Kijelentkezés (felhasználó kijelentkezése)
    def test_logout(self):
        TestConduit.test_sign_in(self)
        logout_btn = self.browser.find_element_by_xpath('//a[@active-class="active"]')
        logout_btn.click()
        home_sign_in_btn = self.browser.find_elements_by_xpath('//a[@href="#/login"]')[0]
        assert home_sign_in_btn.text == "Sign in"
