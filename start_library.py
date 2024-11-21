import time
import json
import os
from typing import List, Dict, Optional


STORAGE_PATH = 'library.json'


class Library:
    """
    Класс для управления библиотекой книг, хранящихся в JSON-файле.
    """
    def __init__(self, storage_path: str = STORAGE_PATH):
        """Проверка наличия и создание JSON библиотеки при отсутствии"""
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def load_books(self) -> List[Dict]:
        """Загрузка книги из JSON-файла."""
        try:
            with open(self.storage_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Ошибка чтения данных: {e}")
            return []

    def save_books(self, books: List[Dict]) -> None:
        """Сохранение книги в JSON-файл."""
        with open(self.storage_path, 'w') as file:
            json.dump(books, file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int, status: str = 'в наличии') -> None:
        """Добавление книги в библиотеку."""
        books = self.load_books()
        book_id = str(int(time.time() * 1_000_000))
        book = {
            'id': book_id,
            'title': title,
            'author': author,
            'year': year,
            'status': status,
        }
        books.append(book)
        self.save_books(books)
        print(f'Книга "{title}" добавлена в библиотеку.')

    def find_book_by_id(self, book_id: str, books: List[Dict]) -> Optional[Dict]:
        """Поиск книги по ID. (Для других функций)"""
        for book in books:
            if book['id'] == book_id:
                return book
        return None

    def delete_book(self, book_id: str) -> None:
        """Удаление книги по ID."""
        books = self.load_books()
        book = self.find_book_by_id(book_id, books)
        if book:
            books.remove(book)
            self.save_books(books)
            print(f'Книга с ID {book_id} удалена.')
        else:
            print(f'Книга с ID {book_id} не найдена.')

    def search_books(self, keyword: str) -> None:
        """Поиск книги по ключевому слову."""
        books = self.load_books()
        results = [
            book for book in books
            if keyword.lower() in book['title'].lower()
            or keyword.lower() in book['author'].lower()
            or str(book['year']) == keyword
        ]
        if results:
            self.display_books(results)
        else:
            print('Книги не найдены.')

    def change_status(self, book_id: str, status: str) -> None:
        """Изменение статуса книги."""
        if status not in ('1', '2'):
            print('Некорректный статус. Используйте "1" для "в наличии" или "2" для "выдана".')
            return

        books = self.load_books()
        book = self.find_book_by_id(book_id, books)
        if book:
            new_status = 'в наличии' if status == '1' else 'выдана'
            if book['status'] != new_status:
                book['status'] = new_status
                self.save_books(books)
                print(f'Статус книги с ID {book_id} обновлен на "{new_status}".')
            else:
                print('Этот статус уже установлен.')
        else:
            print(f'Книга с ID {book_id} не найдена.')

    def display_books(self, books: List[Dict]) -> None:
        """Вывод списока книг."""
        if books:
            print(f'{"ID":<16} {"Название":<20} {"Автор":<20} {"Год":<5} {"Статус":<10}')
            print('-' * 80)
            for book in books:
                print(f'{book["id"]:<16} {book["title"]:<20} {book["author"]:<20} {book["year"]:<5} {book["status"]:<10}')
        else:
            print('Библиотека пуста.')

    def display_all_books(self) -> None:
        """Вывод всех книг из библиотеки."""
        books = self.load_books()
        self.display_books(books)


def main() -> None:
    """
    Основная функция для взаимодействия с библиотекой через консоль.
    """
    library = Library()
    print('Добро пожаловать в консольную библиотеку!')
    while True:
        print('\n1. Добавить книгу\n2. Удалить книгу\n3. Искать книгу\n4. Отобразить все книги\n5. Изменить статус книги\n6. Выход')
        choice = input('Выберите действие: ')
        if choice == '1':
            title = input('Введите название книги: ')
            author = input('Введите автора книги: ')
            while True:
                try:
                    year = int(input('Введите год издания: '))
                    break
                except ValueError:
                    print('Некорректный ввод. Год должен быть числом.')
            library.add_book(title, author, year)
        elif choice == '2':
            book_id = input('Введите ID книги: ')
            library.delete_book(book_id)
        elif choice == '3':
            keyword = input('Введите ключевое слово для поиска: ')
            library.search_books(keyword)
        elif choice == '4':
            library.display_all_books()
        elif choice == '5':
            book_id = input('Введите ID книги: ')
            status = input('Выберите новый статус ("1" - в наличии, "2" - выдана): ')
            library.change_status(book_id, status)
        elif choice == '6':
            print('Выход из программы.')
            break
        else:
            print('Неверный выбор. Попробуйте снова.')


if __name__ == '__main__':
    main()
