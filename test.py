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
        print(f"Transform {input_file} sized {os.path.getsize(input_file)/1024:.1f} to {output_file} successfully")
        return output_file
    except Exception as e:
        print(f"Error：{e}")

def compress_jpeg(input_path, quality):
    output_path = "temp.jpg"
    reverse="reverse_jpg.png"
    start = time.time()
    subprocess.run(f"cjpeg -quality {quality} -outfile {output_path} {input_path}", shell=True)
    end = time.time()
    # subprocess.run(f"convert {output_path}  {reverse} ", shell=True)
    return reverse,output_path,end-start

def compress_bpg(input_path, quality):
    output_path = "temp.bpg"
    reverse = "reverse_bpg.png"
    start = time.time()
    subprocess.run(f"bpgenc -q {quality} {input_path} -o {output_path}", shell=True)
    end = time.time()
    subprocess.run(f"bpgdec  {output_path} -o {reverse} ", shell=True)
    return reverse,output_path,end-start

def evaluate_quality(original_path, compressed_path):
    img_orig = np.array(Image.open(original_path))
    img_comp = np.array(Image.open(compressed_path))
    psnr_val = psnr(img_orig, img_comp)
    ssim_val = ssim(img_orig, img_comp, multichannel=True,channel_axis=2)
    ems_val = mse(img_orig, img_comp)
    return psnr_val, ssim_val, ems_val


# original = "1.png"
ori1 = ["1.png","2.png","3.png","4.png","5.png","6.png","7.png","8.png","9.png","10.png","11.png","12.png","noise_image1.png","noise_image2.png","noise_image5.png"]
# original2 = png_to_ppm(original,"temp.ppm")
jpeg_quality = 80
bpg_quality = 30
data = ""
for original in ori1:
    original2 = png_to_ppm(original,"temp.ppm")
    jpeg_reconstruct_png,jpeg_file,jpeg_time = compress_jpeg(original2, jpeg_quality)
    bpg_reconstruct_png,bpg_file, bpg_time = compress_bpg(original, bpg_quality)

    jpeg_psnr, jpeg_ssim, jpeg_ems = evaluate_quality(original2, jpeg_file)
    bpg_psnr, bpg_ssim, bpg_ems = evaluate_quality(original, bpg_reconstruct_png)

    print(f"JPEG Quality:{jpeg_quality}, MSE: {jpeg_ems:.2f}, PSNR: {jpeg_psnr:.2f} dB, SSIM: {jpeg_ssim:.3f}, Time: {jpeg_time:.5f},file_size={os.path.getsize(jpeg_file)/1024:.1f}")
    print(f"BPG Quality:{bpg_quality}, MSE: {bpg_ems:.2f}, PSNR: {bpg_psnr:.2f} dB, SSIM: {bpg_ssim:.3f}, Time: {bpg_time:.5f},file_size={os.path.getsize(bpg_file)/1024:.1f}")
    jpeg_data = f"JPEG Quality:{jpeg_quality}, MSE: {jpeg_ems:.2f}, PSNR: {jpeg_psnr:.2f} dB, SSIM: {jpeg_ssim:.3f}, Time: {jpeg_time:.5f},file_size={os.path.getsize(jpeg_file)/1024:.1f}"
    bpg_data = f"BPG Quality:{bpg_quality}, MSE: {bpg_ems:.2f}, PSNR: {bpg_psnr:.2f} dB, SSIM: {bpg_ssim:.3f}, Time: {bpg_time:.5f},file_size={os.path.getsize(bpg_file)/1024:.1f}"
    data = data + "\n"+ jpeg_data+ "\n" + bpg_data

with open("output.txt", "w", encoding="utf-8") as file:
    file.write(data)