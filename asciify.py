from PIL import Image


ASCII_SHADING_CHARS = ['M', 'N', 'F', 'V', '$', 'I', '*', ':']  # from darkest to lightest


class Asciify:
    def __init__(self, image, new_width=100):
        self._nw = new_width
        self.im = image
        self.width, self.height = image.size  # image.size returns a 2 tuple (width, height) in pixels

    def grayify_and_resize(self):
        """
        Split the GIF into individual frames. Resize and convert each frame to monochrome.
        :returns: a list of resized black&white Image objects
        """

        # new dimensions for each frame; same aspect ratio as original width x height
        new_width = self._nw
        new_height = new_width * self.height / self.width
        num_frames = self.im.n_frames  # number of frames in the .gif animation
        result_list = []
        for i in range(0, num_frames - 1):
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

        result_list = []
        for image in im_list:
            pixels = image.getdata()  # color data on every pixel per image
            append_list = []
            for pixel_value in pixels:
                append_list.append(ASCII_SHADING_CHARS[pixel_value//color_width])  # 'replace' pixel with ascii char
            result_list.append("".join(append_list))  # adds an element to result_list containing every pixel for image

        return result_list


if __name__ == "__main__":
    asciify_im = Asciify(Image.open("earth.gif"))
    gif_list = asciify_im.grayify_and_resize()
    char_list = asciify_im.ascii_map(gif_list)
