from rest_framework import viewsets
from rest_framework.response import Response
class ResponseTemplate:
    def __init__(self,*args,**kwargs):
        self.status = kwargs.get('status')
        self.code = kwargs.get('code')
        self.data = kwargs.get('data')
        self.kwagrs = kwargs
    def template(self):
        rt = {
            'code':self.code,
            'status':self.status,
            'data':self.data,
                }
        if self.kwagrs.get('kwargs'):
            rt.update({k:v for k,v in self.kwagrs.get('kwargs').items()})
        return rt

class BaseModelViewSet(viewsets.ModelViewSet): 
    '''抽象类'''
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        return Response(ResponseTemplate(status='成功', code=200, data = data, kwargs=kwargs).template())
   
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = response.data
        return Response(ResponseTemplate(status='创建成功', code=200, data = data, kwargs=kwargs).template())
    def update(self, request, *args, **kwargs):
        response = super().update( request, *args, **kwargs)
        data = response.data
        return Response(ResponseTemplate(status='更新成功', code=200, data = data, kwargs=kwargs).template())
    def destroy(self, request, *args, **kwargs):
        response = super().destroy( request, *args, **kwargs)
        data = response.data
        return Response(ResponseTemplate(status='删除成功', code=200, data = data, kwargs=kwargs).template())

    def perform_destroy(self, instance):
        '''打上删除标记'''
        instance.is_delete = True
        instance.save()
       
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve( request, *args, **kwargs)
        data = response.data
        return Response(ResponseTemplate(status='成功', code=response.status_code, data = data).template())
