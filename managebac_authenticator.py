import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


def get_jar(school_code, email, password):
    """
    Get the cookie jar for further MB requests by logging in
    The sessions_request *does* make it to /student but this project is not about efficiency/speed so we'll ignore that

    Args:
        self-explanatory strings
    Returns:
        A Requests cookie jar to be used for further BS4 requests
    """
    tqdm.write('Logging in...')
    login_request = requests.get(f'https://{school_code}.managebac.com/login')
    login_html = BeautifulSoup(login_request.text, features='lxml')
    login_csrf_token = login_html.find_all(
        name='meta', attrs={'name': 'csrf-token'}
    )[0].attrs['content']

    sessions_request = requests.post(f'https://{school_code}.managebac.com/sessions', data={
        'authenticity_token': login_csrf_token,
        'login': email,
        'password': password,
        'commit': 'Sign-In'
    }, cookies=login_request.cookies)
    tqdm.write('Logged in.')

    return sessions_request.cookies


def logout(school_code, jar):
    """
    Dunno if this is necessary but log out of the session just in case.

    Args:
        school_code::String
            The part between https:// and .managebac.com
        jar::RequestsCookieJar
            Cookie jar containing login information
    Returns:
        Boolean
            True if successful, False if not
    """
    logout_request = requests.get(
        f'https://{school_code}.managebac.com/logout', cookies=jar)
    return logout_request.status_code == 200
