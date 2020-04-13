import requests
from tqdm import tqdm
import itertools
import re
from bs4 import BeautifulSoup


def get_classes(school_code, jar):
    """
    Args:
        school_code::String
        jar::RequestsCookieJar
    Returns:
        List
            List of class dicts, each containing keys name and id
    """
    student_request = requests.get(
        f'https://{school_code}.managebac.com/student', cookies=jar)
    student_html = BeautifulSoup(student_request.text, features='lxml')
    classes_html = student_html.select(
        '#menu > ul > li[data-path^="classes"] > ul > li')
    classes = []
    for class_html in tqdm(classes_html, desc='Getting classes...'):
        if class_html.find('span') is None:
            # Not a class, maybe "Join a new class..."
            continue
        classes.append({
            'name': class_html.find('span').text.strip(),
            'id': class_html.find('a').attrs['href'].split('/')[-1]
        })
    return classes


def get_files(school_code, jar, class_dict):
    files = []

    files_htmls = get_files_htmls(jar,
                                  f'https://{school_code}.managebac.com/student/classes/{class_dict["id"]}/files')
    for files_html in tqdm(files_htmls, desc='Parsing...'):
        files += find_file_links(school_code, jar, files_html)

    return files


def get_files_htmls(jar, url):
    htmls = []
    request = requests.get(url, cookies=jar)
    htmls.append(BeautifulSoup(request.text, features='lxml'))
    total_pages_html = htmls[0].select(
        'ul.pagination li:nth-last-child(2) a')
    total_pages = int(total_pages_html[0].text) if len(
        total_pages_html) > 0 else 1
    current_page = 1
    while total_pages > current_page:
        request = requests.get(
            f'{url}/page/{str(current_page + 1)}', cookies=jar)
        htmls.append(BeautifulSoup(request.text, features='lxml'))
        current_page += 1
    return htmls


def find_file_links(school_code, jar, class_html, directory=''):
    links = []
    files_html = class_html.find_all(class_='row file')
    for file_html in files_html:
        details = file_html.find(class_='details')
        if details is None:
            # is a folder
            foldername_html = file_html.find(class_='title').find('a')
            for page in tqdm(get_files_htmls(jar, f'https://{school_code}.managebac.com{foldername_html["href"]}'), desc=f'Parsing {foldername_html.text.strip()}...'):
                links += find_file_links(school_code, jar, page,
                                         directory=directory + get_valid_filename(foldername_html.text.strip()) + '/')
        else:
            filename_html = details.find('a')
            author = details.find('label').text.replace('\nby\n', '').strip()
            creation_date = file_html.find_all(class_='hidden-xs')[-1].text
            links.append({
                'type': 'file',
                'name': directory + filename_html.text,
                'author': author,
                'date': creation_date,
                'url': filename_html['href']
            })
    return links


def get_valid_filename(s):
    """
    - from the django framework
    
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)
