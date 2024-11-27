import numpy as np
from PIL import Image

def to_grayscale(image_path):
    img = Image.open(image_path)
    arr = np.array(img)
    gray = arr.mean(axis=2, keepdims=True).astype(np.uint8)
    return Image.fromarray(np.concatenate([gray]*3, axis=2))

def blur_image(image_path):
    img = Image.open(image_path)
    arr = np.array(img)
    kernel_size = 3
    pad = kernel_size // 2
    padded_arr = np.pad(arr, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
    blurred = np.zeros_like(arr)

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            region = padded_arr[i:i+kernel_size, j:j+kernel_size]
            blurred[i, j] = region.mean(axis=(0, 1))
    return Image.fromarray(blurred.astype(np.uint8))
