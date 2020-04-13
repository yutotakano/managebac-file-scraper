import requests
import shutil
import os
from tqdm import tqdm

def download(files, dir='.', job_pool=None):
    if not dir.endswith('/'):
        dir += '/'
    for file in files:
        file['name'] = dir + file['name']
    list(tqdm(job_pool.imap(add_to_job, files), desc='Downloading ' +
              dir, total=len(files)))

def add_to_job(file):
    filename = file['name']
    with requests.get(file['url'], stream=True) as r:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
