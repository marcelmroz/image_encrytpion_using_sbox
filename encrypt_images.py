from PIL import Image
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import imageio

image1 = Image.open("original_images/lena_color.bmp")
image2 = Image.open("original_images/lena.bmp")
image3 = Image.open("original_images/temp_.bmp")

# Read the S-box values from the file
sbox_array = []
with open("sbox_08x08_20130110_011319_02.sbx", "rb") as f:
    sbox = f.read()
    temp = 0
    # Remove zeros
    for byte in sbox:
        if temp % 2 == 0:
            sbox_array.append(byte)
        temp += 1

# Generate a secure key
key = b"my_secure_key_123"

# Convert the image to a byte array and encrypt each byte using the S-box and key
data1 = bytearray(image1.tobytes())
data2 = bytearray(image2.tobytes())
data3 = bytearray(image3.tobytes())

for i in range(len(data1)):
    data1[i] = sbox_array[(data1[i] ^ key[i % len(key)])]

for i in range(len(data2)):
    data2[i] = sbox_array[(data2[i] ^ key[i % len(key)])]

for i in range(len(data3)):
    data3[i] = sbox_array[(data3[i] ^ key[i % len(key)])]

# Create a new image from the modified byte array
encrypted_image1 = Image.frombytes(image1.mode, image1.size, bytes(data1))
encrypted_image2 = Image.frombytes(image2.mode, image2.size, bytes(data2))
encrypted_image3 = Image.frombytes(image3.mode, image3.size, bytes(data3))

rotated_image1 = encrypted_image1.rotate(180)

data11 = bytearray(rotated_image1.tobytes())
for i in range(len(data11)):
    data11[i] = sbox_array[(data11[i] ^ key[i % len(key)])]

encrypted_image11 = Image.frombytes(encrypted_image1.mode, encrypted_image1.size, bytes(data11))

# Save the encrypted images
#encrypted_image1.save("encrypted_images/encrypted_lena.bmp")
#encrypted_image2.save("encrypted_images/encrypted_lena_stara.bmp")
#encrypted_image3.save("encrypted_images/encrypted_temp.bmp")

figImg, axsImg = plt.subplots(3,2,figsize = [12, 12])
axsImg[0][0].imshow(image1     , vmin=0, vmax=255)
axsImg[0][1].imshow(encrypted_image1     , vmin=0, vmax=255)
axsImg[1][0].imshow(image2     , vmin=0, vmax=255)
axsImg[1][1].imshow(encrypted_image11     , vmin=0, vmax=255)
axsImg[2][0].imshow(image3     , vmin=0, vmax=255)
axsImg[2][1].imshow(encrypted_image3     , vmin=0, vmax=255)