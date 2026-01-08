# cog-disable-openapi-schema
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from cog import BasePredictor, Input, Path
from PIL import Image
import numpy as np
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet

class Predictor(BasePredictor):
    def setup(self):
        model_path = os.path.join(os.path.dirname(__file__), "RealESRGAN_x2plus.pth")
        self.model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        self.upsampler = RealESRGANer(
            scale=2,
            model_path=model_path,
            model=self.model,
            tile=0,
            tile_pad=10,
            pre_pad=0,
            half=False,
            gpu_id=None
        )

    def predict(
        self,
        image: Path = Input(description="Upload an image to enhance"),
        scale: int = Input(default=2, choices=[2])
    ) -> Path:
        img = Image.open(str(image)).convert("RGB")
        img = np.array(img)
        output, _ = self.upsampler.enhance(img, outscale=scale)
        output_img = Image.fromarray(output)
        output_path = "/tmp/output.jpg"
        output_img.save(output_path, quality=95)
        return Path(output_path)
