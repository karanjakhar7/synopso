from bs4 import BeautifulSoup
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor



url = "https://huggingface.co/papers"

SCRIPT_DIR = Path(__file__).resolve().parent

PDF_DIR = SCRIPT_DIR.parent / "papers"
PDF_DIR.mkdir(exist_ok=True, parents=True)


def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def download_arxiv_pdf(arxiv_id: str, dir: str = None):
    arxiv_pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    if dir is None:
        dir = PDF_DIR
    filename = dir / f"{arxiv_id}.pdf"
    download_pdf(arxiv_pdf_url, filename=filename)
    return filename.as_posix()

# def get_paper_info_arxiv_api(arxiv_id):
#     arxiv_api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
#     response = requests.get(arxiv_api_url)
#     soup = BeautifulSoup(response.content, 'html')
#     title = soup.find('title').text
#     authors = soup.find_all('author')
#     authors = [author.find('name').text for author in authors]
#     return title, authors

def get_paper_info(arxiv_id: str):
    arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
    response = requests.get(arxiv_url)
    soup = BeautifulSoup(response.content, 'xml')
    title = soup.find('h1', class_='title mathjax').text.replace("Title:", "").strip()
    authors = soup.find('div', class_='authors').text.replace("Authors:", "").strip()
    paper_info = {
        'title': title,
        'authors': authors
    }
    return paper_info


def fetch_paper_arxiv(arxiv_id: str):
    paper_info = get_paper_info(arxiv_id)
    filename_local = download_arxiv_pdf(arxiv_id)
    paper_info['filename_local'] = filename_local
    return paper_info


def fetch_papers_hf():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    arxiv_ids = []
    articles = soup.find_all('article')
    for article in articles:
        paper_path = article.find_all('a')[0].get('href')
        arxiv_id = paper_path.split('/')[-1]
        arxiv_ids.append(arxiv_id)

    
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(fetch_paper_arxiv, arxiv_ids)
    
    return results



def main():
    results = fetch_papers_hf()
    print(results)


if __name__ == "__main__":
    main()