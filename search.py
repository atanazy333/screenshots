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
            raise FileNotFoundError(f"The directory {search_dir} does not exist.")
    
    def search(self, query: str, use_regex: bool = False) -> List[Path]:
        """
        Searches for images containing the specified text.
        
        Args:
            query: The text to search for
            use_regex: Whether to use regular expressions
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
                logger.error(f"Error reading {image_path.name}: {e}")
        
        return results

    def display_results(self, paths: List[Path]):
        """Displays the found images"""
        if not paths:
            print("No matching images found.")
            return
            
        print(f"\nFound {len(paths)} images:")
        for path in paths:
            print(f"- {path.name}")
            try:
                Image.open(path).show()
            except Exception as e:
                logger.error(f"Cannot display {path.name}: {e}")

def main():
    searcher = ImageSearcher()
    query = input("Enter text to search for in the image: ")
    results = searcher.search(query, use_regex=True)
    searcher.display_results(results)

if __name__ == "__main__":
    main()
