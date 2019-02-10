from __future__ import print_function, division
from .controlled_variables import _linearlySampledGridDimension
from .controlled_variables import _arbitrarilySampledGridDimension
from .controlled_variables import _nonQuantitativeGridDimension
from .uncontrolledVariables import _unControlledVariable
import numpy as np
import json
from scipy.fftpack import fft, fftshift
import os


script_path = os.path.dirname(os.path.abspath(__file__))
# print (script_path)

test_file = {
    "test01": script_path+'/testFiles/test01.csdf',
    "test02": script_path+'/testFiles/test02.csdf'
    }


_open_py = open

def _import_json(filename):
    with _open_py(filename, "rb") as f:
        content = f.read()
        return (json.loads(str(content,encoding = "UTF-8")))

"""A test doc

.. moduleauthor:: Deepansh J. Srivastava <srivastava.89@osu.edu>

"""

def open(filename=None):
    # print (filename)
    if filename is None:
        raise Exception("'open' method requires a data file address.")
    
    try:
        dictionary = _import_json(filename)
    except Exception as e:
        raise Exception(e)

    ### Create the CSDModel and populate the attribures
    _version = dictionary['CSDM']['version']

    csdm = CSDModel(filename, _version)


    for dim in dictionary['CSDM']['controlled_variables']:
        csdm.add_controlled_variable(dim)

    for dat in dictionary['CSDM']['uncontrolled_variables']:
        csdm.add_uncontrolled_variable(dat) #, filename)

    _type = [(item.sampling_type == 'grid') for item in csdm.controlled_variables]

    if np.all(_type):
        npts = [item.number_of_points for item in csdm.controlled_variables]
        [item.reshape(npts[::-1]) for item in csdm.uncontrolled_variables]
    else:
        _type = [(item.sampling_type == 'scatter') for item in csdm.controlled_variables]
        if not np.all(_type):
            raise Exception("controlled_variables can be either be all grid or all scatter type. \
                            Type mixing is not supported.")


    ### Create the augmentation layer model ###
    
    return csdm

def create_new():
    return CSDModel()

class CSDModel:

    current_version = '0.1.0'
    _old_compatible_versions = ('0.1.0')
    _old_incompatible_versions = ('1.0.0')

    """

    The core scientific dataset (CSD) model is designed to be *light-weight*, 
    *portable*, *versatile*, and *standalone*. The CSD model only encapsulates 
    data values and minimum metadata, to accurately describe the data coordinates 
    and coordinates metadata. The model is not intended to encapsulate any 
    information on how the data might be acquired, processed or visualized. 
    The data model is versatile in allowing many use cases for any number of 
    experiments from most spectroscopy, diffraction, and imaging measurements. 
    As such the CSD model supports datasets associated with continuous physical 
    quantities that are discretely sampled in a multi-dimensional space associated 
    with other carefully controlled continuous physical quantities, for e.g., a mass 
    as a function of temperature, a current as a function of voltage and time, a 
    signal voltage as a function of magnetic field gradient strength, etc. It also 
    supports datasets associated with multi-component data values. For example, the 
    left and right audio components as a function of time, a color image with a red, 
    green, and blue (RBG) light intensity components as a function of two independent 
    spatial dimensions, and the six components of the symmetric second-rank diffusion 
    tensor MRI as a function of three independent spatial dimensions. Additionally, 
    the CSD model also supports multiple datasets when identically sampled over the 
    same set of controlled variables. For instance, the current and voltage as a 
    function of time where current and voltage are two datasets sampled over the 
    same temporal coordinates. 

    The CSD model is independent of the hardware, operating system, application 
    software, programming language, and object-oriented file-serialization format 
    used in writing the CSD model to the file.
    The serialized data file is easily human readable and also easily integrable 
    with any number of programming languages and field related application-software.

    """
    __slots__ = [ 
                 'controlled_variables', 
                 'uncontrolled_variables',
                 'version',
                 'filename',
                 ]

    def __init__(self, filename='', version=None):
        """
        The CSDM object 

        ..function::  __init__(self) 
        :param filename: A string containing the address to the data file.

        :attribute: controlled_variables
        :attribute: uncontrolled_variables
        :attribute: version

        :returns: A CSDM object.

        """ 

        if version is None: version = CSDModel.current_version
        elif version in CSDModel._old_incompatible_versions:
            raise Exception("Files created with version {0} of the CSD model are no longer supported.".format([version]))

        super(CSDModel, self).__setattr__('controlled_variables', ())
        super(CSDModel, self).__setattr__('uncontrolled_variables', ())
        super(CSDModel, self).__setattr__('version', version)
        super(CSDModel, self).__setattr__('filename', filename)


    def __delattr__(self, name):
        if name in __class__.__slots__ :
            raise AttributeError("attribute '{0}' cannot be deleted.".format(name))


    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' cannot be modified".format(name))
        else:
            raise AttributeError("'dimensions' object has no attribute '{0}'".format(name))



