def dic_converter(data):
    dic ={}
    fieldnames =['Common Metadata Repository (CMR) APIs',
    'Distributed Active Archive Center (DAAC) APIs',
    'Earthdata Login APIs',
    'Earthdata Search APIs',
    'Earthdata Tools APIs',
    'Global Imagery Browse Services (GIBS) APIs',
    'Science Data Processing Software (SDPS) APIs',
    'OPeNDAP APIs',
    'Hyrax Data Server Installation and Configuration Guide',
    'NASA APIs',]
    e = [i for i in data[0].splitlines() if i!='']  

    for j in range(0,len(e),2):
       if e[j+1] not in fieldnames:
          dic[e[j]] = e[j+1]
       else:
           continue  
    return dic


