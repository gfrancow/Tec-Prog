# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
.. image:: image.jpeg
   :width: 300pt

==============
Modul avrexcep
==============

Es un modul principal del simulador. Els usuaris finals del simulador invoquen aquest modul per simular programes.
"""

class AVRException(Exception):
    """
    Es una excepcio que denota un problema en el simulador de l AVR. En general s empra a traves de subclasses
    """
    pass
