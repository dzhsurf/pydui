# from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
# import numpy
# im = Image.new(mode="RGBA", size=(int(w), int(h)))
#             __ImageFontUtils__.draw_text(
#                 image=im,
#                 text=text,
#                 font="res/fonts/Helvetica.ttc",
#                 font_size=font_size,
#                 font_color=color.to_string(),
#                 start_point=(0, 0),
#                 line_height_ratio=1.5,
#                 max_width=int(w),
#                 align=PyDuiAlign.LEFT,
#             )
#             arr = numpy.array(im)
#             height, width, channels = arr.shape
#             surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_ARGB32, width, height)
#             ctx.set_source_surface(surface, x, y)
#             ctx.paint()
#             surface.finish()
#             im.close()


# class __ImageFontUtils__:
#     @staticmethod
#     def get_font_height(font: str, font_size: int) -> int:
#         ttf = ImageFont.truetype(font, font_size)
#         line_height = ttf.getsize("A")[1]
#         return line_height

#     @staticmethod
#     def draw_text(
#         image: Image,
#         text: str,
#         font: str,
#         font_size: int,
#         font_color: str,
#         start_point: Tuple[int, int],
#         line_height_ratio: float,
#         max_width: int,
#         align: PyDuiTextAlign = PyDuiTextAlign.LEFT,
#     ):
#         if len(text) == 0:
#             return
#         # setup font
#         ttf = ImageFont.truetype(font, font_size)
#         line_height = ttf.getsize("A")[1] * line_height_ratio
#         # draw text to image
#         image_draw = ImageDraw.Draw(image)
#         lines = __ImageFontUtils__.text_wrap(text, ttf, max_width)
#         y_offset = start_point[1]
#         for line in lines:
#             x_offset = 0
#             if align == PyDuiTextAlign.CENTER:
#                 text_size = ttf.getsize(line)
#                 x_offset = int(round((max_width - text_size[0]) / 2))
#             elif align == PyDuiTextAlign.RIGHT:
#                 text_size = ttf.getsize(line)
#                 x_offset = max_width - text_size[0]
#             # draw shadow
#             # shadow_color = font_color
#             # blurred = Image.new(mode="RGBA", size=image.size)
#             # shadow_draw = ImageDraw.Draw(blurred)
#             # shadow_draw.text((start_point[0] + x_offset, y_offset), line, font=ttf, fill=shadow_color)
#             # blurred = blurred.filter(ImageFilter.BoxBlur(1))
#             # image.alpha_composite(blurred)
#             # blurred.close()

#             # draw text
#             image_draw.text((start_point[0] + x_offset, y_offset), line, font=ttf, fill=font_color)
#             y_offset += line_height

#     @staticmethod
#     def calc_text_size(
#         text: str, font: str, font_size: int, max_width: int, line_height_ratio: float
#     ) -> Tuple[int, int]:
#         if len(text) == 0:
#             return (0, 0)

#         ttf = ImageFont.truetype(font, font_size)
#         line_height = ttf.getsize("A")[1] * line_height_ratio
#         lines = text_wrap(text, ttf, max_width)
#         x = 0
#         y = 0
#         for line in lines:
#             size = ttf.getsize(line)
#             x = max(x, size[0])
#             y += line_height

#         return (int(x), int(y))

#     @staticmethod
#     def text_wrap(text: str, font: ImageFont, max_width: int) -> List[str]:
#         lines = []
#         # If the width of the text is smaller than image width
#         # we don't need to split it, just add it to the lines array
#         # and return

#         blocks = text.split("\n")
#         for block_text in blocks:
#             if font.getsize(block_text)[0] <= max_width:
#                 lines.append(block_text)
#             else:
#                 # split the line by spaces to get words
#                 words = block_text.split(" ")
#                 i = 0
#                 # append every word to a line while its width is shorter than image width
#                 while i < len(words):
#                     line = ""
#                     while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
#                         line = line + words[i] + " "
#                         i += 1
#                     if not line:
#                         line = words[i]
#                         i += 1
#                     # when the line gets longer than the max width do not append the word,
#                     # add the line to the lines array
#                     lines.append(line)
#         return lines


# # draw to sf
#         sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.surface.get_width() * 2, self.surface.get_height() * 2)
#         sf_ctx = cairo.Context(sf)
#         self.__do_drawing__(sf_ctx)
#         sf.flush()

#         # create image from im_surface then get the pixbuf
#         pixbuf = Gdk.pixbuf_get_from_surface(sf, 0, 0, sf.get_width(), sf.get_height())
#         scaled_pixbuf = pixbuf.scale_simple(
#             self.surface.get_width(), self.surface.get_height(), GdkPixbuf.InterpType.BILINEAR
#         )

#         # draw pixbuf to surface
#         context = cairo.Context(self.surface)
#         Gdk.cairo_set_source_pixbuf(context, scaled_pixbuf, 0, 0)
#         context.get_source().set_filter(cairo.FILTER_BEST)
#         context.paint()
#         self.surface.flush()

# fo = cairo.FontOptions()
# fo.set_antialias(cairo.ANTIALIAS_SUBPIXEL) # ANTIALIAS_SUBPIXEL
# ctx.set_font_options(fo)
# ctx.set_source_rgb(0.1, 0.1, 0.1)
# ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
# ctx.set_font_size(13)
# ctx.move_to(20, 30)
# ctx.show_text("Most relationships seem so transitory")
