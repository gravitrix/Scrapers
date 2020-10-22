import os
import time
import requests

DEBUG = False
USERNAME = 'Abhishek_G0YAL'
HEADER = {
    'cookie': '_hrank_session=5b84erandom0c3ff722563random9fe3be39ac9random2e226d569f56erandom5d79920e1d3ccrandomc3a4d88389brandom15e38f69a4217arandom1aed9338;',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

def watch(obj):
    if DEBUG:
        print(obj)

def get_ext(language):
    if language == 'c':
        return 'c'
    if language.find('cpp') != -1:
        return 'cpp'
    if language.find('python') != -1:
        return 'py'
    if language.find('bash') != -1:
        return 'sh'
    if language.find('javascript') != -1:
        return 'js'
    return ''

def get_valid_filename(s):
    symbols = '-_.() '
    digits = '0123456789'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    valid_chars = symbols + digits + uppercase + lowercase
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_')
    while filename.find('__') != -1:
        filename = filename.replace('__', '_')
    while filename[-1] in symbols:
        filename = filename[:-1]
    return filename

def save_to_file(challenge, submission_to_save, submission_content):
    file_name = get_valid_filename(submission_to_save['challenge']['name'].replace('-', '_')) + '.' + get_ext(submission_content['language'])
    print(file_name)
    contest_url = f'/contests/{challenge["con_slug"]}' if challenge['con_slug'] != 'master' else ''
    with open(path + file_name, 'w') as f:
        f.write(f'// https://www.hackerrank.com{contest_url}/challenges/{challenge["ch_slug"]}/problem\n' \
            + ('// ' + submission_content['status'] + '\n' if submission_content['status'] != 'Accepted' \
                else '') + '\n' + submission_content['code'])

def get_submission_content(challenge, submission_to_save):
    submission_content = False
    while not submission_content:
        api = f'https://www.hackerrank.com/rest/contests/{challenge["con_slug"]}/challenges/{submission_to_save["challenge"]["slug"]}/submissions/{submission_to_save["id"]}'
        watch(api)
        r = requests.get(api, headers=HEADER)
        submission_content = r.json()['model']
        if not submission_content:
            time.sleep(18)
    return submission_content

def filter_submissions(submissions):
    submission_to_save = submissions['models'][0]
    for submission in submissions['models']:
        if float(submission['score']) > float(submission_to_save['score']):
            submission_to_save = submission
    return submission_to_save

def get_challenge_submissions(challenge):
    api = f'https://www.hackerrank.com/rest/contests/{challenge["con_slug"]}/challenges/{challenge["ch_slug"]}/submissions/?&offset={0}&limit={12}'
    watch(api)
    r = requests.get(api, headers=HEADER)
    return r.json()

def get_recent_challenges(cursor):
    # api = 'https://www.hackerrank.com/rest/hackers/Abhishek_G0YAL/recent_challenges?limit=221&response_version=v1'
    api = f'https://www.hackerrank.com/rest/hackers/{USERNAME}/recent_challenges?limit={16}&response_version={"v2"}&cursor={cursor}'
    watch(api)
    r = requests.get(api, headers=HEADER)
    return r.json()

path = './HackerRank/'
os.makedirs(path, exist_ok=True)

challenges = None
while True:
    challenges = get_recent_challenges(challenges['cursor'] if challenges else '')
    for challenge in challenges['models']:
        submissions = get_challenge_submissions(challenge)
        submission_to_save = filter_submissions(submissions)
        submission_content = get_submission_content(challenge, submission_to_save)
        save_to_file(challenge, submission_to_save, submission_content)
    if challenges['last_page']:
        break