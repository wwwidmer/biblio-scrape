import requests
import os
from fpdf import FPDF

from threading import Thread

base_url = 'https://bibliotekus.artlebedev.ru/'

page_structure = '{base_url}/images/{book_name}/{page_num}.jpg'

THREAD_SIZE = 10

def download_pages(page_num, book_name):
    while True:
        success = download_page(page_num, book_name)
        if not success:
            break
        page_num += THREAD_SIZE


def download_page(page_num, book_name):
    if '{page_num}.jpg'.format(page_num=page_num) in os.listdir(book_name):
        print('Page {page_num} already exists'.format(page_num=page_num))
        return 1
    request = requests.get(page_structure.format(base_url=base_url, book_name=book_name, page_num=page_num))
    print('Requesting page {page_num}'.format(page_num=page_num))
    if request.status_code == 404 or '<title>404</title>' in request.text:
        page_num = None
        print('Page {page_num} not found'.format(page_num=page_num))
        return 
    with open('{name}/{page_num}.jpg'.format(name=book_name, page_num=page_num), 'wb') as f:
        f.write(request.content)
    print ('Page {page_num} saved'.format(page_num=page_num))
    return 1

def main():
    page_num = 0 
    book_names = ['schriften-messinglinien-usw', 'die-schöne-schrift-1']
    for book_name in book_names:  
        os.makedirs(book_name, exist_ok=True)

        threads = []
        for i in range(THREAD_SIZE):
            thread = Thread(target=download_pages, args=(i, book_name))
            threads.append(thread)
            thread.start()
            page_num += 1

        for thread in threads:
            thread.join()
        
        print ("All pages saved; Creating PDF")
        
        pdf = FPDF()

        for page in sorted(os.listdir(book_name), key=lambda x: int(x.split('.')[0])):
            pdf.add_page()
            pdf.image('{name}/{page}'.format(name=book_name, page=page), 0, 0, 200)    
         
        pdf.output('{name}.pdf'.format(name=book_name), 'F')



if __name__ == "__main__":
    main()
    