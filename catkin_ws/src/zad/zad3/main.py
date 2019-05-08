import yaml

if __name__ == '__main__':
    data = yaml.load(open("./plik.yaml"))
    print("\n \n \n Hello \n \n \n")
    dh = data["dh"]
    print(dh)
    print("\n")
    index = 0
    h=0
    wynik = open("wynik.yaml","w")
    for x in dh:
        name = "j"+ str(index)+":"
        z=str(h)
        h=x[4]
        rpy = str(x[2])+" 0.0 "+str(x[3])
        len = "len: "+str(x[4])
        string = name+"\n   r: "+str(x[2])+"\n   p: 0.0\n   yn: "+str(x[3])+"\n   x: "+str(x[1])+"\n   y: 0.0\n   z: "+z+"\n   "+len+"\n"
        print(string)
        wynik.write(string)
        index = index+1
    wynik.close()

