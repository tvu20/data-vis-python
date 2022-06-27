# imports
import re
import json
from bs4 import BeautifulSoup

# general info
general = {
    "title": "",
    "author": "",
    "wordcount": 0,
    "characters": {},
    "themes": [],
    "places": []
}

# character file
f = open("input/characters.json")
characterData = json.load(f)
f.close()
for char in characterData:
    general["characters"][char["name"]] = 0

# themes
f = open("input/themes.json")
themes = json.load(f)
f.close()
for t in themes:
    general["themes"].append(t["name"])

# places
f = open("input/places.json")
places = json.load(f)
f.close()
for p in places:
    general["places"].append(p)

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
            'wordcount': 0,
            "characters": {},
            "themes": {},
            "places": {}
        }

        # character data
        for char in characterData:
            curr["characters"][char["name"]] = 0

        # themes
        for t in themes:
            curr["themes"][t["name"]] = 0

        # places
        for p in places:
            curr["places"][p] = 0

        paragraphs = container.findAll("p")
        for p in paragraphs:
            text = p.text

            # word count
            curr["wordcount"] += len(re.findall(r'\w+', text))

            # characters
            for char in characterData:
                for a in char["aliases"]:
                    num = text.count(a)
                    curr["characters"][char["name"]] += num
                    general["characters"][char["name"]] += num

            # themes
            for t in themes:
                for a in t["aliases"]:
                    num = text.count(a)
                    curr["themes"][t["name"]] += num

            # themes
            for p in places:
                num = text.count(p)
                curr["places"][p] += num

        general["wordcount"] += curr["wordcount"]
        chapters.append(curr)

with open('general-info.txt', 'w') as f:
    print(general, file=f)

with open('chapter-detail.txt', 'w') as f:
    print(chapters, file=f)
