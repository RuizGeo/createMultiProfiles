# -*- coding: utf-8 -*-
"""
/***************************************************************************
 createMultiProfiles
                                 A QGIS plugin
 Create Profiles from drainage network and ridge
                             -------------------
        begin                : 2015-05-22
        copyright            : (C) 2015 by Luis Fernando Chimelo Ruiz
        email                : ruiz.ch@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load createMultiProfiles class from file createMultiProfiles.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from multi_profiles import createMultiProfiles
    return createMultiProfiles(iface)
