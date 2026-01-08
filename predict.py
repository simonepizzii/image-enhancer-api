from cog import BasePredictor, Input, Path
from PIL import Image, ImageFilter, ImageEnhance

class Predictor(BasePredictor):
    def setup(self):
        pass

    def predict(
        self,
        image: Path = Input(description="Upload an image to enhance"),
        mode: str = Input(choices=["photo", "screenshot", "anime"], default="photo")
    ) -> Path:
        img = Image.open(str(image)).convert("RGB")

        if mode == "photo":
            # Migliora foto reali
            sharp = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=150, threshold=3))
            contrast = ImageEnhance.Contrast(sharp).enhance(1.1)
            bright = ImageEnhance.Brightness(contrast).enhance(1.05)
            img = bright

        elif mode == "screenshot":
            # Migliora screenshot (testo più nitido)
            img = img.filter(ImageFilter.SHARPEN)
            img = img.filter(ImageFilter.SMOOTH_MORE)

        elif mode == "anime":
            # Migliora anime-style
            img = img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=180, threshold=0))

        # Upscale x2 con LANCZOS (miglior qualità non-AI)
        w, h = img.size
        img = img.resize((w*2, h*2), Image.LANCZOS)

        output_path = "/tmp/output.jpg"
        img.save(output_path, quality=95)
        return Path(output_path)
