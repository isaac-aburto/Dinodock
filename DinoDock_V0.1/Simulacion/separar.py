with open("Simulacion/contenedores.csv", "r") as archivo:
    for i in archivo:
        if "ID" not in i:
            data = i.strip().split(";")
            with open("Simulacion/contenedores{}.csv".format(data[1]), 'a') as subarchivo:
                subarchivo.write(str(data[0]) + "\n")