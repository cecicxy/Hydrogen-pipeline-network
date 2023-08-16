import requests

# 中国范围：维度3.86至53.55，经度73.66至135.05
la_min=3.86
la_max=53.55
lon_min=73.66
lon_max=135.05
num=2
delta_la=(la_max-la_min)/num
delta_lo=(lon_max-lon_min)/num
z=10
for i in range(num):
    for j in range(num):
        SLA=la_min+i*delta_la
        WLO=lon_min+j*delta_lo 

        NLA=la_min+(i+1)*delta_la 
        ELO=lon_min+(j+1)*delta_lo 

        url=f"https://zh-cn.topographic-map.com/?_path=api.maps.getOverlay&southLatitude={SLA}&westLongitude={WLO}&northLatitude={NLA}&eastLongitude={ELO}&zoom={z}&version=202306301006"
        response=requests.get(url, 
        headers= {
            "sec-ch-ua": "'Not/A)Brand';v='99', 'Microsoft Edge';v='115', 'Chromium';v='115'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "'Windows'",
            "Referer": "https://zh-cn.topographic-map.com/map-72ltt6/%E4%B8%AD%E5%9B%BD/?center=11.87165%2C109.58545&popup=32.80898%2C120.12633&zoom=9",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        });
        print(response.status_code)
        
        with open(f'figure/picture{i}{j}.jpg', 'wb') as file:
            file.write(response.content) 