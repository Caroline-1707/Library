import json
import os
from typing import List

DATA_FILE = 'library.json'


class Book:
    """Класс для представления книги в библиотеке."""

    def __init__(self, id: int, title: str, author: str, year: int, status: str = "в наличии"):
        """
        Инициализация книги.

        :param id: Уникальный идентификатор книги.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания.
        :param status: Статус книги (по умолчанию "в наличии").
        """
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        """Преобразует объект книги в словарь для сохранения в JSON."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status,
        }


def load_books() -> List[Book]:
    """Загружает книги из файла.

    :return: Список книг.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            books_data = json.load(file)
            return [Book(**data) for data in books_data]
    return []


def save_books(books: List[Book]) -> None:
    """Сохраняет список книг в файл.

    :param books: Список книг для сохранения.
    """
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump([book.to_dict() for book in books], file, ensure_ascii=False, indent=4)


def add_book(books: List[Book]) -> None:
    """Добавляет новую книгу в библиотеку.

    Запрашивает у пользователя данные о книге и добавляет ее в список.

    :param books: Список книг, в который будет добавлена новая книга.
    """
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    year = int(input("Введите год издания: "))

    book_id = len(books) + 1
    new_book = Book(book_id, title, author, year)
    books.append(new_book)
    save_books(books)
    print(f"Книга '{title}' добавлена.")


def remove_book(books: List[Book]) -> None:
    """Удаляет книгу из библиотеки по ID.

    Запрашивает у пользователя ID книги и удаляет ее из списка.

    :param books: Список книг, из которого будет удалена книга.
    """
    book_id = int(input("Введите id книги для удаления: "))
    for book in books:
        if book.id == book_id:
            books.remove(book)
            save_books(books)
            print(f"Книга с id {book_id} удалена.")
            return
    print("Книга не найдена.")


def search_books(books: List[Book], search_term: str) -> List[Book]:
    """Ищет книги по названию, автору или году издания.

    :param books: Список книг для поиска.
    :param search_term: Строка для поиска (название, автор или год).
    :return: Список найденных книг.
    """
    found_books = [book for book in books if (search_term in book.title or
                                              search_term in book.author or
                                              search_term == str(book.year))]
    return found_books


def display_books(books: List[Book]) -> None:
    """Отображает все книги в библиотеке.

    :param books: Список книг для отображения.
    """
    if not books:
        print("Библиотека пуста.")
        return

    for book in books:
        print(f"{book.id}: {book.title} - {book.author} ({book.year}) - {book.status}")


def change_status(books: List[Book], book_id: int, new_status: str) -> bool:
    """Изменяет статус книги по ID.

    :param books: Список книг.
    :param book_id: Уникальный идентификатор книги.
    :param new_status: Новый статус ("в наличии" или "выдана").
    :return: True если статус изменен успешно, иначе False.
    """
    for book in books:
        if book.id == book_id:
            if new_status in ["в наличии", "выдана"]:
                book.status = new_status
                save_books(books)
                return True
            else:
                return False
    return False


def main() -> None:
    """Основной цикл приложения."""

    books = load_books()

    while True:
        print(
            "\nМеню:\n"
            "1. Добавить книгу\n"
            "2. Удалить книгу\n"
            "3. Искать книгу\n"
            "4. Отобразить все книги\n"
            "5. Изменить статус книги\n"
            "6. Выход"
        )

        choice = input("Выберите действие: ")

        match choice:
            case '1':
                add_book(books)
            case '2':
                remove_book(books)
            case '3':
                search_term = input("Введите название, автора или год: ")
                found_books = search_books(books, search_term)
                if found_books:
                    for book in found_books:
                        print(f"{book.id}: {book.title} - {book.author} ({book.year}) - {book.status}")
                else:
                    print("Книги не найдены.")
            case '4':
                display_books(books)
            case '5':
                book_id = int(input("Введите id книги для изменения статуса: "))
                new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
                if change_status(books, book_id, new_status):
                    print(f"Статус книги с id {book_id} изменен на '{new_status}'.")
                else:
                    print("Некорректный статус или книга не найдена.")
            case '6':
                break
            case _:
                print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
