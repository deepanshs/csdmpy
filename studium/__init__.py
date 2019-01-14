from __future__ import print_function, division
from .linearQuantitative import _linearQuantitativeControlledVariable as lQCV
from .nonLinearQuantitative import _nonLinearQuantitativeControlledVariable as nlQCV
from .nonQuantitative import _nonQuantitativeControlledVariable as nQCV
from .uncontrolledVariables import _unControlledVariable as uv
import numpy as np
import json
from scipy.fftpack import fft, fftshift



def _importJson(filename):
    with open(filename, "rb") as f:
        content = f.read()
        return (json.loads(str(content,encoding = "UTF-8")))

class dataModel:

    __slots__ = [ 
                 'controlled_variables', 
                 'uncontrolled_variables',
                 'filename'
                 ]

    def __init__(self, filename=''):

        super(dataModel, self).__setattr__('controlled_variables', ())
        super(dataModel, self).__setattr__('uncontrolled_variables', ())
        super(dataModel, self).__setattr__('filename', filename)

        if filename != '':
            dictionary = _importJson(filename)
            for dim in dictionary['controlled_variables']:
                self.addControlledVariable(dim)

            for dat in dictionary['uncontrolled_variables']:
                self.addUncontrolledVariable(dat, filename)

        _type = [(item.sampling_type == 'grid') for item in self.controlled_variables]
        # print (npts, _type, np.all(_type))
        if np.all(_type):
            npts = [item.number_of_points for item in self.controlled_variables]
            [item.reshape(npts[::-1]) for item in self.uncontrolled_variables]
        else:
            _type = [(item.sampling_type == 'scatter') for item in self.controlled_variables]
            if not np.all(_type):
                raise Exception("controlled_variables can be either be all grid or all scatter type. \
                                Type mixing is not supported.")

    def __delattr__(self, name):
        if name in __class__.__slots__ :
            raise AttributeError("attribute '{0}' cannot be deleted.".format(name))

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' cannot be modified".format(name))
        else:
            raise AttributeError("'dimensions' object has no attribute '{0}'".format(name))

