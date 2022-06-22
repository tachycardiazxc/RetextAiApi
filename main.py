from requests_logic.queue_paraphrase import QueueParaphrase


class ReText:

    def __init__(self, text, lang):

        self.text = text
        self.lang = lang

        self.qp = QueueParaphrase()

        self.final_text = {}

    def start(self):

        split_text = self.split_text_by_dot()

        for text in split_text:
            task_id = self.qp.send_queue(source=text+".", lang=self.lang)
            response = self.qp.queue_check(task_id=task_id)
            self.create_final_text(result_text=response, sent_text=text)

    def split_text_by_dot(self):
        return self.text.split(".")

    def create_final_text(self, result_text, sent_text):
        self.final_text[sent_text] = result_text


if __name__ == "__main__":
    text = open('test.txt').readline()
    lang = "ru"
    rt = ReText(text=text, lang=lang)
    rt.start()
    print(rt.final_text)
