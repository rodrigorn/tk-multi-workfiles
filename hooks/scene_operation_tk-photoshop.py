# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import photoshop

from tank import Hook
from tank import TankError

class SceneOperation(Hook):
    """
    Hook called to perform an operation with the
    current scene
    """
    
    def execute(self, operation, file_path, context, parent_action, **kwargs):
        """
        Main hook entry point
        
        :operation:     String
                        Scene operation to perform
        
        :file_path:     String
                        File path to use if the operation
                        requires it (e.g. open)
                    
        :context:       Context
                        The context the file operation is being
                        performed in.
                    
        :parent_action: This is the action that this scene operation is
                        being executed for.  This can be one of: 
                        - open_file
                        - new_file
                        - save_file_as 
                        - version_up
                            
        :returns:       Depends on operation:
                        'current_path' - Return the current scene
                                         file path as a String
                        'reset'        - True if scene was reset to an empty 
                                         state, otherwise False
                        all others     - None
        """

        if operation == "current_path":
            # return the current script path
            doc = self._get_active_document()

            if doc.fullName is None:
                # new file?
                path = ""
            else:
                path = doc.fullName.nativePath
            
            return path

        elif operation == "open":
            # open the specified script
            f = photoshop.RemoteObject('flash.filesystem::File', file_path)
            photoshop.app.load(f)            
        
        elif operation == "save":
            # save the current script:
            doc = self._get_active_document()
            doc.save()
        
        elif operation == "save_as":
            doc = self._get_active_document()
            new_file_name = photoshop.RemoteObject('flash.filesystem::File', file_path)
            # no options and do not save as a copy
            # http://cssdk.host.adobe.com/sdk/1.5/docs/WebHelp/references/csawlib/com/adobe/photoshop/Document.html#saveAs()
            doc.saveAs(new_file_name, None, False)

        elif operation == "reset":
            # do nothing and indicate scene was reset to empty
            return True
        
        elif operation == "prepare_new":
            # file->new. Not sure how to pop up the actual file->new UI,
            # this command will create a document with default properties
            photoshop.app.documents.add()
        
    def _get_active_document(self):
        """
        Returns the currently open document in Photoshop.
        Raises an exeption if no document is active.
        """
        doc = photoshop.app.activeDocument
        if doc is None:
            raise TankError("There is no currently active document!")
        return doc