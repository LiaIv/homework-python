from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os

class TaskManager:
    TASKS_FILE = "tasks.txt"

    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.TASKS_FILE):
            with open(self.TASKS_FILE, "r", encoding="utf-8") as file:
                try:
                    content = file.read().strip()
                    self.tasks = json.loads(content) if content else []
                except json.JSONDecodeError:
                    print("Ошибка чтения tasks.txt. Файл будет перезаписан.")
                    self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        with open(self.TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(self.tasks, file, ensure_ascii=False, indent=4)

    def add_task(self, title, priority):
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
            response = json.dumps(self.task_manager.tasks).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)
        else:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()

    def do_POST(self):
        if self.path == "/tasks":
            content_length = self.get_content_length()
            if content_length is None:
                self.send_response(411)  # Length Required
                self.end_headers()
                self.wfile.write(b"Content-Length header is missing.")
                return

            try:
                body = self.rfile.read(content_length)
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON data.")
                return

            if "title" not in data or "priority" not in data:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing 'title' or 'priority' in data.")
                return

            new_task = self.task_manager.add_task(data["title"], data["priority"])
            response = json.dumps(new_task).encode("utf-8")
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)
            
        elif self.path.startswith("/tasks/") and self.path.endswith("/complete"):
            try:
                task_id_str = self.path.split("/")[2]
                task_id = int(task_id_str)
            except (IndexError, ValueError):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid task ID.")
                return

            task = self.task_manager.complete_task(task_id)
            if task:
                self.send_response(200)
                self.send_header("Content-Length", "0")
                self.end_headers()
            else:
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()
                self.wfile.write(b"Task not found.")
        else:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()

    def get_content_length(self):
        content_length = self.headers.get("Content-Length")
        if content_length is None:
            return None
        try:
            return int(content_length)
        except ValueError:
            return None


def run():
    server_address = ("", 8000)
    httpd = ThreadingHTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Сервер запущен на порту 8000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("Сервер остановлен.")


if __name__ == "__main__":
    run()
