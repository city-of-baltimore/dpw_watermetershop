#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pyodbc
import pandas as pd
import geopandas
import geoplot as gplt
import pyproj


# In[3]:


# connecting to SQL server (requires VPN connection)
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=BALT-AGLISTENER;'
                      'Database=COB_Cityworks;'
                      'Trusted_Connection=yes;')

#SQL Query
SQL_Query = pd.read_sql_query('''SELECT * FROM azteca.WORKORDER
WHERE APPLYTOENTITY = 'WA_METER'
AND INITIATEDATE  BETWEEN '2015-01-01' AND '2020-12-31'
AND DESCRIPTION <> 'WATER METER VAULTS'
''',conn)

#Create dataframe with relevant columns
df = pd.DataFrame(SQL_Query, columns=['WORKORDERID','DESCRIPTION', 'WOADDRESS','INITIATEDATE','PROJSTARTDATE','PROJFINISHDATE','ACTUALSTARTDATE','ACTUALFINISHDATE',
             'WOXCOORDINATE','WOYCOORDINATE'])
#Year WO was actually finished
df['F_Date'] =  pd.to_datetime(df['ACTUALFINISHDATE'], errors='coerce')
df['F_Year'] = df['F_Date'].dt.year

#Year WO was initiated (Possibly use instead of start)
df['I_Date'] =  pd.to_datetime(df['INITIATEDATE'], errors='coerce')
df['I_Year'] = df['I_Date'].dt.year
#Year WO was actually started
df['S_Date'] =  pd.to_datetime(df['ACTUALSTARTDATE'], errors='coerce')
df['S_Year'] = df['S_Date'].dt.year
#


# In[4]:


geodf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.WOXCOORDINATE, df.WOYCOORDINATE))


# In[5]:


gdf = gpd.read_file('C:\\Users\\joale.jupiter\\baltimore_city_boundary.shp')


# In[6]:


geodf = geodf.set_crs('epsg:3857')


# In[10]:


gdf = gdf.to_crs('epsg:3857')


# In[11]:


geodf.crs


# In[12]:


gdf.crs


# In[13]:


#Set to geodata sets to same CRS
#geodf = geodf.to_crs(gdf.crs)

#Plot both layers
f, ax = plt.subplots(figsize=(10, 10))
geodf.geometry.plot(ax=ax, marker='o', color='blue')
gdf.plot(ax=ax, color='green')
plt.axis('equal')
ax.set_axis_off()
plt.show()


# In[ ]:




