from studium import dataModel as dtm

def testQuantitativeLinearObject():
    ## Create a dataModel object
    a=dtm() 

    d1={'number_of_points':50,
        'sampling_interval': "1 Hz",
        'reference_offset': "100 Hz"}

    a.addControlledVariable(d1)
    print (' ')
    print(a.controlled_variables[0])
    print(a.controlled_variables[0].coordinates)