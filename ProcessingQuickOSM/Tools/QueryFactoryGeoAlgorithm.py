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

from QuickOSM.CoreQuickOSM.QueryFactory import QueryFactory
from os.path import isfile,join,basename,dirname,abspath


class QueryFactoryGeoAlgorithm(GeoAlgorithm):
    '''
    Build a query with parameters 
    '''
    
    def __init__(self):
        self.FIELD_KEY = 'FIELD_KEY'
        self.FIELD_VALUE = 'FIELD_VALUE'
        self.FIELD_EXTENT = 'FIELD_EXTENT'
        self.FIELD_NOMINATIM = 'FIELD_NOMINATIM'
        self.FIELD_OSM_OBJECTS = 'FIELD_OSM_OBJECTS'
        self.FIELD_TIMEOUT = 'FIELD_TIMEOUT'
        self.OUTPUT_QUERY = 'OUTPUT_QUERY'
        GeoAlgorithm.__init__(self)
        
    def defineCharacteristics(self):
        self.name = "Query factory"
        self.group = "Tools"
        
        self.addParameter(ParameterString(self.FIELD_KEY, 'Key','',optional=False))
        self.addParameter(ParameterString(self.FIELD_VALUE, 'Value','',optional=True))
        self.addParameter(ParameterExtent(self.FIELD_EXTENT, 'Extent (999,999,999,999 is wrong value)', default="999,999,999,999"))
        self.addParameter(ParameterString(self.FIELD_NOMINATIM, 'Nominatim',optional=True))
        
        #osm_objects = ['node','way','relation','all']
        #self.addParameter(ParameterSelection(self.FIELD_OSM_OBJECTS, 'OSM objects', osm_objects, default=3))
        
        self.addParameter(ParameterNumber(self.FIELD_TIMEOUT, 'Timeout',minValue=20, default=25))        
        
        self.addOutput(OutputString(self.OUTPUT_QUERY,"Query"))

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
        key = self.getParameterValue(self.FIELD_KEY)
        value = self.getParameterValue(self.FIELD_VALUE)
        extent = self.getParameterValue(self.FIELD_EXTENT)
        nominatim = self.getParameterValue(self.FIELD_NOMINATIM)
        
        if nominatim == '':
            nominatim = None
        
        if value == '':
            value = None
        
        if extent == "999,999,999,999":
            extent = None
        
        #osmObjects = self.getParameterValue(self.FIELD_OSM_OBJECTS)
        timeout = self.getParameterValue(self.FIELD_TIMEOUT)
        
        #Missing OSMObjects
        queryFactory = QueryFactory(key = key, value = value, nominatim = nominatim, bbox=extent,timeout=timeout)
        query = queryFactory.make()
        
        self.setOutputValue(self.OUTPUT_QUERY,query)