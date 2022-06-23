from requests_logic.queue_paraphrase import QueueParaphrase


class ReText:

    def __init__(self, text, lang):

        self.text = text
        self.lang = lang

        self.qp = QueueParaphrase()

        self.final_text = {}

    def start(self):

        if type(self.text) != list:
            split_text = self.split_text_by_dot()
            split_text = self.remove_garbage_from_text(split_text)
        else:
            split_text = []
            for text in self.text:
                temp_split_text = self.split_text_by_dot(text=text)
                temp_split_text = self.remove_garbage_from_text(temp_split_text)
                split_text.append(temp_split_text[0])

        k = len(split_text)
        for text in split_text:
            task_id = self.qp.send_queue(source=text+".", lang=self.lang)
            response = self.qp.queue_check(task_id=task_id)
            self.create_final_text(result_text=response, sent_text=text)
            print(k)
            k -= 1
        print("Your text is ready!\n")
        print("-" * 20)

    @staticmethod
    def remove_garbage_from_text(text):
        try:
            text.remove("")
        except ValueError:
            pass
        try:
            text.remove("\n")
        except ValueError:
            pass
        return text

    def split_text_by_dot(self, text=None):
        if text is None:
            return self.text.split(".")
        else:
            return text.split(".")

    def create_final_text(self, result_text, sent_text):
        self.final_text[sent_text] = result_text

    def choose_variant(self):
        keys = self.final_text.keys()
        filtered_text = str()
        for key in keys:
            variants = self.final_text.get(key)
            for variant in range(len(variants)):
                print(f"{variant}: {variants[variant]}")
            user_number = int(input("Chose variant by number: "))
            filtered_text += variants[user_number] + " "
        return filtered_text


if __name__ == "__main__":
    text = open('text.txt', encoding="utf-8").readlines()
    lang = "ru"
    rt = ReText(text=text, lang=lang)
    rt.start()
    print(rt.choose_variant())
