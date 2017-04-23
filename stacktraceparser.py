
def parseStackTrace(stackTraceString):
    lineList = stackTraceString.split("\n")
    return [(line.split(" ")[1]).split("(")[0] for line in lineList[1:]]
