from django.utils.deprecation import MiddlewareMixin
from django.contrib.admin.models import LogEntry
class ApiLoggingMiddleware(MiddlewareMixin):
    '''日志管理'''
    def __init__(self, get_response):
        self.dict_log = dict()
        super().__init__(get_response)

    def process_request(self, request):
        '''请求时执行'''
        self.dict_log['res_path'] = request.META.get('HTTP_HOST') + request.path
        self.dict_log['user'] = request.user.username
        self.dict_log['method'] = request.method
        self.dict_log['import'] = {k:v for k,v in request.GET.items()}
        

    def process_response(self, request, response):
        '''视图函数调用之后，response返回浏览器之前'''
        try:
            LogEntry.objects.create(
                object_id = request.resolver_match.url_name,
                object_repr = request.resolver_match.view_name,
                action_flag = 1,
                change_message = self.dict_log,
                user = request.user,    
            )
        except :
            pass
        return response

    # def process_exception(self, request, exception):
    #     return exception
        
class NotUseCsrfTokenMiddlewareMixin(MiddlewareMixin):
    '''csrf防护残留解决方法'''
    def process_request(self,request):
        setattr(request, '_dont_enforce_csrf_checks', True) 