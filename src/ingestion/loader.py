import re
import pymupdf
import spacy
from pathlib import Path
from src.utils.multi_column import column_boxes 
from llama_index.core import Document

class Ingestion:
    
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.documents = []
        self.documents_metadata = {}

    def extract_title(self, doc: Document) -> str:
        '''
        Extract the title from the document.
        '''
        page = doc[0]
        blocks = page.get_text('dict')['blocks']
        title = ""
        for block in blocks[:10]:
            if block['type']==0:
                for line in block["lines"]:
                    # Ignoring the vertically aligned text
                    if line["dir"] != (0.0,1.0) and line["dir"] != (0,-1.0):
                        for span in line["spans"]:
                            if span["size"] > 12:
                                title += span["text"]
        return title if title else "Unknown Title"

    def extract_authors(self, doc: Document) -> str:
        '''
        Extract the authors from the document.
        '''
        first_page = doc[0]
        top_half = first_page.rect
        top_half.y1 = top_half.y1 / 2
        relevant_text = first_page.get_text(clip=top_half)
        nlp = spacy.load("en_core_web_sm")
        doc_nlp = nlp(relevant_text)
        authors = [ent.text for ent in doc_nlp.ents if ent.label_ == "PERSON"]
        return authors

    def extract_abstract(self, doc: Document) -> str:
        full_text = ""
        for page in doc[:2]:
            full_text += page.get_text()
        pattern = r'Abstract[.\s\-—]*\n?(.*?)(?=\n\s*\n|\b[IVXLCDM]+\.\s+Introduction|\d+\s+Introduction|\bIntroduction\b|\bKeywords:)'

        match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
        
        if match:
            abstract = match.group(1).strip()
            abstract = re.sub(r'\s+', ' ', abstract)
            return abstract[:1500]
        
        return "Abstract not found"

    def parse_pdfs(self, pdf_path: str, document_metadata: dict):
        '''
        Parse the pdf into LlamaIndex Document
        '''
        pdf_path = Path(pdf_path)
        doc = pymupdf.open(str(pdf_path))
        
        title = self.extract_title(doc)
        author = self.extract_authors(doc)
        abstract = self.extract_abstract(doc)

        document = []
        document_metadata[pdf_path.name] = {
            "title": title,
            "author": author,
            "abstract": abstract,
            "total_pages": len(doc),
        }
        for page_num, page in enumerate(doc):
            # Handle multi column page
            bboxes = column_boxes(page)
            curr_page_text = ""
            for rect in bboxes:
                curr_page_text += page.get_text(clip=rect, sort=True)
            cleaned_text = re.sub(r'\n+', ' ', curr_page_text)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            page_metadata = {
                "name":pdf_path.name,
                "title":title,
                "page_number": page_num+1
            }
            document.append(Document(
                text=cleaned_text,
                metadata=page_metadata,
                doc_id = pdf_path.stem,
            ))

        return document

    def parse_all_pdfs(self):
        pdf_dir = Path(self.dir_path)
        pdf_files = list(pdf_dir.glob(pattern="*.pdf"))
        print(f"Found {len(pdf_files)} PDFs in {pdf_dir}")

        for i, pdf_path in enumerate(pdf_files):
            print(f"{i+1}/{len(pdf_files)} Parsing: {pdf_path.name}")
            try:
                doc = self.parse_pdfs(pdf_path, self.documents_metadata)
                self.documents.extend(doc)
            except Exception as e:
                print(f"  ✗ Failed: {e}")
        return self.documents, self.documents_metadata

