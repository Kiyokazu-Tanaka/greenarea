# coding: utf-8
import math
import csv

POLE_RADIUS = 6356752    # 極半径(短半径)
EQUATOR_RADIUS = 6378137 # 赤道半径(長半径)
E = 0.081819191042815790 # 離心率
E2= 0.006694380022900788 # 離心率の２乗

class Coordinate:
    def __init__(self, latitude, longitude, altitude):
        self.latitude  = latitude
        self.longitude = longitude
        self.altitude  = altitude

def distance(point_a, point_b):
    a_rad_lat = math.radians(point_a.latitude)
    a_rad_lon = math.radians(point_a.longitude)
    b_rad_lat = math.radians(point_b.latitude)
    b_rad_lon = math.radians(point_b.longitude)
    m_lat = (a_rad_lat + b_rad_lat) / 2 # 平均緯度
    d_lat = a_rad_lat - b_rad_lat # 緯度差
    d_lon = a_rad_lon - b_rad_lon # 経度差
    W = math.sqrt(1-E2*math.pow(math.sin(m_lat),2))
    M = EQUATOR_RADIUS*(1-E2) / math.pow(W, 3) # 子午線曲率半径
    N = EQUATOR_RADIUS / W # 卯酉線曲率半径
    # d = math.sqrt(math.pow(M*d_lat,2) + math.pow(N*d_lon*math.cos(m_lat),2) + math.pow(point_a.altitude-point_b.altitude,2))
    d = math.sqrt(math.pow(M*d_lat,2) + math.pow(N*d_lon*math.cos(m_lat),2))
    return d

area_addup_50 = 0
area_addup_250 = 0
area_addup_500 = 0
area_addup_700 = 0

writing_file = open('SA_DATA.csv', 'w')
w = csv.writer(writing_file)

with open("LP_address_book.csv") as f:
    for row in csv.reader(f):
        if row[0] == "latitude":
            row_data = ["area_addup_50","area_addup_250","area_addup_500","area_addup_700"]
            w.writerow(row_data)
            continue
        location1 = Coordinate(float(row[0]),float(row[1]), 0)
        with open("SA_address_book.csv") as f2:
            for row_2 in csv.reader(f2):
                if row_2[0] == "latitude":
                    continue
                location2 = Coordinate(float(row_2[0]),float(row_2[1]), 0)
                distance_of_two = distance(location1,location2)

                if distance_of_two < 50 + (float(row_2[2])/3.141592)**0.5:
                    area_addup_50 = area_addup_50 + float(row_2[2])

                if distance_of_two < 250 + (float(row_2[2])/3.141592)**0.5:
                    area_addup_250 = area_addup_250 + float(row_2[2])

                if distance_of_two < 500 + (float(row_2[2])/3.141592)**0.5:
                    area_addup_500 = area_addup_500 + float(row_2[2])

                if distance_of_two < 700 + (float(row_2[2])/3.141592)**0.5:
                    area_addup_700 = area_addup_700 + float(row_2[2])


        print(area_addup_50)
        row_data = [area_addup_50,area_addup_250,area_addup_500,area_addup_700]
        w.writerow(row_data)
        area_addup_50 = 0
        area_addup_250 = 0
        area_addup_500 = 0
        area_addup_700 = 0

writing_file.close()



#SAMPLE1   = Coordinate(35.689608, 139.692080, 0)#東京都庁
#SAMPLE2 = Coordinate(33.606316, 130.418108, 0)#福岡県庁

#print(distance(tokyo,fukuoka),"m")
