import os
import requests
import json
import time
import argparse

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tululu_download import download_txt, download_image, parse_book_page, check_for_redirect


def download_many_books(soup, json_path, dest_folder, genre_id, skip_txt, skip_imgs):

    os.makedirs(dest_folder, exist_ok=True)   
    
    for book_href in soup.select('div.bookimage a'):
        try: 
            book_url = urljoin('https://tululu.org',book_href.get('href'))
            book_response = requests.get(book_url)
            book_response.raise_for_status()
            check_for_redirect(book_response)
            parsed_page = parse_book_page(book_response)
            book_filename = f'{parsed_page["filename"]}.txt'
            image_filename = f'{parsed_page["filename"]}'
            txt_url = 'https://tululu.org/txt.php'
            image_url = parsed_page['book_image']
            book_id = book_href.get('href')[2:-1]
            book_path = 'no book'
            if not skip_txt:
             
                book_path = download_txt(txt_url, book_filename, book_id, folder = os.path.join(dest_folder, 'books'))
            
            book_params = {'title': parsed_page['book_title'],
                           'author': parsed_page['book_author'],
                           'img_src': parsed_page['image_src'],
                           'book_path': book_path,
                           'comments': parsed_page['book_comments'],
                           'genres': parsed_page['book_genres']}
                 
            json_path_and_name = os.path.join(dest_folder, f'books_info{genre_id}.json')                  
            if json_path != '':
                os.makedirs(json_path, exist_ok=True)
                json_path_and_name = os.path.join(json_path, 'books_info{genre_id}.json') 
            with open(json_path_and_name, 'a', encoding='utf_8') as json_file:
                json.dump(book_params, json_file, indent=4, ensure_ascii=False)     
            if not skip_imgs and image_url != 'https://tululu.org/images/nopic.gif': 
                download_image(image_url, image_filename, folder = os.path.join(dest_folder, 'images')) 
        except requests.exceptions.HTTPError as err:
            print(f'No resource: {err}')   
        except requests.exceptions.ConnectionError as err:
            time.sleep(10)
            print(f'No connection: {err}')   
            

def main():

    parser = argparse.ArgumentParser(
        prog='books downloader',
        description='Download books from tululu'
        )
    parser.add_argument('--start_page', help='start page', type=int, default=1)
    parser.add_argument('--end_page', help='end page', type=int, default=2)
    parser.add_argument('--genre_id', help='genre of book', type=int, default=55)
    parser.add_argument("--json_path", help="path for json-file", type=str, default='')
    parser.add_argument("--skip_imgs", help="skip image-files", action='store_true')
    parser.add_argument("--skip_txt", help="skip txt-files", action='store_true')
    parser.add_argument("--dest_folder", help="folder for all downloads", type=str, default='downloads')
    args = parser.parse_args()
    
    start_page = args.start_page
    end_page = args.end_page
    genre_id = args.genre_id
    json_path = args.json_path
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt
    dest_folder = args.dest_folder
    
    for page in range(start_page, end_page+1):
        url_of_genre = f'https://tululu.org/l{genre_id}/{page}/'
        try:
            page = requests.get(url_of_genre)
            page.raise_for_status()
            check_for_redirect(page)
            soup = BeautifulSoup(page.text, 'lxml')
            download_many_books(soup, json_path, dest_folder, genre_id, skip_txt, skip_imgs)
        except requests.exceptions.HTTPError as err:
            print(f'No resource: {err}')   
        except requests.exceptions.ConnectionError as err:
            time.sleep(10)
            print(f'No connection: {err}')   
            
if __name__ == '__main__':
    main()   
     
      
   
