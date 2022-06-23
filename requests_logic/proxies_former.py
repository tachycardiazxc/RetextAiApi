import requests
from bs4 import BeautifulSoup
import base64


class Proxies:

    def __init__(self):

        self.url = "http://free-proxy.cz/ru/proxylist/country/all/https/uptime/all"
        self.ips_and_ports_list = []

    def get_pages(self, page_n):
        k = 0
        for n in range(1, page_n + 1):
            if k < 1:
                html = requests.get(url=f"{self.url}/{n}")
                ports_list, ips_list = self.parse_ip_and_port(html=html.text)
                self.write_ip_and_ports(ports=ports_list, ips=ips_list)
            else:
                break
            k += 1

    def write_ip_and_ports(self, ports, ips):
        for n in range(len(ports)):
            self.ips_and_ports_list.append(f"http://{ips[n]}:{ports[n]}")

    @staticmethod
    def parse_ip_and_port(html):
        soup = BeautifulSoup(html, "lxml")
        ports = soup.find_all(attrs={"class": "fport"})
        ports_list = []
        for port in ports:
            ports_list.append(port.text)
        ips = soup.find_all(name="td", attrs={"class": "left"})
        ips_list = []
        for ip in ips:
            temp_ip = str(ip.previous_element.find("script"))
            if temp_ip == "-1":
                continue
            temp_ip = Proxies.stripper(text=temp_ip)
            decoded_ip = base64.b64decode(temp_ip).decode()
            ips_list.append(decoded_ip)
        return ports_list, ips_list

    @staticmethod
    def stripper(text):
        quotes_count = 0
        final_text = ""
        for elem in text:
            if elem == '"':
                quotes_count += 1
                continue
            if quotes_count != 3:
                pass
            elif quotes_count == 3:
                final_text += elem
            elif quotes_count > 3:
                break
        return final_text
