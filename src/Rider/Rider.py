# -*- coding: utf-8 -*-

import Location
from googlemaps import Client
from datetime import datetime
from polyline.codec import PolylineCodec
import json
import math

gmaps = Client(key='AIzaSyCoIFqQxNU-M9oF62wVj2Fj37wn-wgh1Cw')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# # Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions((23.7846429,90.376789),
#                                      (23.775885, 90.723063),
#                                      mode="driving",
#                                      departure_time=now)


now = datetime.now()
directions_result = gmaps.directions("ShewraPara Bus Stand, Begum Rokeya Ave, Dhaka 1216",
                                     "Mohakhali Bus Stop, Dhaka 1205",
                                     mode="driving",
                                     departure_time=now)

now = datetime.now()
directions_result1 = gmaps.directions("Monipuripara মনিপুরিপাড়া",
                                      "Mohakhali Bus Stop, Dhaka 1205",
                                      mode="driving",
                                      departure_time=now)

directions_result2 = gmaps.directions("Bijoy Sarani, Dhaka",
                                      "Mohakhali Bus Stop, Dhaka 1205",
                                      mode="driving",
                                      departure_time=now)


directions_result3 = gmaps.directions(
    "Gulshan 1, Dhaka 1212", "Uttara, Dhaka", mode="driving", departure_time=now)

directions_result4 = gmaps.directions(
    "Gulshan 2, Dhaka 1212", "Uttara, Dhaka", mode="driving", departure_time=now)

directions_result5 = gmaps.directions(
    "Mohakhali Bus Stop, Dhaka 1205", "Dhaka New Market, Mirpur Road, Dhaka 1205", mode="driving", departure_time=now)


# dis = gmaps.distance_matrix(["ShewraPara Bus Stand, Begum Rokeya Ave, Dhaka 1216", "Monipuripara মনিপুরিপাড়া"],
#                             ["Mohakhali Bus Stop, Dhaka 1205"
#                                 ]
#                             )

# print(json.dumps(dis, indent=4))
# j = json.loads('{"one" : "1", "two" : "2", "three" : "3"}')
# print (j['two'])

# directions_result1 = json.load(directions_result1)

# print(directions_result1["bounds"])

# print(json.dumps(directions_result, indent=4))
# print(json.dumps(directions_result1, indent=4))
dir1dict = directions_result1[0]['legs']

# print(dir1dict['steps'])
# print(type(directions_result1[0]['legs']))
dir1lat = directions_result1[0]['legs'][0]['start_location']['lat']
dir1lng = directions_result1[0]['legs'][0]['start_location']['lng']

# print(dir1lng, end='\n\n\n')

