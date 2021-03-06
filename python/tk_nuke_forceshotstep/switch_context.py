# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
from sgtk import TankError
import os
import sys
import threading


# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog

def execute():
    try:
        step = sgtk.platform.current_bundle().get_setting("pipeline_step")
        context = sgtk.platform.current_engine().context
        currentShot = context.entity
        filters = [["project", "is", context.project],
                ["step", "name_contains", step],
                ['entity', 'is', currentShot]]
        fields = ['id']
        result = sgtk.platform.current_engine().shotgun.find("Task", filters, fields)
        tk = sgtk.sgtk_from_entity("Task",result[0]["id"])
        ctx = tk.context_from_entity("Task", result[0]["id"])
        print "Changing context to " +str(ctx)
        sgtk.platform.change_context(ctx)
    except:
        #QtGui.QMessageBox.warning(None,"Force Shot-Step Context","tk-nuke-forceshotstep Could not switch context! Check to be sure that the nuke script is named correctly and that the current shot has a task in the work area defined in the configuration.")
        raise TankError("tk-nuke-forceshotstep Could not switch context! Check to be sure that the nuke script is named correctly and that the current shot has a task in the work area definted in the configuration.")

def auto_switch():
    # We must run this in the main thread, but it's being called from a timer.
    sgtk.platform.current_engine().execute_in_main_thread(execute)
    

class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """
    
    def __init__(self):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)
        
        # now load in the UI that was created in the UI designer
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)
        
        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self._app = sgtk.platform.current_bundle()
        
        # via the self._app handle we can for example access:
        # - The engine, via self._app.engine
        # - A Shotgun API instance, via self._app.shotgun
        # - A tk API instance, via self._app.tk 
        
        # lastly, set up our very basic UI
        self.ui.context.setText("Current Context: %s" % self._app.context)
        
        
