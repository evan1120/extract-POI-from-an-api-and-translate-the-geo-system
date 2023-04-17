import requests
import pandas as pd
import os
# import transCoordinateSystem as tcs

# key(必选)
amp_api_key = 'a195daf5b2babc96fd87d2310513a95e'
#  请求地址前缀
req_url_pref = "https://restapi.amap.com/v3/place/text?"
# 分页信息(可选)
page_size = 25  # 每页25条数据
page_num = 1  # 代表第1页

#  请求参数
rep_params = {
    # "keywords": "商场",
    "types": "060000",
    "city": "421182",
    "offset": page_size,  # 当前页记录数(每页记录数)
    "page": page_num,  # 当前页
    "extensions": "base",
    "key": amp_api_key,
    "children": 1,
    "citylimit": "true"
}


def get_poi_from_amap():
    """
    从高德地图API下载POI数据
    """
    result = pd.DataFrame()  # 初始化
    i = 1
    while True:
        print("i:", i)
        page_num = i
        rep_params["page"] = page_num
        response = requests.get(req_url_pref, params=rep_params)
        data = response.json()  # 返回字典数据dict
        count = data["count"]
        print("count:", count)
        if count == "0":  # 结束条件
            break

        #  将每次分页结果数据插入指定目标文件中
        for j in range(0, len(data["pois"])):  # 遍历每一个poi对象，获取name,address等属性
            name = data["pois"][j]["name"]
            address = data["pois"][j]["address"]
            location = data["pois"][j]["location"]
            lon = float(data["pois"][j]["location"].split(",")[0])
            lat = float(data["pois"][j]["location"].split(",")[1])
            # wgs84_lon = tcs.gcj02_to_wgs84(lon,lat)[0]
            # wgs84_lat = tcs.gcj02_to_wgs84(lon,lat)[1]

            # 通过字典来构建DataFrame对象
            busi_data = [
                {
                    "name": name,
                    "address": address,
                    "location": location,
                    "lon": lon,
                    "lat": lat,
                    #   "wgs84_lon": wgs84_lon,
                    #   "wgs84_lat": wgs84_lat
                }
            ]

            df = pd.DataFrame(busi_data)
            result = result.append(df)  # 将每次j结果union在一块（列方面追加）
            # 重置索引
            print(result)
            # 将脚本所在路径作为excel输出路径
            output_path = os.getcwd() + os.sep + "poi_commercial.xlsx"
            # 将结果写入到output_path 所在d额excel中
            result.to_excel(output_path)

        i = i + 1


if __name__ == '__main__':
    get_poi_from_amap()
