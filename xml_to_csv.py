import xmltodict
import argparse
import pandas as pd
import csv
import os
import sys

"""
Converts label xml files from LabelImg to csv files.

Format:
filename, width, height, class, xmin, ymin, xmax, ymax

Usage:
    python3 xml_to_csv.py --path path/to/xml/ --output path/to/file

"""

OUTPUT_NAME = "labels.csv"

class FeatureSet:
    """
    Represents an image with labels. It expects the xml structure from
    LabelImg.

    Expects filename, width, height, class, xmin, xmax, ymin, ymax
    attributes.
    """
    def __init__(self, xmlpath=None):
        self._filename = None 
        self._path = None

        self._width = None 
        self._height = None 

        self._cls = None 

        self._xmin = None 
        self._ymin = None 

        self._xmax = None 
        self._ymax = None 

        self.initialized = False

        if xmlpath:
            self.readxml(xmlpath)

    def columns():
        return ['filename',
                'width',
                'height',
                'class',
                'xmin',
                'ymin',
                'xmax',
                'ymax'
                ]

    def readxml(self, filepath):

        self.initialized = False

        if not filepath.endswith('xml'):
            return

        with open(filepath) as fd:
            doc = xmltodict.parse(fd.read())

            self._filename = doc['annotation']['filename'] 
            self._path = doc['annotation']['path']

            self._width = doc['annotation']['size']['width']
            self._height = doc['annotation']['size']['height']

            self._cls = doc['annotation']['object']['name']

            self._xmin = doc['annotation']['object']['bndbox']['xmin']
            self._ymin = doc['annotation']['object']['bndbox']['ymin']

            self._xmax = doc['annotation']['object']['bndbox']['xmax']
            self._ymax = doc['annotation']['object']['bndbox']['ymax']

            if not self._filename or not self._path:
                return
            if not self._width or not self._height:
                return
            if not self._cls:
                return
            if not self._xmin or not self._ymin:
                return
            if not self._xmax or not self._ymax:
                return

            self.initialized = True 

    def values(self):
        if not self.initialized:
            print("[INFO] Not initialized.")
            return ""

        return (self._filename,
                self._width,
                self._height,
                self._cls,
                self._xmin,
                self._ymin,
                self._xmax,
                self._ymax)


if __name__ == "__main__":
    """ 
    We are expecting a directory as an argument.

    The directory is expected to contain all the 
    target xml files.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--path',
        help="path to directory containing labelImg xml files",
        required=True
    )

    parser.add_argument('-o', '--output',
        help="path to make output file",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print("""[INFO] {} is not a directory.""".format(args.path))
        sys.exit(-1)

    if args.output:
        if not os.path.isdir(args.output): 
            output_fullpath = args.output 
        else:
            output_fullpath = os.path.join(args.output, OUTPUT_NAME)
    else:
        output_fullpath = OUTPUT_NAME

    rows = []
    for xmlfile in os.listdir(args.path):
        feature = FeatureSet(os.path.join(args.path, xmlfile))
        if feature.initialized:
            rows.append(feature.values())
    
    pd.DataFrame(rows, columns=FeatureSet.columns()).to_csv(
        output_fullpath, index=None) 

    print("""[INFO] Completed.""")

