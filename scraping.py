# imports
import re
import json
from bs4 import BeautifulSoup

# general info

general = {
    "title": "",
    "author": "",
    "characters": {}
}

# character file

f = open("input/characters.json")
characterData = json.load(f)
f.close()
for char in characterData:
    general["characters"][char["name"]] = 0

# beautiful soup

with open("./input/war-and-peace-full-text.html", "r") as f:
    doc = BeautifulSoup(f, "html.parser")
elements = doc.findAll("div", class_="chapter")

# finding metadata

currDiv = doc.find("div", text=re.compile('Title: (.+)'))
general["title"] = re.search('Title: (.+)', currDiv.text).group(1)

currDiv = doc.find("div", text=re.compile('Author: (.+)'))
general["author"] = re.search('Author: (.+)', currDiv.text).group(1)

# chapter detailed info

chapters = []
book = ''

for container in elements:
    title = container.find("h2").text

    if "BOOK" in title:
        num = re.search('BOOK (.+):', title)
        book = num.group(1)

    if "CHAPTER" in title:
        chapter = re.search('CHAPTER (.+)', title).group(1)

        curr = {
            'book': book,
            'chapter': chapter,
            "characters": {}
        }

        # character data
        for char in characterData:
            curr["characters"][char["name"]] = 0

        paragraphs = container.findAll("p")
        for p in paragraphs:
            text = p.text
            for char in characterData:
                for a in char["aliases"]:
                    num = text.count(a)
                    curr["characters"][char["name"]] += num
                    general["characters"][char["name"]] += num

        chapters.append(curr)

with open('general-info.txt', 'w') as f:
    print(general, file=f)

with open('chapter-detail.txt', 'w') as f:
    print(chapters, file=f)
