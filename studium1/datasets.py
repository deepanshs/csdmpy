from ._studium import _datasetObject
import numpy as np

class datasets:

    __slots__ = ['_keywordsDataset', '_stopDataset', 'dataset']
    
    def __init__(self):
        _key = ['name',
                'unit',
                'quantity',
                'label',
                'encoding',
                'numeric_type',
                'dataset_type',
                'uncertainty',
                'components',
                'uncertainties',
                'components_url',
                'uncertainties_url']

        super(datasets, self).__setattr__('_keywordsDataset', _key)
        super(datasets, self).__setattr__('_stopDataset', 0)
        super(datasets, self).__setattr__('dataset', ())

    def keys(self, keyword=None):
        if keyword is None:
            return self._keywordsDataset
        else:
            print ('add informations to the keywords')
            # return _detailKeywods(keyword)

    def addDataset(self, *arg, **kwargs):
        default = {'name': '',
                   'unit' : '',
                   'quantity' : 'dimensionless',
                   'label': '',
                   'encoding': None,
                   'numeric_type' : 'float32',
                   'dataset_type': 'scalar',
                   'uncertainty' : 0.0,
                   'components':None,
                   'uncertainties' : None,
                   'components_url' : None,
                   'uncertainties_url' : None}

        defaultKeys = self._keywordsDataset

        if arg != ():
            if type(arg[0]) == dict:
                inputDict = arg[0]
                filename = arg[1]
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

        super(datasets, self).__setattr__('dataset', 
                self.dataset + (_datasetObject(
                                _name = default['name'],
                                _unit = default['unit'],
                                _quantity = default['quantity'], 
                                _label = default['label'], 
                                _encoding = default['encoding'],
                                _numeric_type = default['numeric_type'],
                                _dataset_type = default['dataset_type'],
                                _uncertainty = default['uncertainty'], 
                                _components = default['components'],
                                _uncertainties = default['uncertainties'],
                                _components_url = default['components_url'], 
                                _uncertainties_url = default['uncertainties_url'],
                                _filename = filename), ) )
        super(datasets, self).__setattr__('_stopDataset', self._stopDataset + 1)
       
    def __len__(self):
        return self._stopDataset

    def info(self):
        x = ['components_url',\
            'name', \
            'unit', \
            'quantity', \
            'label', \
            'encoding', \
            'numeric_type', \
            'dataset_type']
        y = []
        for i in range(len(self.dataset)):
            y.append(self.dataset[i].info())
        pack = np.asarray(y).T, x, ['dataset '+str(i) for i in range(len(self.dataset))]
        return pack


    def __getitem__(self, i):
        length = self._stopDataset
        while i < 0:
            i += length
        if 0 <= i < length:
            return self.dataset[i]
        raise IndexError('Index out of range: {}'.format(i))

    def to(self, unit, axis=-1):
        self.dataset[axis]._values = self.dataset[axis]._values.to(unit)


    def reshape(self, shape):
        _s = shape
        for i in range(self._stopDataset):
            shape = _s + (self.dataset[i]._channels,)
            nptype = self.dataset[i]._npType
            super(_datasetObject, self.dataset[i]).__setattr__('_components', \
                np.asarray(self.dataset[i]._components.reshape(shape), dtype=nptype))

            # super(_datasetObject, self.dataset[i]).__setattr__('channel', \
            #     np.asarray(self.dataset[i]._values.reshape(shape), dtype=nptype))
            return self

    @property
    def size(self):
        return len(self.dataset)

    # def __iadd__(self, other):
    #     for i in range(self._stopDataset):
    #         self.dataset[i]._values+=other


