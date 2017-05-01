'''
Created on Mar 21, 2015

@author: root
'''
import json
import LBlog.usettings as usettings
from django.conf import settings 
from django.http.response import HttpResponse
import datetime,random
import os
from django.views.decorators.csrf import csrf_exempt
import codecs
from gunicorn.http.wsgi import Response
import base64

def GetUeditorSettings():
    content = json.dumps(usettings.UploadSettings)  
    return content

def GetValue(key):
    return usettings.UploadSettings.get(key)

def configAction(request): 
    content = GetUeditorSettings()
    callback = request.GET.get("callback")
    if callback:
        return HttpResponse("{0}{1}".format(callback, content))
    return HttpResponse(content)

class initJsonResult(object):
    def __init__(self,state="未知的错误",url="",title="",original="",error="null"):
        super(initJsonResult).__init__()
        self.state = state
        self.url = url
        self.title = title
        self.original = original
        self.error = error

def bulidJsonResult(result):
    jsondata = {
                "state":result.state,
                "url":result.url,
                "title":result.title,
                "original":result.original,
                "error":result.error
                }
    return json.dumps(jsondata)

def buildFileName(filename):
    dt = datetime.datetime.now()
    name,ext = os.path.splitext(filename)
    return "%s-" % name + dt.strftime("%Y%m%d%M%H%S{0}{1}".format(random.randint(1,653323), ext))
    
def checkFileName(filename,AllowExtensions):
    exts = list(AllowExtensions)
    name,ext = os.path.splitext(filename)
    return ext in exts

def checkFileSize(filesize,SizeLimt):
    return filesize < SizeLimt

def checkDirExit(saveDir):
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        
@csrf_exempt
def uploadFile(request,UploadFieldName,SizeLimit,AllowExtensions,SavePath,Base64,Base64Filename):
    
    action = request.GET.get("action")
#     print(action)
    result = initJsonResult()
    
    if action == "uploadscrawl":
        filename = Base64Filename
        saveName = buildFileName(filename)
        webUrl = SavePath + saveName
        saveDir = settings.MEDIA_ROOT + SavePath
        checkDirExit(saveDir)
        savePath = settings.MEDIA_ROOT + webUrl
        try:
            content = request.POST.get(UploadFieldName)
            f = open(savePath,'wb')
            f.write(base64.urlsafe_b64decode(content))
            f.close()
            result.state = "SUCCESS"
        except Exception as e:
            e.message
            result.state = "ERROR"
        result.url = saveName
        result.title = saveName
        result.original =saveName
        response = HttpResponse(bulidJsonResult(result))
        response["Content-Type"]="text/plain"
        return response
    else:
        buf = request.FILES.get(UploadFieldName)
        filename = buf.name
        if not checkFileName(filename, AllowExtensions):
            result.error = "不允许的文件格式"
            return HttpResponse(bulidJsonResult(result))
        if not checkFileSize(buf.size, SizeLimit):
            result.error = "文件大小超出了限制"
            return HttpResponse(bulidJsonResult(result))
        
        try:
            saveName = buildFileName(filename)
            webUrl = SavePath + saveName
#             print(settings.MEDIA_ROOT)
            saveDir = settings.MEDIA_ROOT + SavePath
            checkDirExit(saveDir)
            savePath = settings.MEDIA_ROOT + webUrl
            f = codecs.open(savePath, "wb")
            for chunk in buf.chunks():
                f.write(chunk)
            f.flush()
            f.close()
            result.state = "SUCCESS"
            result.url = saveName
            result.title = saveName
            result.original =saveName
            response = HttpResponse(bulidJsonResult(result))
            response["Content-Type"]="text/plain"
            return response
        except:
            result.error = "ERROR"
            return HttpResponse(bulidJsonResult(result))
@csrf_exempt
def listFileManager(request,imageManagerListPath,imageManagerAllowFiles,listsize):

    start = int(request.GET.get("start",0))
    size = int(request.GET.get("size",GetValue(listsize)))
    localPath = settings.MEDIA_ROOT + imageManagerListPath
    filelist = []
    exts = list(imageManagerAllowFiles)
    index = start
    for imagename in os.listdir(localPath):
        name,ext = os.path.splitext(imagename)
        if ext in exts:
            filelist.append(dict(url=imagename))
            index += 1
            if index - start>=size:
                break
    jsondata = {"state":"SUCCESS","list":filelist,"start":start,"size":size,"total":index}
    return HttpResponse(json.dumps(jsondata))

@csrf_exempt
def uploadimageAction(request):
    AllowFiles = GetValue("imageAllowFiles") 
    MaxSize = GetValue("imageMaxSize")
    FieldName = GetValue("imageFieldName")
    SavePath = GetValue("imagePath")
    return uploadFile(request,FieldName,MaxSize,AllowFiles,SavePath,False,'')
@csrf_exempt
def uploadvideoAction(request):
    AllowFiles = GetValue("videoAllowFiles") 
    MaxSize = GetValue("videoMaxSize")
    FieldName = GetValue("videoFieldName")
    SavePath = GetValue("videoPath")
    return uploadFile(request,FieldName,MaxSize,AllowFiles,SavePath,False,'')
@csrf_exempt
def uploadfileAction(request):
    AllowFiles = GetValue("fileAllowFiles") 
    MaxSize = GetValue("fileMaxSize")
    FieldName = GetValue("fileFieldName")
    SavePath = GetValue("filesPath")
    return uploadFile(request,FieldName,MaxSize,AllowFiles,SavePath,False,'')
@csrf_exempt
def listimageAction(request):
    imageManagerListPath = GetValue("imageManagerListPath")
    imageManagerAllowFiles = GetValue("imageManagerAllowFiles")
    imagelistsize = GetValue("imageManagerListSize")
    return listFileManager(request,imageManagerListPath,imageManagerAllowFiles,imagelistsize)

@csrf_exempt
def ListFileManagerAction(request):
    fileManagerListPath = GetValue("fileManagerListPath")
    fileManagerAllowFiles = GetValue("fileManagerAllowFiles")
    filelistsize = GetValue("fileManagerListSize")
    return listFileManager(request,fileManagerListPath,fileManagerAllowFiles,filelistsize)

def uploadscrawlAction(request):
    MaxSize = GetValue("scrawlMaxSize")
    FieldName = GetValue("scrawlFieldName")
    SavePath = GetValue("scrawlPath")
    return uploadFile(request,FieldName,MaxSize,'',SavePath,True,'scrawlFile.png')

actions = {
            "config" : configAction,
            "uploadimage" : uploadimageAction,
            "uploadvideo":uploadvideoAction,
            "uploadfile":uploadfileAction,
            "listimage":listimageAction,
            "listfile":ListFileManagerAction,
            "uploadscrawl":uploadscrawlAction,
           }

@csrf_exempt
def Get_Actions(request):
    action = request.GET.get("action")
    print(action)
    return actions.get(action)(request)