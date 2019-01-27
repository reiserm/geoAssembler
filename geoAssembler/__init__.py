"""Call the calibration routine for ringbased calibration

Copyright (c) 2017, European X-Ray Free-Electron Laser Facility GmbH
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

You should have received a copy of the 3-Clause BSD License along with this
program. If not, see <https://opensource.org/licenses/BSD-3-Clause>


Author: bergeman
"""


__version__ = "0.1.0"


from pyqtgraph import QtGui

from .nb_viewer import CalibrateNb
from .qt_viewer import CalibrateQt


def Calibrate(*args, **kwargs):
    """Parameters:
            data (2d-array)  : File name of the geometry file, if none is given
                               (default) the image will be assembled with 29 Px
                               gaps between all modules.

            Keywords:
             geom (str/AGIPD_1MGeometry) :  The geometry file can either be
                                            an AGIPD_1MGeometry object or
                                            the filename to the geometry file
                                            in CFEL fromat
             vmin (int) : minimal value in the data array (default: -1000)
                          anything below this value will be clipped
             vmax (int) : maximum value in the data array (default: 5000)
                          anything above this value will be clipped
        """

    app = QtGui.QApplication([])
    calib = CalibrateQt(*args, **kwargs)
    calib.window.show()
    app.exec_()
    app.closeAllWindows()
    return calib
