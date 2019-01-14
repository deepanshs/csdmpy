from __future__ import print_function, division
import base64, json, warnings, os
from urllib.request import urlopen
import numpy as np
from ._studium import (_assignAndCheckUnitConsistency, 
                       _checkQuantity,
                       _checkEncoding,
                       _checkNumericType,
                       _checkDatasetType)

class _unControlledVariable:
    """
        keywork aruament :
          name : any string
          format : either 'binary' or 'text'.
          data_type : one of 'float32', 'float64', 'comple64' or 'complex128'.
          unit : unit associated with the dataset.
          quantity : the physical qunatity associated with the dataset.
          values : ordered array in format specified at keywords 'format' and 'data_type'.
    """

    __slots__ = ['_name', 
                 '_unit',
                 '_quantity', 
                 '_encoding', 
                 '_numeric_type', 
                 '_dataset_type', 
                 '_component_labels', 
                 '_components',
                 '_components_URI', 
                 '_sampling_schedule',

                 '_npType',
                 '_channels',
                 '_filename']

    def __init__(self, 
                _name = '',
                _unit = '',
                _quantity = None, 
                _encoding = None, 
                _numeric_type = None,
                _dataset_type = 'scalar',
                _component_labels = None,                
                _components = None,
                _components_URI = None,
                _sampling_schedule = None,
                _filename = ''):

        if _components is None and _components_URI is None:
            raise ValueError("No uncontrolled-variables found.")

        if _encoding is None:
            raise ValueError("Encoding type not specified.")

        # if _components != None and _encoding is None: _encoding = 'none'
        # elif _components_URI != None and _encoding is None: _encoding = 'raw'

        self.setAttribute('_encoding', _checkEncoding(_encoding))
        _va = _assignAndCheckUnitConsistency(_unit, None)
        self.setAttribute('_unit', _va.unit)
        self.setAttribute('_name', str(_name))
        self.setAttribute('_quantity', _checkQuantity(_quantity, self.unit))

        _va, npType = _checkNumericType(_numeric_type)
        self.setAttribute('_numeric_type', _va)
        self.setAttribute('_npType', npType)

        _va, total_components = _checkDatasetType(_dataset_type)
        self.setAttribute('_dataset_type', _va)        
        self.setAttribute('_channels', total_components)
        

        if _components is not None:
            _components = self._decodeComponents(_components)


        if _components_URI is not None : 
            _components = urlopen(_components_URI).read() 
            _components = self._decodeComponents(_components)

            # if self.encoding == 'raw':
            #     splt = os.path.split(_filename)
            #     # print (splt)
            #     _components = np.fromfile( os.path.join(splt[0], _components_URI), dtype=npType)
            #     _components = _components.reshape(total_components, \
            #                         int(_components.size/total_components))#*self.unit
            # else:
            #     raise Exception("'{0}' is an invalid data 'encoding'.".format(self.encoding))


        if _component_labels is None:
            self.setAttribute('_component_labels', ['' for i in range(total_components)])
        elif len(_component_labels) != total_components:
            warnings.warn('number of component labels, {0}, is not equal to the number of components, {1}. Inconsistency is resolved by appropriate truncation or entry string padding.'.format(len(_component_labels), total_components))
            _lables = ['' for i in range(total_components)]
            for i in range(len(_component_labels)):
                _lables[i] = _component_labels[i]
        else:
            self.setAttribute('_component_labels', _component_labels)

        

        # _components = np.asarray(_components, dtype=npType).swapaxes(0,-1)
        self.setAttribute('_components', _components)
        self.setAttribute('_components_URI', _components_URI)

        self.setAttribute('_sampling_schedule', _sampling_schedule)


    def setAttribute(self, name, value):
        super(_unControlledVariable, self).__setattr__(name, value)

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' cannot be modified".format(name))
        elif name in __class__.__dict__.keys():
            return self.setAttribute(name, value)
        else:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(__class__.__name__, name))

    def _downloadFileContentsFromURL(self, filename):
        pass
        
    def _checkNumberOfComponentsAndEncodingKey(self,length):
        if length != self._channels:
            raise Exception("dataset_type '{0}' is non consistent with total number of components, {1}".format(self.dataset_type, _val_len))

    def _decodeComponents(self, _components):
        _val_len = len(_components)

        if self.encoding == 'base64':
            self._checkNumberOfComponentsAndEncodingKey(_val_len)
            _components = np.asarray([np.fromstring(base64.b64decode(item), \
                            dtype=self._npType) for item in _components])
            return _components

        if self.encoding == 'none':
            self._checkNumberOfComponentsAndEncodingKey(_val_len)
            if self._numeric_type[:7] == 'complex':
                _components = np.asarray([np.asarray(item[0::2]) + 1j*np.asarray(item[1::2]) \
                            for item in _components])
            else:
                _components = np.asarray([np.asarray(item) \
                            for item in _components])
            return _components
        
        if self.encoding == 'raw':
            _components = np.frombuffer(_components, dtype=self._npType)
            _components = _components.reshape(self._channels, \
                                int(_components.size/self._channels))
            return _components

        raise Exception("'{0}' is an invalid data 'encoding'.".format(self.encoding))


