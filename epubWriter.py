# Epub writer
# Author: Dylan Thiemann
# Created Date: 1/30/20

from ebooklib import epub
from bs4 import BeautifulSoup
import random
import requests
import re
import html


class EpubBookWriter:

    def __init__(self, bookTitle, bookAuthor):
        super().__init__()

        self.book = epub.EpubBook()
        self.book.set_identifier(
            "id_" + str(random.randint(111111, 222222)) + "_" + bookTitle)

        self.book.set_title(bookTitle)
        self.book.add_author(bookAuthor)

        self.chapters = []

    def addChapter(self, title, html_content, number, lang="en"):
        fileName = "Chapter" + str(number) + ".html"
        chapter = epub.EpubHtml(title=title, file_name=fileName, lang=lang)
        chapter.content = (
            u"<html><body><p>%s<p></body></html>" % (html_content))
        self.chapters.append(chapter)
        self.book.add_item(chapter)

    def finalizeBook(self, outputFileName):

        # define CSS style
        style = 'BODY {color: white;}'
        nav_css = epub.EpubItem(
            uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

        # add CSS file
        self.book.add_item(nav_css)

        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        self.book.spine = ['nav', *self.chapters]

        epub.write_epub(outputFileName, self.book, {})


def main():
    book = EpubBookWriter(
        "Economy, Society, and Public Policy", "The Core Team")
    baseUrl = "https://www.core-econ.org/espp/book/text/%02d.html"
    for i in range(1, 13):
        print("Writing Chapter %d" % i)
        url = baseUrl % i
        r = requests.get(url)
        r.encoding = "utf-8"

        html = r.text
        soup = BeautifulSoup(html, features="lxml")

        # Find <h1> element
        h1TagText = soup.find("h1").getText()

        chapterTitle = re.sub(r'<strong>.*</strong>', "", str(h1TagText))
        content = str(soup.find("div", {"id": "content"}))
        book.addChapter(chapterTitle, content, i)

    print("Finalizing book")
    book.finalizeBook("test.epub")
    print("Done!")


main()
# x = "<strong>12</strong> asdfasdfasdfasdfa"
# print(re.sub(r'<strong>.*</strong>', "", x))
