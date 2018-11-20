from ._studium import Dimension, _nusDimensionObject
import numpy as np

class dimensions:

    __slots__ = ['_keywords', '_stopDimensions', 'dimension', '_shape']

    def __init__(self):
        _key = ('number_of_points', 
                'sampling_interval', 
                'coordinates', 
                'reference_offset',
                'origin_offset', 
                'made_dimensionless', 
                'reverse',
                'fft_output_order', 
                'periodic', 
                'quantity', 
                'label', 
                'inverse_sampling_interval', 
                'inverse_reference_offset', 
                'inverse_origin_offset', 
                'inverse_made_dimensionless', 
                'inverse_reverse', 
                'inverse_quantity', 
                'inverse_label',
                'inverse_periodic')
        super(dimensions, self).__setattr__('_keywords', _key)
        super(dimensions, self).__setattr__('_stopDimensions', 0)
        super(dimensions, self).__setattr__('dimension', ())
        super(dimensions, self).__setattr__('_shape', ())

    def __delattr__(self, name):
        if name in __class__.__slots__ :
            raise AttributeError("attribute '{0}' cannot be deleted.".format(name))

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' cannot be modified".format(name))
        else:
            raise AttributeError("'dimensions' object has no attribute '{0}'".format(name))

    @property
    def keys(self):
        return self._keywords

    @property
    def shape(self):
        return self._shape

    @property
    def size(self):
        return len(self.dimension)

    def addDimension(self, *arg, **kwargs):

        default = {'number_of_points':None, 
                   'sampling_interval':None, 
                   'coordinates':None, 
                   'reference_offset':None,
                   'origin_offset':None, 
                   'made_dimensionless':False, 
                   'reverse':False, 'fft_output_order':False, 
                   'periodic':False, 
                   'quantity':None, 'label':'',
                   'reciprocal':{
                        'sampling_interval':None, 
                        'reference_offset':None, 
                        'origin_offset':None, 
                        'made_dimensionless':False, 
                        'reverse':False, 
                        'periodic':False,
                        'quantity':None, 
                        'label':''}
                    }
        defaultKeys = default.keys()

        if arg != ():
            if type(arg[0]) == dict:
                inputDict = arg[0]
            else:
                errorString = ''.join(['The arguament must be a dictionary with allowed keywords or keyword arguaments.',
                                  '\nUse keys() method of dimensions object to find the list of allowed keywords'])
                raise Exception(errorString)
        else:
            inputDict = kwargs

        inputKeys = inputDict.keys()
        if 'reciprocal' in inputKeys:
            inputSubKeys = inputDict['reciprocal'].keys()
        for key in inputKeys:
            if key in defaultKeys:
                if key == 'reciprocal':
                    for subkey in inputSubKeys:
                        default[key][subkey]=inputDict[key][subkey]
                else:
                    default[key]=inputDict[key]

        if default['quantity'] == 'non-physical':
            if default['coordinates'] is None:
                raise Exception("'coordinates' key is required.")
            pass

        
        if default['number_of_points'] is None and default['coordinates'] is None:
            raise Exception("either 'number_of_points' or 'coordinates' key is required.")

        if default['coordinates'] is not None:
            super(dimensions, self).__setattr__('dimension', \
                    self.dimension + (_nusDimensionObject( \
                        _coordinates            = default['coordinates'], \
                        _reference_offset        = default['reference_offset'],  \
                        _origin_offset           = default['origin_offset'], \
                        _made_dimensionless      = default['made_dimensionless'], \
                        _reverse                = default['reverse'], \
                        _periodic               = default['periodic'], \
                        _quantity               = default['quantity'], \
                        _label                  = default['label']), ) )
            super(dimensions, self).__setattr__('_stopDimensions', self._stopDimensions +1)
            # print ('length',  len(default['coordinates']))
            super(dimensions, self).__setattr__('_shape', self._shape + (len(default['coordinates']), ) )
            return

        
        if default['number_of_points'] is not None and default['sampling_interval'] is None:
            default['sampling_interval'] = '1'

        if default['number_of_points'] is not None and default['sampling_interval'] is not None:
            super(dimensions, self).__setattr__('dimension', \
                    self.dimension + (Dimension(
                        _number_of_points       = default['number_of_points'], 
                        _sampling_interval      = default['sampling_interval'], 
                        _reference_offset       = default['reference_offset'], 
                        _origin_offset          = default['origin_offset'], 
                        _made_dimensionless     = default['made_dimensionless'],
                        _reverse                = default['reverse'], 
                        _fft_output_order       = default['fft_output_order'], 
                        _periodic               = default['periodic'], 
                        _quantity               = default['quantity'], 
                        _label                  = default['label'], 
                        _inverse_sampling_interval = default['reciprocal']['sampling_interval'],
                        _inverse_reference_offset = default['reciprocal']['reference_offset'], 
                        _inverse_origin_offset    = default['reciprocal']['origin_offset'],
                        _inverse_made_dimensionless = default['reciprocal']['made_dimensionless'], 
                        _inverse_reverse         = default['reciprocal']['reverse'], 
                        _inverse_quantity        = default['reciprocal']['quantity'],
                        _inverse_periodic        = default['reciprocal']['periodic'],
                        _inverse_label           = default['reciprocal']['label']), ) )
            super(dimensions, self).__setattr__('_stopDimensions', self._stopDimensions +1)
            super(dimensions, self).__setattr__('_shape', self._shape + (default['number_of_points'], ) )

            # print (self._shape)
            return 

    def __getitem__(self, i):
        length = self._stopDimensions
        while i < 0:
            i += length
        if 0 <= i < length:
            return self.dimension[i]._coordinates
        raise IndexError('Index out of range: {}'.format(i))

    def info(self):
        x = ['number_of_points',\
            'sampling_interval', \
            'reference_offset', \
            'origin_offset', \
            'made_dimensionless', \
            'reverse', \
            'quantity', \
            'label', \
            'ftFlag', \
            'periodic']
        y = []
        for i in range(len(self.dimension)):
            y.append(self.dimension[i].info())
        pack = np.asarray(y).T, x, ['dimension '+str(i) for i in range(len(self.dimension))]
        return pack

    def __str__(self):
        for i in range(len(self.dimension)):
            print ('Dimension', str(i))
            print (self.dimension[i])
        return ('')

    def to(self, unit, axis=-1):
        super(Dimension, self.dimension[axis]).__setattr__('_coordinates', \
                                self.dimension[axis]._coordinates.to(unit))
        # super(Dimension, self.dimension[axis]).__setattr__('_unit', unit)
        # self.dimension[axis]._coordinates = self.dimension[axis]._coordinates.to(unit)


