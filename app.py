# watchdog 

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

df_wines = pd.read_csv('wines.tsv', sep='\t')
df_wineries = pd.read_csv('wineries.tsv', sep='\t')
df_wineries = pd.merge(df_wineries, df_wines[['winery', 'url']], how='left')

# breakpoint()

st.title('Virginia Award-Winning Wineries')
"Vineyards with a Governors Cup Awarded Wine in 2023"
# st.map(data = df, latitude = 'lat', longitude = 'lon'
# )

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=38,
        longitude=-79.5,
        zoom=6,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            pickable='True',
            data=df_wineries,
            get_position='[lon, lat]',
            get_color='[100, 25, 30, 150]',
            get_radius=1000,
        ),
    ],
    tooltip = {"text": "{winery}\n{address}"}
))

"_Source: https://www.virginiawine.org/governors-cup/awards_"
