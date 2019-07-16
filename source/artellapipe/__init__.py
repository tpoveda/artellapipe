#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for artellapipe
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os
import inspect

from tpPyUtils import importer, path as path_utils
from tpQtLib.core import resource as resource_utils

from artellapipe.core import defines

# =================================================================================

logger = None
resource = None
project = None

# =================================================================================


class ArtellaResource(resource_utils.Resource, object):
    RESOURCES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')


class ArtellaPipe(importer.Importer, object):
    def __init__(self):
        super(ArtellaPipe, self).__init__(module_name='artellapipe')

    def get_module_path(self):
        """
        Returns path where tpNameIt module is stored
        :return: str
        """

        try:
            mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
        except Exception:
            try:
                mod_dir = os.path.dirname(__file__)
            except Exception:
                try:
                    import tpDccLib
                    mod_dir = tpDccLib.__path__[0]
                except Exception:
                    return None

        return mod_dir


def init(do_reload=False):
    """
    Initializes module
    :param do_reload: bool, Whether to reload modules or not
    """

    artella_importer = importer.init_importer(importer_class=ArtellaPipe, do_reload=do_reload)

    global logger
    global resource

    logger = artella_importer.logger
    resource = ArtellaResource

    artella_importer.import_modules()


def set_project(project_class):
    """
    This functions sets the given class instance as the current Artella project used
    :param project_class: ArtellaProject
    """

    global project
    project = project_class()
    project.init()


def get_project_config_path():
    """
    Returns path where default Artella project config is located
    :return: str
    """

    return path_utils.clean_path(os.path.join(os.path.dirname(__file__), defines.ARTELLA_PROJECT_CONFIG_FILE_NAME))
