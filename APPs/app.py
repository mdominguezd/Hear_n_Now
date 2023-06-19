#!/usr/bin/env python
# coding: utf-8
from dash import Dash, dcc, html, callback, Input, Output, dash_table
import base64, io
import pandas as pd
import os
import glob
from urllib.parse import quote as urlquote
from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
from datetime import datetime, date
import dash_bootstrap_components as dbc
from pydub import AudioSegment
# Credits: https://medium.com/@adrianmrit/creating-simple-image-datasets-with-flickr-api-2f19c164d82f
from flickrapi import FlickrAPI
from ebird.api import *
import plotly.express as px
from dash.exceptions import PreventUpdate

with open('KEYS.txt') as f:
    lines = f.readlines()

KEY = [l.split(': ')[1].split('\n')[0] if ('Key' in l) else ' ' for l in lines][1]
SECRET = [l.split(': ')[1].split('\n')[0] if ('Secret' in l) else ' ' for l in lines][2]

flickr = FlickrAPI(KEY, SECRET)

api_key = [l.split(': ')[1].split('\n')[0] if ('Key' in l) else ' ' for l in lines][-1]

UPLOAD_DIRECTORY = "assets_app"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

for i in glob.glob(UPLOAD_DIRECTORY+'/*.mp3'):
    os.remove(i)


app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.title = 'HearAndNow'

app.layout = html.Div([html.H1("Welcome to our project!"),
                       html.Div([], style = {'height' : 40}),
                       html.Div([html.Img(src = r'assets/Hear & now.png', alt='image', style = {'width' : '20%','aspect-ratio' : 1/1, 'margin' : 'auto'}),
                                 html.Div([dcc.Markdown("Hey there! Good to have you here. **Hear and Now** was born as a project for the Geo Information Science and Remote Sensing intergration course given "
                                                        "for master's students in *Wageningen University & Research*. During this course, together with other 5 master's  students, we visited the beautiful "
                                                        "Achterhoek region in the Netherlands. During out time there we fell in love with the enchanting songs of birds in the region. Because of this we developed "
                                                        "a web application for bird watchers or bird waching enthusiasts like us. Our main objective with this application is to make people more aware of the"
                                                        "biodivesity around them."
                                                        ),
                                           dcc.Markdown("In our web application you will find what you need to boost your love for bird watching. In it you can either detect birds using audio files or check some "
                                                        "birds that have been seen nearby. Right now the default coordinates are the ones in the Achterhoek region, nevertheless, you can simply change this by "
                                                        "modifying the values in Latitude and Longitude."
                                                        ),
                                           dcc.Markdown("Hope you enjoy the app as much as we enjoyed making it for you! :)")]),
                                ], style = {'display':'flex', 'width' : '70%', 'margin' : 'auto'}),
                       html.Div([], style = {'height':20}),
                       html.Div([], style = {'height' : 10, 'background-color' : 'black', 'width' : '80%', 'margin' : 'auto'}),
                       html.Div([], style = {'height':20}),
                       html.H2("Upload here your audio files :)"),
                       dcc.Checklist(id = 'RangeOfDetection',options = ['Detect only birds in the Achterhoek'], value = ['Detect only birds in the Achterhoek']),
                       html.Div([], style = {'height':20}),
                       dcc.Upload(id="upload-data",
                                  children=html.Div([html.B("Click to select an audio file to upload.")]),
                                  style={"width": "80%",
                                         "height": "60px",
                                         "lineHeight": "60px",
                                         "borderWidth": "1px",
                                         "borderStyle": "dashed",
                                         "borderRadius": "5px",
                                         "textAlign": "center",
                                         "margin": "auto",},
                                  multiple=True,
                                 ),
                       dcc.Loading(html.Div([
                           html.Div([],style = {'height' : 60}),
                           html.H2("Bird species detected:"),
                           html.Div([html.Div(id="file-list", style = {'width' : '32%', 'margin' : 'auto'}),
                                     html.Div(id = 'img-list', style = {'width' : '32%', 'margin' : 'auto'}),
                                     html.Div(id = 'audios', style = {'width' : '32%', 'margin' : 'auto'})],
                                    style = {'display':'flex'}
                                   ),
                       ], style = {'height' : 450})),
                       html.Div([], style = {'height':20}),
                       html.Div([], style = {'height' : 10, 'background-color' : 'black', 'width' : '80%', 'margin' : 'auto'}),
                       html.Div([], style = {'height':20}),
                       html.H2('Have a look at some of the birds that\nhave been detected nearby.'),
                       html.Div([], style = {'height' : 50}),
                       html.Div([html.P('Latitude  : ', style = {"width": "50%", 'font-family' : 'bahnschrift'}), 
                                 dcc.Input(id = 'lat', type='number', value = 52.03, style = {"width": "50%"})], 
                                style = {'display' : 'flex', "width": "20%", "position": "relative"}),
                       html.Div([html.P('Longitude: ', style = {"width": "50%", 'font-family' : 'bahnschrift'}), 
                                 dcc.Input(id = 'long', type='number', value = 6.65, style = {"width": "50%"})], 
                                style = {'display' : 'flex', "width": "20%", "position": "relative"}),
                       html.Div([], style = {'height' : 50}),
                       html.P(id = 'click'),
                       dcc.Loading(html.Div(dcc.Graph(id = 'fig', ), 
                                            style={"height": "400px", "width": "80%", "position": "relative", "margin":"auto"}), style = {"height": "400px"}),
                       html.Div([], style = {'height' : 90, 'width':"100%"}),
                       html.Div(dash_table.DataTable(id = 'observations',
                                                     style_header={'backgroundColor': 'rgb(30, 30, 30)','color': 'white', 'fontFamily' : 'bahnschrift', 'textAlign' : 'center'},
                                                     style_data = {'whiteSpace':'normal', 'textAlign' : 'center'}
                                                     ), 
                                style={"height": "400px", "width": "80%", "position": "relative", "margin":"auto"}),
                       
                       ],
                      style={"width": "100%", "textAlign": "center", 'margin':'auto'},
                     )


