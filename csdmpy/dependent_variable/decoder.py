"""Decoder for components' encoding types."""
import base64

import numpy as np


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["Decoder"]


class Decoder:
    """Decoder class"""

    def __new__(cls, encoding, quantity_type, components, dtype):
        """Decode the components based on the encoding key value.

        The valid encodings are 'base64', 'none' (text), and 'raw' (binary).
        """
        if encoding != "raw":
            check_number_of_components_and_encoding_type(len(components), quantity_type)
        component_len = quantity_type.p
        method = getattr(cls, "decode_" + encoding)
        return method(components, dtype, component_len)

    @staticmethod
    def decode_base64(components, dtype, component_len=None):
        """Read components form a base64 buffer"""
        components = np.asarray(
            [np.frombuffer(base64.b64decode(item), dtype=dtype) for item in components]
        )
        return components

    @staticmethod
    def decode_none(components, dtype, component_len=None):
        """Read components form a text buffer"""
        return (
            np.asarray(
                [
                    np.asarray(item[0::2]) + 1j * np.asarray(item[1::2])
                    for item in components
                ],
                dtype=dtype,
            )
            if dtype in ["<c8", "<c16", ">c8", ">c16"]
            else np.asarray(components, dtype=dtype)
        )

    @staticmethod
    def decode_raw(components, dtype, component_len=None):
        """Read components form a binary buffer"""
        components = np.frombuffer(components, dtype=dtype)
        if not components.flags["WRITEABLE"]:
            components = components.copy()
        size = int(components.size / component_len)
        components = components.reshape(component_len, size)
        return components


def check_number_of_components_and_encoding_type(length, quantity_type):
    """Verify the consistency of encoding wrt the number of components."""
    if length != quantity_type.p:
        raise Exception(
            f"The quantity_type, '{quantity_type.value}', requires exactly "
            f"{quantity_type.p} component(s), found {length} components."
        )