### ----------- Public Methods -------------- ###
    def addControlledVariable(self, *arg, **kwargs):

        default = {'sampling_type':"grid",
                   'non_quantitative': False,
                   'number_of_points':None, 
                   'sampling_interval':None, 
                   'coordinates':None, 
                   'reference_offset':None,
                   'origin_offset':None, 
                   'made_dimensionless':False, 
                   'reverse':False, 'fft_output_order':False, 
                   'periodicity':None, 
                   'quantity':None, 'label':'',
                   'reciprocal':{
                        'sampling_interval':None, 
                        'reference_offset':None, 
                        'origin_offset':None, 
                        'made_dimensionless':False, 
                        'reverse':False, 
                        'periodicity':None,
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

        if default['non_quantitative']:
            if default['coordinates'] is None:
                raise Exception("'coordinates' key is required.")
            else:
                super(dataModel, self).__setattr__('controlled_variables', \
                    self.controlled_variables + (nQCV( \
                        _sampling_type          = default['sampling_type'], \
                        _non_quantitative           = default['non_quantitative'], \

                        _coordinates            = default['coordinates'], \
                        _reverse                = default['reverse'], \
                        _label                  = default['label'] ), ))

        if not default['non_quantitative']:
            if default['number_of_points'] is None and \
                    default['sampling_interval'] is None and \
                    default['coordinates'] is None:
                raise Exception("either 'number_of_points/sampling_interval' or 'coordinates' key is required.")

        if not default['non_quantitative'] and default['coordinates'] is not None:
            super(dataModel, self).__setattr__('controlled_variables', \
                    self.controlled_variables + (nlQCV( \
                        _sampling_type          = default['sampling_type'], \
                        _non_quantitative           = default['non_quantitative'], \

                        _coordinates            = default['coordinates'], \
                        _reference_offset       = default['reference_offset'],  \
                        _origin_offset          = default['origin_offset'], \
                        _quantity               = default['quantity'], \
                        _reverse                = default['reverse'], \
                        _label                  = default['label'], \
                        _periodicity            = default['periodicity'], \
                        _made_dimensionless     = default['made_dimensionless'], \

                        _reciprocal_reference_offset    = default['reciprocal']['reference_offset'], 
                        _reciprocal_origin_offset       = default['reciprocal']['origin_offset'],
                        _reciprocal_quantity            = default['reciprocal']['quantity'],
                        _reciprocal_reverse             = default['reciprocal']['reverse'],
                        _reciprocal_periodicity         = default['reciprocal']['periodicity'],
                        _reciprocal_label               = default['reciprocal']['label'],
                        _reciprocal_made_dimensionless  = default['reciprocal']['made_dimensionless']), ))

        if not default['non_quantitative'] and \
                default['number_of_points'] is not None and \
                default['sampling_interval'] is not None:
            super(dataModel, self).__setattr__('controlled_variables', \
                    self.controlled_variables + (lQCV(
                        _sampling_type          = default['sampling_type'], \
                        _non_quantitative           = default['non_quantitative'], \

                        _number_of_points       = default['number_of_points'], 
                        _sampling_interval      = default['sampling_interval'], 
                        _reference_offset       = default['reference_offset'], 
                        _origin_offset          = default['origin_offset'], 
                        _quantity               = default['quantity'], 
                        _reverse                = default['reverse'], 
                        _label                  = default['label'],
                        _periodicity            = default['periodicity'], 
                        _fft_output_order       = default['fft_output_order'], 
                        _made_dimensionless     = default['made_dimensionless'],

                        _reciprocal_sampling_interval   = default['reciprocal']['sampling_interval'],
                        _reciprocal_reference_offset    = default['reciprocal']['reference_offset'], 
                        _reciprocal_origin_offset       = default['reciprocal']['origin_offset'],
                        _reciprocal_quantity            = default['reciprocal']['quantity'],
                        _reciprocal_reverse             = default['reciprocal']['reverse'],
                        _reciprocal_periodicity         = default['reciprocal']['periodicity'],
                        _reciprocal_label               = default['reciprocal']['label'],
                        _reciprocal_made_dimensionless  = default['reciprocal']['made_dimensionless']), ))

    def addUncontrolledVariable(self, *arg, **kwargs):
        default = {'name': '',
                   'unit' : '',
                   'quantity' : None,
                   'component_labels': None,
                   'encoding': None,
                   'numeric_type' : None,
                   'dataset_type': 'scalar',
                   'components':None,
                   'components_URI' : None,
                   'sampling_schedule' : None}

        defaultKeys = default.keys()

        if arg != ():
            if type(arg[0]) == dict:
                inputDict = arg[0]
                if (len(arg) >= 2):
                    filename = arg[1]
                else:
                    filename = ''
            else:
                errorString = ''.join(['This method only accept keyword arguaments or a dictionary with keywords.',
                                  '\nUse keys() method of dimensions object to find the list of allowed keywords'])
                raise Exception(errorString)
        else:
            inputDict = kwargs

        inputKeys = inputDict.keys()
        for key in inputKeys:
            if key in defaultKeys:
                default[key]=inputDict[key]

        # if default['coordinates'] is None and default['sampling_interval'] is None:
        #     raise Exception("The method either requires input '{0}' or '{1}'.".format('sampling_interval', 'coordinate'))

        super(dataModel, self).__setattr__('uncontrolled_variables', 
                self.uncontrolled_variables + (uv(
                                _name = default['name'],
                                _unit = default['unit'],
                                _quantity = default['quantity'], 
                                _encoding = default['encoding'],
                                _numeric_type = default['numeric_type'],
                                _dataset_type = default['dataset_type'],
                                _component_labels = default['component_labels'],
                                _components = default['components'],
                                _components_URI = default['components_URI'], 
                                _sampling_schedule = default['sampling_schedule'],
                                _filename = filename), ) )


    def datum(self, index):
        for i in range(len(self.uncontrolled_variables[0])):
            (self.uncontrolled_variables[0].components[index])


    def _info(self):
        x =['sampling_type',\
            'non_quantitative',\
            'number_of_points',\
            'sampling_interval', \
            'reference_offset', \
            'origin_offset', \
            'made_dimensionless', \
            'reverse', \
            'quantity', \
            'label', \
            'ftFlag', \
            'periodicity']
        y = []
        for i in range(len(self.controlled_variables)):
            y.append(self.controlled_variables[i].info())
        pack = np.asarray(y).T, x, ['dimension '+str(i) for i in range(len(self.controlled_variables))]
        return pack

    def __str__(self):
        dictionary = self._getPythonDictonary(self.filename, print_function=True)
        return (json.dumps(dictionary, sort_keys=False, indent=2))

    def _getPythonDictonary(self, filename, print_function=False, version='1.0.0'):
        dictionary = {}
        dictionary["uncontrolled_variables"] = []
        dictionary["controlled_variables"] = []
        dictionary["version"] = version
        for i in range(len(self.controlled_variables)):
            dictionary["controlled_variables"].append( \
                    self.controlled_variables[i]._getPythonDictonary(version=version))
        
        _length_of_uncontrolled_variables =  len(self.uncontrolled_variables)
        for i in range(_length_of_uncontrolled_variables):
            dictionary["uncontrolled_variables"].append( \
                    self.uncontrolled_variables[i]._getPythonDictonary(
                                filename = filename,
                                dataset_index = i, 
                                number_of_components = _length_of_uncontrolled_variables, 
                                for_display = print_function, 
                                version = version))
        return dictionary

    def save(self, filename, version='1.0.0'):
        dictionary = self._getPythonDictonary(filename, version=version)
        with open(filename, 'w') as outfile:
            json.dump(dictionary, outfile, sort_keys=False, indent=2)

    def fft(self, dimension=0):
        if self.controlled_variables[dimension].non_quantitative:
            raise ValueError('Non-quantitative dimensions cannot be Fourier transformed.')
        if self.controlled_variables[dimension]._type == 'non-linear' or \
                self.controlled_variables[dimension].sampling_type == 'scatter':
            raise ValueError('Fourier transform of non-linear or scattered dimensions is not yet implemented.')


        cs = self.controlled_variables[dimension].reciprocal_coordinates + \
                    self.controlled_variables[dimension].reciprocal_reference_offset
        phase = np.exp(1j * 2*np.pi* self.controlled_variables[dimension].reference_offset * cs)

        for i in range(len(self.uncontrolled_variables)):
            signalFT = fftshift(fft(self.uncontrolled_variables[i].components, \
                                    axis=-dimension-1), axes=-dimension-1)*phase
            self.uncontrolled_variables[i].setAttribute('_components', signalFT)
        self.controlled_variables[dimension]._reciprocal()
        

        