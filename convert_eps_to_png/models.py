from django.db import models

from PIL import Image


class converter:
    DEFINITION 	= (2048, 2048)
    SCALE 		= 8


    def convert_eps_to_png(file_name):
        ts = turtle.getscreen()
        ts.getcanvas().postscript(file=file_name + ".eps")
        TARGET_BOUNDS = (DEFINITION)
        pic = Image.open('dna_walk.eps')
        pic.load(scale=SCALE)
        if pic.mode in ('P', '1'):
            pic = pic.convert("RGB")
        ratio = min(TARGET_BOUNDS[0] / pic.size[0],
                    TARGET_BOUNDS[1] / pic.size[1])
        new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))
        pic = pic.resize(new_size, Image.ANTIALIAS)
        pic.save(file_name + ".png")