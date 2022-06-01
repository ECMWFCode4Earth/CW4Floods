#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 14:40:17 2022

This function extracts the points for which there simultaneously exist streamflow
basin of the points make sense and are coherent between GloFas, ECCC and observations)


@author: marie-amelie
"""

# Import all the observations from Water Survey of Canada

def importObsWSC(fichierObs):

    import csv
    import numpy as np

    StationID = []
    LatitudeObs = []
    LongitudeObs = []
    UpAreaObs =[]

    with open(fichierObs) as csv_file:
        fichier = csv.reader(csv_file, delimiter=',')
        next(fichier , None)

        for row in fichier:

            ID = row[0]
            Lat = row[4]
            Lon = row[5]
            Area = row[8]

# Some of the strings for latitude, longitudes, etc are empty so they cannot
# be converted to floats
            try:
                float(Lat)
                LatitudeObs.append(float(Lat))
            except ValueError:
                LatitudeObs.append(np.nan)

            try:
                float(Lon)
                LongitudeObs.append(360+float(Lon))
            except ValueError:
                LongitudeObs.append(np.nan)

            try:
                float(Area)
                UpAreaObs.append(float(Area))
            except ValueError:
                UpAreaObs.append(np.nan)

            StationID.append(ID)

            # Il faudrait enlever les bassins trop petits
    UpAreaObs = np.array(UpAreaObs)
    indAssezGrands = np.where(UpAreaObs>500)
    UpAreaObs = UpAreaObs[indAssezGrands[0]]
    StationID = np.array(StationID)[indAssezGrands[0]]
    LatitudeObs = np.array(LatitudeObs)[indAssezGrands[0]]
    LongitudeObs = np.array(LongitudeObs)[indAssezGrands[0]]

    return StationID, LatitudeObs, LongitudeObs, UpAreaObs

# Get rid of the whole UpArea map. Instead, keep only the upstream areas that
#correspond to forecast points Specific to GloFAS

def UpAreaFcstsGloFAS(LatitudeFcstGloFAS, LongitudeFcstGloFAS, UpAreaGloFAS,\
                      LatUpAreaGloFAS, LonUpAreaGloFAS):
    import numpy as np
    indLatDansUpArea=[]

    for iLat in range(0, len(LatitudeFcstGloFAS)):

        indtemp = np.where(np.round(LatUpAreaGloFAS,2)==np.round(LatitudeFcstGloFAS[iLat],2))
        indLatDansUpArea.append(indtemp[0][0])

    indLonDansUpArea=[]

    for iLon in range(0, len(LongitudeFcstGloFAS)):

        indtemp = np.where(np.round(360+LonUpAreaGloFAS,2)==np.round(LongitudeFcstGloFAS[iLon],2))
        indLonDansUpArea.append(indtemp[0][0])

    UpAreaFcst = UpAreaGloFAS[indLatDansUpArea[0]:indLatDansUpArea[-1]+1,\
                              indLonDansUpArea[0]:indLonDansUpArea[-1]+1]
        # Le +1 est necessaire sinon ca s'arrete a l'avant-derniere adresse
    UpAreaFcst = UpAreaFcst/(1000**2) # convert to km^2

    return UpAreaFcst  

# GENERAL: Match stations to gridpoints

def MatchStationsWgridPoints(StationID, LatitudeObs, LongitudeObs,\
                             LatitudeFcst, LongitudeFcst, UpAreaFcst, \
                                 UpAreaObs, path_fichier_resultat):
    import numpy as np
    import pandas as pd
    # conda install -c conda-forge haversine
    from haversine import haversine

    LongitudeObs = np.array(LongitudeObs)#-360
    LatitudeObs = np.array(LatitudeObs)
    coordPointsObs = np.column_stack((LatitudeObs, LongitudeObs))
    
    
    # ECCC UpArea file contains nan values, which later cause issues when
    #computing the coverage ratio and selecting the best grid point
    # I replace nan values with a very small up area to avoid that
    rep = np.isnan(UpAreaFcst)
    indNaN=np.where(rep==True)
    UpAreaFcstnew=UpAreaFcst
    UpAreaFcstnew[indNaN]=0.001

    PointsFcst = []

    for Lat in LatitudeFcst:

        for Lon in LongitudeFcst:
            #Lon = Lon-360
            UnPointFcst = ((Lat,Lon))
            PointsFcst.append(UnPointFcst)
            
    NoStation = []
    SuperficieDrainee = []
    LongitudeStation = []
    LatitudeStation = []
    Recouvrement = []
    LongitudePointsSelect = []
    LatitudePointsSelect = []
    surfPointsSelect = []
    SmallDist = []
    indexSmallDist = []
    influence = []
    Troncon = []
    RankECCC = []
    Distance = []

    for i in range(0,len(StationID)):
        print(StationID[i])
        #print(StationID[i])
        UnPointObs = coordPointsObs[i,:]
        
        distanceObs2Fcsts = []
        upAreaUneObs = UpAreaObs[i]

        for j in range(0, len(PointsFcst)):
            #dist = np.linalg.norm(UnPointObs-PointsFcst[j])
            
            dist = haversine(UnPointObs, PointsFcst[j]) # en km
            
            distanceObs2Fcsts.append(dist)
            

        distanceObs2Fcsts=np.array(distanceObs2Fcsts)

        indexSmallDist.append(np.where(np.array(distanceObs2Fcsts)<7))
        # Can be empty but can also contain more than one value

        SmallDist.append(np.array(distanceObs2Fcsts[indexSmallDist[i][0]]))
        #SmallDist = np.array(SmallDist)

        array_small_dist = np.array(SmallDist[0])
        
        if array_small_dist.size > 0: # if not empty
            #print(array_small_dist)
            DiffAireRatio = []
            UpAreaPotListe = []
            indexLatPotListe = []
            indexLonPotListe = []
            # SurfECCC = []
            # LonECCC = []
            # LatECCC = []

            for k in range(0,len(indexSmallDist[i][0])):
                # Pour chacun des points qui a ete trouve dans le rayon
                #determine, on trouve le upstream area

                index = int(indexSmallDist[i][0][k])
                PtFcstSmallDist = PointsFcst[index]

                LatUnPoint = PtFcstSmallDist[0]
                LonUnPoint = PtFcstSmallDist[1]

                indexLatUpArea = np.where(LatitudeFcst==LatUnPoint)
                indexLonUpArea = np.where(LongitudeFcst==LonUnPoint)#+360)

                UpAreaPot = UpAreaFcstnew[indexLatUpArea[0], indexLonUpArea[0]]

                Ratio = 1-abs(UpAreaPot-upAreaUneObs)/upAreaUneObs
                
                DiffAireRatio.append(Ratio)

                UpAreaPotListe.append(UpAreaPot)
                indexLatPotListe.append(indexLatUpArea)

                indexLonPotListe.append(indexLonUpArea)

            
            Recouv = np.max(DiffAireRatio)
            
            # On identifie le meilleur ratio de recouvrement
            #des superficie upstream

            if Recouv>0.9:

                indMaxiDiffAire = np.where(DiffAireRatio==Recouv)
                # DiffAireRatio a la longueur k

                indexLatFcst = indexLatPotListe[indMaxiDiffAire[0][0]]
                indexLonFcst = indexLonPotListe[indMaxiDiffAire[0][0]]

                NoStation.append(StationID[i])
                SuperficieDrainee.append(upAreaUneObs)
                LongitudeStation.append(LongitudeObs[i])#+360)
                LatitudeStation.append(LatitudeObs[i])
                

                Recouvrement.append(Recouv)
                LongitudePointsSelect.append(LongitudeFcst[indexLonFcst][0])
                LatitudePointsSelect.append(LatitudeFcst[indexLatFcst][0])
                surfPointsSelect.append(UpAreaPotListe[indMaxiDiffAire[0][0]][0])
                influence.append(0.1)
                Troncon.append(0.1)
                RankECCC.append(0.1)
                point_fcst_final = [LatitudeFcst[indexLatFcst][0], LongitudeFcst[indexLonFcst][0]]
                dist_final = haversine(UnPointObs, point_fcst_final)
                Distance.append(dist_final)

    # Changer les noms des champs pour quelque chose de general
    # Pour les codes de Jean, les champs doivent etre:
    # No.Station;Superficie.Drainee;Longitude.Station;Latitude.Station;
    #Influence;Troncon.Associe;rank_ECCC;surf_ECCC;lon_ECCC;lat_ECCC;
    # recouvrement;Longitude.GLOFAS;Latitude.GLOFAS;surf.GLOFAS
    dict = {'No.Station':NoStation, 'Superficie.Drainee':SuperficieDrainee, \
            'Longitude.Station':LongitudeStation, \
            'Latitude.Station':LatitudeStation, 'Influence':influence, \
            'Troncon.Associe': Troncon,'rank_ECCC': RankECCC, \
             'Recouvrement':Recouvrement, \
             'Longitude.FCST':LongitudePointsSelect, \
            'Latitude.FCST':LatitudePointsSelect, 'surf.FCST':surfPointsSelect, 'Distance':Distance}

    df = pd.DataFrame(dict)
    # Prevoir le chemin et le nom du fichier ailleurs
    df.to_csv(path_fichier_resultat)

    return df
#
