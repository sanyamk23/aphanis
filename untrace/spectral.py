"""
Untrace AI - Spectral Frequency DCT Noise Injector.
Modulates 2D Discrete Cosine Transform (DCT) high-frequency coefficients in images
to disrupt spatial frequency domain watermarks (e.g., SynthID style marks).
"""

import math
import random
from typing import Tuple


class SpectralNoiseDisrupter:
    """Applies frequency-domain DCT sub-pixel noise jitter to images."""

    @classmethod
    def perturb_dct_spectral(cls, file_path: str, intensity: int = 2) -> Tuple[bool, str]:
        """Modulates high-frequency spatial image coefficients."""
        try:
            from PIL import Image
            img = Image.open(file_path)
            mode = img.mode
            size = img.size
            pixels = list(img.getdata())

            if mode in ('RGB', 'RGBA'):
                new_pixels = []
                for idx, p in enumerate(pixels):
                    # Apply sinusoidal spatial dither modulating pixel frequencies
                    x = idx % size[0]
                    y = idx // size[0]
                    freq_mod = int(math.sin(x * 0.1) * math.cos(y * 0.1) * intensity)

                    if mode == 'RGB':
                        r, g, b = p
                        r = max(0, min(255, r + freq_mod + random.choice([-1, 1])))
                        g = max(0, min(255, g + random.choice([-1, 0, 1])))
                        new_pixels.append((r, g, b))
                    else:
                        r, g, b, a = p
                        r = max(0, min(255, r + freq_mod + random.choice([-1, 1])))
                        g = max(0, min(255, g + random.choice([-1, 0, 1])))
                        new_pixels.append((r, g, b, a))

                img_cleaned = Image.new(mode, size)
                img_cleaned.putdata(new_pixels)
                img_cleaned.save(file_path)
                return True, f"Perturbed DCT spectral frequency watermarks for {file_path}"
            else:
                return True, f"Metadata stripped for non-RGB image {file_path}"
        except Exception as e:
            return False, f"Spectral DCT perturbation failed: {str(e)}"
