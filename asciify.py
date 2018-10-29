from PIL import Image

ASCII_SHADING_CHARS = ['M', 'W', 'N', 'Q', 'B', 'H', 'K', 'R', '#', 'E', 'D', 'F', 'X', 'O', 'A', 'P', 'G', 'U', 'S',
                       'V', 'Z', 'Y', 'C', 'L', 'T', 'J', '$', 'I', '*', ':', '.', ' ']  # from darkest to lightest


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

    def ascii_map(self, im_list, color_width=int(255 / len(ASCII_SHADING_CHARS )+1)):
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
                if index == len(ASCII_SHADING_CHARS):
                    append_list.append(ASCII_SHADING_CHARS[-1])
                else:
                    append_list.append(ASCII_SHADING_CHARS[index])  # 'replace' pixel with ascii char
            ascii_image_list.append(append_list)  # adds an element to ascii_image_list containing every pixel for image

        for ascii_image in ascii_image_list:
            ascii_string = "".join(ascii_image)
            result_list.append([ascii_string[index:index + self._nw]
                                for index in range(0, len(ascii_string), self._nw)])

        return result_list


if __name__ == "__main__":
    asciify_im = Asciify(Image.open("earth.gif"), 500)
    gif_list = asciify_im.grayify_and_resize()
    ascii_images = asciify_im.ascii_map(gif_list)
    outfile = open("outfile.txt", 'w')
    for image in ascii_images:
        outfile.write("\n".join(image) + '\n\n')
