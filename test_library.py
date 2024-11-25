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
        
        with self.assertRaises(Exception):  # Проверяем на наличие исключения
            save_books([])  # Пытаемся сохранить пустой список

    def test_add_book(self):
        """Тест добавления новой книги."""
        new_book = Book(4, "Fahrenheit 451", "Ray Bradbury", 1953)
        add_book(self.books)  # Ввод данных будет запрашиваться
        self.assertIn(new_book.title, [book.title for book in load_books()])

    def test_remove_book(self):
        """Тест удаления книги по ID."""
        remove_book(self.books)  # Ввод данных будет запрашиваться
        self.assertNotIn("1984", [book.title for book in load_books()])

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
