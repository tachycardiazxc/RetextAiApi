import time
import requests
from .proxies_former import Proxies


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

        self.is_deny = False

        self.https_proxies = []
        self.proxies = {}

        self.url_proxies = None

    def send_queue(self, source, lang):
        data = {
            "source": source,
            "lang": lang
        }
        print(self.proxies)
        if not self.is_deny:
            status = requests.post(url=self.url, json=data)
        else:
            self.form_proxies()
            if self.url_proxies is None:
                self.url_proxies = self.return_proxies(https_proxies=self.https_proxies)
            try:
                status = requests.post(url=self.url, json=data, proxies=self.proxies, timeout=5)
                if status.json().get("status") == "limit_exceeded":
                    print(status.json())
                    url = next(self.url_proxies)
                    self.proxies["http"] = url
                    return self.send_queue(source=source, lang=lang)
            except Exception:
                url = next(self.url_proxies)
                self.proxies["http"] = url
                return self.send_queue(source=source, lang=lang)

        response_data = status.json()
        if status.status_code == 200 and not self.is_deny:
            try:
                return response_data.get("data").get("taskId")
            except AttributeError:
                self.is_deny = True
                return self.send_queue(source=source, lang=lang)
        elif status.status_code == 400:
            raise NotAvailableException(message=self.errors_messages, errors=self.errors)

    def form_proxies(self):
        p = Proxies()
        p.get_pages(page_n=5)
        self.https_proxies = p.ips_and_ports_list

    @staticmethod
    def return_proxies(https_proxies):
        for url in https_proxies:
            yield url

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
