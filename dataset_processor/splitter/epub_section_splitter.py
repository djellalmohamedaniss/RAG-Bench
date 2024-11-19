import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from splitter import BaseSplitter


class EPubSectionSplitter(BaseSplitter):

    def __init__(self) -> None:
        super().__init__()

    def read(self, epub_path):
        return epub.read_epub(epub_path)

    def split(self, content: epub.EpubBook):
        content_by_title = {}
        for item in content.items:
            # Check if the item is a chapter
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Parse the HTML content
                soup = BeautifulSoup(item.get_content(), "html.parser")
                # Initialize current title
                current_title = "Untitled Section"
                content = ""
                for element in soup.find_all(True):  # Iterate over all elements
                    if element.name in ["h1", "h2", "h3"]:
                        # Save previous section content
                        if current_title and content.strip():
                            content_by_title[current_title] = content.strip()

                        # Start a new section
                        current_title = element.get_text(strip=True)
                        content = ""
                    else:
                        # Append content to the current section
                        content += element.get_text(strip=True) + "\n"

                # Save the last section
                if current_title and content.strip():
                    content_by_title[current_title] = content.strip()

        return content_by_title
