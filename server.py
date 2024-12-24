from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

class TaskManager:
    TASKS_FILE = "tasks.txt"

    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Загружает задачи из файла."""
        if os.path.exists(self.TASKS_FILE):
            with open(self.TASKS_FILE, "r") as file:
                try:
                    content = file.read().strip()
                    self.tasks = json.loads(content) if content else []
                except json.JSONDecodeError:
                    print("Ошибка чтения tasks.txt. Файл будет перезаписан.")
                    self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        """Сохраняет задачи в файл."""
        with open(self.TASKS_FILE, "w") as file:
            json.dump(self.tasks, file)

    def add_task(self, title, priority):
        """Добавляет новую задачу."""
        new_task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "priority": priority,
            "isDone": False,
        }
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def complete_task(self, task_id):
        """Отмечает задачу как выполненную."""
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if task:
            task["isDone"] = True
            self.save_tasks()
            return task
        return None


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    task_manager = TaskManager()

    def do_GET(self):
        if self.path == "/tasks":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(self.task_manager.tasks).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/tasks":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            if "title" not in data or "priority" not in data:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid data")
                return

            new_task = self.task_manager.add_task(data["title"], data["priority"])
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(new_task).encode("utf-8"))
        elif self.path.startswith("/tasks/") and self.path.endswith("/complete"):
            try:
                task_id = int(self.path.split("/")[2])
            except ValueError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid task ID")
                return

            task = self.task_manager.complete_task(task_id)
            if task:
                self.send_response(200)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Task not found")
        else:
            self.send_response(404)
            self.end_headers()


def run():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Сервер запущен на порту 8000")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
