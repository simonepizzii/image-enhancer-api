from cog import BasePredictor, Input, Path
from PIL import Image
from rembg import remove

class Predictor(BasePredictor):
    def setup(self):
        pass

    def predict(
        self,
        image: Path = Input(description="Upload a photo of a person, product, or object"),
        format: str = Input(choices=["png", "jpg"], default="png", description="Output format (PNG = transparent background, JPG = solid background)"),
        background_color: str = Input(default="#FFFFFF", description="Background color in hex (used only for JPG, e.g. #FF0000)")
    ) -> Path:
        input_img = Image.open(str(image)).convert("RGB")
        # Usa modello leggero per CPU
        output_img = remove(input_img, model_name="u2netp", post_process_mask=True)

        if format == "png":
            output_path = "/tmp/output.png"
            output_img.save(output_path, "PNG")
        else:
            # Crea sfondo solido
            r = int(background_color[1:3], 16)
            g = int(background_color[3:5], 16)
            b = int(background_color[5:7], 16)
            bg = Image.new("RGB", output_img.size, (r, g, b))
            bg.paste(output_img, mask=output_img.split()[-1])  # Usa alpha
            output_path = "/tmp/output.jpg"
            bg.save(output_path, "JPEG", quality=95)

        return Path(output_path)
