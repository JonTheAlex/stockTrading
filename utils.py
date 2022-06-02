import os, re, pickle, requests, sys, shutil, pathlib, shutil
import random, time, datetime, itertools
import numpy as np
import concurrent.futures

record_dir = r'C:\Users\yao56\Documents\Code\Pineapple\records'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
proxy_url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all'

def file_download(record_year):
    for record_coll in record_year:
        for record_page in record_coll:
            for record_list in record_page:
                for record in record_list:
                    record_path = make_record_path(record)
                    file_name = make_file_name(record)
                    file_dir = f'{record_path}\\{file_name}'

                    if os.path.exists(file_dir):
                        continue           
                    else:
                        if os.path.exists(record_path):
                            proxy_request(record[0], record_path, file_dir)
                        else:
                            os.mkdir(record_path)
                            proxy_request(record[0], record_path, file_dir)
    
def make_record_path(record):
    sub_dir = record[1].replace('\n','').replace('\"','').replace("'","").replace(".",'').replace(',','')
    record_path = f'{record_dir}\\{sub_dir}'

    return record_path

def make_file_name(record):
    file_year = re.findall('\d+', record[0])[0]
    file_id = re.findall('\d+', record[0])[1]

    return f'{file_year}{file_id}.pdf'

def proxy_request(record, record_path, file_dir):
    proxy_list = get_proxy_list()

    while True:

        for proxy in proxy_list:

            s = get_session(proxy)
            try:
                pdf_bytes = s.get(record, headers=headers, timeout=10).content
                with open(file_dir, 'wb') as pdf_file:
                    pdf_file.write(pdf_bytes)
                return
            except requests.RequestException as e:
                time = datetime.datetime.now()
                print(f'{time} Error occured: ', e)

        proxy_list = get_proxy_list()

def get_proxy_list():
    r = requests.get(proxy_url)
    proxy_list = re.findall(r"\d+\.\d+\.+\d+\.\d+\:\d+", r.text)

    return proxy_list

def get_session(proxy):
    session = requests.Session()
    
    proxies = {
        'http': proxy,
        'https': proxy
    }
    session.proxies = proxies

    return session

def new_file_explorer():
    try:
        shutil.rmtree('C:\\Users\\yao56\\Documents\\Code\\Pineapple\\records\\New_Files')
    except:
        print('File directory not found')

    for root, dirs, files in os.walk('C:\\Users\\yao56\\Documents\\Code\\Pineapple\\records', topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            file_name = pathlib.Path(file_path)
            file_modified = file_name.stat().st_mtime

            current_date = f'{datetime.date.today()} 00:00:00'
            date_epoch = time.mktime(time.strptime(current_date, '%Y-%m-%d %H:%M:%S'))

            if file_modified > date_epoch:
                move_file(file_path)
            else:
                continue

def move_file(source):
    destination = 'C:\\Users\\yao56\\Documents\\Code\\Pineapple\\records\\New_Files'

    if os.path.exists(destination):
        shutil.copy(source, destination)
    else:
        os.mkdir(destination)
        shutil.copy(source, destination)

def save_pdf(filePath, ptr_links):

    def download_pdf(ptr_link):
        time.sleep(random.randint(5,10))
        pdfbytes = requests.get(ptr_link).content
        pdf_name = ptr_link.split('/')[-1]
        full_path = f'{filePath}\\{pdf_name}'
        with open(full_path, 'wb') as pdf_file:
            pdf_file.write(pdfbytes)
            print(f'{pdf_name} was downloaded...')

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_pdf, ptr_links)