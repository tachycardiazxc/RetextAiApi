import time
import requests


class QueueParaphrase:

    def __init__(self):

        self.errors_messages = {
            "nae": "The service currently unavailable, or my code is outdated."
        }
        self.errors = {
            "nae": "Could not establish connection with ReText."
        }

        self.url = "https://api.retext.ai/api/v1/queue_paraphrase"
        self.url_check = "https://api.retext.ai/api/v1/queue_check?taskId="
        self.task_id = ""

    def send_queue(self, source, lang):
        data = {
            "source": source,
            "lang": lang
        }
        status = requests.post(url=self.url, json=data)
        response_data = status.json()
        if status.status_code == 200:
            return response_data.get("data").get("taskId")
        elif status.status_code == 400:
            raise NotAvailableException(message=self.errors_messages, errors=self.errors)

    def queue_check(self, task_id):
        status = requests.get(url=self.url_check+task_id)
        data = status.json()
        ready = False
        if status.status_code == 200:
            ready = self.is_ready(data=data.get("data").get("ready"))
        elif status.status_code == 400:
            raise NotAvailableException(message=self.errors_messages, errors=self.errors)
        if not ready:
            time.sleep(0.25)
            return self.queue_check(task_id=task_id)
        return data.get("data").get("result")

    @staticmethod
    def is_ready(data):
        if not data:
            return False
        elif data:
            return True


class NotAvailableException(Exception):

    def __init__(self, message, errors):
        super().__init__(message)

        self.errors = errors
