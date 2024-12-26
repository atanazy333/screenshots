# search_images.py
from pathlib import Path
from PIL import Image
import logging
import re
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageSearcher:
    def __init__(self, search_dir: str = "./processed_images"):
        self.search_dir = Path(search_dir)
        if not self.search_dir.exists():
            raise FileNotFoundError(f"Katalog {search_dir} nie istnieje")
    
    def search(self, query: str, use_regex: bool = False) -> List[Path]:
        """
        Wyszukuje obrazy zawierające zadany tekst.
        
        Args:
            query: Tekst do wyszukania
            use_regex: Czy używać wyrażeń regularnych
        """
        query = query.lower()
        if use_regex:
            pattern = re.compile(re.escape(query))
        
        results = []
        for image_path in self.search_dir.glob('*.png'):
            try:
                with Image.open(image_path) as img:
                    ocr_text = img.info.get("OCR_Text", "").lower()
                    if use_regex:
                        if pattern.search(ocr_text):
                            results.append(image_path)
                    else:
                        if query in ocr_text:
                            results.append(image_path)
            except Exception as e:
                logger.error(f"Błąd odczytu {image_path.name}: {e}")
        
        return results

    def display_results(self, paths: List[Path]):
        """Wyświetla znalezione obrazy"""
        if not paths:
            print("Nie znaleziono pasujących obrazów.")
            return
            
        print(f"\nZnaleziono {len(paths)} obrazów:")
        for path in paths:
            print(f"- {path.name}")
            try:
                Image.open(path).show()
            except Exception as e:
                logger.error(f"Nie można wyświetlić {path.name}: {e}")

def main():
    searcher = ImageSearcher()
    query = input("Wprowadź tekst do wyszukania obrazu: ")
    results = searcher.search(query)
    searcher.display_results(results)

if __name__ == "__main__":
    main()