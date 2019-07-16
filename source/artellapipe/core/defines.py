#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains all constant definitions used by artellapipe library
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os

# Defines the name of the configuration file used by artellapipe to setup project
ARTELLA_PROJECT_CONFIG_FILE_NAME = 'config.json'

# Defines the name of the attribute that defines the Artella project name
ARTELLA_CONFIG_PROJECT_NAME = 'PROJECT_NAME'

# Defines the name of the attribute that defines the Artella project number
ARTELLA_CONFIG_PROJECT_NUMBER = 'PROJECT_NUMBER'

# Defines the name of the attributes that defines the asset types in the Artella project
ARTELLA_CONFIG_ASSET_TYPES = 'ASSET_TYPES'

# Defines the name of the attributes that defines the asset files types in the Artella project
ARTELLA_CONFIG_ASSET_FILES = 'ASSET_FILES'

# Defines the name of the attributes that defines the asset files types that must be published to consider
# an asset ready for production
ARTELLA_CONFIG_ASSET_MUST_FILES = 'ASSET_MUST_FILES'

# Defines the name of the attributes that defines the working status of an asset
ARTELLA_CONFIG_ASSET_WIP_STATUS = 'ASSET_WIP_STATUS'

# Defines the name of the attributes that defines the working status of an asset
ARTELLA_CONFIG_ASSET_PUBLISH_STATUS = 'ASSET_PUBLISH_STATUS'

# Defines the name of the attribute that defines the Artella project id
ARTELLA_CONFIG_PROJECT_ID = 'PROJECT_ID'

# Defines the default name used by Artella projects
ARTELLA_DEFAULT_PROJECT_NAME = 'Artella'

# Defines the name of the Artella plugin
ARTELLA_MAYA_PLUGIN_NAME = 'Artella.py'

# Defines the name of the Artella executable
ARTELLA_APP_NAME = 'lifecycler'

# Defines the environment variable used by Artella to reference to user local installation folder
ARTELLA_ROOT_PREFIX = '$ART_LOCAL_ROOT'

# Defines path to Artella webpage
ARTELLA_WEB = 'https://www.artella.com'

# Defines path to Artella server
ARTELLA_CMS_URL = 'https://cms-static.artella.com'

# Defines file name used by Artella to detect next version name
ARTELLA_NEXT_VERSION_FILE_NAME = 'version_to_run_next'

# Defines path where Artella is located in Windows
ARTELLA_WINDOWS_INSTALL_PATH = os.path.join(os.getenv('PROGRAMDATA'), 'Artella')

# Defines path where Artella is located in Windows
ARTELLA_MAC_INSTALL_PATH = os.path.join(os.path.expanduser('~/Library/Application Support/'), 'Artella')