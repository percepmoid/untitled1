from PIL import Image, ImageFont, ImageDraw

ASCII_SHADING_CHARS = ['M', 'W', 'N', 'Q', 'B', 'H', 'K', 'R', '#', 'E', 'D', 'F', 'X', 'O', 'A', 'P', 'G', 'U', 'S',
                       'V', 'Z', 'Y', 'C', 'L', 'T', 'J', '$', 'I', '*', ':', '.', ' ']  # from darkest to lightest 32


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
        for im in im_list:
            pixels = im.getdata()  # color data on every pixel per image
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
        font = ImageFont.truetype('ascii.ttf', 8)
        ascii_images = ['\n'.join(image) for image in ascii_image_list]
        pil_gifs = [Image.new('RGBA', (self._nw*5, self._nh*11)) for ascii_image in ascii_images]
        draw_gifs = [ImageDraw.Draw(pil_gif) for pil_gif in pil_gifs]
        for draw_gif in draw_gifs:
            draw_gif.text((0,0), ascii_images[draw_gifs.index(draw_gif)], (255,255,255), font=font)
        gif = Image.new('RGBA', size=(self._nw*5, self._nh*11))
        gif.save('ascii.gif', save_all=True, loop=0, append_images=pil_gifs)

        resize_list = []
        gif_big = Image.open('ascii.gif')
        for i in range(gif_big.n_frames - 1):
            resize_list.append(gif_big.resize((self._nw, self._nh)))
            gif_big.seek(gif_big.tell() + 1)
        resized_gif = Image.new('RGBA', (self._nw, self._nh))
        resized_gif.save('ascii_resized.gif', save_all=True, loop=0, append_images=resize_list)


if __name__ == "__main__":
    asciify_im = Asciify(Image.open("earth.gif"), 200)
    gif_list = asciify_im.grayify_and_resize()
    ascii_images = asciify_im.ascii_map(gif_list)
    gif = asciify_im.gifify(ascii_images)
    #outfile = open("outfile.txt", 'w')
    #for image in ascii_images:
    #    outfile.write("\n".join(image) + '\n\n')
