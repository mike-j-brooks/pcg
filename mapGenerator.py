import os
import random

###################################################################
######## VARIABLES ################################################
###################################################################

mapArray = []
roomRecord = []
newMapArray = []

mapHeight = 250
mapWidth = 250

roomWidth = 20
roomHeight = 20

cursor = [0,0]


###################################################################
######## FUNCTIONS ################################################
###################################################################


def createMapArray(mapHeight,mapWidth,mapArray):
    '''
    ''  creates a blank map array
    '''
    for i in range(0,mapHeight):
        mapArray.append([])
        for j in range(0,mapWidth):
            mapArray[i].append('-')


def genRooms(mapArray, mapWidth, mapHeight):
    '''
    ''  random room generation
    '''
    for y in range(2,mapHeight-2):
        for x in range(2, mapWidth-2):
            if random.randint(0,1000) > 996:
                ### generate room
                if x < (mapWidth - (roomWidth+2)):
                    if y < (mapHeight - (roomHeight+2)):
                        for a in range(0,roomHeight):
                            for b in range(0,roomWidth):
                                mapArray[y+a][x+b] = "x"


def roomExistCheck(mapHeight,mapWidth):
    '''
    ''  boolean check
    ''  1 = rooms still exist in initial map
    ''  0 = initial map is cleared
    ''  **Can be optimized by using 'return 1' to break scan loop
    '''
    roomExists = 0
    for i in range(0,mapHeight):
        for j in range(0,mapWidth):
            if mapArray[i][j] != "-":
                roomExists = 1
    if roomExists == 0:
        return 0
    else:
        return 1


def findRoom(mapHeight,mapWidth,mapArray,cursor):
    '''
    '' Changes cursor to the coordinates of the first room unit located
    '''
    for y in range(0,mapHeight):
        for x in range(0,mapWidth):
            if mapArray[y][x] == "x":
                cursor = [x,y]
                return cursor

def buildWalls(mapHeight,mapWidth,mapArray,cursor):
    cursor = findRoom(mapHeight,mapWidth,mapArray,cursor)
    cursorStart = cursor
    ### store array element in each direction from the cursor
    ### note : mapArray[y = rows][x = columns]
    cRight = mapArray[cursor[1]][cursor[0]+1]
    cDown = mapArray[cursor[1]+1][cursor[0]]
    cLeft = mapArray[cursor[1]][cursor[0]-1]
    cUp = mapArray[cursor[1]-1][cursor[0]]

    cursorTrig = 1              ## trigger to break out of while loop
    while cursorTrig == 1:
        if cursor[1] < mapHeight:
            if cursor[0] < mapWidth:  ## keep cursor in bounds of map array
                if mapArray[cursor[1]][cursor[0]] == "x":
                    ## update cursor environent data :
                    cRight = mapArray[cursor[1]][cursor[0]+1]
                    cDown = mapArray[cursor[1]+1][cursor[0]]
                    cLeft = mapArray[cursor[1]][cursor[0]-1]
                    cUp = mapArray[cursor[1]-1][cursor[0]]
                    ## change state of current cursor position in mapArray
                    mapArray[cursor[1]][cursor[0]] = "0"
                    ## record cursor location for outline
                    roomRecord.append([cursor[0],cursor[1]])
                    ## move cursor :
                    if cursor ==[cursorStart[0],cursorStart[1]+1]:      ## breaks loop when room outline is finished
                        cursorTrig = 0
                    if cursor != [cursorStart[0],cursorStart[1]+1]:
                        ## left block is open space
                        if cUp == "x":
                            if cLeft != "x":
                                cursor = [cursor[0],cursor[1]-1] #up
                            elif cLeft == "x" and cDown != "x":
                                cursor = [cursor[0]-1,cursor[1]] #left
                            else:
                                cursor = [cursor[0],cursor[1]+1] #down
                        ## right block is open space
                        elif cRight == "x":
                            if cUp != "x":
                                cursor = [cursor[0]+1,cursor[1]] #right
                            elif cUp == "x":
                                cursor = [cursor[0],cursor[1]+1] #up
                        ## down block is open space
                        elif cDown == "x":
                            if cRight != "x":
                                cursor = [cursor[0],cursor[1]+1] #down
                            elif cRight == "x":
                                cursor = [cursor[0]+1,cursor[1]] #right
                        ## left block open space
                        elif cLeft == "x":
                            if cDown != "x":
                                cursor = [cursor[0]-1,cursor[1]] #left
                            elif cDown == "x":
                                cursor = [cursor[0],cursor[1]+1] #down

    ## build interior walls
    fillTrigger = 0
    for i in range(0,mapHeight):
        for j in range(0,mapWidth):
            if mapArray[i][j] == "0":
                fillTrigger = 0
            if mapArray[i][j] == "x" and mapArray[i][j-1] == "0":
                fillTrigger = 1
            if fillTrigger == 1 and mapArray[i][j] == "-":
                if mapArray[i][j+1] == "x" or mapArray[i][j-1] == "x" or mapArray[i+1][j] == "x" or mapArray[i-1][j] == "x":
                    mapArray[i][j] = "0"
                    roomRecord.append([j,i])

def delRoom(mapHeight,mapWidth,mapArray):
    deleteTrigger = 0
    for i in range(0,mapHeight):
        for j in range(0,mapWidth):
            if mapArray[i][j] == "0":
                deleteTrigger = 0
            if mapArray[i][j] == "x" and mapArray[i][j-1] == "0":
                deleteTrigger = 1
            if deleteTrigger == 1:
                mapArray[i][j] = "-"

    for i in range(0,mapHeight):
        for j in range(0,mapWidth):
            if mapArray[i][j] == "0":
                mapArray[i][j] = "-"

def printMap(mapArray):
    for row in mapArray:
        for item in row:
            print(item, end="")
        print()

###################################################################
######## MAIN PROGRAM #############################################
###################################################################

createMapArray(mapHeight, mapWidth, mapArray)

printMap(mapArray)

genRooms(mapArray, mapWidth, mapHeight)

printMap(mapArray)

roomCount = 0

while roomExistCheck(mapHeight,mapWidth) == 1:
    roomCount += 1
    buildWalls(mapHeight,mapWidth,mapArray,cursor)
    delRoom(mapHeight,mapWidth,mapArray)

createMapArray(mapHeight, mapWidth, newMapArray)

for i in range(0,len(roomRecord)):
    index1 = roomRecord[i][0]
    index2 = roomRecord[i][1]
    newMapArray[index2][index1] = "0"

file = open("map.txt","w+")
for k in range(0,len(newMapArray)):
    file.write(str(''.join(newMapArray[k]))+"\n")
file.close()

print(roomCount)
print(roomRecord)

file = open("mapData.txt","w+")
for i in range(len(roomRecord)):
    file.write(str(roomRecord[i][0]) + " " + str(roomRecord[i][1]) + "\n")
file.close()
