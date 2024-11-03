from .fetch_papers import fetch_papers_hf
from .parsers.pdf_parser import PDFParser
from .summarizers.summarize import summarize_paper_with_oai
from .models import Paper


pdf_parser = PDFParser("pypdf")

def main():
    papers = fetch_papers_hf()

    for paper in papers:
        paper.summary = summarize_paper_with_oai(paper)
    
    


def test():
    from pathlib import Path
    SCRIPT_DIR = Path(__file__).resolve().parent
    TEST_DIR = SCRIPT_DIR.parent / "test"
    paper = Paper(
        url="https://arxiv.org/abs/2201.00001",
        title="Test paper",
        authors="Test author",
        filepath_local=TEST_DIR / "test.pdf",
    )
    paper.text = pdf_parser.extract_text(paper.filepath_local)
    paper.summary = summarize_paper_with_oai(paper)
    print(paper.summary)

if __name__ == "__main__":
    test()