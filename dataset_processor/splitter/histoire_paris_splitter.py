from ebooklib.epub import EpubBook
from splitter import EPubSectionSplitter


class HistoireParisSplitter(EPubSectionSplitter):

    def __init__(self) -> None:
        super().__init__()

    def split(self, content: EpubBook):
        sections = super().split(content)
        chapters = []
        start = False
        for title, content in sections.items():
            if title == "AVERTISSEMENT.":
                start = True
                continue
            if not start:
                continue
            if title == "TABLE DES MATIÈRES.":
                break
            chapters.append(content)
        return chapters
