import sys

from PyQt6.QtSql import QSqlQuery, QSqlDatabase
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QHBoxLayout, QListWidget, QLineEdit, QTextEdit,
                             QListWidgetItem, QLabel, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(400, 500)

        self.setWindowTitle('Список задач')
        self.setWindowIcon(QIcon('task_list.png'))

        self.list_name_label = QLabel('Список задач:')
        self.tasks_list = QListWidget()

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.list_name_label)
        self.vbox.addWidget(self.tasks_list)

        self.all_tasks_button = QPushButton('Все задачи', self)
        self.active_tasks_button = QPushButton('Активные задачи', self)
        self.completed_tasks_button = QPushButton('Выполненные задачи', self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.all_tasks_button)
        self.hbox.addWidget(self.active_tasks_button)
        self.hbox.addWidget(self.completed_tasks_button)
        self.vbox.addLayout(self.hbox)

        self.name_label = QLabel('Название задачи:')
        self.task_name = QLineEdit()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.name_label)
        self.hbox.addWidget(self.task_name)
        self.vbox.addLayout(self.hbox)

        self.description_label = QLabel('Описание задачи:')
        self.task_description = QTextEdit()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.description_label)
        self.hbox.addWidget(self.task_description)
        self.vbox.addLayout(self.hbox)

        self.status_label = QLabel('Статус задачи:')
        self.task_status = QLineEdit()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.status_label)
        self.hbox.addWidget(self.task_status)
        self.vbox.addLayout(self.hbox)

        self.category_label = QLabel('Категория задачи:')
        self.category_name = QLineEdit()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.category_label)
        self.hbox.addWidget(self.category_name)
        self.vbox.addLayout(self.hbox)

        self.list_category_label = QLabel('Список категорий:')
        self.category_list = QListWidget()
        self.vbox.addWidget(self.list_category_label)
        self.vbox.addWidget(self.category_list)

        self.add_task_button = QPushButton('Добавить задачу', self)
        self.edit_task_button = QPushButton('Изменить задачу', self)
        self.delete_task_button = QPushButton('Удалить задачу', self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.add_task_button)
        self.hbox.addWidget(self.edit_task_button)
        self.hbox.addWidget(self.delete_task_button)
        self.vbox.addLayout(self.hbox)

        self.add_category_button = QPushButton('Добавить категорию', self)
        self.edit_category_button = QPushButton('Изменить категорию', self)
        self.delete_category_button = QPushButton('Удалить категорию', self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.add_category_button)
        self.hbox.addWidget(self.edit_category_button)
        self.hbox.addWidget(self.delete_category_button)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

        self.create_tables()
        self.load_tasks()
        self.load_categories()

        self.add_category_button.clicked.connect(self.add_category)
        self.add_task_button.clicked.connect(self.add_task)

        self.category_list.itemClicked.connect(self.category_detail)
        self.tasks_list.itemClicked.connect(self.task_detail)

        self.delete_category_button.clicked.connect(self.delete_category)
        self.delete_task_button.clicked.connect(self.delete_task)

        self.edit_category_button.clicked.connect(self.edit_category)
        self.edit_task_button.clicked.connect(self.edit_task)

        self.all_tasks_button.clicked.connect(self.load_tasks)
        self.active_tasks_button.clicked.connect(self.active_tasks)
        self.completed_tasks_button.clicked.connect(self.completed_tasks)

    def create_tables(self):
        query = QSqlQuery()

        query.exec(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL
            );
            """
        )

        query.exec(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                description VARCHAR(255) NOT NULL,
                active BOOL NOT NULL DEFAULT TRUE,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            );
            """
        )

    def load_categories(self):
        query = QSqlQuery()
        query.exec(
            """
            SELECT * FROM categories;
            """
        )

        self.categories = []
        count = query.record().count()

        while query.next():
            temp = []

            for i in range(count):
                temp.append(query.value(i))

            self.categories.append(temp)

        self.category_list.clear()
        for category in self.categories:
            self.category_list.addItem(QListWidgetItem(category[1]))

    def load_tasks(self):
        query = QSqlQuery()
        query.exec(
            """
            SELECT * FROM tasks LEFT JOIN categories ON tasks.category_id=categories.id;
            """
        )

        self.tasks = []
        count = query.record().count()

        while query.next():
            temp = []

            for i in range(count):
                temp.append(query.value(i))

            self.tasks.append(temp)

        self.tasks_list.clear()
        for task in self.tasks:
            self.tasks_list.addItem(QListWidgetItem(task[1]))

    def add_category(self):
        name = self.category_name.text()

        query = QSqlQuery()
        query.exec(
            f"""
            INSERT INTO categories (name) VALUES ('{name}');
            """
        )

        self.load_categories()

    def add_task(self):
        name = self.task_name.text()
        description = self.task_description.toPlainText()
        status = self.task_status.text().replace('+', 'True').replace('-', 'False')

        if self.categories == []:
            message_box = QMessageBox()
            message_box.setText("Для того чтобы добавить задачу - необходимо сначала создать категорию")
            message_box.setWindowTitle("Добавление категории")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.show()
            result = message_box.exec()

        else:
            row = self.category_list.currentRow()
            category_id = self.categories[row][0]

            query = QSqlQuery()
            query.exec(
                f"""
                INSERT INTO tasks (name, description, active, category_id) VALUES ('{name}', '{description}',
                                                                                    {status}, {category_id})
                """
            )

            self.load_tasks()

        print(self.tasks)

    def category_detail(self):
        row = self.category_list.currentRow()
        self.category_name.setText(self.categories[row][1])

    def task_detail(self):
        row = self.tasks_list.currentRow()
        self.task_name.setText(self.tasks[row][1])
        self.task_description.setText(self.tasks[row][2])
        self.task_status.setText(str(self.tasks[row][3]).replace('0', '-').replace('1', '+'))
        #self.category_name.setText(self.tasks[row][4])

    def delete_category(self):
        query = QSqlQuery()

        row = self.category_list.currentRow()
        category_id = self.categories[row][0]

        message_box = QMessageBox()
        message_box.setText(f"Вы точно хотите удалить категорию: {self.categories[row][1]}?")
        message_box.setWindowTitle("Удаление категории")
        message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        message_box.show()
        result = message_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            query.exec(
                f"""
                DELETE FROM categories WHERE id={category_id};
                """
            )

            self.load_categories()

    def delete_task(self):
        query = QSqlQuery()

        row = self.tasks_list.currentRow()
        task_id = self.tasks[row][0]

        message_box = QMessageBox()
        message_box.setText(f"Вы точно хотите удалить задачу: {self.tasks[row][1]}?")
        message_box.setWindowTitle("Удаление задачи")
        message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        message_box.show()
        result = message_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            query.exec(
                f"""
                        DELETE FROM tasks WHERE id={task_id};
                        """
            )

            self.load_tasks()

    def edit_category(self):
        query = QSqlQuery()

        row = self.category_list.currentRow()
        category_id = self.categories[row][0]

        name = self.category_name.text()

        query.exec(
            f"""
            UPDATE categories SET name='{name}' WHERE id={category_id};
            """
        )

        self.load_categories()

    def edit_task(self):
        query = QSqlQuery()

        row = self.tasks_list.currentRow()
        task_id = self.tasks[row][0]

        name = self.task_name.text()
        description = self.task_description.toPlainText()
        status = self.task_status.text().replace('+', 'True').replace('-', 'False')
        cat_row = self.category_list.currentRow()
        category_id = self.categories[cat_row][0]

        print(1)

        query.exec(
            f"""
            UPDATE tasks SET name='{name}', description='{description}', active={status}, category_id={category_id}
            WHERE id={task_id};
            """
        )

        self.load_tasks()

    def active_tasks(self):
        query = QSqlQuery()
        query.exec(
            """
            SELECT * FROM tasks WHERE active = 1;
            """
        )

        self.tasks = []
        count = query.record().count()

        while query.next():
            temp = []

            for i in range(count):
                temp.append(query.value(i))

            self.tasks.append(temp)

        self.tasks_list.clear()

        for task in self.tasks:
            self.tasks_list.addItem(QListWidgetItem(task[1]))

    def completed_tasks(self):
        query = QSqlQuery()
        query.exec(
            """
            SELECT * FROM tasks WHERE active = 0;
            """
        )

        self.tasks = []
        count = query.record().count()

        while query.next():
            temp = []

            for i in range(count):
                temp.append(query.value(i))

            self.tasks.append(temp)

        self.tasks_list.clear()

        for task in self.tasks:
            self.tasks_list.addItem(QListWidgetItem(task[1]))


if __name__ == '__main__':
    conn = QSqlDatabase.addDatabase('QSQLITE')
    conn.setDatabaseName('task_list_3')
    conn.open()

    app = QApplication(sys.argv)
    window = MainWindow()

    print(conn.tables())

    window.show()
    app.exec()