def save_file(name, content):
    # Credits: https://docs.faculty.ai/user-guide/apps/examples/dash_file_upload_download.html
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def species_detection(filename, globalDet = True):
    """
    Function: Detect the species in an audio file

    Input:
        - filename: path of the audio file to be used in species detection

    Output:
        - det: DataFrame with the bird species detected
    """
    analyzer = Analyzer()

    if globalDet:
        recording = Recording(analyzer,
                              filename,
                              date=datetime(year=date.today().year, month=date.today().month, day=date.today().day),
                              min_conf=0.4)
    else:
        recording = Recording(analyzer,
                              filename,
                              lat=52.03164,
                              lon=6.6464,
                              date=datetime(year=date.today().year, month=date.today().month, day=date.today().day),
                              min_conf=0.4)

    recording.analyze()

    det = pd.json_normalize(recording.detections)

    return det

def get_picture(Specie, maxi = 1):
    """
    Function: Get URLs of images of bird species detected

    Input:
        - Specie: Common name of the specie
        - maxi: Max number of urls
    Output:
        - urls: list with the URLs
    """
    photos = flickr.walk(text=Specie,  # it will search by image title and image tags
                         extras='url_s',  # get the urls for each size we want
                         privacy_filter=1,  # search only for public photos
                         per_page=50,
                         sort='relevance')  # we want what we are looking for to appear first
    k = 0
    urls = []

    for photo in photos:

        if k < maxi:
            k += 1
            url = photo.get('url_s')

            urls.append(url)

        else:
            break

    return urls

@app.callback(
    [Output("file-list", "children"), Output('img-list', 'children'), Output('audios', 'children')],
    [Input("upload-data", "filename"), Input("upload-data", "contents"), Input('RangeOfDetection', 'value')],
)
def update_output(uploaded_filenames, uploaded_file_contents, rangeDet):
    """
    Function: Update the layout showing the species detected, the images and the audios.
    """

    species = pd.DataFrame([])

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            if name not in os.listdir(UPLOAD_DIRECTORY):
                save_file(name, data)

            globDet = (len(rangeDet) == 0)

            df = species_detection(UPLOAD_DIRECTORY+'/'+name, globDet)
            newAudio = AudioSegment.from_file(UPLOAD_DIRECTORY+'/'+name)

            if len(df) != 0:

                species = df['common_name'].unique()

                for i in species:

                    df_ = df[df['common_name'] == i].sort_values('confidence', ascending = False).iloc[0]

                    t_i = df_['start_time']*1000
                    t_f = df_['end_time']*1000

                    newAudio[t_i:t_f].export(UPLOAD_DIRECTORY + '/' + i+'.mp3', format = 'mp3')
            else:
                return [html.P(" ")], [html.P("No birds detected :(. Try again recording a new audio.")], [html.P(" ")]

            os.remove(UPLOAD_DIRECTORY+'/'+name)

    if len(species) == 0:
        return [html.P(" ")], [html.P("No file uploaded yet!")], [html.P(" ")]
    else:
        return [html.Div([sp], style = {'height' : 200, 'margin' : 'auto'}) for sp in species], [html.Div([html.Img(src = get_picture(sp)[0], style = {'margin' : 'auto'})], style = {'height' : 200, 'margin' : 'auto'}) for sp in species], [html.Div([html.Audio(src = UPLOAD_DIRECTORY + '/' + sp + '.mp3', controls = True, title = sp)], style = {'height' : 200, 'margin' : 'auto'}) for sp in species]




@app.callback(
    Output("fig", "figure"),
    Output('observations', 'data'),
    Input("lat", "value"),
    Input("long", "value"),
)
def get_table_n_map(lat, long):
    
    if (lat is None or long is None):
        print('que pasa')
        raise PreventUpdate
    else:
        coords = [lat, long]
        records = get_nearby_observations(api_key, coords[0], coords[1], dist=20, back=7)
        
        # Avoid update if no records were found
        if len(records) == 0:
            print('no actualiza')
            raise PreventUpdate
        else:
            print('mapactualiza')
            df = pd.json_normalize(records)

            count = df.groupby(['lat','lng']).count().reset_index()
            count = count[['lat','lng','howMany']]
            count.columns = ['lat','lng','Number of observations']

            map_b = px.scatter_mapbox(count, 'lat', 'lng', zoom = 10,
                                      color_continuous_scale = ['red','yellow','lightgreen'],
                                      color = 'Number of observations', size = 'Number of observations', 
                                      mapbox_style = 'carto-darkmatter')
            map_b.update_layout(margin = { 'r': 0, 't': 0, 'b': 0, 'l': 0 })

            records = [{'Common name' : i['comName'], 'Scientific name' : i['sciName'], 'Location' : i['locName']} for i in records]
        
        return map_b, records

@app.callback(
    [Output('long','value'),Output('lat', 'value')], 
    Input('fig', 'relayoutData')
)
def click(clickData):
    if (clickData == None or 'mapbox.center' not in clickData.keys()):
        print('no actualiza')
        return 6.65, 52.03
        # raise PreventUpdate
    else:
        print('actualiza')
        return round(clickData['mapbox.center']['lon'], 3), round(clickData['mapbox.center']['lat'], 3)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader = False, port = 8070)