for item in directions_result[0]['legs']:
    for it in item['steps']:
        startLocLat = it['start_location']['lat']
        startLocLng = it['start_location']['lng']
        endLocLat = it['end_location']['lat']
        endLocLng = it['end_location']['lng']

        # print("start", startLocLng)
        # print("end", endLocLng)
        if (dir1lat >= startLocLat and dir1lat >= endLocLat):
            if (dir1lng >= startLocLng and dir1lng <= endLocLng):
                print("inside")
                break

    def getDistance(p1, p2):
        R = 6378137  # Earth’s mean radius in meter
        dLat = math.radians(p2[0] - p1[0])
        dLong = math.radians(p2[1] - p1[1])
        a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(p1[0])) * math.cos(
            math.radians(p2[0])) * math.sin(dLong / 2) * math.sin(dLong / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return d  # returns the distance in meter


def matchPolyLine(poly1, poly2):
    intersectedNodes = []
    ctr = 0
    for i in range(len(poly1)):
        val = poly1[i]
        for j in range(len(poly2)):
            dis = getDistance(val, poly2[j])
            if dis <= 20:
                intersectedNodes.append((dis, val, poly2[j]))

    # print(len(intersectedNodes))
    # intersectedNodes.sort()
    # for i in intersectedNodes:
    #     if i[0] <= 30:
    #         print(i, end='\n')
    return intersectedNodes


def dis_desFromPath(host, requesterDes):

    max = 1e9
    vals = []
    for item in host:
        vals.append(getDistance(item, requesterDes))
    # for i in vals:
    #     print(i)
    val = min(vals)
    return val


def calcTime(intersectedNodes, path):
    time = 0
    node = (intersectedNodes[0][2][0], intersectedNodes[0][2][1])
    # print(intersectedNodes[0][2][0], intersectedNodes[0][2][1])
    des = (path[0]['legs'][0]['steps'][0]['start_location']['lat'],
           path[0]['legs'][0]['steps'][0]['start_location']['lng'])

    time = gmaps.distance_matrix(
        node, des)['rows'][0]['elements'][0]['duration']['value']
    return time
    # print(json.dumps(time, indent=4))
    # for item in path[0]['legs']:
    #     for it in item['steps']:
    #         startLocLat = it['start_location']['lat']
    #         endLocLat = it['end_location']['lat']
    #         startLocLng = it['start_location']['lng']
    #         endLocLng = it['end_location']['lng']
    #         time = it['duration']['text']
    #         print("time", time)
    # for node in intersectedNodes:
    #     # print(node, startLocLat, endLocLat, end='\n')
    #     # print(abs(startLocLat-node[2][0]), end='\n')
    #     if (abs(startLocLat-node[2][0]) <= 0.00001 or abs(endLocLat-node[2][0]) <= 0.00001):
    #         # if (node >= startLocLat and node <= endLocLat):
    #         print("TRUE", node[2][0], startLocLat, startLocLng,
    #               endLocLat, endLocLng, end='\n')
    # startLocLng = it['start_location']['lng']

    # endLocLng = it['end_location']['lng']


def takeInput():
    hostsrc = input("Source: ")
    hostdes = input("Destination: ")
    return (hostsrc, hostdes)
    # print(hostsrc, hostdes)
# print(getDistance((23.80331, 90.37016), (23.80372, 90.36998)))
# print(getDistance((23.80372, 90.36998), (23.80443, 90.36964)))
# print(getDistance((23.80443, 90.36964), (23.80511, 90.3693)))


host = takeInput()
now = datetime.now()
sp1 = gmaps.directions(host[0], host[1],
                       mode="driving",
                       departure_time=now)
sp1src = (sp1[0]['legs'][0]['start_location']
          ['lat'], sp1[0]['legs'][0]['start_location']['lng'])
sp1end = (sp1[0]['legs'][0]['end_location']
          ['lat'], sp1[0]['legs'][0]['end_location']['lng'])
poly1 = PolylineCodec().decode(sp1[0]['overview_polyline']['points'])
# for i in range(len(poly1)-1):
#     print("{" + 'lat: {d[0]}, lng: {d[1]}'.format(d=poly1[i]) + "},")
num = input("num of request: ")
for i in range(int(num)):
    print("I: ", i)
    req = takeInput()
    now = datetime.now()
    sp2 = gmaps.directions(req[0], req[1], mode="driving",
                           departure_time=now)

    sp2src = (sp2[0]['legs'][0]['start_location']
              ['lat'], sp2[0]['legs'][0]['start_location']['lng'])

    sp2end = (sp2[0]['legs'][0]['end_location']
              ['lat'], sp2[0]['legs'][0]['end_location']['lng'])

    poly2 = PolylineCodec().decode(sp2[0]['overview_polyline']['points'])
    # for i in range(len(poly2)-1):
    #     print("{" + 'lat: {d[0]}, lng: {d[1]}'.format(d=poly2[i]) + "},")
    intersectedNodes = matchPolyLine(poly1, poly2)
    val = dis_desFromPath(poly1, (sp2[0]['legs'][0]['end_location']
                                  ['lat'], sp2[0]['legs'][0]['end_location']['lng']))

    srcdes = req[0].split(host[1])
    d1 = math.atan2(sp2end[1] - sp1end[1], sp2end[0] - sp1end[0])
    d2 = math.atan2(sp2end[1] - sp2src[1], sp2end[0] - sp2src[0])
    d = False

    
    # else:
    #     if(poly2[0][0] >= poly2[1][0]):
    #         print(poly2[0][0], poly2[1][0])
    #         if(poly1[0][0] >= poly1[1][0]):
    #             print("Increasing")
    #             print(poly1[0][0], poly1[1][0])
    #             d = True
    #         else:
    #             d = False
    #     elif(poly2[0][0] < poly2[1][0]):
    #         print(poly2[0][0], poly2[1][0])
    #         if(poly1[0][0] < poly1[1][0]):
    #             d = True
    #         else:
    #             d = False
    #     else:
    #         print("eq")
    #         d = False

    # print(d)
    # print(d1)
    # print(d1)
    # print(d2)
    # if(d1 < 0 and d2 < 0):
    #     d = True
    # elif (d1 >= 0 and d2 >= 0):
    #     d = True
    # else:
    #     d = False
    # print(srcdes)
    # print("Val : ",val)
    # print("int :",intersectedNodes)
    # print(val)
    # print(len(intersectedNodes))
    print(getDistance(sp1src, sp2src))
    print(getDistance(sp1src, sp2end))
    if(getDistance(sp1src, sp2src) > getDistance(sp1src, sp2end)):
        print("NO")
    else:
        if(val <= 5000 and len(intersectedNodes) >= 10):
            print("Yes")
        else:
            print("min dis from path:" ,val)
            print("interesected nodes :",intersectedNodes)
            print("NO")
            

data1 = PolylineCodec().decode(
    "eqepCynrfPiHdCeCt@_DbACWpJsC~@[|XoJjH_CfCy@fCq@hD{@pIiBbEs@vIcB|IqBb@uA\\q@LOj@SrBYh@A`CNt@@j@KhUmEfAUh@Sb@Ir@IzEYvF_@rGg@|@O\\OXSTWPa@PqAjBqTHqA?YI_@QUYKiAGcDGsDI]?uB\\W@KAg@e@Q[Qg@qD_@eAMgBUeCWkCYuASuB[aAGeACsBJuEZg@?OCEGa@}FSuCYwC]wAoAsCe@i@iA_CmAkC_AqBeBqESu@Cw@?c@")

# print(data1,end='\n\n')

# print(json.dumps(directions_result1, indent=4))
data2 = PolylineCodec().decode(
    "{_`pCqotfPc@NGUAGBEf@QBMOw@WH_Bf@KAGEKOU?KEEOQyAGcCBc@E_@KOQQGq@G{ACYcBHgBJiE@gGO}EQkBOkGq@gBUkBSYCkCYkEo@aAGeACiIf@s@AGEAIq@mJSeCUyAQo@oAsCe@i@iA_CmAkC_AqBeBqESu@AUAeA")

data3 = PolylineCodec().decode(
    directions_result2[0]['overview_polyline']['points'])

data4 = PolylineCodec().decode(
    directions_result3[0]['overview_polyline']['points'])

data5 = PolylineCodec().decode(
    directions_result4[0]['overview_polyline']['points'])

data6 = PolylineCodec().decode(
    directions_result5[0]['overview_polyline']['points'])

# print(data2, end='\n\n')
# print(len(data1))
# print(len(data2))
intersectedNodes1 = matchPolyLine(data1, data2)
intersectedNodes2 = matchPolyLine(data1, data3)
# from gulshan 1 and 2 to uttara
intersectedNodes3 = matchPolyLine(data3, data4)
intersectedNodes4 = matchPolyLine(data1, data6)
# print(intersectedNodes1)
time1 = calcTime(intersectedNodes1, directions_result1)
user1 = (intersectedNodes1[0][2][0], intersectedNodes1[0][2][1])
time2 = calcTime(intersectedNodes2, directions_result2)
user2 = (intersectedNodes2[0][2][0], intersectedNodes2[0][2][1])


val = dis_desFromPath(data1, (directions_result5[0]['legs'][0]['end_location']
                              ['lat'], directions_result5[0]['legs'][0]['end_location']['lng']))


# if(val <= 2000.0):
#     print("YES")
#     if(time1 < time2):
#         print(
#             f"User 1 can join the ride in {math.ceil(time1/60)} mins from {user1}")
#     else:
#         print(
#             f"User 2 can join the ride in {math.ceil(time2/60)} mins from {user2}")
# else:
#     print("NO")


# if(time1 < time2):
#     print(
#         f"User 1 can join the ride in {math.ceil(time1/60)} mins from {user1}")
# else:
#     print(
#         f"User 2 can join the ride in {math.ceil(time2/60)} mins from {user2}")


# for d in intersectedNodes1:
#     print(d, end='\n')


# for i in range(len(data1)-1):
#     print("{"+ 'lat: {d[0]}, lng: {d[1]}'.format(d=data1[i]) + "},")

# for i in range(len(data2)-1):
#     print("{"+ 'lat: {d[0]}, lng: {d[1]}'.format(d=data2[i]) + "},")


dir1 = [(23.8007712, 90.371387), (23.7657205,
                                  90.3832515), (23.7645019, 90.3888759)]


# dir2 = [()]
# if 23.8007712 > 23.7657205:
#     # print("YES")
# else:
#     # print("NO")


# dir2 = [(23.8007712, 90.371387), ]

# class Rider:

#     def __init__(self, xs, xd, xt, xf):
#         self.xs = xs  # source node
#         self.xd = xd  # destination node
#         self.xt = xt  # time of departure of driver
#         self.xf = xf  # number of free seats

#     def showRiderDetails(self):
#         print("Source Node : \n" + self.xs.getLocation() + "\n")
#         print("Destination Node : \n" + self.xd.getLocation() + "\n")
#         print("Time of Departure Node : " + str(self.xt) + "\n")
#         print("Free seats : " + str(self.xf) + "\n")


# xs = Location.Location(23.775885, 89.723063)
# xd = Location.Location(23.775885, 90.723063)

# xs1 = Location.Location(23.775885, 89.723064)
# xd1 = Location.Location(23.775885, 89.723065)

# xs2 = Location.Location(23.775885, 89.723066)
# xd2 = Location.Location(23.775885, 89.723067)

# rider1 = Rider(xs, xd, 2, 3)
# rider2 = Rider(xs1, xd1, 3, 1)
# rider3 = Rider(xs2, xd2, 3, 5)

# # rider1.showRiderDetails()
# # rider2.showRiderDetails()
# # rider3.showRiderDetails()

# record = dict()
# record[(xs.getLat(), xd.getLng())] = rider1
# record[(xs1.getLat(), xd1.getLng())] = rider2
# record[(xs2.getLat(), xd2.getLng())] = rider3


# for item in record:
#     print(record[item].showRiderDetails())