### ----------- Public Methods -------------- ###

    def add_controlled_variable(self, *arg, **kwargs):

        default = {'sampling_type':"grid",
                   'non_quantitative': False,
                   'number_of_points':None, 
                   'sampling_interval':None, 
                   'coordinates':None, 
                   'reference_offset':None,
                   'origin_offset':None, 
                   'made_dimensionless':False, 
                   'reverse':False, 'fft_output_order':False, 
                   'period':None, 
                   'quantity':None, 'label':'',
                   'reciprocal':{
                        'sampling_interval':None, 
                        'reference_offset':None, 
                        'origin_offset':None, 
                        'made_dimensionless':False, 
                        'reverse':False, 
                        'period':None,
                        'quantity':None, 
                        'label':''}
                    }
        default_keys = default.keys()

        if arg != ():
            if type(arg[0]) == dict:
                input_dict = arg[0]
            else:
                error_string = ''.join(['The arguament must be a dictionary with allowed keywords or keyword arguaments.',
                                  '\nUse keys() method of dimensions object to find the list of allowed keywords'])
                raise Exception(error_string)
        else:
            input_dict = kwargs

        input_keys = input_dict.keys()
        if 'reciprocal' in input_keys:
            input_subkeys = input_dict['reciprocal'].keys()
        for key in input_keys:
            if key in default_keys:
                if key == 'reciprocal':
                    for subkey in input_subkeys:
                        default[key][subkey]=input_dict[key][subkey]
                else:
                    default[key]=input_dict[key]

        if default['non_quantitative']:
            if default['coordinates'] is None:
                raise Exception("'coordinates' key is required.")
            else:
                super(CSDModel, self).__setattr__('controlled_variables', \
                    self.controlled_variables + (_nonQuantitativeGridDimension( \
                        _sampling_type          = default['sampling_type'], \
                        _non_quantitative       = default['non_quantitative'], \

                        _coordinates            = default['coordinates'], \
                        _reverse                = default['reverse'], \
                        _label                  = default['label'] ), ))

        if not default['non_quantitative']:
            if default['number_of_points'] is None and \
                    default['sampling_interval'] is None and \
                    default['coordinates'] is None:
                raise Exception("either 'number_of_points/sampling_interval' or 'coordinates' key is required.")

        if not default['non_quantitative'] and default['coordinates'] is not None:
            super(CSDModel, self).__setattr__('controlled_variables', \
                    self.controlled_variables + (_arbitrarilySampledGridDimension( \
                        _sampling_type          = default['sampling_type'], \
                        _non_quantitative       = default['non_quantitative'], \

                        _coordinates            = default['coordinates'], \
                        _reference_offset       = default['reference_offset'],  \
                        _origin_offset          = default['origin_offset'], \
                        _quantity               = default['quantity'], \
                        _reverse                = default['reverse'], \
                        _label                  = default['label'], \
                        _period                 = default['period'], \
                        _made_dimensionless     = default['made_dimensionless'], \

                        _reciprocal_reference_offset    = default['reciprocal']['reference_offset'], 
                        _reciprocal_origin_offset       = default['reciprocal']['origin_offset'],
                        _reciprocal_quantity            = default['reciprocal']['quantity'],
                        _reciprocal_reverse             = default['reciprocal']['reverse'],
                        _reciprocal_period              = default['reciprocal']['period'],
                        _reciprocal_label               = default['reciprocal']['label'],
                        _reciprocal_made_dimensionless  = default['reciprocal']['made_dimensionless']), ))

        if not default['non_quantitative'] and \
                default['number_of_points'] is not None and \
                default['sampling_interval'] is not None:
            super(CSDModel, self).__setattr__('controlled_variables', \
                    self.controlled_variables + (_linearlySampledGridDimension(
                        _sampling_type          = default['sampling_type'], \
                        _non_quantitative       = default['non_quantitative'], \

                        _number_of_points       = default['number_of_points'], 
                        _sampling_interval      = default['sampling_interval'], 
                        _reference_offset       = default['reference_offset'], 
                        _origin_offset          = default['origin_offset'], 
                        _quantity               = default['quantity'], 
                        _reverse                = default['reverse'], 
                        _label                  = default['label'],
                        _period                 = default['period'], 
                        _fft_output_order       = default['fft_output_order'], 
                        _made_dimensionless     = default['made_dimensionless'],

                        _reciprocal_sampling_interval   = default['reciprocal']['sampling_interval'],
                        _reciprocal_reference_offset    = default['reciprocal']['reference_offset'], 
                        _reciprocal_origin_offset       = default['reciprocal']['origin_offset'],
                        _reciprocal_quantity            = default['reciprocal']['quantity'],
                        _reciprocal_reverse             = default['reciprocal']['reverse'],
                        _reciprocal_period              = default['reciprocal']['period'],
                        _reciprocal_label               = default['reciprocal']['label'],
                        _reciprocal_made_dimensionless  = default['reciprocal']['made_dimensionless']), ))



    def add_uncontrolled_variable(self, *arg, **kwargs):
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

        default_keys = default.keys()

        if arg != ():
            if type(arg[0]) == dict:
                input_dict = arg[0]
                # if (len(arg) >= 2):
                #     filename = arg[1]
                # else:
                #     filename = ''
            else:
                error_string = ''.join(['This method only accept keyword arguaments or a dictionary with keywords.',
                                  '\nUse keys() method of dimensions object to find the list of allowed keywords'])
                raise Exception(error_string)
        else:
            input_dict = kwargs

        input_keys = input_dict.keys()
        for key in input_keys:
            if key in default_keys:
                default[key]=input_dict[key]

        # if default['coordinates'] is None and default['sampling_interval'] is None:
        #     raise Exception("The method either requires input '{0}' or '{1}'.".format('sampling_interval', 'coordinate'))

        super(CSDModel, self).__setattr__('uncontrolled_variables', 
                self.uncontrolled_variables + (_unControlledVariable(
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
                                _filename = self.filename), ) )


    # def datum(self, index):
    #     for i in range(len(self.uncontrolled_variables[0])):
    #         (self.uncontrolled_variables[0].components[index])



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
            'period']
        y = []
        for i in range(len(self.controlled_variables)):
            y.append(self.controlled_variables[i]._info())
        pack = np.asarray(y).T, x, ['dimension '+str(i) for i in range(len(self.controlled_variables))]
        return pack


    def data_structure(self):
        dictionary = self._get_python_dictonary(self.filename, print_function=True)
        return (json.dumps(dictionary, sort_keys=False, indent=2))


    def _get_python_dictonary(self, filename, print_function=False, version=current_version):
        dictionary = {}
        dictionary["uncontrolled_variables"] = []
        dictionary["controlled_variables"] = []
        dictionary["version"] = version
        for i in range(len(self.controlled_variables)):
            dictionary["controlled_variables"].append( \
                    self.controlled_variables[i]._get_python_dictonary())
        
        _length_of_uncontrolled_variables =  len(self.uncontrolled_variables)
        for i in range(_length_of_uncontrolled_variables):
            dictionary["uncontrolled_variables"].append( \
                    self.uncontrolled_variables[i]._get_python_dictonary(
                                filename = filename,
                                dataset_index = i, 
                                for_display = print_function, 
                                version = version))
        csdm = {}
        csdm['CSDM'] = dictionary
        return csdm


    def save(self, filename, version=current_version):
        dictionary = self._get_python_dictonary(filename, version=version)
        with _open_py(filename, 'w') as outfile:
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
            signal_ft = fftshift(fft(self.uncontrolled_variables[i].components, \
                                    axis=-dimension-1), axes=-dimension-1)*phase
            self.uncontrolled_variables[i].set_attribute('_components', signal_ft)
        self.controlled_variables[dimension]._reciprocal()
        

        