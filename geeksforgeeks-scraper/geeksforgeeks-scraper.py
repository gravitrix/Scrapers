'''
Author: Abhishek Goyal

GeeksforGeeks Scraper is a python program that logins into your GeeksforGeeks account, and copies your code for your solved 
problems into its corresponding file.

For example, your solution to the problem <name> will be stored in the file <name>.<lang>
'''

TIME_DELAY = 5
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip

chrome_options = Options()
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(TIME_DELAY)

def get_code(problem_link):
    driver.get(problem_link)
    driver.get(driver.find_element_by_xpath('//*[@id="problems"]/div/div[1]/div/div[2]/div/a[2]').get_attribute('href'))
    table = driver.find_element_by_xpath('//*[@id="problemSubmissionTable"]')
    rows = table.find_elements_by_tag_name('tr')[1:]
    row = rows[0].find_elements_by_tag_name('td')
    time_ist = row[0].text
    status = row[1].text
    lang = row[2].text
    submission_link = row[3].find_element_by_tag_name('a').get_attribute('href')
    for row in rows:
        row = row.find_elements_by_tag_name('td')
        if (status := row[1].text) == 'Correct':
            time_ist = row[0].text
            lang = row[2].text
            submission_link = row[3].find_element_by_tag_name('a').get_attribute('href')
            break
    print(submission_link, type(submission_link))
    driver.get(submission_link)
    code_box = driver.find_element_by_xpath('//*[@id="editor"]').click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
    code = pyperclip.paste()
    problem_link = '// ' + problem_link + '\n'
    info = '// '+ status + '\n' if status != 'Correct' else ''
    return problem_link + info + '\n' + code, lang

def save_codes(solved_problems, path):
    os.makedirs(path, exist_ok=True)
    for problem_name in solved_problems:
        code, lang = get_code(solved_problems[problem_name])
        file_path = path + problem_name.replace(' ', '_') + '.' + lang
        with open(file_path, 'w') as f:
            f.write(code)

def get_solved_problems():
    driver.get(driver.current_url + '/practice/')
    xpaths = ['//*[@id="School"]', '//*[@id="Basic"]', '//*[@id="Easy"]', '//*[@id="Medium"]', '//*[@id="Hard"]']
    problems = {}
    for i, xpath in enumerate(xpaths):
        driver.find_element_by_xpath(f'//*[@id="problem-solved-div"]/a[{i+1}]').click()
        li_a = driver.find_element_by_xpath(xpath).find_elements_by_tag_name('a')
        problems.update({a.text : a.get_attribute('href') for a in li_a})
    return problems

def sign_into_geeksforgeeks(username, password):
    driver.get('https://auth.geeksforgeeks.org/')
    driver.find_element_by_xpath('//*[@id="luser"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(Keys.ENTER)

if __name__ == '__main__':
    sign_into_geeksforgeeks(username='abhishek_g0yal', password='cKGRg$Niap#yBm9')
    time.sleep(3)
    solved_problems = get_solved_problems()
    with open('solved_problems.json', 'w') as f:
        json.dump(solved_problems, f, indent=4)
    save_codes(solved_problems, path='./GeeksforGeeks/')
    driver.close()