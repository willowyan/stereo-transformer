#  Authors: Zhaoshuo Li, Xingtong Liu, Francis X. Creighton, Russell H. Taylor, and Mathias Unberath
#
#  Copyright (c) 2020. Johns Hopkins University - All rights reserved.

import re
import sys

import numpy as np


def readPFM(file):
    file = open(file, 'rb')

    color = None
    width = None
    height = None
    scale = None
    endian = None

    header = file.readline().rstrip()
    if header.decode("ascii") == 'PF':
        color = True
    elif header.decode("ascii") == 'Pf':
        color = False
    else:
        raise Exception('Not a PFM file.')

    dim_match = re.match(r'^(\d+)\s(\d+)\s$', file.readline().decode("ascii"))
    if dim_match:
        width, height = list(map(int, dim_match.groups()))
    else:
        raise Exception('Malformed PFM header.')

    scale = float(file.readline().decode("ascii").rstrip())
    if scale < 0:  # little-endian
        endian = '<'
        scale = -scale
    else:
        endian = '>'  # big-endian

    data = np.fromfile(file, endian + 'f')
    shape = (height, width, 3) if color else (height, width)

    data = np.reshape(data, shape)
    data = np.flipud(data)
    return data, scale


# def writePFM(file, image, scale=1):
#     file = open(file, 'wb')

#     color = None

#     if image.dtype.name != 'float32':
#         raise Exception('Image dtype must be float32.')

#     image = np.flipud(image)

#     if len(image.shape) == 3 and image.shape[2] == 3:  # color image
#         color = True
#     elif len(image.shape) == 2 or len(image.shape) == 3 and image.shape[2] == 1:  # greyscale
#         color = False
#     else:
#         raise Exception('Image must have H x W x 3, H x W x 1 or H x W dimensions.')

#     file.write('PF\n' if color else 'Pf\n'.encode())
#     file.write('%d %d\n'.encode() % (image.shape[1], image.shape[0]))

#     endian = image.dtype.byteorder

#     if endian == '<' or endian == '=' and sys.byteorder == 'little':
#         scale = -scale

#     file.write('%f\n'.encode() % scale)

#     image.tofile(file)

def writePFM(file, image, scale=1):
    with open(file, 'wb') as file:
        if image.dtype.name != 'float32':
            raise Exception('Image dtype must be float32.')

        image = np.flipud(image)

        if len(image.shape) == 3 and image.shape[2] == 3:  # color image
            color = True
        elif len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1):  # greyscale
            color = False
        else:
            raise Exception('Image must have H x W x 3, H x W x 1 or H x W dimensions.')

        file.write(('PF\n' if color else 'Pf\n').encode())
        file.write(f'{image.shape[1]} {image.shape[0]}\n'.encode())

        endian = image.dtype.byteorder

        if endian == '<' or (endian == '=' and sys.byteorder == 'little'):
            scale = -scale

        file.write(f'{scale}\n'.encode())

        image.tofile(file)

def convert_tiff_to_pfm(input_folder_path, output_folder_path):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(input_folder_path):
        if filename.endswith(".tiff") or filename.endswith(".tif"):
            tiff_path = os.path.join(input_folder_path, filename)
            pfm_filename = os.path.splitext(filename)[0] + '.pfm'
            pfm_path = os.path.join(output_folder_path, pfm_filename)

            image = cv2.imread(tiff_path, -1)  # -1 to read the image as is
            if image is None:
                print(f"Failed to load {tiff_path}")
                continue

            image_np = np.array(image, dtype=np.float32)

            writePFM(pfm_path, image_np)
            print(f"Written PFM file: {pfm_path}")
