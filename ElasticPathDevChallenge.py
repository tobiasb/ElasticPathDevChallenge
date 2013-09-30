import httplib2
import json
import urllib

def post(command, params=""):
    h = httplib2.Http(".cache")
    content = h.request("http://www.epdeveloperchallenge.com/" + command + "?" + params, "POST")[1]
    print(content)
    decoded = json.loads(content.decode("utf-8"))
    #print(json.dumps(decoded, sort_keys=True, indent=4))
    return decoded

def initChallenge():
    data = post("/api/init", )
    return data["currentCell"]

def move(mazeGuid, direction):
    data = post("/api/move", urllib.parse.urlencode(dict(mazeGuid=mazeGuid, direction=direction.upper())))
    return data["currentCell"]

def getOrientationString(direction):
    if direction % 360 == 0: return "north"
    if direction % 360 == 90: return "east"
    if direction % 360 == 180: return "south"
    if direction % 360 == 270: return "west"
    
def canMove(orientation, direction, data):
    return data[getOrientationString(orientation + direction)] != "BLOCKED"

orientation=0#north
steps=0
data = initChallenge()
maze = [[0]*50 for i in range(50)]

while data["atEnd"] == False:
    if canMove(orientation, 90, data):
        orientation=orientation+90
        data = move(data["mazeGuid"], getOrientationString(orientation))
    elif canMove(orientation, 0, data):
        orientation=orientation+0
        data = move(data["mazeGuid"], getOrientationString(orientation))
    elif canMove(orientation, -90, data):
        orientation=orientation-90
        data = move(data["mazeGuid"], getOrientationString(orientation))
    elif canMove(orientation, 180, data):
        orientation=orientation+180
        data = move(data["mazeGuid"], getOrientationString(orientation))
    else:
        break
    maze[data["x"]][data["y"]]="X"
    steps=steps+1
    
print("\n".join(["".join(map(str, r)) for r in maze]))
print("Steps: " + str(steps))

#b'{"currentCell":{"note":"Congratulations, you have successfully found your way through the Elastic Path blackout maze. Based on your problem solving skills, we would love to talk to you about our software development opportunities in our Vancouver, BC and Reading, United Kingdom offices. Don\'t be shy, let\'s chat! Start by applying via the unique link below and include the following phrase:\\n\\nPhrase: \\"In the blackest night, no hidden path shall escape my sight!\\"\\n\\nLink: http://tbe.taleo.net/NA1/ats/careers/requisition.jsp?org=EKKON&cws=38&rid=352","x":49,"y":49,"mazeGuid":"72fd4b92-9629-439b-98e8-0578107aef98","atEnd":true,"previouslyVisited":false,"north":"BLOCKED","east":"BLOCKED","south":"BLOCKED","west":"VISITED"}}'