# To-Do List Mobile Android App with KivyMD

## Overview
This is a simple To-Do List mobile application built using the KivyMD framework. The app allows users to add, edit, and delete tasks, each with a title, description, due date, priority, and category. The tasks are stored in a SQLite database.

## Prerequisites
- Python installed on your system.
- Kivy and KivyMD libraries installed. You can install them using the following commands:
  ```
  pip install kivy
  pip install kivymd
  ```

## How to Run the App
1. Ensure that you have Python, Kivy, and KivyMD installed on your system.
2. Download or copy the provided code into a file, e.g., `todo_app.py`.
3. Open a terminal or command prompt in the directory containing the `todo_app.py` file.
4. Run the app by executing the following command:
   ```
   python todo_app.py
   ```

## Features
- **Add Task**: Click the "Add Task" button to open a dialog for entering task details. Required fields are marked with an asterisk.
- **Edit Task**: Click on a task in the list to open a dialog for editing its details.
- **Delete Task**: In the task options dialog, you can delete a task.
- **Task List**: Displays a list of tasks with their titles and secondary information.
- **SQLite Database**: Tasks are stored in an SQLite database (`tasks.db`).

## Customization
- You can customize the appearance of the app by modifying the KivyMD theme settings in the `TodoApp` class.
- The SQLite database connection and schema are defined in the `TaskDB` class. You can customize the database structure or connection details if needed.

## Contributing
Feel free to contribute to the project by submitting issues or pull requests. Your feedback and improvements are highly appreciated.

**Note**: Ensure that you have the necessary permissions to access and modify SQLite databases on your system. The provided code assumes a basic understanding of Python and KivyMD.

## App overview 
<img width="260" alt="image" src="https://github.com/Subhra46/Todo-App/assets/84471896/85015941-c9bf-4c06-b454-51a58790fde7">

## Adding task
<img width="286" alt="image" src="https://github.com/Subhra46/Todo-App/assets/84471896/69a92230-f3de-4ae7-b494-583d5ffaff1b">

## Operations in Todo App
<img width="241" alt="image" src="https://github.com/Subhra46/Todo-App/assets/84471896/95381f83-9332-4c86-86f4-d98bb8f337da">

## Editing the Todo App
<img width="193" alt="image" src="https://github.com/Subhra46/Todo-App/assets/84471896/3005d26f-8750-4a5a-9985-1aa4c05d3f2a">

## After Editing
<img width="238" alt="image" src="https://github.com/Subhra46/Todo-App/assets/84471896/ff944656-ada2-4ec3-9604-af6af5926ca6">

## After delete operation
<img width="232" alt="image" src="https://github.com/Subhra46/Todo-App/assets/84471896/a1d4ccf5-4ad4-4259-96c1-047db4a89966">



