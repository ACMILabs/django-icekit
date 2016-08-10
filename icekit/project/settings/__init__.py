from __future__ import absolute_import

import os

try:
    from settings import *
except ImportError:
    os.environ.setdefault('BASE_SETTINGS_MODULE', 'develop')
    from .calculated import *
