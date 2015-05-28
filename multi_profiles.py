# -*- coding: utf-8 -*-
"""
/***************************************************************************
 createMultiProfiles
                                 A QGIS plugin
 Create Profiles from drainage network and ridge
                              -------------------
        begin                : 2015-05-22
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Luis Fernando Chimelo Ruiz
        email                : ruiz.ch@gmail.com
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
# Import the PyQt and QGIS libraries
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import numpy as np
try:
    import ogr
except:
    QMessageBox.information(self.iface.mainWindow(), "Problem dependences", "Install OGR/GDAL", QMessageBox.Close)
try:
    from sklearn.neighbors import BallTree
except:
    QMessageBox.information(self.iface.mainWindow(), "Problem dependences", "Install scikit-learn", QMessageBox.Close)
    
# Initialize Qt resources from file resources.
import resources_rc
# Import the code for the dialog
from multi_profiles_dialog import multiProfilesDialog
#import module calculate profiles
from funcCreateMultiProfiles import classCreateMultiProfiles
import os.path


class createMultiProfiles:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'createMultiProfiles_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        
        
        self.dlg = multiProfilesDialog()

        #INSERT EVERY SIGNAL CONECTION HERE!
        QObject.connect(self.dlg.ui.comboBoxDrainNet, SIGNAL("currentIndexChanged(int)"), self.funcComboBoxDrainNet) 
        QObject.connect(self.dlg.ui.pushButtonOutShp, SIGNAL("clicked()"), self.outputProfiles)
        QObject.connect(self.dlg.ui.pushButtonProcess,SIGNAL("clicked()"),self.process)
        QObject.connect(self.dlg.ui.pushButtonQuit,SIGNAL("clicked()"),self.exitProgram)
        #QObject.connect(self.dlg.ui.pushButtonExit,SIGNAL("clicked()"),self.exitProgram)       
        
        self.dlg.setWindowModality(QtCore.Qt.NonModal)
        self.dlg.setParent(self.iface.mainWindow(),QtCore.Qt.Dialog)
        
        #self.dlg = Ui_mainWindow()
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&CreateMultiProfiles')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'createMultiProfiles')
        self.toolbar.setObjectName(u'createMultiProfiles')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('createMultiProfiles', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/createMultiProfiles/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Create Multi Profiles'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&CreateMultiProfiles'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        self.dlg.ui.labelNumVertIter.clear()
        self.dlg.ui.labelNumVert.clear()
        #Limpar lineEdit output profiles
        self.dlg.ui.lineEditOutShp.clear()
        #Iniciar varival keysNomes
        self.keysNomes = []
        #Zera as variaveis 
        self.valueProgress = 0
        #insert zero no progress bar
        self.dlg.ui.progressBar.setValue(self.valueProgress)
        #Inserir value in neighbor and leaf size
        self.dlg.ui.lineEditNeaNeigh.setText("50")
        self.dlg.ui.lineEditLeafSize.setText("20")
        #Obter a lista de layers que estÃ¡ aberta no QGIS
        self.allLayerMap = QgsMapLayerRegistry.instance().mapLayers() 
        #Obtem uma lista de todos items que estão no mapa
        self.itensMaps=self.allLayerMap.items()
        #Obtem os nomes dos layers do mapa, a partir das chaves do dicionário
        self.keysNomes = self.allLayerMap.keys()
        #Clear widget for start
        self.dlg.ui.comboBoxDrainNet.clear()
        self.dlg.ui.comboBoxRidge.clear()
        #Obtem os layers que estao na lista dos mapas, adiciona o nome e assim busca a gemetria (dicionario)
        self.keysNomesVectors =[]
        for i  in xrange(len(self.allLayerMap.keys())):
            self.layerVectorClass = self.allLayerMap[self.keysNomes[i]] 
            if self.layerVectorClass.type() == QgsMapLayer.VectorLayer:
                self.keysNomesVectors.append(self.keysNomes[i]) 
        if len(self.keysNomesVectors) == 0:
            return QMessageBox.information(self.iface.mainWindow(), "Info", "There are no vetors in QGIS", QMessageBox.Close)
        #Inserir os nomes dos layers no combobox
        self.dlg.ui.comboBoxDrainNet.addItems(self.keysNomesVectors)      
        #obter o indice selecionado no comboboxDrainNet
        self.indexComboDrainNet = self.dlg.ui.comboBoxDrainNet.currentIndex()        
        #Remover do self.keysNomesRasters o raster que esta no combobox
        self.popkeysNomesVectors = self.keysNomesVectors.pop(self.indexComboDrainNet)
        #Inserir os nomes dos layers no combobox
        self.dlg.ui.comboBoxRidge.addItems(self.keysNomesVectors) 
        #Adicionar do self.keysNomesRasters o raster que esta no combobox
        self.keysNomesVectors.insert(self.indexComboDrainNet,self.popkeysNomesVectors)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
    def funcComboBoxDrainNet (self):
        '''Get index comboBoxDrainNet and delete in comboBoxRidge'''
        #obter o indice selecionado no comboboxDrain
        self.indexComboDrainNet = self.dlg.ui.comboBoxDrainNet.currentIndex()
        #Remover do self.keysNomesRasters o raster que esta no combobox
        self.popkeysNomesVectors = self.keysNomesVectors.pop(self.indexComboDrainNet)
        #limpar comboBoxRidge
        self.dlg.ui.comboBoxRidge.clear()
        #Adiciona os layers comboBoxRidge                                   
        self.dlg.ui.comboBoxRidge.addItems(self.keysNomesVectors)
        #Adicionar do self.keysNomesVectors o raster que esta no combobox
        self.keysNomesVectors.insert(self.indexComboDrainNet,self.popkeysNomesVectors)
        

    def outputProfiles(self):
        self.fileSHProfiles = QFileDialog.getSaveFileName(self.iface.mainWindow(), 'Save file Shapefile', '.shp', '*.shp')
        self.dlg.ui.lineEditOutShp.setText(self.fileSHProfiles)
    def exitProgram(self):
          self.dlg.hide()
    def process(self):
        #get function create profiles
        funcCreateProfiles=classCreateMultiProfiles()
        #Controlar acesso aos pontos da geometria
        ini=0
        fim=0
        cont=0
        try:
            k=int(self.dlg.ui.lineEditNeaNeigh.text())
            leaf_size_value = int(self.dlg.ui.lineEditLeafSize.text())
        except:
            QMessageBox.information(self.iface.mainWindow(), "Info", "There are no vetors in QGIS", QMessageBox.Close)
            self.dlg.hide()

         
        #Obter drive    
        driver = ogr.GetDriverByName("ESRI Shapefile")
        #Get path shapefile
        fileSHPDren= self.allLayerMap[self.dlg.ui.comboBoxDrainNet.currentText().encode()].dataProvider().dataSourceUri().split('|')[0]
        fileSHPRidge = self.allLayerMap[self.dlg.ui.comboBoxRidge.currentText().encode()].dataProvider().dataSourceUri().split('|')[0]        
        print 'fileSHPDren: ',fileSHPDren
        print 'fileSHPRidge: ',fileSHPRidge
        #Read shapefiles
        dataSourceRidge = driver.Open( fileSHPRidge, 0)
        dataSourceDren = driver.Open(fileSHPDren, 0)
        #Get layers
        cumeada = dataSourceRidge.GetLayer()
        drenagens = dataSourceDren.GetLayer()
        #Start create shapefile profiles
        funcCreateProfiles.createSHPprofiles(self.fileSHProfiles)
        #Criar array of coordenate
        cooX_dren, cooY_dren,IDX, rings= funcCreateProfiles.getCooSHP(drenagens)
        
        #Get coordenates cume
        cooX_cume, cooY_cume, IDc,r = funcCreateProfiles.getCooSHP(cumeada)
        
        #Gerar BallTree para as coordenadas da cumeada
        bTreeCume =BallTree(np.asarray(zip(cooX_cume,cooY_cume)),leaf_size=leaf_size_value) 

        #Ultimos Perfis criados
        geomProfiles=[None,None]
        #Set total vertex
        total_vert=np.sum(IDX)
        labelTolVert = 'Number vertex drainage: ' +total_vert.astype(np.string0)
        self.dlg.ui.labelNumVert.setText(labelTolVert)
        #Percorrer as linhas nao repetindo coordenadas finais
        for ind in xrange(len(IDX)):
            
            #Soma o valor de indice da linha
            fim = fim +IDX[ind]
            #Insert first and last coo
            cooX_dren_subset= cooX_dren[ini:fim]
            #Duplicate first and last coordenate
            cooX_dren_subset=np.insert(cooX_dren_subset,[len(cooX_dren_subset),0],[cooX_dren_subset[-1],cooX_dren_subset[0]])
            cooY_dren_subset= cooY_dren[ini:fim]
            #Duplicate first and last coordenate
            cooY_dren_subset=np.insert(cooY_dren_subset,[len(cooY_dren_subset),0],[cooY_dren_subset[-1],cooY_dren_subset[0]])
            print cooX_dren_subset
            
            #Percorre cada linha mas termina no ultimo ponto, cotrolado pelo IND
            for j in xrange(1,IDX[ind]+1):
                cont=cont+1
                #labelTolVert = labelTolVert+ ' - '+ str(j)
                self.dlg.ui.labelNumVertIter.setText(str(cont))
                #Procurar o ponto de cumeada mais perto da drenagem, retorna distacia e indice na lista                   
                distVizinhos, idxVizinhos= bTreeCume.query([cooX_dren_subset[j],cooY_dren_subset[j]],k)
               
                #Calcula os angulos do alinhamento drenagem ate drenagem
                azAlinDrePosterior = funcCreateProfiles.getAzimute((cooX_dren_subset[j+1]-cooX_dren_subset[j]),(cooY_dren_subset[j+1]-cooY_dren_subset[j]))
                azAlinDreAnterior = funcCreateProfiles.getAzimute((cooX_dren_subset[j-1]-cooX_dren_subset[j]),(cooY_dren_subset[j-1]-cooY_dren_subset[j]))
                #Create array alin only with azimuth
                azAlinDreAntPos=[azAlinDreAnterior[0],azAlinDrePosterior[0]]
               
                #Percorrer as coordenadas K do cume mais proximas da drengagem
                geomProfiles = funcCreateProfiles.assesCreateProfiles(idxVizinhos[0],cooX_cume,cooY_cume,cooX_dren_subset,cooY_dren_subset,j,rings,geomProfiles,azAlinDreAntPos)
                self.dlg.ui.progressBar.setValue(int((100*cont)/total_vert))
            #Indica o valor para iniciar o FOR
            ini = ini+IDX[ind]  
        funcCreateProfiles.outDS.Destroy() 
        self.dlg.ui.progressBar.setValue(100)