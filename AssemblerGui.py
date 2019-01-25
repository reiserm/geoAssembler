#!/usr/bin/env python3
"""Script that run geoAssembler GUI."""
import os
import sys

from argparse import ArgumentParser
import numpy as np

from geoAssembler import Calibrate


def set_args(argv=None):
    """Define the help string."""
    ap = ArgumentParser(description="""
    This prgram allows for a ring based geometry calibration.

    The program will open a GUI to assemble data according to a geometry that
    can either be loaded or that can be based on fixed quadrant positions.

    To select quadrants click on the quadrant and to move the selected quadrant
    use CTRL+arrow-keys.""")

    ap.add_argument('-r','--run', default=None,
                    help='Select a run')
    ap.add_argument('-g','--geometry', default=None,
                    help='Select a cfel geometry file')
    ap.add_argument('-c','--clen', default=0.119,
                    help='Detector distance [m]')
    ap.add_argument('-e','--energy', default=10235,
                    help='Photon energy [ev]')
    ap.add_argument('-l','--level', nargs='+', default=None, type=int,
                    help='Pre defined display range for plotting')
    return ap.parse_args(argv)


if __name__ == '__main__':

    # First lets load the data, this can either be done by karabo-data's
    # RunDirectory, a virtual dataset or by reading the data from hdf files.
    # The only constraint is that the data should be of shape (16x512x128)
    # which means only one image

    # Get some mock data for testing
    #
    args = set_args()

    # Define a header that should be added to the geometry file, this is useful
    # to use the geometry file with tools like hdfsee
    header = """data = /entry_1/data_1/data
;mask = /entry_1/data_1/mask

mask_good = 0x0
mask_bad = 0xffff

adu_per_eV = 0.0075  ; no idea
clen = {}  ; Camera length, aka detector distance
photon_energy = {} ;""".format(args.clen, args.energy)

    try:
        levels = args.level[:2]
    except IndexError:
        raise IndexError('Levels should be one min and one max value')
    except TypeError:
        levels = args.level
    C = Calibrate(args.run, args.geometry, levels=levels, header=header)

    # The centre coordinates might be of interest (i.e azimuthal integration)
    #print('Geometry-centre is P(y: {}/x: {})'.format(*C.centre))
