import asyncio
from pathlib import Path
from .fetch_papers import fetch_papers_hf
from .parsers.pdf_parser import PDFParser
from .summarizers.summarize import summarize_paper_with_ai
from .models import Paper
from typing import List
from tqdm import tqdm
from .share.telegram import send_message_on_telegram


pdf_parser = PDFParser("pypdf")


async def summarize_batch(papers: List[Paper], batch_size: int = 5):
    """Process papers in batches asynchronously"""
    total_batches = (len(papers) + batch_size - 1) // batch_size
    for i in tqdm(
        range(0, len(papers), batch_size),
        total=total_batches,
        desc="Processing batches",
    ):
        batch = papers[i : i + batch_size]
        tasks = [summarize_paper_with_ai(paper) for paper in batch]
        summaries = await asyncio.gather(*tasks)
        for paper, summary in zip(batch, summaries):
            paper.summary = summary


def cleanup_papers(papers: List[Paper]):
    for paper in papers:
        path = Path(paper.filepath_local)
        if path.exists():
            path.unlink()


async def main(cleanup: bool = False):
    papers = fetch_papers_hf()

    for paper in papers:
        paper.text = pdf_parser.extract_text(paper.filepath_local)

    await summarize_batch(papers)

    for paper in papers:
        content = (
            f"*{paper.title}*\n{paper.authors}\n\n{paper.summary}\nLink: {paper.url}"
        )
        await send_message_on_telegram(content)

    if cleanup:
        cleanup_papers(papers)


def run_main(cleanup: bool = False):
    asyncio.run(main(cleanup=cleanup))


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
    paper.summary = asyncio.run(summarize_paper_with_ai(paper))
    print(paper.summary)

    content = f"*{paper.title}*\n{paper.authors}\n\n{paper.summary}\nLink: {paper.url}"
    asyncio.run(send_message_on_telegram(content))


if __name__ == "__main__":
    from argparse import ArgumentParser

    arg_parser = ArgumentParser()
    arg_parser.add_argument("--test", action="store_true")
    arg_parser.add_argument("--cleanup", action="store_true", help="Delete downloaded PDFs after processing")

    args = arg_parser.parse_args()

    if args.test:
        test()
    else:
        run_main(cleanup=args.cleanup)
