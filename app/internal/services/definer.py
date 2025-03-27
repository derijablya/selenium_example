import pytesseract
import requests
from PIL import Image

__all__ = ["DefinerService"]


class DefinerService:
    @staticmethod
    def get_digits_from_image(image_url) -> int:
        try:
            r = requests.get(image_url, stream=True)
            r.raise_for_status()
            r.raw.decode_content = True
            with Image.open(r.raw) as img:
                custom_config = r"--oem 3 --psm 6 outputbase digits"
                res = pytesseract.image_to_string(img, config=custom_config)
                res = res(int)
            r.close()
            return res
        except Exception:
            raise Exception
