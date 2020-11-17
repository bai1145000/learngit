from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination,CursorPagination

class Pagination(PageNumberPagination):

    page_size= 10 #默认每页显示个数配置
    
    page_query_param = 'current' 

    page_size_query_param ='pageSize'  # 指定每页显示个数参数
    max_page_size = None

    def get_paginated_response(self, data):

        return Response(data)


 
