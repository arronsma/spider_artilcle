from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import logger


class RSC_article_abstract:
    def __init__(self):
        self.title = ""
        self.href = ""
        self.author = ""

    def print(self):
        print("title:{}, href:{}, author:{}".format(
            self.title, self.href, self.author))


class RSC_articleList_parser:
    def __init__(self, url):
        self.url = url
        self.article_list = []
        self.logger = logger.getDefaultLog()
        self.basic_url = "https://pubs.rsc.org/"
        self.cur_page = 0

    def parseUrl(self):
        web = webdriver.Chrome()
        web.get(self.url)
        sleep(2)

        self.parseHtml(web.page_source)
        self.output()
        
        for i in range(751) :
            nextCandidate = web.find_elements_by_tag_name("nav")
            sleep(3)
            while(True):
                try:
                    for candidate in nextCandidate :
                        if candidate.get_attribute("class") != "paging-control paging--right" :
                            continue
                        bottom = candidate.find_elements_by_tag_name("li")[1]
                        bottom.click()
                        break
                    break
                except:
                    print("error occur\n")
                    sleep(10)
                    nextCandidate = web.find_elements_by_tag_name("nav")

            sleep(3)
            self.parseHtml(web.page_source)
            self.output()

    def parseAbstract(self, t):
        articleInfo = t.find("a", class_="capsule__action")
        title = articleInfo.find("h3").text.strip()
        title.replace("–", "-")
        author = articleInfo.find("div", class_="article__authors article__author-link").text.strip()
        author.replace("–", "-")
        href = articleInfo.attrs['href']

        t_abstract = RSC_article_abstract()
        t_abstract.title = title
        t_abstract.author = author
        t_abstract.href = href
        self.article_list.append(t_abstract)

    def parseHtml(self, text):
        bs = BeautifulSoup(text, "html.parser")
        for i in bs.findAll(name='div', attrs={'class': "capsule capsule--article"}):
            self.parseAbstract(i)

    def print(self):
        for i in self.article_list:
            i.print()

    def output(self):
        with open("abstract_{}.txt".format(self.cur_page), 'w', encoding="utf-8") as f:
            for i in self.article_list:
                f.write("{}[sep]{}[sep]{}\n".format(i.title, i.author, i.href))
        self.cur_page += 1
        self.article_list.clear()


if __name__ == "__main__":
    url = "https://pubs.rsc.org/en/results/all?Category=All&AllText=MOF&IncludeReference=false&SelectJournal=false&DateRange=false&SelectDate=false&Type=Months&PriceCode=False&OpenAccess=false"
    parser = RSC_articleList_parser(url)
    parser.parseUrl()
    parser.print()
    parser.output()
