# Hear & Now project repository

The present repository has the code and data used in the making of the Hear & Now web application and the Story Maps associated to this project.

* Here & Now application: **http://hearandnow.eu.pythonanywhere.com/**
* ArcGIS project Collection: **https://storymaps.arcgis.com/collections/9df713390129463784616c13f2acfc4f**

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
* `NL_Hotspots.geojson` : File with the Bird biodiversity hotspots of the Netherlands according to eBird.
* `Corrine_1990_2018.zip`: Zippped folder with .tif files that show the land cover change from 1990 to 2018.
* `Het_Heirinck_VI.zip`: Zipped folder with .tif files of vegetation indices calculated for the area around Het Reirink, Achterhoek, the Netherlands.

## Data stored in cloud services

* Go [here](https://drive.google.com/file/d/16ETHCfMj3_QmN5gU960lUimnDYm53WPD/view?usp=sharing) to download the point clouds. The point clouds were acquired using the Green Valley Mobile Laser Scanner in the surroundings of the Reirink, Achterhoek, The Netherlands.
* Go [here](https://wageningenur4.sharepoint.com/sites/3Dradarguys/Gedeelde%20documenten/Forms/AllItems.aspx?id=%2Fsites%2F3Dradarguys%2FGedeelde%20documenten%2FGeneral%2FIDV%2FAudiomoths&p=true&ga=1) to download the audio files that we used to detect bird species.

## BirdData

Excel file with all of the bird observation during the day when audio was recorded in the Achterhoek. (24 and 25 May 2023) 

## IDVDocuments

This folder includes the `data management plan` and the `case study` document.

## Google Colab code
* Check the code with which we calculated the acoustic indices of the audios [here](https://colab.research.google.com/drive/1w5arc29Hxe52qfZgo6AdiwFBEkXkKK4z?usp=sharing)
* The code used to get the Bird species can be accessed [here](https://colab.research.google.com/drive/19_LIVrV9PAirAP_alEODXYTYxgUOrZ7P?usp=sharing)

## Google Earth Engine Code
* The code to get the vegetation indices using Google Earth Engine is [here](https://code.earthengine.google.com/d9f0d033d38a959bbcb724cc2b92fa25)
* You can access the code for the Land Cover Change analysis [here](https://code.earthengine.google.com/cb968d668e77795302e68da9c968c7d7)
