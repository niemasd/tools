#! /usr/bin/env python3
'''
Convert a graphic novel epub to cbz
'''

# imports
from io import BytesIO
from natsort import natsorted
from pathlib import Path
from PIL import Image
from sys import argv
from xml.etree import ElementTree
from zipfile import ZipFile, Path as ZipPath

# useful constants
IMG_SUFFIXES = {'.arw', '.bmp', '.cr2', '.gif', '.jpeg', '.jpg', '.pdf', '.png', '.raw', '.rw2', '.svg', '.tif', '.tiff', '.webp'}
XML_SUFFIXES = {'.html', '.xhtml', '.xml'}

# main program
if __name__ == "__main__":
    # check user args
    if len(argv) != 2 or argv[1].split('-')[-1].strip().lower() in {'h', 'help'}:
        print("USAGE: %s <epub>" % argv[0]); exit(1)
    epub_path = Path(argv[1].strip()).expanduser().absolute()
    if not epub_path.is_file():
        raise ValueError("Input file not found: %s" % epub_path)
    cbz_path = Path('.').expanduser().absolute() / epub_path.parent.name / (epub_path.stem + '.cbz')
    if cbz_path.exists():
        raise ValueError("Output file exists: %s" % cbz_path)

    # load data from input epub
    with ZipFile(epub_path, mode='r') as epub_zip:
        # parse epub to build page map, which maps page numbers to image paths
        page_map = dict() # keys = page number as integer (0 = cover, 1-n = pages); values = ZipPath to image file
        
        # check replicaMap.xml
        replicaMap_xml_path = ZipPath(epub_zip, at='OPS/replicaMap.xml'); replicaMap_xml = None
        if replicaMap_xml_path.is_file():
            try:
                replicaMap_xml = ElementTree.fromstring(replicaMap_xml_path.read_text())
            except:
                pass

        # Barnes and Noble epub (not really valid epub)
        if replicaMap_xml is not None:
            replicaMap_xml_pages = None
            for child in replicaMap_xml:
                if child.tag.strip().endswith('Pages'):
                    replicaMap_xml_pages = child; break
            if replicaMap_xml_pages is None:
                raise ValueError("Invalid replicaMap.xml file in epub: %s" % epub_path)
            for child in replicaMap_xml_pages:
                if child.tag.strip().endswith('Page'):
                    page_num = int(child.attrib['pageNum'])
                    if page_num in page_map:
                        raise ValueError("Duplicate page number (%d) in replicaMap.xml in epub: %s" % (page_num, epub_path))
                    page_file_path = ZipPath(epub_zip, at='OPS/' + child.attrib['file'].strip().lstrip('/').strip())
                    if not page_file_path.is_file():
                        raise ValueError("Page file from replicaMap.xml (%s) not found in epub: %s" % (page_file_path, epub_path))
                    page_map[page_num] = page_file_path
            if min(page_map.keys()) != 0:
                raise NotImplementedError("TODO HANDLE MISSING COVER: ADD AS PAGE 0")

        # general epub
        else:
            # check epub for validity and load container.xml
            try:
                assert epub_zip.read('mimetype').decode().strip().lower() == 'application/epub+zip'
                container_xml = ElementTree.fromstring(epub_zip.read('META-INF/container.xml').decode())
            except:
                raise ValueError("Input file is not a valid epub: %s" % epub_path)
            container_xml_container_xml_rootfiles = None
            for child in container_xml:
                if child.tag.strip().endswith('rootfiles'):
                    container_xml_container_xml_rootfiles = child; break
            if container_xml_container_xml_rootfiles is None:
                raise ValueError("Input file is not a valid epub: %s" % epub_path)
            container_xml_rootfile = None
            for child in container_xml_container_xml_rootfiles:
                if child.tag.strip().endswith('rootfile'):
                    container_xml_rootfile = child; break
            if container_xml_rootfile is None:
                raise ValueError("Input file is not a valid epub: %s" % epub_path)
            rootfile_path = container_xml_rootfile.attrib['full-path']
            rootfile_base_dir = ZipPath(epub_zip, at=rootfile_path).parent

            # parse rootfile
            try:
                rootfile_xml = ElementTree.fromstring(epub_zip.read(rootfile_path).decode())
            except:
                raise ValueError("Input file is not a valid epub: %s" % epub_path)
            manifest_xml = None; spine_xml = None; guide_xml = None
            for child in rootfile_xml:
                child_tag_strip = child.tag.strip()
                if child_tag_strip.endswith('manifest'):
                    manifest_xml = child
                elif child_tag_strip.endswith('spine'):
                    spine_xml = child
                elif child_tag_strip.endswith('guide'):
                    guide_xml = child
            if manifest_xml is None or spine_xml is None or guide_xml is None:
                raise ValueError("Input file is not a valid epub: %s" % epub_path)
            
            # parse manifest
            manifest_map = dict() # keys = ids; values = ZipPath to href file
            for child in manifest_xml:
                if child.tag.strip().endswith('item'):
                    item_id = child.attrib['id'].strip()
                    if item_id in manifest_map:
                        raise ValueError("Duplicate ID (%s) in manifest section of rootfile in epub: %s" % (item_id, epub_path))
                    item_href_path = rootfile_base_dir / child.attrib['href'].strip()
                    if not item_href_path.exists():
                        raise ValueError("File not found in epub: %s" % item_href_path)
                    manifest_map[item_id] = item_href_path

            # parse guide for cover
            spine_xml_children = list(spine_xml)
            for child in guide_xml:
                if child.attrib['type'].strip().lower() == 'cover':
                    child_path = rootfile_base_dir / child.attrib['href'].strip()
                    if child_path.is_file():
                        spine_xml_children = [child] + spine_xml_children

            # parse spine
            spine_files = list(); xml_pages_parsed = set()
            for child in spine_xml_children:
                if child.tag.strip().endswith('itemref'):
                    item_href_path = manifest_map[child.attrib['idref'].strip()]
                    item_href_path_suffix = item_href_path.suffix.strip().lower()

                    # if this item isn't itself an image, need to search for an image within it
                    if item_href_path_suffix not in IMG_SUFFIXES:
                        # if this item is an XML/HTML, search for image within it
                        if item_href_path_suffix in XML_SUFFIXES and str(item_href_path) not in xml_pages_parsed:
                            try:
                                item_href_xml = ElementTree.fromstring(item_href_path.read_text())
                            except:
                                continue
                            image_xmls = [child for child in item_href_xml.iter() if child.tag.strip().endswith('img') or child.tag.strip().endswith('image')]
                            if len(image_xmls) != 1:
                                raise ValueError("Expected exactly 1 image file, but there were %d: %s" % (len(image_xmls), item_href_path))
                            image_path = None
                            for val in image_xmls[0].attrib.values():
                                val_parts = [s.strip() for s in val.strip().split('/')]
                                val_path = item_href_path.parent
                                for val_part in val_parts:
                                    if val_part == '..':
                                        val_path = val_path.parent
                                    else:
                                        val_path = val_path / val_part
                                if val_path.suffix in IMG_SUFFIXES:
                                    image_path = val_path
                            if image_path is None:
                                raise ValueError("No image files detected in: %s" % item_href_path)
                            elif not image_path.is_file():
                                raise ValueError("Image file not found: %s" % image_path)
                            xml_pages_parsed.add(str(item_href_path))
                            item_href_path = image_path

                        # this item is some unknown type
                        else:
                            raise NotImplementedError("Unsupported spine item filetype: %s" % item_href_path)
                    spine_files.append(item_href_path)

            # populate page_map
            page_map = {page_num : spine_file for page_num, spine_file in enumerate(spine_files)}

        # if didn't find any pages, manually search for all images ending with a number
        if len(page_map) == 0:
            cover = None; page_paths = list()
            for fn in epub_zip.namelist():
                fn_path = ZipPath(epub_zip, fn)
                if fn_path.suffix in IMG_SUFFIXES:
                    if cover is None and 'cover' in str(fn_path).lower():
                        cover = fn_path
                    elif fn_path.stem.strip()[-1].isdigit():
                        page_paths.append(fn_path)
            page_paths = natsorted(page_paths, key=lambda x: str(x))
            if cover is not None:
                page_paths = [cover] + page_paths
            page_map = {page_num : page_path for page_num, page_path in enumerate(page_paths)}

        # write images to output cbz file
        if len(page_map) == 0:
            raise ValueError("Failed to parse any page images from epub: %s" % epub_path)
        sorted_page_nums = sorted(page_map.keys())
        pad_length = len(str(sorted_page_nums[-1]))
        cbz_path.parent.mkdir(exist_ok=True)
        with ZipFile(cbz_path, mode='w', compresslevel=9) as cbz_zip:
            for page_num in sorted_page_nums:
                page_file_path = page_map[page_num]
                img_data = page_file_path.read_bytes()
                try:
                    Image.open(BytesIO(img_data)) # if this crashes, image data is corrupt
                    cbz_zip.writestr(str(page_num).zfill(pad_length) + page_file_path.suffix, img_data)
                except:
                    raise ValueError("Invalid image: %s" % page_file_path)