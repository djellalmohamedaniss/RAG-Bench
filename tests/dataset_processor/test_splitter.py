import pandas as pd

from dataset_processor.splitter import HistoireParisSplitter


def test_histoire_paris_splitter():
    file_path = "./datasets/tableau-historique-paris/1.epub"
    splitter = HistoireParisSplitter()
    content = splitter.read(file_path)
    assert len(splitter.split(content)) > 0
