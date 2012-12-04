# -*- coding: utf-8 -*-
"""
gites.shop

Licensed under the GPL license, see LICENCE.txt for more details.
"""
from gites.core.utils import publishObject, changeDocumentView, addViewToType


def setupshop(context):
    if context.readDataFile('gites.shop_various.txt') is None:
        return
    portal = context.getSite()
    if 'shop' not in portal.objectIds():
        #ajout du dossier
        portal.invokeFactory('Folder', 'shop')
        shop_folder = getattr(portal, 'shop')
        shop_folder.manage_addProperty('left_slots', [], 'lines')

    shop_folder_folder = getattr(portal, 'shop')

    if 'shop' not in shop_folder_folder.objectIds():
        #ajout du document
        shop_folder_folder.invokeFactory('Document', 'shop')

    left_slots = ['here/portlet_menu_gites_meubles/macros/portlet',
                  'here/portlet_outil/macros/portlet',
                  'here/portlet_partenaires/macros/portlet']
    shop_folder_folder.manage_changeProperties(left_slots=left_slots)

    #determine la vue par default du folder comme le document
    shop_folder_folder.setDefaultPage('shop')
    publishObject(shop_folder_folder)

    shop_folder_document = getattr(shop_folder_folder, 'shop')
    #determine la vue par default du document
    addViewToType(portal, 'Document', 'shop_folder_view')
    changeDocumentView(shop_folder_document, 'shop_folder_view')
    publishObject(shop_folder_document)
