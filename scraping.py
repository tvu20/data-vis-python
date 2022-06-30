# imports
import re
import json
from bs4 import BeautifulSoup

# general info
general = {
    "title": "",
    "author": "",
    "sections": 0,
    "wordcount": 0,
    "characters": {},
    "themes": [],
    "places": []
}

# book themes
bookThemes = []
currentBookThemes = {"book": ""}

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
    currentBookThemes[t["name"]] = 0

print(currentBookThemes)
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

culmulative = 0

for container in elements:
    title = container.find("h2").text

    if "BOOK" in title:
        num = re.search('BOOK (.+):', title)
        book = num.group(1)
        general["sections"] += 1

        bookThemes.append(currentBookThemes.copy())
        for k in currentBookThemes: currentBookThemes[k] = 0
        currentBookThemes["book"] = book
        continue

    if "EPILOGUE" in title:
        num = re.search('(.+):', title)
        book = num.group(1).strip()
        general["sections"] += 1

        bookThemes.append(currentBookThemes.copy())
        for k in currentBookThemes: currentBookThemes[k] = 0
        currentBookThemes["book"] = book
        continue

    if "CHAPTER" in title:
        chapter = re.search('CHAPTER (.+)', title).group(1)

        culmulative += 1

        curr = {
            'book': book,
            'chapter': chapter,
            'total': culmulative,
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
                    currentBookThemes[t["name"]] += num

            # themes
            for p in places:
                num = text.count(p)
                curr["places"][p] += num

        general["wordcount"] += curr["wordcount"]
        chapters.append(curr)

bookThemes.append(currentBookThemes.copy())

# writing out to json
general_obj = json.dumps(general, indent=4)
with open("output/general-info.json", "w") as outfile:
    outfile.write(general_obj)

detail_obj = json.dumps(chapters, indent=4)
with open("output/chapter-detail.json", "w") as outfile:
    outfile.write(detail_obj)

theme_obj = json.dumps(bookThemes, indent=4)
with open("output/theme-details.json", "w") as outfile:
    outfile.write(theme_obj)

# with open('general-info.txt', 'w') as f:
#     print(general, file=f)

# with open('chapter-detail.txt', 'w') as f:
#     print(chapters, file=f)
