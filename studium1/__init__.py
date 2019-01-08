from .datasets import datasets
from .dimensions import Dimensions
import numpy as np
import json
import matplotlib.pyplot as plt

def _importJson(filename):
    with open(filename, "rb") as f:
        content = f.read()
        return (json.loads(str(content,encoding = "UTF-8")))

class data:

    __slots__ = ['dimension', 'dataset']

    def __init__(self, filename=None):
        d = Dimensions()
        s = datasets()
        if filename is not None:
            dictionary = _importJson(filename)
            for dim in dictionary['dimensions']:
                d.addDimension(dim)
                # print (dim)

            for dat in dictionary['datasets']:
                s.addDataset(dat, filename)

            super(data, self).__setattr__('dimension', d)
            super(data, self).__setattr__('dataset', s.reshape(d._shape[::-1]))        
        else:
            super(data, self).__setattr__('dimension', d)
            super(data, self).__setattr__('dataset', s)

    def addDimension(self, dim):
        self.dimension.addDimension(dim)

    def addDataset(self, data):
        self.dataset.addDataset(data)
        self.dataset[-1].reshape(self.dimension._shape[::-1])


    def __delattr__(self, name):
        raise AttributeError("Attribute '{0}' of class '{1}' cannot be deleted.".\
                                        format(name, __class__))

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("Attribute '{0}' cannot be modified.".format(name))

    def info(self):
        dim = self.dimension.info()
        dat = self.dataset.info()
        pack = *dim, *dat
        
        html = '<table><tr>{}</tr></table>'.format(
        '</tr><tr>'.join(
            '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in data))
        return pack
    # def __add__(self, other)

    def save(self, filename):
        d = {}
        d["datasets"] = []
        d["dimensions"] = []
        d["version"] = "0.1"
        for i in range(self.dimension.size):
            d["dimensions"].append(self.dimension.dimension[i].getJsonDictionary())
        for i in range(self.dataset.size):
            d["datasets"].append(self.dataset[i].getJsonDictionary(filename, i))
        with open(filename, 'w') as outfile:
            json.dump(d, outfile, sort_keys=True, indent=2)
