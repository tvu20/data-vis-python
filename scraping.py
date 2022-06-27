import re
from bs4 import BeautifulSoup

with open("./input/war-and-peace-full-text.html", "r") as f:
    doc = BeautifulSoup(f, "html.parser")
elements = doc.findAll("div", class_="chapter")

chapters = []
book = ''

total = 0

for container in elements:
    title = container.find("h2").text

    if "BOOK" in title:
        num = re.search('BOOK (.+):', title)
        book = num.group(1)

    if "CHAPTER" in title:
        chapter = re.search('CHAPTER (.+)', title).group(1)
        chapters.append({
            'Book': book,
            'Chapter': chapter
        })

        pierre = 0

        paragraphs = container.findAll("p")
        for pg in paragraphs:
            pgText = pg.text
            pierre += pgText.count('Pierre')
        total += pierre

        chapters.append({
            'Book': book,
            'Chapter': chapter,
            'Pierre': pierre
        })

print(total)

with open('out.txt', 'w') as f:
    print(chapters, file=f)
