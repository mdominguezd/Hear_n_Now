# Hear & Now project repository

The present repository has the code and data used in the making of the Hear & Now web application and the Story Maps associated to this project.

* Here & Now application: **http://hearandnow.eu.pythonanywhere.com/**
* ArcGIS Story Maps: **https://storymaps.arcgis.com/collections/9df713390129463784616c13f2acfc4f**

## Hear & Now application (APPs folder)

When executed this application:
1. Receives an audio file.
1. Detects birds' singing in the file and display the name in the layout.
1. Gets a flickr image of the species detected and display it in the Layout.
1. Clips the section of the audio file in which the species was detected and display it in the layout.

#### API Keys disclaimer
A `KEYS.txt` file with the API key for the flickr API needs to be created to run the code `app.py` 

## GeoData

Files used for visualization purposes in the story maps created.
* `NL_Hotspots.geojson` : File with the Bird biodiversity hotspots of he Netherlands accoding to eBird.
* `Corrine_1990_2018.zip`: Zippped folder with .tif files that show the land cover change from 1990 to 2018.
* `Het_Heirinck_VI.zip`: Zipped folder with .tif files of vegetation indices calculated for the area around Het Reirink, Achterhoek, the Netherlands.

## BirdData

Excel file with all of the bird observation during the day when audio was recorded in the Achterhoek. (24 and 25 May 2023) 

