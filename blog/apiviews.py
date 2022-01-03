
from rest_framework import authentication, request,status
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.serializers import Serializer
from .serializers import PostSerializers, RegisterSerializers 
from .models import Post
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view

class PostListView(ListCreateAPIView):
    serializer_class = PostSerializers
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request, *args, **kwargs):
        serializer = PostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  
        return Response(data=
         {
             "message":"success"
         }
        )


class PostView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return Post.objects.all().filter(author=user)


@api_view(['POST'])
def register_view(request):

    if request.method == 'POST':
        serializer = RegisterSerializers(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully registerd a new user"
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)        