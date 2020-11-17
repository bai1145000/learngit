from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from django.contrib.auth import authenticate, login,  logout
from rest_framework.authtoken.models import Token

class UserLogin(APIView):
    '''用户登录'''
    permission_classes = []
    authentication_classes = []
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password) #验证账号是否正确,返回用户实例
        if user:
            login(request, user) #保持登录
            # token = Token.objects.create(user=user) #创建token值,和login有冲突
            # request.session['Token'] = token.key
            superuser = 1 if user.is_superuser else 0
            return Response({ 'code':200,'status': '登录验证成功!', 'username': username,'user_id': superuser,
                    'token': request.session.session_key})
        return Response({'code': 400, 'text': '验证失败!,密码错误','账户为:':username})
    
    def patch(self,request):
        '''更新密码'''
        username =request.data.get('username') 
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        if hasattr(request.session,'session_key') : #检查session是否存在
            user = request.user
            username = request.user.username    
        else:
            user = authenticate(username=username, password=password)
            
        if user:
            user.set_password(new_password)
            user.save()
            return Response({ 'code':200,'text': '密码修改为:%s'%user.password})
        return Response({'code':404,'text':'账号或者密码错误'})        

class UserLogout(APIView):
    '''用户退出'''
    permission_classes = []
    def post(self,request):
        if hasattr(request.session,'session_key'):
            user = request.user.username
            logout(request)
            return Response({'code': 200, 'text': '退出成功','账户为:': user})
        return Response({'code': 400, 'text': '退出失败,当前没有账号登录'})
    
class RegisterViews(APIView):
    '''注册'''
    permission_classes = []
    authentication_classes = []
    
    def post(self,request,*args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not User.objects.filter(username=username) and password:
            email = request.POST.get("email",None)
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return Response({'code': 200, 'status': '注册成功'})
        return Response({'code': 400, 'status': '注册失败'})