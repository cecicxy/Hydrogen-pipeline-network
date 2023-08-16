import matplotlib.pyplot as plt
import geopandas as gpd
from src.const import order
from shapely.geometry import LineString
import matplotlib as mpl

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 10
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.rm'] = 'Times New Roman'
mpl.rcParams['mathtext.it'] = 'Times New Roman:italic'
mpl.rcParams['mathtext.bf'] = 'Times New Roman:bold'


def pipeline_filter(modify_x,N,P,filepath="../data/capital coordination/capital coordination.shp"): 
  
    coord=gpd.read_file(filepath)
    coord.set_index('index', inplace=True)
    
    pipeline=gpd.GeoDataFrame(index=[(i,j) for i in order for j in order ],columns=["start province","end province","capacity_n","capacity_p","geometry","ifbuildh2"],crs="EPSG:4326")
    pipeline.geometry=pipeline.index.to_series().apply(lambda x: LineString([coord.geometry[x[0]],coord.geometry[x[1]]]))
    pipeline["start province"]=pipeline.index.to_series().apply(lambda x: x[0])
    pipeline["end province"]=pipeline.index.to_series().apply(lambda x: x[1])
    pipeline.capacity_n=pipeline.index.to_series().apply(lambda x: N[x[0],x[1]].X)
    pipeline.capacity_p=pipeline.index.to_series().apply(lambda x: P[x[0],x[1]].X)
    pipeline["ifbuildh2"]=pipeline.index.to_series().apply(lambda y: modify_x.loc[y[0],y[1]])
    return pipeline,coord




def draw_sankey(modify_x,N,P,filepath_china="../data/china-shapefiles/china.shp",filepath_nine="../data/china-shapefiles/china_nine_dotted_line.shp"):
    china = gpd.read_file(filepath_china,encoding='utf-8') 
    china = china.dissolve(by='OWNER').reset_index(drop=False)             # 由于每行数据是单独的面，因此按照其省份列OWNER融合
    nine_lines = gpd.read_file(filepath_nine,encoding='utf-8')
    fig = plt.figure(figsize=(8.3/2, 6),dpi=300)
    ax = plt.axes([0,0,1,1])  #左下角x坐标，左下角y坐标,宽度，高度（0~1，归一化了）
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
    
    pipeline,coord=pipeline_filter(modify_x,N,P)
    pipeline=pipeline.to_crs(albers_proj)
    pipe_h2=pipeline[pipeline["ifbuildh2"]>0]
    pipe_h2=pipe_h2.set_geometry("geometry")
    for i in range(len(pipe_h2)):
        pipe=pipe_h2.iloc[i]    
        base=pipe["capacity_p"]/pipe_h2["capacity_p"].max()
        ax.annotate("",
                    xy=pipe.geometry.coords[1],
                    xytext=pipe.geometry.coords[0],
                    size=5, 
                    va="center",
                    ha="center",
                    arrowprops=dict(connectionstyle="arc3",  # for straight line, rad=0
                                    edgecolor='none',
                                    width=base*4, headwidth=base*10,headlength=base*10)
                    )
       
        x_text=(pipe.geometry.coords[1][0]+pipe.geometry.coords[0][0])/2
        y_text=(pipe.geometry.coords[1][1]+pipe.geometry.coords[0][1])/2
        ax.text(x_text,y_text,'{:.1f}'.format(pipe["capacity_p"]/1000000),fontsize=3)
    coord.to_crs(albers_proj).plot(ax=ax, color='green', markersize=50, marker='.')
    fig.suptitle('Pure hydrogen pipeline distribution of China in 2060 ', fontsize=12, fontweight='bold')
    ax.set_title('Capacity unit:million ton')
    return ax


