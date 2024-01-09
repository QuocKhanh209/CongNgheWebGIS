import os
from geo.Geoserver import Geoserver

geo = Geoserver('http://127.0.0.1:8080/geoserver', username='admin', password='geoserver')


#Kiểm tra workspace đã tồn tại chưa
def wsp_exist(wsp):
    try:
        all_wsp = geo.get_workspaces()['workspaces']['workspace']
    except:
        return False
    
    if wsp in [item['name'] for item in all_wsp]:
        return True
    
    return False

#Kiểm tra store đã tồn tại chưa
def store_exist(wsp, store):
    try:
        wsp_stores = geo.get_datastores(wsp)['dataStores']['dataStore']
    except:
        return False
    
    if store in [item['name'] for item in wsp_stores]:
        return True

    return False

#Tạo workspace
def create_workspace(_wsp = None):
    if _wsp is None:
        wsp = 'project'
    else:
        wsp = _wsp
    
    if not wsp_exist(wsp):
        try:
            geo.create_workspace(workspace=wsp)
        except:
            pass

#Tạo store
def create_store_postgis(_wsp = None, _store=None):
    from . import postgis

    pg_params = postgis.get_parmas()
    store_name = pg_params.get('db')

    if _wsp is None:
        wsp = 'project'
    else:
        wsp = _wsp

    if _store is None:
        store = store_name
    else:
        store = _store

    create_workspace(wsp)

    if not store_exist(wsp, store):
        try:
            geo.create_featurestore(store_name=store, workspace=wsp, **pg_params)
        except:
            pass

#public các bảng thành một lớp layer
def publish_layer_postgis(table_name, _wsp, _store):
    try:
        geo.publish_featurestore(workspace=_wsp, store_name=_store, pg_table=table_name)
    except:
        pass