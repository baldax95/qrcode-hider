import click
from PIL import Image, ImageFilter

import math


class Steganography(object):

    @staticmethod
    def printpix(img):
        """DEBUG function used to print the rgb composition of the pixels in an image"""

        filePath = "./res/imgPrint.txt"
        fileOutput = open(filePath, 'w')

        pixel_map = img.load()

        for i in range(0, 10):
            r, g, b = Steganography.__int_to_bin(pixel_map[i, 0])
            fileOutput.write(f'[{i}]r={r},g={g},b={b}\t')
        fileOutput.close()

    @staticmethod
    def __int_to_bin(rgb):
        """Convert an integer tuple to a binary (string) tuple.

        :param rgb: An integer tuple (e.g. (220, 110, 96))
        :return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        """

        r, g, b = rgb
        return ('{0:08b}'.format(r),
                '{0:08b}'.format(g),
                '{0:08b}'.format(b))

    @staticmethod
    def __bin_to_int(rgb):
        """Convert a binary (string) tuple to an integer tuple.

        :param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :return: Return an int tuple (e.g. (220, 110, 96))
        """
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))

    @staticmethod
    def __merge_rgb(rgb1, rgb2):
        """Merge two RGB tuples.

        :param rgb1: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :param rgb2: Another string tuple
        (e.g. ("00101010", "11101011", "00010110"))
        :return: An integer tuple with the two RGB values merged.
        """
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2

        rgb = (r1[:4] + r2[:4],
               g1[:4] + g2[:4],
               b1[:4] + b2[:4])
        return rgb

    @staticmethod
    def __merge_rgb_r(rgb1, rgb2):

        r1, g1, b1 = rgb1
        r2 = rgb2[0]

        if r2[0] == '1':
            r2 = '11111111'
        else:
            r2 = '00000000'

        rgb = (r1[:4] + r2[:4],
               g1,
               b1)

        return rgb

    @staticmethod
    def __merge_rgb_g(rgb1, rgb2):

        r1, g1, b1 = rgb1
        g2 = rgb2[1]

        if g2[0] == '1':
            g2 = '11111111'
        else:
            g2 = '00000000'

        rgb = (r1,
               g1[:4] + g2[:4],
               b1)

        return rgb

    @staticmethod
    def __merge_rgb_b(rgb1, rgb2):

        r1, g1, b1 = rgb1
        b2 = rgb2[2]

        if b2[0] == '1':
            b2 = '11111111'
        else:
            b2 = '00000000'

        rgb = (r1,
               g1,
               b1[:4] + b2[:4])

        return rgb

    @staticmethod
    def __merge_rgb_d(rgb1, rgb2):
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2

        rgb = (r1[:4] + r2[4:],
               g1[:4] + g2[4:],
               b1[:4] + b2[:4])

        return rgb

    @staticmethod
    def merge(img1, img2):
        """Merge two images. The second one will be merged into the first one.

        :param img1: First image
        :param img2: Second image
        :return: A new merged image.
        """

        img1_width = img1.size[0]   # columns
        img1_height = img1.size[1]  # rows

        img2_width = img2.size[0]   # columns
        img2_height = img2.size[1]  # rows

        # Check the images dimensions
        if img2_width > (math.ceil((img1_width - 179)/3)) * 3 or img2_height > (math.ceil((img1_height - 179)/3)) * 3:
            raise ValueError('Image 2 should not be larger than Image 1!')

        # Get the pixel map of the two images
        pixel_map1 = img1.load()
        pixel_map2 = img2.load()

        # Create a new image that will be outputted
        new_image = Image.new(img1.mode, img1.size)
        pixels_new = new_image.load()

        width_digits_count = 1
        height_digits_count = 1

        count_h = 0
        for i in range(img1_height):
            count_w = 0
            for j in range(img1_width):
                rgb1 = Steganography.__int_to_bin(pixel_map1[j, i])

                if i % 3 == 0 and i >= 90 and i < (img1_height - 90) and j % 3 == 0 and j >= 90 and j < (img1_width - 90):
                    for x in range(3):
                        if (count_w < img2_width and count_h < img2_height):
                            rgb2 = Steganography.__int_to_bin(
                                pixel_map2[count_w, count_h])
                            if x == 0:
                                rgb = Steganography.__merge_rgb_r(rgb1, rgb2)
                            elif x == 1:
                                rgb = Steganography.__merge_rgb_g(rgb1, rgb2)
                            else:
                                rgb = Steganography.__merge_rgb_b(rgb1, rgb2)
                            count_w += 1

                elif i == 90 and (j == 91 or j == 92 or j == 94 or j == 95 or j == 97):
                    if(j == 91):
                        width_digit = len(str(img2_width))
                        height_digit = len(str(img2_height))
                    else:
                        if width_digits_count <= len(str(img2_width)):
                            width_digit = int(
                                str(img2_width)[-width_digits_count])
                            width_digits_count += 1
                        else:
                            width_digit = 100

                        if height_digits_count <= len(str(img2_height)):
                            height_digit = int(
                                str(img2_height)[-height_digits_count])
                            height_digits_count += 1
                        else:
                            height_digit = 100

                    rgb2 = Steganography.__int_to_bin(
                        (width_digit, height_digit, 100))
                    rgb = Steganography.__merge_rgb_d(rgb1, rgb2)

                else:
                    rgb2 = Steganography.__int_to_bin((100, 100, 100))
                    rgb = Steganography.__merge_rgb(rgb1, rgb2)

                pixels_new[j, i] = Steganography.__bin_to_int(rgb)

            if i % 3 == 0 and i >= 90:
                count_h += 1

        return new_image

    @staticmethod
    def unmerge(img):
        """Unmerge an image.

        :param img: The input image.
        :return: The unmerged/extracted image.
        """

        # Load the pixel map
        pixel_map = img.load()
        img1_width = img.size[0]
        img1_height = img.size[1]

        img2_width_digits_count, img2_height_digits_count, _ = Steganography.__int_to_bin(
            pixel_map[91, 90])

        img2_width_digits_count = int(img2_width_digits_count[4:], 2)
        img2_height_digits_count = int(img2_height_digits_count[4:], 2)

        indexes = [92, 94, 95, 97]

        img2_width = 0
        img2_height = 0
        x1 = 0
        x2 = 0
        for i in indexes:
            w, h, _ = Steganography.__int_to_bin(pixel_map[i, 90])
            w = (int(w[4:], 2))
            h = (int(h[4:], 2))
            if img2_width_digits_count > 0:
                img2_width += w * pow(10, x1)
                img2_width_digits_count -= 1
                x1 += 1
            if img2_height_digits_count > 0:
                img2_height += h * pow(10, x2)
                img2_height_digits_count -= 1
                x2 += 1

        img2_size = img2_width, img2_height

        # Create the new image and load the pixel map
        new_image = Image.new(img.mode, img2_size)
        pixels_new = new_image.load()

        img2_count_h = 0
        for i in range(img1_height):
            img2_count_w = 0
            for j in range(img1_width):
                # Get the RGB (as a string tuple) from the current pixel
                r, g, b = Steganography.__int_to_bin(pixel_map[j, i])

                if i % 3 == 0 and i >= 90 and i < (img1_height - 90) and j % 3 == 0 and j >= 90 and j < (img1_width - 90):
                    for x in range(3):
                        if (img2_count_w < img2_width and img2_count_h < img2_height):
                            if x == 0:
                                rgb = (r[4:] + r[4:],
                                       r[4:] + r[4:],
                                       r[4:] + r[4:])
                                pixels_new[img2_count_w, img2_count_h] = Steganography.__bin_to_int(
                                    rgb)
                            elif x == 1:
                                rgb = (g[4:] + g[4:],
                                       g[4:] + g[4:],
                                       g[4:] + g[4:])
                                pixels_new[img2_count_w, img2_count_h] = Steganography.__bin_to_int(
                                    rgb)
                            else:
                                rgb = (b[4:] + b[4:],
                                       b[4:] + b[4:],
                                       b[4:] + b[4:])
                                pixels_new[img2_count_w, img2_count_h] = Steganography.__bin_to_int(
                                    rgb)
                            img2_count_w += 1

            if i % 3 == 0 and i >= 90:
                img2_count_h += 1

        return Steganography.filter(new_image)

    @staticmethod
    def filter(img):
        support = img.filter(ImageFilter.ModeFilter(5))
        return support.filter(ImageFilter.MedianFilter(5))


@click.group()
def cli():
    pass


@cli.command()
@click.option('--img1', required=True, type=str, help='Image that will hide another image')
@click.option('--img2', required=True, type=str, help='Image that will be hidden')
@click.option('--output', required=True, type=str, help='Output image')
def merge(img1, img2, output):
    merged_image = Steganography.merge(Image.open(img1), Image.open(img2))
    merged_image.save(output)


@cli.command()
@click.option('--img', required=True, type=str, help='Image that will be hidden')
@click.option('--output', required=True, type=str, help='Output image')
def unmerge(img, output):
    unmerged_image = Steganography.unmerge(Image.open(img))
    unmerged_image.save(output)


@cli.command()
@click.option('--img', required=True, type=str, help='The image you want to be printed')
def printpix(img):
    Steganography.printpix(Image.open(img))


@cli.command()
@click.option('--img', required=True, type=str, help='The image you want to filter')
@click.option('--output', required=True, type=str, help='Output image')
def filter(img, output):
    filtered_image = Steganography.filter(Image.open(img))
    filtered_image.save(output)


if __name__ == '__main__':
    cli()
