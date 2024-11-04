import asyncio
from .fetch_papers import fetch_papers_hf
from .parsers.pdf_parser import PDFParser
from .summarizers.summarize import summarize_paper_with_oai
from .models import Paper
from typing import List
from tqdm import tqdm


pdf_parser = PDFParser("pypdf")

async def summarize_batch(papers: List[Paper], batch_size: int = 5):
    """Process papers in batches asynchronously"""
    total_batches = (len(papers) + batch_size - 1) // batch_size  # ceiling division
    for i in tqdm(range(0, len(papers), batch_size), total=total_batches, desc="Processing batches"):
        batch = papers[i : i + batch_size]
        tasks = [summarize_paper_with_oai(paper) for paper in batch]
        summaries = await asyncio.gather(*tasks)
        for paper, summary in zip(batch, summaries):
            paper.summary = summary


async def main():
    papers = fetch_papers_hf()
    await summarize_batch(papers)

    # TODO: Save papers to database or file or do something with them


def run_main():
    asyncio.run(main())


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
    paper.summary = asyncio.run(summarize_paper_with_oai(paper))
    print(paper.summary)


if __name__ == "__main__":
    from argparse import ArgumentParser
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--test", action="store_true")

    args = arg_parser.parse_args()  # This line is missing in your code
    
    if args.test:
        test()
    else:
        run_main()
