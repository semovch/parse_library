import requests

import os

import time

import argparse

from bs4 import BeautifulSoup

from urllib.parse import urljoin

from requests.exceptions import HTTPError, ConnectionError

from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise HTTPError(f'Redirectrd url: {response.url}')  
        
        
def download_txt(url, filename, book_id, folder='books'):        
        
        os.makedirs(folder, exist_ok=True)
           
        params = {'id':book_id}
        response = requests.get(url, params=params)  
        response.raise_for_status()
        check_for_redirect(response)
        with open(os.path.join(folder, filename), 'wb') as file:
            file.write(response.content)

        return os.path.join(folder, filename)    


def download_image(url, filename, folder='images'):    
    
    if url != 'https://tululu.org/images/nopic.gif':        

        os.makedirs(folder, exist_ok=True)
        
        response = requests.get(url)   
        response.raise_for_status()
        check_for_redirect(response)
        with open(os.path.join(folder, filename), 'wb') as file:
            file.write(response.content)
            
        return os.path.join(folder, filename)        
      
                           
def parse_book_page(book_id, page):  
    
    soup = BeautifulSoup(page.text, 'lxml')
    
    book_title = soup.find('div', {"id": "content"}).find('h1').next[:-8]
    book_author = soup.find('div', {"id": "content"}).find('a').text
    book_image = urljoin(page.url, soup.find('div', class_='bookimage').find('img')['src'])
    book_genres = [genre.text for genre in soup.find('span', class_='d_book').find_all('a')]
    book_comments = [comment.find('span', class_='black').text for comment in soup.find_all('div', class_='texts')]
        
    filename = f'{sanitize_filename(book_title)}-{sanitize_filename(book_author)}'
    txt_url = f'https://tululu.org/txt.php' #?id={book_id} 
        
    return {'filename':filename,
            'txt_url': txt_url,
            'book_image':book_image,
            'book_genres':book_genres,
            'book_comments':book_comments}

    
def download_books(start_id, end_id):
    for book_id in range(start_id, end_id+1):
        
        book_url = f'https://tululu.org/b{book_id}/'
       
        try: 
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response)
            parsed_page = parse_book_page(book_id, response)
            book_filename = f'{parsed_page["filename"]}.txt'
            image_filename = f'{parsed_page["filename"]}'
            txt_url = parsed_page['txt_url']
            image_url = parsed_page['book_image']
            download_txt(txt_url, book_filename, book_id)
            download_image(image_url, image_filename)            
        except requests.exceptions.HTTPError as err:
            print(f'No resource: {err}')   
        except requests.exceptions.ConnectionError as err:
            time.sleep(10)
            print(f'No connection: {err}')       

       
def main():
    parser = argparse.ArgumentParser(
       description='Download books from tululu'
       )
    parser.add_argument('--start_id', help='start id', type = int, default=1)
    parser.add_argument('--end_id', help='end id', type = int, default=10)
    args = parser.parse_args()  
    start_id = args.start_id
    end_id = args.end_id
    download_books(start_id, end_id)
       
    
if __name__ == '__main__':
    main()   
  
