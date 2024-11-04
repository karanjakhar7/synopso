class PDFParser:
    def __init__(self, parser="pypdf"):
        self.parser = parser

        assert self.parser in ["pypdf"], "Parser not supported"

    def py_pdf_parser(self, pdf_path):
        from pypdf import PdfReader

        reader = PdfReader(pdf_path)
        text = ""
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text += "\n" + page.extract_text()
        return text

    def extract_text(self, pdf_path):
        if self.parser == "pypdf":
            return self.py_pdf_parser(pdf_path)
        else:
            raise ValueError("Parser not supported")
