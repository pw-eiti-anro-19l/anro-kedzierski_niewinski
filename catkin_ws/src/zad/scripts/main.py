import yaml

if __name__ == '__main__':
    data = yaml.load(open("./plik.yaml"))
    print("\n \n \n Hello \n \n \n")
    dh = data["dh"]
    print(dh)
    print("\n")
    index = 0
    wynik = open("wynik.yaml","w")
    for x in dh:
        name = "j"+ str(index)+":"
        xyz = str(x[1])+" 0.0 "+str(x[0])
        rpy = str(x[2])+" 0.0 "+str(x[3])
        len = "len: "+str(x[4])
        string = name+"\n\txyz: "+xyz+"\n\trpy: " + rpy+"\n\t"+len+"\n"
        print(string)
        wynik.write(string)
        index = index+1
    wynik.close()

