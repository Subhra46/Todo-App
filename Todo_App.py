from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem, MDList
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import sqlite3

class TaskDB:
    def __init__(self):
        self.connection = sqlite3.connect("tasks.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                due_date TEXT,
                priority TEXT,
                category TEXT,
                status TEXT
            )
            """
        )
        self.connection.commit()

    def add_task(self, title, description, due_date, priority, category, status):
        self.cursor.execute(
            """
            INSERT INTO tasks (title, description, due_date, priority, category, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, description, due_date, priority, category, status),
        )
        self.connection.commit()

    def get_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()

    def update_task(self, task_id, title, description, due_date, priority, category, status):
        self.cursor.execute(
            """
            UPDATE tasks SET title=?, description=?, due_date=?, priority=?, category=?, status=?
            WHERE id=?
            """,
            (title, description, due_date, priority, category, status, task_id),
        )
        self.connection.commit()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.connection.commit()

class AddTaskContent(GridLayout):
    cols = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title_text_field = MDTextField(
            hint_text="Title", required=True, helper_text="*Required"
        )
        self.description_text_field = MDTextField(
            hint_text="Description", required=False, multiline=True
        )
        self.due_date_text_field = MDTextField(
            hint_text="Due Date (YYYY-MM-DD)", required=False
        )
        self.priority_spinner = MDTextField(
            hint_text="Priority", helper_text="Low, Medium, High", required=False
        )
        self.category_text_field = MDTextField(
            hint_text="Category", required=False
        )

        self.add_widget(self.title_text_field)
        self.add_widget(self.description_text_field)
        self.add_widget(self.due_date_text_field)
        self.add_widget(self.priority_spinner)
        self.add_widget(self.category_text_field)

    def clear_fields(self):
        self.title_text_field.text = ""
        self.description_text_field.text = ""
        self.due_date_text_field.text = ""
        self.priority_spinner.text = ""
        self.category_text_field.text = ""

class TodoApp(MDApp):
    def build(self):
        self.task_db = TaskDB()
        self.theme_cls.primary_palette = "BlueGray"
        self.screen = MDScreen()

        self.task_list = MDList()
        self.load_tasks()

        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.task_list)

        self.add_task_button = Button(
            text="Add Task",
            on_press=self.show_add_task_dialog,
            size_hint=(None, None),
            size=(150, 50),
            bold=True,
        )

        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.layout.add_widget(self.scroll_view)
        self.layout.add_widget(self.add_task_button)

        self.screen.add_widget(self.layout)
        return self.screen

    def load_tasks(self):
        tasks = self.task_db.get_tasks()
        for task in tasks:
            self.add_task_to_list(task)

    def add_task_to_list(self, task):
        task_item = OneLineAvatarIconListItem(
            text=task[1], secondary_text=task[2], on_release=self.show_task_options
        )
        task_item.task_details = task
        self.task_list.add_widget(task_item)

    def show_add_task_dialog(self, *args):
        self.dialog = MDDialog(
            title="Add Task",
            type="custom",
            content_cls=AddTaskContent(),
            size_hint=(0.8, 0.8),
            buttons=[
                MDFlatButton(
                    text="Cancel", on_release=lambda *x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="Add", on_release=lambda *x: self.add_task_and_dismiss()
                ),
            ],
        )
        self.dialog.open()

    def add_task_and_dismiss(self):
        task_content = self.dialog.content_cls
        title = task_content.title_text_field.text
        if title:
            description = task_content.description_text_field.text
            due_date = task_content.due_date_text_field.text
            priority = task_content.priority_spinner.text
            category = task_content.category_text_field.text
            status = "New"

            self.task_db.add_task(
                title, description, due_date, priority, category, status
            )
            self.add_task_to_list(
                (
                    None,
                    title,
                    description,
                    due_date,
                    priority,
                    category,
                    status,
                )
            )
            task_content.clear_fields()
            self.dialog.dismiss()

    def show_task_options(self, task_item):
        task_details = task_item.task_details
        priority_text = f"Priority: {task_details[4]}"
        due_date_text = f"Due Date: {task_details[3]}"
        description_text = f"Description: {task_details[2]}"
        full_text = f"{priority_text}\n{due_date_text}\n{description_text}"

        options_dialog = MDDialog(
            title="Task Options",
            size_hint=(0.8, 0.4),
            text=full_text,
            buttons=[
                MDFlatButton(
                    text="Edit", on_release=lambda *x: self.show_edit_task_dialog(task_details)
                ),
                MDFlatButton(
                    text="Delete", on_release=lambda *x: self.delete_task(task_details)
                ),
                MDFlatButton(text="Cancel", on_release=lambda *x: options_dialog.dismiss()),
            ],
        )
        options_dialog.open()

    def show_edit_task_dialog(self, task_details):
        self.dialog = MDDialog(
            title="Edit Task",
            type="custom",
            content_cls=AddTaskContent(),
            size_hint=(0.8, 0.8),
            buttons=[
                MDFlatButton(
                    text="Cancel", on_release=lambda *x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="Save", on_release=lambda *x: self.edit_task_and_dismiss(task_details)
                ),
            ],
        )
        self.dialog.content_cls.title_text_field.text = task_details[1]
        self.dialog.content_cls.description_text_field.text = task_details[2]
        self.dialog.content_cls.due_date_text_field.text = task_details[3]
        self.dialog.content_cls.priority_spinner.text = task_details[4]
        self.dialog.content_cls.category_text_field.text = task_details[5]

        self.dialog.open()

    def edit_task_and_dismiss(self, task_details):
        task_content = self.dialog.content_cls
        title = task_content.title_text_field.text
        if title:
            description = task_content.description_text_field.text
            due_date = task_content.due_date_text_field.text
            priority = task_content.priority_spinner.text
            category = task_content.category_text_field.text
            status = task_details[6]

            self.task_db.update_task(
                task_details[0], title, description, due_date, priority, category, status
            )

            self.task_list.clear_widgets()
            self.load_tasks()
            task_content.clear_fields()
            self.dialog.dismiss()

    def delete_task(self, task_details):
        self.task_db.delete_task(task_details[0])
        self.task_list.clear_widgets()
        self.load_tasks()

if __name__ == "__main__":
    TodoApp().run()
