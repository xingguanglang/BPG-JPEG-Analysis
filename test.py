import subprocess
import os
import time
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
from PIL import Image
import numpy as np


def png_to_ppm(input_file, output_file):
    try:
        with Image.open(input_file) as img:
            img = img.convert('RGB')
            img.save(output_file)
        print(f"Transform {input_file} to {output_file} successfully")
        return output_file
    except Exception as e:
        print(f"Error：{e}")

def compress_jpeg(input_path, quality):
    output_path = "temp.jpg"
    subprocess.run(f"cjpeg -quality {quality} -outfile {output_path} {input_path}", shell=True)
    return output_path

def compress_bpg(input_path, quality):
    output_path = "temp.bpg"
    reverse = "reverse_input.png"
    subprocess.run(f"bpgenc -q {quality} {input_path} -o {output_path}", shell=True)
    subprocess.run(f"bpgdec  {output_path} -o {reverse} ", shell=True)
    return reverse,output_path

def evaluate_quality(original_path, compressed_path):
    img_orig = np.array(Image.open(original_path))
    img_comp = np.array(Image.open(compressed_path))
    psnr_val = psnr(img_orig, img_comp)
    ssim_val = ssim(img_orig, img_comp, multichannel=True,channel_axis=2)
    ems_val = mse(img_orig, img_comp)
    return psnr_val, ssim_val, ems_val


original = "input.png"
original2 = png_to_ppm(original,"input.ppm")
jpeg_file = compress_jpeg(original2, 80)
bpg_reconstruct_png,bpg_file = compress_bpg(original, 32)

jpeg_psnr, jpeg_ssim, jpeg_ems = evaluate_quality(original2, jpeg_file)
bpg_psnr, bpg_ssim, bpg_ems = evaluate_quality(original, bpg_reconstruct_png)

print(f"JPEG MSE: {jpeg_ems:.2f}, PSNR: {jpeg_psnr:.2f} dB, SSIM: {jpeg_ssim:.3f},file_size={os.path.getsize(jpeg_file)}")
print(f"BPG MSE: {bpg_ems:.2f}, PSNR: {bpg_psnr:.2f} dB, SSIM: {bpg_ssim:.3f},file_size={os.path.getsize(bpg_file)}")