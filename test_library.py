import unittest
from unittest.mock import patch, mock_open
import json
import os
from main import Book, load_books, save_books, add_book, remove_book, search_books, change_status

DATA_FILE = 'library.json'


class TestLibrary(unittest.TestCase):
    def setUp(self):
        """Создаем тестовые данные перед каждым тестом."""
        self.books = [
            Book(1, "1984", "George Orwell", 1949),
            Book(2, "To Kill a Mockingbird", "Harper Lee", 1960),
            Book(3, "The Great Gatsby", "F. Scott Fitzgerald", 1925),
        ]
        save_books(self.books)

    def tearDown(self):
        """Удаляем файл данных после каждого теста."""
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def test_load_books(self):
        """Тест загрузки книг из файла."""
        loaded_books = load_books()
        self.assertEqual(len(loaded_books), len(self.books))
        self.assertEqual(loaded_books[0].title, "1984")

    def test_save_books(self):
        """Тест сохранения книг в файл."""
        new_book = Book(4, "Brave New World", "Aldous Huxley", 1932)
        self.books.append(new_book)
        save_books(self.books)

        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(len(data), 4)
            self.assertEqual(data[3]['title'], "Brave New World")

    @patch("builtins.open", new_callable=mock_open)
    def test_load_books_permission_error(self, mock_file):
        """Тест загрузки книг с ошибкой доступа."""
        mock_file.side_effect = IOError("Недостаточно прав для чтения файла.")

        books = load_books()
        self.assertEqual(books, [])  # Ожидаем пустой список

    @patch("builtins.open", new_callable=mock_open)
    def test_save_books_permission_error(self, mock_file):
        """Тест сохранения книг с ошибкой доступа."""
        mock_file.side_effect = IOError("Недостаточно прав для записи файла.")

        with self.assertRaises(OSError):  # Проверяем на наличие исключения
            save_books([])  # Пытаемся сохранить пустой список

    @patch('builtins.input', side_effect=["Тестовая книга", "Автор", "1953"])
    def test_add_book_valid(self, mock_input):
        """Тест добавления новой книги с корректными данными."""
        books = []
        add_book(books)  # Вводим корректные данные

        self.assertEqual(len(books), 1)  # Книга должна быть добавлена
        self.assertEqual(books[0].title, "Тестовая книга")

    @patch('builtins.input', side_effect=[
        "Тестовая книга",  # Название книги
        "Автор",  # Автор книги
        "некорректный год",  # Некорректное значение
        "2000"  # Корректное значение
    ])
    def test_add_book_invalid_year_string(self, mock_input):
        """Тест добавления книги с некорректным годом (строка)."""
        books = []

        add_book(books)  # Вызываем функцию

        # Проверяем, что книга была добавлена
        self.assertEqual(len(books), 1)  # Должно быть 1 книга

        # Проверяем, что добавленная книга имеет корректные параметры
        self.assertEqual(books[0].title, "Тестовая книга")
        self.assertEqual(books[0].author, "Автор")
        self.assertEqual(books[0].year, 2000)  # Год должен быть 2000

    @patch('builtins.input', side_effect=["Тестовая книга", "Автор", "19з1", "2000"])
    def test_add_book_invalid_year_mixed(self, mock_input):
        """Тест добавления книги с некорректным годом (смешанный ввод)."""
        books = []

        # Вызываем функцию, которая теперь должна обработать ввод
        add_book(books)  # Вводим некорректный год и затем корректный

        # Проверяем, что книга была добавлена
        self.assertEqual(len(books), 1)  # Должно быть 1 книга

        # Проверяем, что добавленная книга имеет корректные параметры
        self.assertEqual(books[0].title, "Тестовая книга")
        self.assertEqual(books[0].author, "Автор")
        self.assertEqual(books[0].year, 2000)  # Год должен быть 2000

    @patch('builtins.input', side_effect=["Тестовая книга", "Автор", "-1999", "2000"])
    def test_add_book_negative_year(self, mock_input):
        """Тест добавления книги с отрицательным годом."""
        books = []
        add_book(books)

        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Тестовая книга")
        self.assertEqual(books[0].author, "Автор")
        self.assertEqual(books[0].year, 2000)

    @patch('builtins.input', side_effect=["1"])  # Удаляем книгу с ID 1
    def test_remove_book(self, mock_input):
        """Тест удаления книги по ID."""
        remove_book(self.books)

        self.assertNotIn("1984", [book.title for book in load_books()])

    @patch('builtins.input', side_effect=["не числовое значение", 2])
    def test_remove_book_invalid_id_string(self, mock_input):
        """Тест удаления книги с некорректным ID (строка)."""
        books = [Book(1, "1984", "George Orwell", 1949)]

        remove_book(books)  # Пытаемся удалить книгу, вводя некорректный ID

        self.assertEqual(len(books), 1)  # Проверяем, что книга должна остаться в списке
        self.assertEqual(books[0].title, "1984")  # Проверяем, что это все та же книга

    @patch('builtins.input', side_effect=["-1"])
    def test_remove_book_negative_id(self, mock_input):
        """Тест удаления книги с отрицательным ID."""
        books = [Book(1, "1984", "George Orwell", 1949)]

        remove_book(books)

        self.assertEqual(len(books), 1)  # Книга должна остаться
        self.assertEqual(books[0].title, "1984")  # Проверяем, что это все та же книга

    @patch('builtins.input', side_effect=["2"])
    def test_remove_book_nonexistent_id(self, mock_input):
        """Тест удаления книги с несуществующим ID."""
        books = [Book(1, "1984", "George Orwell", 1949)]

        remove_book(books)

        self.assertEqual(len(books), 1)  # Книга должна остаться
        self.assertEqual(books[0].title, "1984")  # Проверяем, что это все та же книга

    def test_search_books(self):
        """Тест поиска книг."""
        found_books = search_books(self.books, "1984")

        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].title, "1984")

    def test_change_status(self):
        """Тест изменения статуса книги."""
        book_id = 1
        new_status = "выдана"

        result = change_status(self.books, book_id, new_status)

        self.assertTrue(result)
        self.assertEqual(self.books[0].status, new_status)

    def test_invalid_change_status(self):
        """Тест изменения статуса на некорректное значение."""
        book_id = 1
        new_status = "недоступно"

        result = change_status(self.books, book_id, new_status)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
