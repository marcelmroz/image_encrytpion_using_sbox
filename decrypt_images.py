from PIL import Image
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import imageio

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

# Load the encrypted images
encrypted_image1 = Image.open("encrypted_images/encrypted_lena.bmp")
encrypted_image2 = Image.open("encrypted_images/encrypted_lena_stara.bmp")
encrypted_image3 = Image.open("encrypted_images/encrypted_temp.bmp")

# Convert the encrypted image data to byte arrays
encrypted_data1 = bytearray(encrypted_image1.tobytes())
encrypted_data2 = bytearray(encrypted_image2.tobytes())
encrypted_data3 = bytearray(encrypted_image3.tobytes())

# Decrypt each byte of the encrypted data using the S-box and key
key = b"my_secure_key_123"
#key = b"bardzozlyklucz123"

for i in range(len(encrypted_data1)):
    encrypted_data1[i] = sbox_array.index(encrypted_data1[i]) ^ key[i % len(key)]

for i in range(len(encrypted_data2)):
    encrypted_data2[i] = sbox_array.index(encrypted_data2[i]) ^ key[i % len(key)]

for i in range(len(encrypted_data3)):
    encrypted_data3[i] = sbox_array.index(encrypted_data3[i]) ^ key[i % len(key)]

# Create a new image from the decrypted byte arrays
decrypted_image1 = Image.frombytes(encrypted_image1.mode, encrypted_image1.size, bytes(encrypted_data1))
decrypted_image2 = Image.frombytes(encrypted_image2.mode, encrypted_image2.size, bytes(encrypted_data2))
decrypted_image3 = Image.frombytes(encrypted_image3.mode, encrypted_image3.size, bytes(encrypted_data3))


# Save the decrypted images
#decrypted_image1.save("decrypted_images/decrypted_lena.bmp")
#decrypted_image2.save("decrypted_images/decrypted_lena_stara.bmp")
#decrypted_image3.save("decrypted_images/decrypted_temp.bmp")

figImg, axsImg = plt.subplots(3,2,figsize = [12, 12])
axsImg[0][0].imshow(image1     , vmin=0, vmax=255)
axsImg[0][1].imshow(decrypted_image1, vmin=0, vmax=255)
axsImg[1][0].imshow(image2     , vmin=0, vmax=255)
axsImg[1][1].imshow(decrypted_image2, vmin=0, vmax=255)
axsImg[2][0].imshow(image3     , vmin=0, vmax=255)
axsImg[2][1].imshow(decrypted_image3, vmin=0, vmax=255)
