from genericpath import exists
from django.conf import settings
from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated

from dogApp.models.user import User
from dogApp.models.dog import Dog
from dogApp.serializers.dogSerializer import DogSerializer

# Esta clase extrae API.VIEW una funcionalidad general del 
# API con la definición del método HTTP post se ejecutara 
# la función cuando se pida en la vista crear un usuario   
class DogCreateView(views.APIView):
# Este atributo indica que solo se puede crear un registro
# en la entidad si tiene un access token
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        # Se valida que el oken sea valido
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm = settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify = False)
        # Se almacena el JSON ingresado en el serializer
        serializer = DogSerializer(data = request.data)
        # Se valida que el registro del Dog se asocia al User autenticado
        if valid_data['user_id'] != request.data.get("id_user"):
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
       
        # Se crea el registro en la BD
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(status = status.HTTP_201_CREATED)

# Esta clase permite ver una lista de todos los perros
class DogList(generics.ListAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

# Esta clase permite obtener la información del registro por nombre en la entidad
class DogDetailView(generics.ListAPIView):
    serializer_class = DogSerializer
    
    def get_queryset(self):
        name = self.kwargs['name']
        return Dog.objects.filter(name=name)

# Esta clase permite obtener los registros por filtro is_adopted = True
class DogFilterListView(generics.ListAPIView):
    serializer_class = DogSerializer
    
    def get_queryset(self):
        return Dog.objects.filter(is_adopted=True)

# Esta clase permite actualizar la información en la entidad
class DogUpdateView(generics.UpdateAPIView):
    # Estos 3 atributos le indican a Django que usar en la funcionalidad
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    permission_classes = (IsAuthenticated,)
    # Con esta definición se cambia que no solicitie la pk sino el name en la URL
    lookup_field = 'name' 

    # Esta función valida que quien colicita la actualización tiene acceso
    def put(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm = settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify = False)

        if valid_data['user_id'] != request.data.get("id_user"):
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, 
                            status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()
        instance.picture = request.data.get("picture")
        instance.is_adopted = request.data.get("is_adopted")
        instance.create_date = request.data.get("create_date")
        instance.save()

        stringResponse = {'detail':'Sucessfully updated'}
        return super().put(request, *args, **kwargs)

# Esta clase permite borrar el registro 
class DogDeleteView(generics.DestroyAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'name' 

    def delete(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

    
        stringResponse = {'detail':'Sucessfully deleted'}
        return super().delete(request, *args, **kwargs)