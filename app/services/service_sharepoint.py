from decouple import config
from fastapi.responses import JSONResponse
from shareplum import Office365
from shareplum import Site
from shareplum.site import Version
import pandas as pd

class SharepointService:
    def __init__(self):
        self.sp_server = config("SP_SERVER")
        self.sp_data = {}

    def config(self, username, password, site_name, list_name, folder_name):
        content = {"message": True}
        response = JSONResponse(content=content)
        response.set_cookie(key='username', value=username)
        response.set_cookie(key='password', value=password)
        response.set_cookie(key='sitename', value=site_name)
        response.set_cookie(key='listname', value=list_name)
        response.set_cookie(key='foldername', value=folder_name)
        return response

    def sp_connect(self, username, password, sitename):
        authcookie = Office365(self.sp_server, username=username, password=password).GetCookies()
        site = Site(self.sp_server + 'sites/' + sitename, version=Version.v365, authcookie=authcookie)
        return site

    def upload(self, username, password, site_name, folder_name, file, filename):
        site = self.sp_connect(username, password, site_name)
        try:
            folder = site.Folder(folder_name)
            folder.upload_file(file, filename)
            return JSONResponse(status_code=200, content={"message": True})
        except:
            return JSONResponse(status_code=535, content={"message": False})

    def all_records(self, username, password, site_name, list_name):
        site = self.sp_connect(username, password, site_name)
        list = site.List(list_name)
        data = list.GetListItems(fields=['ID', 'Title'])
        return data

    def search_record(self, username, password, site_name, list_name, record_id):
        site = self.sp_connect(username, password, site_name)
        list = site.List(list_name)
        query = {'Where': [('Eq', 'ID', str(record_id))]}
        data = list.GetListItems(fields=['ID', 'Title'], query=query)
        if bool(data) is not False:
            return data
        else:
            return JSONResponse(status_code=404, content={"message": 'Resource not found'})

    def create_record(self, username, password, site_name, list_name, columns, rows):
        site = self.sp_connect(username, password, site_name)
        list = site.List(list_name)
        for x in range(len(columns)):
            self.sp_data[columns[x]] = rows[x]
        list.UpdateListItems(data=[self.sp_data], kind='New')
        return JSONResponse(status_code=200, content={"message": True})

    def delete_record(self, username, password, site_name, list_name, record_id):
        site = self.sp_connect(username, password, site_name)
        try:
            list = site.List(list_name)
            query = {'Where': [('Eq', 'ID', str(record_id))]}
            row = list.GetListItems(fields=['ID'], query=query)
            obj = pd.DataFrame.from_dict(row)
            data = obj['ID'].tolist()
            list.UpdateListItems(data=data, kind='Delete')
            return JSONResponse(status_code=200, content={"message": True})
        except:
            return JSONResponse(status_code=404, content={"message": 'Resource not found'})