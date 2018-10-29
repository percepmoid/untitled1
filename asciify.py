from PIL import Image


ASCII_SHADING_CHARS = ['M', 'N', 'F', 'V', '$', 'I', '*', ':']  # from darkest to lightest


class Asciify:
    def __init__(self, image, new_width=500):
        self.width, self.height = image.size  # image.size returns a 2 tuple (width, height) in pixels
        self._nw = new_width
        self._nh = int(new_width * self.height / self.width)
        self.im = image

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

    def ascii_map(self, im_list, color_width=32):
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
                append_list.append(ASCII_SHADING_CHARS[pixel_value//color_width])  # 'replace' pixel with ascii char
            ascii_image_list.append(append_list)  # adds an element to ascii_image_list containing every pixel for image

        for ascii_image in ascii_image_list:
            pass

        return ascii_image_list


if __name__ == "__main__":
    asciify_im = Asciify(Image.open("earth.gif"), 10)
    gif_list = asciify_im.grayify_and_resize()
    char_list = asciify_im.ascii_map(gif_list)
    outfile = open("outfile.txt", 'w')
    for list in char_list:
        outfile.write("".join(list))
        print(len(char_list[0]))
    outfile.close()
