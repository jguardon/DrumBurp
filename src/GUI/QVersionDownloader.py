# Copyright 2011-12 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>
'''
Created on Mar 31, 2013

@author: Mike Thomas
'''

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QTimer
from DBVersion import doesNewerVersionExist
from ui_versionDownloader import Ui_VersionDownloader
class QVersionDownloader(QDialog, Ui_VersionDownloader):
    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(QVersionDownloader, self).__init__(parent = parent)
        self.setupUi(self)
        QTimer.singleShot(0, self._download)

    def _download(self):
        newer = doesNewerVersionExist()
        self.resultBox.setEnabled(True)
        self.message.setText("Finished.")
        if newer is None:
            self.resultLabel.setText("Could not access version information.")
        elif newer == "":
            self.resultLabel.setText("No newer version is available.")
        else:
            self.resultLabel.setText("DrumBurp version %s is now available "
                                     "from <a href='http://www.whatang.org'>"
                                     "www.whatang.org</a>" % newer)


