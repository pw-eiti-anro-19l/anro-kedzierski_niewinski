import yaml

if __name__ == '__main__':
    data = yaml.load(open("./plik.yaml"))
    print("\n \n \n Hello \n \n \n")
    dh = data["dh"]
    print(dh)
    print("\n")
    index = 0
    for x in dh:
        print("joint number:"+ str(index))
        xyz = "\""+str(x[1])+" 0.0 "+str(x[0])+"\""
        rpy = "\""+str(x[2])+" 0.0 "+str(x[3])+"\""
        print("xyz: "+xyz+"\nrpy:" + rpy)
        index = index+1

