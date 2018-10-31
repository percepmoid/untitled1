from PIL import Image, ImageFont, ImageDraw


__author__ = 'Nikolas'


ASCII_SHADING_CHARS = ['M', 'W', 'N', 'Q', 'B', 'H', 'K', 'R', '#', 'E', 'D', 'F', 'X', 'O', 'A', 'P', 'G', 'U', 'S',
                       'V', 'Z', 'Y', 'C', 'L', 'T', 'J', '$', 'I', '*', ':', '.', ' ']  # from darkest to lightest 32
#ASCII_SHADING_CHARS = ASCII_SHADING_CHARS[::-1]


class Asciify:
    def __init__(self, img, new_width=500):
        self.width, self.height = img.size  # image.size returns a 2 tuple (width, height) in pixels
        self._nw = new_width
        self._nh = int(new_width * self.height / self.width)
        self.im = img

    def grayify_and_resize(self, img=None):
        """
        Split the GIF into individual frames. Resize and convert each frame to monochrome.
        :returns: a list of resized black&white Image objects
        """

        print("Converting image to grayscale and resizing...", end=' ')
        result_list = []
        if img:
            width, height = self._nw, self._nh
            num_frames = img.n_frames
            for i in range(num_frames - 1):
                result_list.append(img.resize((width, height)))
                img.seek(img.tell() + 1)

        else:
            new_width = self._nw
            new_height = self._nh
            num_frames = self.im.n_frames  # number of frames in the .gif animation
            for i in range(0, num_frames - 1):
                # convert to mode L (b&w); resize to new dimensions
                result_list.append(self.im.convert('L').resize((int(new_width), new_height)))
                self.im.seek(self.im.tell() + 1)  # move to the next frame in the gif animation
        print("done!")

        return result_list

    def ascii_map(self, im_list, color_width=int(255 / len(ASCII_SHADING_CHARS))):
        """
        Maps an ascii shading character to a pixel of each frame of the GIF
        :param im_list: a list of black and white Image objects
        :param color_width: determines the color intensity of each pixel
        :returns: a list of each frame of the gif converted to ascii pixels
        """

        print("Creating ascii character pixels...", end=' ')
        ascii_image_list = []  # unformatted ascii images; needs to be broken into proper rows and columns
        result_list = []  # ascii_image_list broken into proper rows and columns; how convinient
        for image in im_list:
            pixels = image.getdata()  # color data on every pixel per image
            append_list = []  # temporary list to append to ascii_image_list
            for pixel_value in pixels:
                index = int(pixel_value // color_width)
                if index >= len(ASCII_SHADING_CHARS):
                    append_list.append(ASCII_SHADING_CHARS[-1])
                else:
                    append_list.append(ASCII_SHADING_CHARS[index])  # 'replace' pixel with ascii char
            ascii_image_list.append(append_list)  # adds an element to ascii_image_list containing every pixel for image

        for ascii_image in ascii_image_list:
            ascii_string = "".join(ascii_image)
            result_list.append([ascii_string[index:index + self._nw]
                                for index in range(0, len(ascii_string), self._nw)])
        print("done!")

        return result_list

    def gifify(self, ascii_image_list):
        """
        Return the ascii strings to .gif format for use in a traditional image viewer.
        :param ascii_image_list: A list of ascii 'pixel' images
        :returns: None
        """

        print("Creating your gif (this may take awhile)...")
        # 7 = nw*4, nh*10
        # 5 = nw*3, nh*8
        font = ImageFont.truetype('ascii.ttf', 11)  # set font and font size
        ascii_image_strings = ['\n'.join(image) for image in ascii_image_list]
        ascii_image_gifs = []
        resized_ascii_gifs = []
        for image in ascii_image_strings:
            temp_image = Image.new('RGBA', (self._nw*7, self._nh*13), 'white')
            image_draw = ImageDraw.Draw(temp_image)
            image_draw.text((0, 0), image, font=font, fill='black')
            ascii_image_gifs.append(temp_image)
            print("{}% complete".format(round(len(ascii_image_gifs) / len(ascii_image_strings)*100), 2))
        print("Resizing your gif back to original dimensions...", end=' ')
        for i in range(len(ascii_image_gifs)):
            resized = ascii_image_gifs[i].resize((self.width, self.height))
            resized_ascii_gifs.append(resized)
        resized_ascii_gifs[0].save('resized_gif.gif', save_all=True, loop = 0, duration=1, append_images=resized_ascii_gifs[1:])
        print("done!")


if __name__ == "__main__":
    im = Image.open("sponge.gif")
    width, _ = im.size
    asciify_im = Asciify(im, int(width))
    gif_list = asciify_im.grayify_and_resize()
    ascii_images = asciify_im.ascii_map(gif_list)
    asciify_im.gifify(ascii_images)

    # Debugging ascii image creation #
    # outfile = open("outfile.txt", 'w')
    # for image in ascii_images:
    #    outfile.write("\n".join(image) + '\n\n')
