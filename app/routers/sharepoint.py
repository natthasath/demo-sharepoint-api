from fastapi import APIRouter, Depends, Form, File, UploadFile, Request
from fastapi.responses import JSONResponse
from app.models.model_sharepoint import ConfigSchema, SearchSchema, CreateSchema
from app.services.service_sharepoint import SharepointService

router = APIRouter(
    prefix="/sharepoint",
    tags=["SHAREPOINT"],
    responses={404: {"message": "Not found"}}
)

@router.post("/config")
async def config(data: ConfigSchema = Depends(ConfigSchema)):
    return SharepointService().config(data.username, data.password.get_secret_value(), data.site_name, data.list_name, data.folder_name)

@router.put("/document/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    site_name = request.cookies.get("sitename")
    folder_name = request.cookies.get("foldername")
    return SharepointService().upload(username, password, site_name, folder_name, file.file, file.filename)

@router.get("/list/record")
async def all_records(request: Request):
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    site_name = request.cookies.get("sitename")
    list_name = request.cookies.get("listname")
    return SharepointService().all_records(username, password, site_name, list_name)

@router.post("/list/record/search")
async def search_record(request: Request, data: SearchSchema = Depends(SearchSchema)):
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    site_name = request.cookies.get("sitename")
    list_name = request.cookies.get("listname")
    return SharepointService().search_record(username, password, site_name, list_name, data.record_id)

@router.put("/list/record/create")
async def create_record(request: Request, data: CreateSchema = Depends(CreateSchema)):
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    site_name = request.cookies.get("sitename")
    list_name = request.cookies.get("listname")
    columns = data.columns.strip('][').split(', ')
    rows = data.rows.strip('][').split(', ')
    return SharepointService().create_record(username, password, site_name, list_name, columns, rows)

@router.delete("/list/record/delete")
async def delete_record(request: Request, data: SearchSchema = Depends(SearchSchema)):
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    site_name = request.cookies.get("sitename")
    list_name = request.cookies.get("listname")
    return SharepointService().delete_record(username, password, site_name, list_name, data.record_id)