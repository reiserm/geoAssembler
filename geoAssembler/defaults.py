
"""Methods and classes that handle different detectors and their defaults."""

import os

INC = 1

class DefaultGeometryConfig:
    """Define global default configuration parameters."""
    # Fallback quad positions if no geometry file is given as a starting point:
    #from .geometry import AGIPDGeometry, LPDGeometry
    fallback_quad_pos = {
                        'AGIPD': [(-540, 610),
                                  (-540, -15),
                                  (540, -143),
                                  (540, 482)],
                        'LPD': [(11.4, 299),
                                (-11.5, 8),
                                (254.5, -16),
                                (278.5, 275)]
                        }

    # Definition of increments (INC) the quadrants should move
    # (u = up, d = down, r = right, l = left is given:
    direction = {'u': (0, -INC),
                 'd': (0, INC),
                 'r': (INC, 0),
                 'l': (-INC, 0)}
    # Translate quad's into module indices
    quad2index = {
                  'AGIPD' : {1: 12, 2: 8, 3: 4, 4: 0},
                  'LPD' : {1: 12, 2: 8, 3: 4, 4: 0},
                }

    canvas_margin = 300  # pixel, used as margin on each side of detector quadrants
    geom_sel_width = 114

    # Default colormaps
    cmaps = ['binary_r',
             'viridis',
             'coolwarm',
             'winter',
             'summer',
             'hot',
             'OrRd']

    # Default file formats for certain detectors
    file_formats = {
                    'AGIPD': ('CFEL', '*.geom'),
                    'LPD': ('XFEL', '*.h5')
                   }
