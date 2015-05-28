# -*- coding: utf-8 -*-
"""
Created on Wed May 27 13:48:37 2015

@author: ruiz
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 11:36:01 2015

@author: ruiz
"""
import os
import ogr
import numpy as np
import math

class classCreateMultiProfiles():
    """Gerar multi perfis a partir das drenagenagens e da linha de cumeada"""
          
    def getCooSHP(self,layer):
        
        rings=[]
        self.layer=layer
        """Gerar array com as coordenadas dos vertices
        Return -> ndarray cooX e cooY"""
        #Inicializar array auxiliares            
        cooX=np.array([],dtype=np.float16)
        cooY=np.array([],dtype=np.float16)
        idx =np.array([],dtype=np.int16)        
        #Percorrer as geometrias
        for featDren in self.layer: 
            #Obter geometrias
            geom = featDren.GetGeometryRef()
            #Obter geometrias rings
            countRing= geom.GetGeometryCount()
            #Obter a geometria dos rings
            for i in xrange(countRing):
                #Obter os pontos de uma geometria
                ring=geom.GetGeometryRef(i)
                
                #print ring.ExportToWkt()
                rings.append(ring.ExportToWkt())
                #print ring.GetPointCount()
                points = ring.GetPoints()                
                #arrayDren = np.append(arrayDren,np.asarray(points),axis=0)        
                idx =np.append(idx,np.asarray(ring.GetPointCount()))
                cooX =np.append(cooX,np.asarray(points)[:,0])
                cooY =np.append(cooY,np.asarray(points)[:,1])             
                
        return cooX,cooY, idx,rings
    def createSHPprofiles(self, path_file):
        '''
        Create the shapefile profiles
        '''
        #create variables
        self.path_file=path_file
        #Deletar caso existente
        DriverName = "ESRI Shapefile"      # e.g.: GeoJSON, ESRI Shapefile

        driver = ogr.GetDriverByName(DriverName)
        if os.path.exists(self.path_file):
            driver.DeleteDataSource(self.path_file)
        #Criar layer perfis
        self.outDS= driver.CreateDataSource(self.path_file)
        self.outLayer=self.outDS.CreateLayer('perfis',geom_type=ogr.wkbLineString)
        outFeatDef=self.outLayer.GetLayerDefn()
        self.outFeat=ogr.Feature(outFeatDef)
        
    
    def getAzimute(self,Dx,Dy):
        """Obter o azimute a partir da diferenca das coordenadas
        Return -> Azimute, minAng e maxAng"""
        self.Dx= Dx
        self.Dy=Dy
        try:
            #Calcular azimute radianos
            rumo = math.atan((self.Dx/self.Dy))
        except:
            rumo=0
               
        #Converter para graus
        rumo = math.degrees(rumo)
        #Converter para 0-360
        if self.Dx ==0:
                azimute=0
                minAng=0
                maxAng=180
        
        elif self.Dy ==0:
                azimute=90
                minAng=90
                maxAng=270
           
        elif self.Dx > 0:
            if self.Dy >0:
                azimute= rumo
                minAng = azimute
                maxAng= rumo + 180
            else:
                azimute = rumo+180
                minAng = azimute
                maxAng= azimute+ 180
        else:
            if self.Dy > 0:
                azimute= rumo +360
                maxAng = azimute
                minAng = rumo+ 180
            else:
                azimute= 180+ rumo
                maxAng = azimute
                minAng = rumo
               
        return [round(azimute,3),round(maxAng,3),round(minAng,3)]
  
    #Gerar BallTree para as coo
    def assesCrosses(self,alinhamento, linesDren):
        #Iniciar vairiaveis        
        self.alinamentoDrenCume= alinhamento
        self.linesDren= linesDren
        values=[]
        #Assess across
        for ring in self.linesDren:
                
                values.append(ogr.CreateGeometryFromWkt(ring).Crosses(self.alinamentoDrenCume))
        
        return values
    def assesCrossesProfiles(self,alinDrenCume, profiles):            
        #Iniciar variaveis
        self.alinDrenCume = alinDrenCume
        self.profiles = profiles
        assessProfiles=[]
        
        #Verificar se cruza
        for geom in self.profiles:
            #print 'geom: ',geom
            if geom == None:
                assessProfiles.append(False)
            else:
                #for geom in profiles:
                assessProfiles.append(geom.Crosses(self.alinDrenCume))
                #assessProfiles.append(profiles[-2].Crosses(self.alinDrenCume))
        return assessProfiles
        
    def assesCreateProfiles(self,idxNeighbor,cooX_cume,cooY_cume,cooX_dren,cooY_dren, idxDren,rings, geomProfiles,azAlinDreAntPos):
        '''
        Create profiles
        Assess profiles across drainage
        Return profilies for two sides
        '''        
        proc = classCreateMultiProfiles()        
        #Create variable
        self.idxNeighbor = idxNeighbor
        self.cooX_cume =cooX_cume
        self.cooY_cume=cooY_cume
        self.cooX_dren=cooX_dren
        self.cooY_dren=cooY_dren
        self.idxDren =idxDren
        self.rings=rings
        self.geomProfiles = geomProfiles
        self.azAlinDreAntPos=azAlinDreAntPos
        ladoPerfil=[]
        #Travel index  neighbor
        for i,idx in enumerate(self.idxNeighbor):
            
            #calcular os angulos do alinhamento entre a drenagem e o ponto da cumeada
            azAlin_DC = proc.getAzimute((self.cooX_cume[idx]-self.cooX_dren[self.idxDren]),(self.cooY_cume[idx]- self.cooY_dren[self.idxDren])) 
            azAlin_DC=azAlin_DC[0]
            #Criar linhas
            lineDrenCume = ogr.Geometry(ogr.wkbLineString)
    
            #Criar alinhamento Dren ate cume
            lineDrenCume.AddPoint(self.cooX_dren[self.idxDren], self.cooY_dren[self.idxDren])
            lineDrenCume.AddPoint(self.cooX_cume[idx],self.cooY_cume[idx])
            
            #Verificar se ha interseccao entre cume e drenagem            
            across= proc.assesCrosses(lineDrenCume,self.rings)
            
            #Verificar se cruza com os dois perfis anteriormente criados
            assessAcrossProfiles=proc.assesCrossesProfiles(lineDrenCume,self.geomProfiles)

            if True in across:  
                pass
            
            elif True in assessAcrossProfiles:                
                pass
            
            elif 'esquerdo' in ladoPerfil and 'direito' in ladoPerfil:     
                    #print 'geomProfiles: ',  self.geomProfiles
                    return self.geomProfiles
                
            elif azAlin_DC <= max(self.azAlinDreAntPos) and azAlin_DC >= min(self.azAlinDreAntPos):
                if 'direito' in ladoPerfil:
                    
                    pass
                else:
                    ladoPerfil.append('direito')   
                    #print 'direito'
                    
                    self.outFeat.SetGeometry(lineDrenCume)
                    self.outLayer.CreateFeature(self.outFeat)
                    #Inserir geom profiles
                    self.geomProfiles.pop(0)
                    self.geomProfiles.insert(0,lineDrenCume)
                    
            elif 'esquerdo' in ladoPerfil:
                    pass
            else:
                    ladoPerfil.append('esquerdo') 
                    #print 'esquerdo'
                    self.outFeat.SetGeometry(lineDrenCume)
                    
                    self.outLayer.CreateFeature(self.outFeat)
                    #Inserir geom profiles
                    self.geomProfiles.pop(1)
                    self.geomProfiles.insert(1,lineDrenCume)
        return self.geomProfiles