# process_images.py
from pathlib import Path
from PIL import Image, PngImagePlugin
import pytesseract
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self, 
                 input_dir: str = "./",
                 output_dir: str = "./processed_images",
                 tesseract_path: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
        self.input_path = Path(input_dir)
        self.output_path = Path(output_dir)
        self.output_path.mkdir(parents=True, exist_ok=True)
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
    def process_image(self, image_path: Path) -> Optional[Path]:
        """Przetwarza pojedynczy obraz, dodając metadane OCR"""
        if not image_path.suffix.lower() in ('.png', '.jpg', '.jpeg'):
            return None
            
        try:
            # Ekstrakcja tekstu
            text = pytesseract.image_to_string(
                Image.open(image_path), 
                lang='pol'
            ).strip()
            
            with Image.open(image_path) as img:
                meta = PngImagePlugin.PngInfo()
                meta.add_text("OCR_Text", text)
                
                if img.format != "PNG":
                    img = img.convert("RGBA")
                
                output_path = self.output_path / f"{image_path.stem}.png"
                img.save(output_path, "PNG", pnginfo=meta)
                logger.info(f"Przetworzono: {image_path.name}")
                return output_path
                
        except Exception as e:
            logger.error(f"Błąd przetwarzania {image_path.name}: {e}")
            return None
    
    def process_all(self, max_workers: int = 4):
        """Przetwarza wszystkie obrazy w katalogu wejściowym"""
        image_files = list(self.input_path.glob('*.[pj][np][g]*'))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.process_image, image_files))
        
        processed = [r for r in results if r is not None]
        logger.info(f"Przetworzono {len(processed)} z {len(image_files)} plików")

if __name__ == "__main__":
    processor = OCRProcessor()
    processor.process_all()