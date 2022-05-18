from django.conf import settings
from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated

from dogApp.models.user import User
from dogApp.serializers.userSerializer import UserSerializer

# Esta clase extrae API.VIEW una funcionalidad del API 
# con la definición del método HTTP post se ejecutara 
# la función cuando se pida en la vista crear un usuario   
class UserCreateView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        tokenData = {"username":request.data["username"],
                    "password":request.data["password"]}
        tokenSerializer = TokenObtainPairSerializer(data = tokenData)
        tokenSerializer.is_valid(raise_exception = True)
        return Response(tokenSerializer.validated_data, 
                        status = status.HTTP_201_CREATED)

# Esta clase permite obtener la información del registro en la entidad
class UserDetailView(generics.RetrieveAPIView):
    # Estos 3 atributos le indican a Django que usar en la funcionalidad
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    # Esta función valida que quien solicita la información tiene acceso
    def get(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm = settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify = False)

        if valid_data['user_id'] != kwargs['pk']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, 
                            status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

# Esta clase permite actualizar la información del registro en la entidad
class UserUpdateView(generics.UpdateAPIView):
    # Estos 3 atributos le indican a Django que usar en la funcionalidad
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    # Esta función valida que quien colicita la actualización tiene acceso
    def put(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm = settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify = False)

        if valid_data['user_id'] != kwargs['pk']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, 
                            status=status.HTTP_401_UNAUTHORIZED)
        
        instance = self.get_object()
        instance.name = request.data.get("name")
        instance.last_name = request.data.get("last_name")
        instance.email = request.data.get("email")
        instance.password = request.data.get("password")
        instance.save()

        stringResponse = {'detail':'Sucessfully updated'}
        return super().put(request, *args, **kwargs)

# Esta clase permite ver una lista de todos los usuarios y crear nuevos
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Esta clase permite borrar el registro del usuario autenticado 
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
                
        if valid_data['user_id'] != kwargs['pk']:
            stringResponse = {'detail':f'Unauthorized Request'}
            return Response(stringResponse, 
                            status=status.HTTP_401_UNAUTHORIZED)
                
        stringResponse = {'detail':'Sucessfully deleted'}
        return super().delete(request, *args, **kwargs)