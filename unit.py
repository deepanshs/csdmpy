from astropy import units as u
# from astropy.units import cds

# cds.enable()

_ppm = u.def_unit('ppm', 1e-6*u.Unit(1))
_tr = u.def_unit(['tr', 'turn', 'cycle', 'revolution'], 1*u.Unit(1))

convert = {
    "Å" : "Angstrom",
    "°C" : "deg_C",
    "°F" : "deg_F",
    "°" : "deg",
    "µ" : "u",
    "ℏ" : "/h",
    "Ω" : "Ohm",
    # "ppm" : _ppm,
}

# dimensionless_frequency_ratio = [(u.Hz, _ppm, lambda x: 1000.0 * x, lambda x: x / 1000.0)]


def string_to_quantity(string, dtype=float):

    numeric = '0123456789-+.eE*/j^ ()'
    string = string.strip()+' '
    
    for i,c in enumerate(string):
        if c not in numeric:
            break

    j=1
    for j in range(1,i+1):
        if string[:i][-j] == '(': break
        if string[:i][-j] == ')':
            j = j-1
            break
    if i-j==0: index=i
    else: index=i-j
    # print (index)
    #    print (string[:index])
    #    print (eval(string[:index]))
    if index != -1:
        try:
            number = eval(string[:index])
        except:
            raise Exception('Invalid numerical operation, ', string[:index])
    #        return (False, "Invalid numerical operation")
    else:
        index = 0
        number = 1.0

    unit = string[index:].strip()
    if unit != '' and unit != '()':
        if unit[0] == '(' and unit[-1] == ')': unit = unit[1:-1]
    # unit = unit.replace("µ", "u")

    for key in convert:
        unit = unit.replace(key, convert[key])

    # unit_list = unit.split(' ')
    # for item in unit_list:
    #     numerator, denominator = item.split('/')
    try:
        unitQt = u.Unit(unit)
        # print (unit, unitQt)
        analysis = dtype(number) * unitQt
        
#        if dataType=='float':
#            analysis = float(number) * unitQt
#        if dataType=='int':
#            analysis = int(number) * unitQt
        return analysis
    except BaseException as e:
        raise BaseException(e)

def valueObjectFormat(quantity):
    # mode = 'fits'
    string = quantity.unit.to_string('fits').strip()
    # print ('string', string)
    for key in convert:
        string = string.replace(convert[key], key)
    string = string.replace("10**-6", "ppm")
    # print ('string', string)

    catString = [str(quantity.value)]
    subunits = string.split(' ')
    for item in subunits:
        power = False
        if item.find('-') == -1:
            for i,c in enumerate(item):
                if c.isnumeric():
                    if i == 0: break
                    catString.append(item[:i]+'^'+item[i:]+' *')
                    power = True
                    break
            if not power : catString.append(item+' *')       
        else:
            l, r = item.split('-')
            catString.append(l+'^-'+r+' *')
    string = ' '.join(catString)[:-2]
    string = string.replace('* / *', '/')
    # string = string.replace('* ( *', '(')
    # string = string.replace('* ) *', ')')
    return string

def unitToLatex(unit):
    # mode = 'fits'
    string = unit.to_string('fits').strip()
    # print (string)
    convertTex = {
        "Angstrom" : "\\AA",
        "deg_C" : "$^\\circ$C",
        "deg_F" : "$^\\circ$C",
        "deg" : "$^\\circ$",
        "u" : "$\\mu$",
        "/h" : "$\\hbar$",
        "Ohm" : "$\\Ohm$",
        "10**-6" : "ppm"
}
    for key in convertTex:
        string = string.replace(key, convertTex[key])
    # print (string)

    catString = []
    subunits = string.split(' ')
    for item in subunits:
        power = False
        if item.find('-') == -1:
            for i,c in enumerate(item):
                if c.isnumeric():
                    if i == 0: break
                    catString.append(item[:i]+'$^{'+item[i:]+'}$ ')
                    power = True
                    break
            if not power : catString.append(item+' ')       
        else:
            l, r = item.split('-')
            catString.append(l+'$^{-'+r+'}$ ')
    string = ' '.join(catString)
    # string = string.replace('* / *', '/')
    # string = string.replace('* ( *', '(')
    # string = string.replace('* ) *', ')')
    return string

if __name__ == '__main__':
    # import numpy as np
    from timeit import default_timer as timer
    start = timer()
    s = "4 ppm"
    # s = '5 cm^-1 µs °'
    # print (s, type(s))
    a = string_to_quantity(s)#, dtype=np.float32)
    print (timer() - start)
    print (a)
    # print (type(a.unit), a.unit.physical_type)
    # print (valueObjectFormat(a))
    # print (unitToLatex(a.unit))
