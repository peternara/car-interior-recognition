import os
import argparse

"""
Converts all filenames to number given ext
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Path to directory of files",
                        required=True)
    parser.add_argument("-ext", "--extension", help="Extension of files",
                        required=True)
    parser.add_argument("-prefix", "--prefix", help="New filename prefix",
                        required=True)

    args = parser.parse_args()

    ext = args.extension
    if ext.find('.') != -1:
        ext = ext[1:]

    i = 1
    for f in os.listdir(args.path):
        if f.endswith(ext):
            fullpath = os.path.join(args.path, f)
            newpath = os.path.join(args.path, """{}_{}.{}""".format(args.prefix, i, ext))
            os.rename(fullpath, newpath)
            i += 1


