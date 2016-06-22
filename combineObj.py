'''
Combine two wavefront obj files, one whit vertex position and another with vertex uv
Obj file name convention:
    xxx_pos.obj     xxx_uv.obj

Usage: 
    python combineObj.py

All files in current folder will be scaned
'''

import os 

# @return pos, faces
def loadOBJ(filename):  
    numVerts = 0  
    verts = []  
    faces = []  
    for line in open(filename, "r"):  
        vals = line.split()
        if len(vals) > 0:
            if vals[0] == "v":  
                v = map(float, vals[1:4])  
                verts.append(v)  
            if vals[0] == "f":  
                f = map(int, vals[1:4])  
                faces.append(f)  
    return verts, faces

# @return {filePrefix: [posFile, uvFile]}
def parseDir(dir_):
    objFiles = {}
    for (dirpath, dirnames, filenames) in os.walk(dir_):
        for filename in filenames:
            if filename.endswith(u"_pos.obj"):
                prefixName = filename[:-8]
                full_path = os.path.join(dirpath, filename)
                if prefixName in objFiles:
                    fileList = objFiles[prefixName]
                else:
                    fileList = [None, None]
                    objFiles[prefixName] = fileList
                fileList[0] = full_path
            if filename.endswith(u"_uv.obj"):
                prefixName = filename[:-7]
                full_path = os.path.join(dirpath, filename)
                fileList = objFiles[prefixName]
                if not fileList:
                    fileList = []
                    objFiles[prefixName] = fileList
                fileList[1] = full_path

    return objFiles

def writeObj(pos_, uv_, faces_, filePath):
    f = open(filePath, "w")

    # write pos
    for pos in pos_:
        f.write(u"v " + unicode(pos[0]) + u" " + unicode(pos[1]) + " " + unicode(pos[2]) + "\n")

    f.write("\n")

    # write uv
    for uv in uv_:
        # flip v
        v = uv[1]
        v = 1 - v
        f.write(u"vt " + unicode(uv[0]) + u" " + unicode(v) + " " + unicode(uv[2]) + "\n")

    f.write("\n")

    # write faces
    for face in faces_:
        f.write(u"f " + unicode(face[0]) + u"/" + unicode(face[0]) + u" " + unicode(face[1]) + u"/" + unicode(face[1]) + " " + unicode(face[2]) + u"/" + unicode(face[2]) + "\n")

    f.close()

if __name__ == "__main__":
    # scan all files in current folder
    curDir = os.path.dirname(os.path.realpath(__file__))
    objs = parseDir(curDir)
    for prefixName in objs:
        fileList = objs[prefixName]

        # make pos and uv obj file both exit
        if not fileList[0] or not fileList[1]:
            continue

        # read pos
        pos, posFaces = loadOBJ(fileList[0])

        # read uv
        uv, uvFaces = loadOBJ(fileList[1])

        # write obj file
        finalFileName = prefixName + u".obj"
        finalFilePath = os.path.join(curDir, finalFileName)
        writeObj(pos, uv, posFaces, finalFilePath)