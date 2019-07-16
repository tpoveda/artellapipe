#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains basic implementation for Artella Projects
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os
import sys
import json
import traceback

import tpDccLib as tp
from tpPyUtils import osplatform

import artellapipe
from artellapipe.core import defines, artellalib


class ArtellaProject(object):

    PROJECT_RESOURCE = None
    PROJECT_CONFIG_PATH = artellapipe.get_project_config_path()
    PROJECT_SHELF_FILE_PATH = artellapipe.get_shelf_path()

    def __init__(self, resource=None):
        super(ArtellaProject, self).__init__()

        self._name = None
        self._project_env_var = None
        self._logger = None
        self._tray = None
        self._config = None
        self._id_number = None
        self._id = None
        self._asset_types = list()
        self._asset_files = list()
        self._asset_must_files = list()
        self._wip_status = None
        self._publish_status = None
        self._shelf_icon = None
        self._resource = resource

        # To make sure that all variables are properly initialized we must call init_config first
        self.init_config()
        self._logger = self.create_logger()[1]

    @property
    def name(self):
        """
        Returns the name of the Artella project
        :return: str
        """

        return self._name

    @property
    def project_environment_variable(self):
        """
        Returns name used to store path to the current project
        :return: str
        """

        return self._project_env_var

    @property
    def logger(self):
        """
        Returns the logger used by the Artella project
        :return: Logger
        """

        return self._logger

    @property
    def tray(self):
        """
        Returns the tray used by the Artella project
        :return: Tray
        """

        return self._tray

    @property
    def asset_types(self):
        """
        Returns the list of asset types being used by the Artella project
        :return: list(str)
        """

        return self._asset_types

    @property
    def asset_files(self):
        """
        Returns the list of asset files being used by the Artella project
        :return: list(str)
        """

        return self._asset_files

    @property
    def asset_must_files(self):
        """
        Returns the list of asset files that an asset need to have published to consider the asset ready for production
        :return: list(str)
        """

        return self._asset_must_files

    @property
    def working_status(self):
        """
        Returns the name of the working status
        :return: str
        """

        return self._wip_status

    @property
    def publish_status(self):
        """
        Returns the name of the publish status
        :return: str
        """

        return self._publish_status

    @property
    def resource(self):
        """
        Returns the class used by the project to load resources (icons, images, fonts, etc)
        :return: Resource
        """

        return self._resource

    def init(self, force_skip_hello=False):
        """
        This function initializes Artella project
        :param force_skip_hello: bool, Whether the hello window should be showed or not
        """

        if force_skip_hello:
            os.environ['ARTELLA_PIPELINE_SHOW'] = ''

        self.update_paths()
        self.set_environment_variables()
        self.create_shelf()
        self.update_project()

    def init_config(self):
        """
        Function that reads project configuration file and initializes project variables properly
        This function can be extended in new projects
        """

        if not self.PROJECT_CONFIG_PATH or not os.path.isfile(self.PROJECT_CONFIG_PATH):
            tp.Dcc.error('Project Configuration File for Artella Project not found! {}'.format(self.PROJECT_CONFIG_PATH))
            return

        with open(self.PROJECT_CONFIG_PATH, 'r') as f:
            project_config_data = json.load(f)
        if not project_config_data:
            tp.Dcc.error('Project Configuration File for Artella Project is empty! {}'.format(self.PROJECT_CONFIG_PATH))
            return

        self._name = project_config_data.get(defines.ARTELLA_CONFIG_PROJECT_NAME, defines.ARTELLA_DEFAULT_PROJECT_NAME)
        self._project_env_var = project_config_data.get(defines.ARTELLA_CONFIG_ENVIRONMENT_VARIABLE, defines.ARTELLA_DEFAULT_ENVIRONMENT_VARIABLE)
        self._id_number = project_config_data.get(defines.ARTELLA_CONFIG_PROJECT_NUMBER, -1)
        self._id = project_config_data.get(defines.ARTELLA_CONFIG_PROJECT_ID, -1)
        self._asset_types = project_config_data.get(defines.ARTELLA_CONFIG_ASSET_TYPES, list())
        self._asset_files = project_config_data.get(defines.ARTELLA_CONFIG_ASSET_FILES, list())
        self._asset_must_files = project_config_data.get(defines.ARTELLA_CONFIG_ASSET_MUST_FILES, list())
        self._wip_status = project_config_data.get(defines.ARTELLA_CONFIG_ASSET_WIP_STATUS, None)
        self._publish_status = project_config_data.get(defines.ARTELLA_CONFIG_ASSET_PUBLISH_STATUS, None)
        self._shelf_icon = project_config_data.get(defines.ARTELLA_CONFIG_SHELF_ICON, None)

        if self._id_number == -1 or self._id == -1 or not self._wip_status or not self._publish_status:
            tp.Dcc.error('Project Configuration File for Project: {} is not valid!'.format(self.name))
            return

    def get_clean_name(self):
        """
        Returns a clenaed version of the project name (without spaces and in lowercase)
        :return: str
        """

        return self.name.replace(' ', '').lower()

    def get_data_path(self):
        """
        Returns path where user data for Artella project should be located
        This path is mainly located to store tools configuration files and log files
        :return: str
        """

        data_path = os.path.join(os.getenv('APPDATA'), self.get_clean_name())
        if not os.path.isdir(data_path):
            os.makedirs(data_path)

        return data_path

    def create_logger(self):
        """
        Creates and initializes Artella project logger
        """

        from tpPyUtils import log as log_utils

        log_path = self.get_data_path()
        if not os.path.exists(log_path):
            raise RuntimeError('{} Log Path {} does not exists!'.format(self.name, log_path))

        log = log_utils.create_logger(logger_name=self.get_clean_name(), logger_path=log_path)
        logger = log.logger

        if '{}_DEV'.format(self.get_clean_name().upper()) in os.environ and os.environ.get(
                '{}_DEV'.format(self.get_clean_name().upper())) in ['True', 'true']:
            logger.setLevel(log_utils.LoggerLevel.DEBUG)
        else:
            logger.setLevel(log_utils.LoggerLevel.WARNING)

        return log, logger

    def update_paths(self):
        """
        Updates system path with custom paths needed by Artella project
        This function is called during project initialization and can be extended in new projects
        """

        # We add Artella Python Scripts folder if it is not already added
        artella_folder = artellalib.get_artella_python_folder()
        if artella_folder not in sys.path:
            sys.path.append(artella_folder)

    def set_environment_variables(self):
        """
        Initializes environment variables needed by the Artella Project
        This function is called during project initialization and can be extended in new projects
        :return:
        """

        self.logger.debug('Initializing environment variables for: {}'.format(self.name))

        try:
            artellalib.update_local_artella_root()
            artella_var = os.environ.get(defines.ARTELLA_ROOT_PREFIX, None)
            self.logger.debug('Artella environment variable is set to: {}'.format(artella_var))
            if artella_var and os.path.exists(artella_var):
                os.environ[self._project_env_var] = '{}_art/production/{}/{}/'.format(artella_var, self._id_number, self._id)
            else:
                self.logger.warning('Impossible to set Artella environment variable!')
        except Exception as e:
            self.logger.debug('Error while setting Solstice Environment Variables. Solstice Tools may not work properly!')
            self.logger.error('{} | {}'.format(e, traceback.format_exc()))

        self.logger.debug('=' * 100)
        self.logger.debug("{} Pipeline initialization completed!".format(self.name))
        self.logger.debug('=' * 100)
        self.logger.debug('*' * 100)
        self.logger.debug('-' * 100)
        self.logger.debug('\n')

    def create_shelf(self):
        """
        Creates Artella Project shelf
        """

        self.logger.debug('Building {} Tool Shelf'.format(self.name))

        shelf_category_icon = None
        if self.resource and self._shelf_icon:
            shelf_category_icon = self.resource.icon(self._shelf_icon, theme=None)
        project_shelf = tp.Shelf(name=self._name.replace(' ', ''), category_icon=shelf_category_icon)
        project_shelf.create(delete_if_exists=True)
        shelf_file = self.PROJECT_SHELF_FILE_PATH
        if not shelf_file or not os.path.isfile(shelf_file):
            self.logger.warning('Shelf File for Project {} is not valid: {}'.format(self._name, shelf_file))
            return

        project_shelf.build(shelf_file=shelf_file)
        project_shelf.set_as_active()

    def update_project(self):
        """
        Sets the current Maya project to the path where Artella project is located inside Artella folder
        """

        try:
            if tp.is_maya():
                import tpMayaLib as maya
                self.logger.debug('Setting {} Project ...'.format(self.name))
                project_folder = os.environ.get(self._project_env_var, 'folder-not-defined')
                if project_folder and os.path.exists(project_folder):
                    maya.cmds.workspace(project_folder, openWorkspace=True)
                    self.logger.debug('{} Project setup successfully! => {}'.format(self.name, project_folder))
                else:
                    self.logger.warning('Unable to set {} Project! => {}'.format(self.name, project_folder))
        except Exception as e:
            self.logger.error('{} | {}'.format(str(e), traceback.format_exc()))

    def message(self, msg, title=None):
        """
        Shows tray given message in OS tray. If tray is not available, the message will be
        output in the debug logger
        :param msg: str, message to show
        :param title: str, title to show; if None, the project name will be used
        :return:
        """

        if not title:
            title = self.PROJECT_NAME.title()

        if osplatform.is_windows():
            if self.tray:
                self.tray.show_message(title=title, msg=msg)
            else:
                self.logger.debug(str(msg))
        else:
            self.logger.debug(str(msg))











