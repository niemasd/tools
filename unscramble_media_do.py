#! /usr/bin/env python3
'''
Unscramble a JPG + XML pair from Media Do
'''

# imports
from pathlib import Path
from PIL import Image
from sys import argv
from xml.etree import ElementTree

# main program
if __name__ == "__main__":
    # check user args
    if len(argv) not in {3,5} or argv[1].split('-')[-1].strip().lower() in {'h', 'help'}:
        print("USAGE: %s <jpg> <xml> [zone_width] [zone_height]" % argv[0]); exit(1)
    img_scrambled_path = Path(argv[1].strip()).expanduser().absolute()
    xml_path = Path(argv[2].strip()).expanduser().absolute()
    for p in [img_scrambled_path, xml_path]:
        if not p.is_file():
            raise ValueError("Input file not found: %s" % p)
    img_unscrambled_path = img_scrambled_path.parent / (img_scrambled_path.stem + '.unscrambled.jpg')
    if img_unscrambled_path.exists():
        raise ValueError("Output file exists: %s" % img_unscrambled_path)
    try:
        img_scrambled = Image.open(img_scrambled_path)
    except:
        raise ValueError("Unable to open Media Do JPG: %s" % img_scrambled_path)

    # determine width and height (either user-provided, or width // 4 and height // 4)
    if len(argv) == 3:
        zone_width = img_scrambled.width // 4
        zone_height = img_scrambled.height // 4
    else:
        try:
            zone_width = int(argv[3])
            assert zone_width > 0
        except:
            raise ValueError("Invalid zone width: %s" % argv[3])
        try:
            zone_height = int(argv[4])
            assert zone_height > 0
        except:
            raise ValueError("Invalid zone height: %s" % argv[4])

    # load scramble data from XML
    xml_root = ElementTree.parse(xml_path).getroot()
    scramble = [int(v) for v in xml_root.find('Scramble').text.split(',')]
    if len(scramble) != 16:
        raise ValueError("Expected scramble length of 16, but it was %d: %s" % (len(scramble), xml_path))

    # unscramble image
    img_unscrambled = img_scrambled.copy()
    img_width, img_height = img_unscrambled.size
    for unscrambled_zone, scrambled_zone in enumerate(scramble):
        unscrambled_x_start = (unscrambled_zone % 4) * zone_width
        unscrambled_y_start = (unscrambled_zone // 4) * zone_height
        scrambled_x_start = (scrambled_zone % 4) * zone_width
        scrambled_y_start = (scrambled_zone // 4) * zone_height
        img_zone = img_scrambled.crop((scrambled_x_start, scrambled_y_start, scrambled_x_start+zone_width, scrambled_y_start+zone_height))
        img_unscrambled.paste(img_zone, (unscrambled_x_start, unscrambled_y_start, unscrambled_x_start+zone_width, unscrambled_y_start+zone_height))
    img_unscrambled.save(img_unscrambled_path, quality=95)
