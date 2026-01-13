# loader.py
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
import logging

# Logger beállítása
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_documents(data_dir: str):
    """
    Betölti a PDF-eket a megadott mappából.
    Paraméterek:
        data_dir: PDF-ek mappája (abszolút vagy relatív)
    Visszatér:
        list of Document objektumok
    """
    documents = []

    data_path = Path(data_dir)
    if not data_path.exists() or not data_path.is_dir():
        logger.warning(f"Directory not found: {data_dir}")
        return documents

    pdf_files = list(data_path.glob("*.pdf"))
    if not pdf_files:
        logger.warning(f"No PDF files found in {data_dir}")
        return documents

    for pdf in pdf_files:
        logger.info(f"Loading document: {pdf.name}")
        loader = PyPDFLoader(str(pdf))
        try:
            docs = loader.load()  # Document objektumok
            documents.extend(docs)
        except Exception as e:
            logger.error(f"Failed to load {pdf.name}: {e}")

    logger.info(f"Loaded {len(documents)} pages total")
    return documents