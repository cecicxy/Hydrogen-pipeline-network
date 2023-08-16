import matplotlib.pyplot as plt
import geoplot as gplt
import geoplot.crs as gcrs
import geopandas as gpd
from src.const import order

def visualization_generation(G):
    province=gpd.read_file(
    "../data/china_province_map/china_province_map.shp", encoding="utf-8"
)
    province=province.set_index("OWNER")
    for i in order:
        province.loc[i, "generation"] = G[i].X
        
    gplt.choropleth(
    province, hue='generation', projection=gcrs.AlbersEqualArea(),
    edgecolor='black', linewidth=0.8,
    cmap='Greens', legend=True
)
    # fig.suptitle('Pure hydrogen pipeline distribution of China in 2060 ', fontsize=12, fontweight='bold')
    # ax.set_title('Capacity unit:million ton')
    plt.savefig("../result/fig_gen.pdf")
    

def visualization_consumption(h2_cons):
    province=gpd.read_file(
    "../data/china_province_map/china_province_map.shp", encoding="utf-8"
)
    province=province.set_index("OWNER")
    for i in order:
        province.loc[i, "consumption"] = h2_cons.loc[i, "h2"]

    gplt.choropleth(
    province, hue='consumption', projection=gcrs.AlbersEqualArea(),
    edgecolor='black', linewidth=0.8,
    cmap='Reds', legend=True
)
    plt.savefig("../result/fig_con.pdf")

def visualization_gen_con(G,h2_cons):
    province=gpd.read_file(
    "../data/china_province_map/china_province_map.shp", encoding="utf-8"
)
    province=province.set_index("OWNER")
    for i in order:
        province.loc[i, "gen_con"] = G[i].X-h2_cons.loc[i, "h2"]

    gplt.choropleth(
    province, hue='gen_con', projection=gcrs.AlbersEqualArea(),
    edgecolor='black', linewidth=0.8,
    cmap='Oranges', legend=True
)
    plt.savefig("../result/fig_gen_con.pdf")