from cog import BasePredictor, Input, Path
from PIL import Image, ImageFilter, ImageEnhance

class Predictor(BasePredictor):
    def setup(self):
        pass

    def predict(
        self,
        image: Path = Input(description="Upload an image to enhance"),
        enhance: bool = Input(default=True, description="Apply sharpening and contrast"),
        upscale: bool = Input(default=False, description="Double image size with LANCZOS")
    ) -> Path:
        img = Image.open(str(image)).convert("RGB")

        if enhance:
            # Unsharp Mask: simula nitidezza avanzata
            blurred = img.filter(ImageFilter.GaussianBlur(radius=0.5))
            img = Image.blend(blurred, img, 1.5)
            
            # Migliora contrasto leggermente
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)

        if upscale:
            w, h = img.size
            img = img.resize((w*2, h*2), Image.LANCZOS)

        output_path = "/tmp/output.jpg"
        img.save(output_path, quality=95)
        return Path(output_path)
