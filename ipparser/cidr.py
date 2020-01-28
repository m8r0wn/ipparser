def cidr_ranges(cidr):
    a = []
    b = []
    c = []
    div = (cidr//8)
    mod = (cidr%8)
    mod = abs(mod-8)
    classes = {}
    power = (2 ** mod)
    if div == 4:
        a = range(0,1)
        b = range(0,1)
        c = range(0,1)
    elif div == 3:
        a = range(0,1)
        b = range(0,1)
        c = range(0,power)
    elif div ==2:
        a = range(0,1)
        b = range(0,power)
        c = range(0,256)
    elif div == 1:
        a = range(0,power)
        b = range(0,256)
        c = range(0,256)
    elif div == 0:
        a = range(0,255)
        b = range(0,255)
        c = range(0,255)
    classes["a"] = a
    classes["b"] = b
    classes["c"] = c
    return classes

def parse_cidr(host_input):
    output = []
    ip_base = host_input.split("/")[0]
    cidr = int(host_input.split("/")[1])
    ip_base = ip_base.split(".")
    classes = cidr_ranges(cidr)
    for a in classes["a"]:
        for b in classes["b"]:
            for c in classes["c"]:
                tmp = ip_base[0] + "." + str(int(ip_base[1]) + a) + "." + str(int(ip_base[2]) + b) + "." + str(int(ip_base[3]) + c)
                output.append(tmp)
    return output