# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
                             -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info at 3liz dot com
        contributor          : Etienne Trimaille
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from QuickOSM import *
from QuickOSM.ProcessingQuickOSM import *

from os.path import isfile,join,basename,dirname,abspath
from QuickOSM.CoreQuickOSM.FileQuery import FileQuery
from QuickOSM.CoreQuickOSM.Tools import *


class ListIniFilesGeoAlgorithm(GeoAlgorithm):
    '''
    List all the INI files 
    '''
    
    def __init__(self):
        self.NAME_FILE = 'NAME'
        self.OUTPUT_INI = 'INI'
        GeoAlgorithm.__init__(self)
        
    def defineCharacteristics(self):
        self.name = "Queries available"
        self.group = "Tools"
        
        #Get the folder and all filequeries
        folder = Tools.getUserQueryFolder()
        catfiles = FileQuery.getIniFilesFromFolder(folder,force=False)
        
        self.__queries = {}
        for cat in catfiles:
            for query in catfiles[cat]:
                self.__queries[cat + " : " + query.getName()] = query
        
        self.__names = self.__queries.keys()
        
        self.addParameter(ParameterSelection(self.NAME_FILE, 'Queries available', self.__names))
        
        self.addOutput(OutputString(self.OUTPUT_INI,"Ini filepath as string"))

    def help(self):
        locale = QSettings().value("locale/userLocale")[0:2]
        locale = "." + locale

        currentFile = __file__
        if currentFile.endswith('pyc'):
            currentFile = currentFile[:-1]
        currentFile = basename(currentFile)
        
        helps = [currentFile + locale +".html", currentFile + ".html"]
        
        docPath = join(dirname(dirname(dirname(abspath(__file__)))),'doc')
        for helpFileName in helps :
            fileHelpPath = join(docPath,helpFileName)
            if isfile(fileHelpPath):
                return False, fileHelpPath
        
        return False, None
    
    def getIcon(self):
        return QIcon(dirname(__file__) + '/../../icon.png')
        
    def processAlgorithm(self, progress):
        index = self.getParameterValue(self.NAME_FILE)
        for query in self.__queries:
            if query == self.__names[index]:
                path = self.__queries[query].getFilePath()
                self.setOutputValue(self.OUTPUT_INI,path)