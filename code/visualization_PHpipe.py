import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import LineString,Point,MultiPoint
from shapely.geometry import LineString
import os
from src.const import order
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator,FormatStrFormatter,MaxNLocator
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 10
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.rm'] = 'Times New Roman'
mpl.rcParams['mathtext.it'] = 'Times New Roman:italic'
mpl.rcParams['mathtext.bf'] = 'Times New Roman:bold'
#fig = plt.figure(figsize=(8.3, 1.0), dpi=600)


def pipeline_filter(DF_x,N,P,filepath="../data/capital coordination/capital coordination.shp"): 
  
    coord=gpd.read_file(filepath)
    coord.set_index('index', inplace=True)
    
    pipeline=gpd.GeoDataFrame(index=[(i,j) for i in order for j in order ],columns=["start province","end province","capacity_n","capacity_p","geometry","ifbuildh2"],crs="EPSG:4326")
    pipeline.geometry=pipeline.index.to_series().apply(lambda x: LineString([coord.geometry[x[0]],coord.geometry[x[1]]]))
    pipeline["start province"]=pipeline.index.to_series().apply(lambda x: x[0])
    pipeline["end province"]=pipeline.index.to_series().apply(lambda x: x[1])
    pipeline.capacity_n=pipeline.index.to_series().apply(lambda x: N[x[0],x[1]].X)
    pipeline.capacity_p=pipeline.index.to_series().apply(lambda x: P[x[0],x[1]].X)
    pipeline["ifbuildh2"]=pipeline.index.to_series().apply(lambda y: DF_x.loc[y[0],y[1]])
    return pipeline,coord

def visualization_PHpipe(DF_x,N,P,filepath_china="../data/china-shapefiles/china.shp",filepath_nine="../data/china-shapefiles/china_nine_dotted_line.shp",filepath_coord="../data/coordination.csv"):
    #plt.rcParams["font.family"] = "SimHei" # 设置全局中文字体为黑体
    china = gpd.read_file(filepath_china,encoding='utf-8') 
    china = china.dissolve(by='OWNER').reset_index(drop=False)   # 由于每行数据是单独的面，因此按照其省份列OWNER融合
    nine_lines = gpd.read_file(filepath_nine,encoding='utf-8')
    fig = plt.figure(figsize=(8.3/2, 6),dpi=300)
    ax = plt.axes([0,0,1,1])  #左下角x坐标，左下角y坐标,宽度，高度（0~1，归一化了）
    # fig, ax = plt.subplots(figsize=(12, 8))
    albers_proj = '+proj=aea +lat_1=25 +lat_2=47 +lon_0=105'
    ax = china.geometry.to_crs(albers_proj).plot(ax=ax,
                                                facecolor='grey',
                                                edgecolor='white',
                                                linestyle='--',
                                                alpha=0.8)
    ax = nine_lines.geometry.to_crs(albers_proj).plot(ax=ax,
                                                    edgecolor='grey',
                                                    linewidth=1,
                                                    alpha=0.4)
    ax.axis('off') # 移除坐标轴
    pipeline,coord=pipeline_filter(DF_x,N,P)
    pipeline=pipeline.to_crs(albers_proj)
    pipe_h2=pipeline[pipeline["ifbuildh2"]>0]
    pipe_h2=pipe_h2.set_geometry("geometry")
    

    for pipe in pipe_h2.geometry:
        x, y = pipe.xy
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        ax.arrow(x[0], y[0], dx, dy, shape='full', lw=1, length_includes_head=True, head_width=.2)
    
    coord.to_crs(albers_proj).plot(ax=ax, color='green', markersize=50, marker='.')
    return fig
    
