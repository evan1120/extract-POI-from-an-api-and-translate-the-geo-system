import hashlib
from urllib import parse
import math
import requests
import xlrd as xlrd

x_pi = 3.14159265358979324 * 3000.0 / 180.0
# 圆周率π
pi = 3.1415926535897932384626
# 长半轴长度
a = 6378245.0
# 地球的角离心率
ee = 0.00669342162296594323
# 矫正参数
interval = 0.000001


def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:列表返回
    """
    # 判断是否在国内
    #  if out_of_china(lng, lat):
        #  return lng, lat
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    gclng = lng + dlng
    gclat = lat + dlat
    return [gclng, gclat]


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:列表返回
    """
    # 判断是否在国内
    #   if out_of_china(lng, lat):
        #   return lng, lat
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    wgslng = lng + dlng
    wgslat = lat + dlat

    # 新加误差矫正部分
    corrent_list = wgs84_to_gcj02(wgslng, wgslat)
    clng = corrent_list[0] - lng
    clat = corrent_list[1] - lat
    dis = math.sqrt(clng * clng + clat * clat)

    while dis > interval:
        clng = clng / 2
        clat = clat / 2
        wgslng = wgslng - clng
        wgslat = wgslat - clat
        corrent_list = wgs84_to_gcj02(wgslng, wgslat)
        cclng = corrent_list[0] - lng
        cclat = corrent_list[1] - lat
        dis = math.sqrt(cclng * cclng + cclat * cclat)
        clng = clng if math.fabs(clng) > math.fabs(cclng) else cclng
        clat = clat if math.fabs(clat) > math.fabs(cclat) else cclat

    return [wgslng, wgslat]


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


#   def out_of_china(lng, lat):
    #   """
    #   判断是否在国内，不在国内不做偏移
    #   :param lng:
    #   :param lat:
    #   :return:
    #   """
    #  return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)
    #   return not (lng > "73.66" and lng < "135.05" and lat > "3.86" and lat < "53.55")


if __name__ == '__main__':
    filepath = r'F:\PythonProject\poi_sport_selected.xls'  # 文件路径
    xls_file = xlrd.open_workbook(filepath)
    xls_sheet = xls_file.sheet_by_name("Sheet1")  # Excel里的sheet名
    for i in range(1, xls_sheet.nrows):
        alldata = xls_sheet.row_values(i)  # 获取整行数据
        lng = alldata[5]  # 经度所在的列号
        lat = alldata[6]  # 纬度所在的列号
        transform_lon = gcj02_to_wgs84(lng, lat)
        print(transform_lon[0], transform_lon[1])
