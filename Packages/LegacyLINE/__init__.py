# -*- coding: utf-8 -*-
"""
    line 
    ~~~~

    May the LINE be with you...

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""


import sys

from .LegacyClient import LineClient, LineGroup, LineContact, LineRoom

__version__ = '0.1.0'
__all__ = ['LineClient','LineRoom', 'LineGroup','LineContact']