### --------------- Attributes ------------------ ###
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self.setAttribute('_name', value)
    
    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, value):
        _va = _assignAndCheckUnitConsistency(value, None)
        self.setAttribute('_unit', _va)
        self.quantity = _va.unit.physical_type

    @property
    def quantity(self):
        return self._quantity

    @property
    def encoding(self):
        return self._encoding
    @encoding.setter
    def encoding(self, value):
        value = _checkEncoding(value)
        self.setAttribute('_encoding', value)
    
    @property
    def numeric_type(self):
        return self._numeric_type
    @numeric_type.setter
    def numeric_type(self, value):
        _va, npType = _checkNumericType(value)
        self.setAttribute('_numeric_type', value)
        self.setAttribute('_npType', npType)
        self.setAttribute('_components', \
                np.asarray(self.components, dtype=npType))*self.unit

    @property
    def dataset_type(self):
        return self._dataset_type
    @dataset_type.setter
    def dataset_type(self, value):
        value = _checkDatasetType(value)
        self.setAttribute('_dataset_type', value)

    @property
    def component_labels(self):
        return self._component_labels
    @component_labels.setter
    def component_labels(self, value):
        self.setAttribute('_label', value)

    @property
    def components(self):
        return self._components

    @property
    def components_URI(self):
        return self._components_URI

    @property
    def schedule(self):
        return self._sampling_schedule

    


###--------------Private Methods------------------###
    def _info(self):
        _response =[self.components_URI, 
                    self.name,
                    str(self.unit),
                    self.quantity,
                    self.component_labels,
                    self.encoding,
                    self.numeric_type,
                    self.dataset_type]
        return _response

    def _getPythonDictonary(self, filename, dataset_index=None, number_of_components=None, for_display=True):
        dictionary = {}
        if self.name.strip() != '' and self.name is not None:
            dictionary['name'] = self.name

        if str(self.unit) != '':
            dictionary['unit'] = str(self.unit)

        if self.quantity not in ['dimensionless', 'unknown', None]:
            dictionary['quantity'] = self.quantity

        print_label=False
        for label in self.component_labels:
            if label.strip() != '':
                print_label=True
                break

        if print_label:
            dictionary['component_labels'] = self.component_labels

        dictionary['encoding'] = str(self.encoding)

        dictionary['numeric_type'] = str(self.numeric_type)

        if self.dataset_type != 'scalar':
            dictionary['dataset_type'] = self.dataset_type
        
        if for_display:
            if self.encoding in ['none', 'base64']:
                dictionary['components'] = 'To avoid large ouput display, components array is not printed.'
            if self.encoding in ['raw']:
                dictionary['components_URI'] = self.components_URI
                
        if not for_display:

            size = self.components[0].size
            if self.numeric_type[:7] == 'complex':
                if self.numeric_type == 'complex64':
                    c = np.empty((self._channels, size*2), dtype=np.float32)
                if self.numeric_type == 'complex128':
                    c = np.empty((self._channels, size*2), dtype=np.float64)

                for i in range(self._channels):
                    c[i, 0::2] = self.components.real[i].ravel()
                    c[i, 1::2] = self.components.imag[i].ravel()
            else:
                c = np.empty((self._channels, size), dtype=self._npType)
                for i in range(self._channels):
                    c[i] = self.components[i].ravel()

            if self.encoding == 'none':
                dictionary['components'] = c.tolist()
            if self.encoding == 'base64':
                dictionary['components'] = [base64.b64encode(item).decode("utf-8") \
                                for item in c]

            if self.encoding == 'raw':
                if self.name == '': 
                    index = str(dataset_index)
                else:
                    index = self.name

                splt = os.path.split(filename)
                fname = os.path.splitext(splt[1])[0]

                if number_of_components > 1:
                    directory = os.path.join(splt[0], fname)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    filepath = ''.join([ fname, '/', index, '.dat'])
                else:
                    filepath = ''.join([ fname, '_', index, '.dat'])
                dictionary['components_URI'] = filepath
                c.ravel().tofile( os.path.join(splt[0], dictionary['components_URI'] ))

            c = None
            del c               
        return dictionary

### ------------- Public Methods ------------------ ###

    def __str__(self):
        dictionary = self._getPythonDictonary()
        return (json.dumps(dictionary, sort_keys=False, indent=2))

    def scale(self, value):
        value = _assignAndCheckUnitConsistency(value, None)
        self.setAttribute('_unit', self._unit*value.unit)
        value = self._unit*value.value
        self.setAttribute('_components',self.components*value)

    def to(self, unit):
        factor = self.unit.to(unit)
        self.setAttribute('_components', self.components*factor)
        self.setAttribute('_unit', unit)

    def reshape(self, shape):
        shape = (self._channels,) + tuple(shape)
        nptype = self._npType
        self.setAttribute('_components', \
            np.asarray(self.components.reshape(shape), dtype=nptype))
