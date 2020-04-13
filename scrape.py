import argparse
import sys
import requests
import managebac_authenticator
import managebac_browser
import downloader
from tqdm import tqdm
from multiprocessing import Pool, freeze_support

if __name__ == '__main__':
    # Windows support for multiprocessing
    # Probably not necessary but doesn't hurt to have here
    freeze_support()

    parser = argparse.ArgumentParser(description='Download all the files in the \'Files\' tab for ManageBac classes. Handy for keeping a local copy of all class materials.')
    parser.add_argument('school_code', help='https://<school_code>.managebac.com')
    parser.add_argument('username', help='Login email address, such as johndoe@school.com')
    parser.add_argument('password', help='Login password')
    parser.add_argument('output_dir', help='Output directory location')
    parser.add_argument('class_name', help='Name of the class to filter out', nargs='?')

    args = parser.parse_args()

    cookie_jar = managebac_authenticator.get_jar(args.school_code, args.username, args.password)
    classes = managebac_browser.get_classes(args.school_code, cookie_jar)

    if args.class_name is not None:
        classes = [
            class_dict for class_dict in classes if class_dict['name'] == args.class_name
        ]
    
    dest_dir = args.output_dir
    if not dest_dir.endswith('/') and not dest_dir.endswith('\\'):
        dest_dir += '/'

    job_pool = Pool()

    with tqdm(desc='Class Progress: ', postfix='') as t:
        for class_dict in classes:
            t.postfix = class_dict['name']
            files = managebac_browser.get_files(args.school_code, cookie_jar, class_dict)
            downloader.download(files, job_pool=job_pool, dir=dest_dir + managebac_browser.get_valid_filename(class_dict['name']))
            t.update()

    managebac_authenticator.logout(args.school_code, cookie_jar)
