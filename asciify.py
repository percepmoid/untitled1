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

    def grayify_and_resize(self):
        """
        Split the GIF into individual frames. Resize and convert each frame to monochrome.
        :returns: a list of resized black&white Image objects
        """

        new_width = self._nw
        new_height = self._nh
        num_frames = self.im.n_frames  # number of frames in the .gif animation
        result_list = []
        for i in range(0, num_frames - 1):
            # convert to mode L (b&w); resize to new dimensions
            result_list.append(self.im.convert('L').resize((int(new_width), new_height)))
            self.im.seek(self.im.tell() + 1)  # move to the next frame in the gif animation

        return result_list

    def ascii_map(self, im_list, color_width=int(255 / len(ASCII_SHADING_CHARS))):
        """
        Maps an ascii shading character to a pixel of each frame of the GIF
        :param im_list: a list of black and white Image objects
        :param color_width: determines the color intensity of each pixel
        :returns: a list of each frame of the gif converted to ascii pixels
        """

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

        return result_list

    def gifify(self, ascii_image_list):
        """
        Return the ascii strings to .gif format for use in a traditional image viewer.
        :param ascii_image_list: A list of ascii 'pixel' images
        :returns: None
        """

        font = ImageFont.truetype('ascii.ttf', 7)  # set font and font size
        ascii_image_strings = ['\n'.join(image) for image in ascii_image_list]
        # Create n PIL images, where n is the number of frames in the original gif
        pil_gifs = [Image.new('RGBA', (self._nw*4, self._nh*10)) for i in range(len(ascii_image_strings))]
        draw_gifs = [ImageDraw.Draw(pil_gif) for pil_gif in pil_gifs]  # create a PIL ImageDraw for the new frames
        for draw_gif in draw_gifs:  # write the ascii strings to each frame
            draw_gif.text((0, 0), ascii_image_strings[draw_gifs.index(draw_gif)], (255, 255, 255), font=font)
        save_as = Image.new('RGBA', size=(self._nw*4, self._nh*10))  # create a new PIL Image to save the frames to
        save_as.save('ascii.gif', save_all=True, loop=0, duration=42, append_images=pil_gifs[1:-1])  # save it


if __name__ == "__main__":
    im = Image.open("trippy.gif")
    asciify_im = Asciify(im, 110)
    gif_list = asciify_im.grayify_and_resize()
    ascii_images = asciify_im.ascii_map(gif_list)
    asciify_im.gifify(ascii_images)

    # Debugging ascii image creation #
    # outfile = open("outfile.txt", 'w')
    # for image in ascii_images:
    #    outfile.write("\n".join(image) + '\n\n')
