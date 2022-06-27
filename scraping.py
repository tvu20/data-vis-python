from bs4 import BeautifulSoup

with open("./input/war-and-peace-full-text.html", "r") as f:
    doc = BeautifulSoup(f, "html.parser")


chapters = doc.findAll("div", class_="chapter")
# print(chapters)

for c in chapters:
    title = c.find("h2").text

    if "CHAPTER" in title:
        print(title)
