from tkinter import *
from tkinter import messagebox
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


class Account:
    def __init__(self, username, password):
        self._username = username
        self._password = password

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    def is_valid(self, accounts):
        return any(account.username == self._username and account.password == self._password for account in accounts)


class SEOAnalyzer:
    def __init__(self, url, keywords):
        self.url = url
        self.keywords = keywords
        self.soup = None
        self.external_links_count = 0
        self.internal_links_count = 0
        self.alt_tags_percentage = 0
        self.keywords_found = []
        self.report = None

    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            messagebox.showerror("Error", f"An error occurred while fetching the page: {e}")

    def count_links(self):
        if self.soup is None:
            return
        parsed_uri = urlparse(self.url)
        base_domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        for link in self.soup.find_all('a', href=True):
            if link['href'].startswith(base_domain) or link['href'].startswith('/'):
                self.internal_links_count += 1
            else:
                self.external_links_count += 1

    def calculate_alt_tags(self):
        images = self.soup.find_all('img')
        images_with_alt = [img for img in images if img.get('alt')]
        if images:
            self.alt_tags_percentage = (len(images_with_alt) / len(images)) * 100

    def analyze_keywords(self):
        text = self.soup.get_text().lower()
        for keyword in self.keywords:
            if keyword.lower() in text:
                self.keywords_found.append(keyword)

    def analyze(self):
        self.fetch_page()
        self.count_links()
        self.calculate_alt_tags()
        self.analyze_keywords()

    def get_report(self):
        return self.report


class MainUI(Tk):
    def __init__(self, valid_accounts):
        super().__init__()
        self.title("SEO Analyzer")
        self.geometry("400x300")
        self.analyzer = None
        self.valid_accounts = valid_accounts
        self.create_widgets()

    def create_widgets(self):
        Label(self, text="URL:").pack()
        self.url_entry = Entry(self, width=50)
        self.url_entry.pack()

        Label(self, text="Keywords (comma-separated):").pack()
        self.keywords_entry = Entry(self, width=50)
        self.keywords_entry.pack()

        analyze_button = Button(self, text="Analyze", command=self.launch_analysis)
        analyze_button.pack()

    def launch_analysis(self):
        url = self.url_entry.get()
        keywords = [kw.strip() for kw in self.keywords_entry.get().split(',')]
        self.analyzer = SEOAnalyzer(url, keywords)
        self.analyzer.analyze()
        self.show_report()

    def show_report(self):
        report_ui = ReportUI(self.analyzer)
        report_ui.mainloop()


class ReportUI(Toplevel):
    def __init__(self, analyzer):
        super().__init__()
        self.title("SEO Report")
        self.analyzer = analyzer
        self.create_widgets()

    def create_widgets(self):
        report = f"External Links: {self.analyzer.external_links_count}\n"
        report += f"Internal Links: {self.analyzer.internal_links_count}\n"
        report += f"Alt Tags Percentage: {self.analyzer.alt_tags_percentage}%\n"
        report += f"Keywords Found: {', '.join(self.analyzer.keywords_found)}"
        Label(self, text=report).pack(padx=10, pady=10)


if __name__ == "__main__":
    valid_accounts = [Account('user1', 'pass1'), Account('user2', 'pass2')]
    app = MainUI(valid_accounts)
    app.mainloop()
