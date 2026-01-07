from cog import BasePredictor, Input, Path
from PIL import Image

class Predictor(BasePredictor):
    def setup(self):
        """Nessun modello da caricare (per ora)"""
        pass

    def predict(self, image: Path = Input(description="Input image to enhance")) -> Path:
        """
        Placeholder: restituisce l'immagine invariata.
        Sostituisci questa logica con il tuo modello di enhancement.
        """
        # Carica e assicura formato RGB
        img = Image.open(image).convert("RGB")
        # Salva output
        output_path = "/tmp/output.png"
        img.save(output_path)
        return Path(output_path)
