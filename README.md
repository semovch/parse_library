#Парсер книг с сайта tululu.org
Скрипт main.py скачивает с сайта tululu.org кинги в формате txt, а также обложки книг, еслит таковые имеюся.

###Как установить
Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
Рекомендуется испоьзовать [virtualenv/venv] для изоляции проекта.
Для запуска в терминале:
```
python main.py

```
Есть необязательные аргументы --start_id и --end_id - условные номера книг, с которого по который(включительно) скрипт скачает книги.
Пример запуска с аргументами:

```
python main.py --start_id 3 --end_id 15

```
Скрипт скачает книги с номера 3 по номер 15(включительно)
Аргументы по умолчанию start_id = 1, end_id =  10

##Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).