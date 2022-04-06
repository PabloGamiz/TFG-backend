from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import redirect
#from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
from django import forms
#from .forms import SubmitForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .models import (ClassificationResidentialBuilding, ClassificationNotResidentialBuilding, NewBuildingDemand, NewBuildingEnergyConsume, NewBuildingEmissions, ExistingBuildingDemand, ExistingBuildingEnergyConsume, ExistingBuildingEmissions, NewBuldingDemandDispersions, NewBuldingEnergyAndEmissionsDispersions, ExistingBuldingDemandDispersions, ExistingBuldingEnergyAndEmissionsDispersions)
from .serializers import (ClassificationResidentialBuildingSerializer, ClassificationNotResidentialBuildingSerializer, NewBuildingDemandSerializer, NewBuildingEnergyConsumeSerializer, NewBuildingEmissionsSerializer, ExistingBuildingDemandSerializer, ExistingBuildingEnergyConsumeSerializer, ExistingBuildingEmissionsSerializer, NewBuldingDemandDispersionsSerializer, NewBuldingEnergyAndEmissionsDispersionsSerializer, ExistingBuldingDemandDispersionsSerializer, ExistingBuldingEnergyAndEmissionsDispersionsSerializer)
from django.db.models import Case, When
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_yasg import openapi
#from allauth.socialaccount import providers
#from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from django.shortcuts import get_object_or_404
#from allauth.socialaccount.providers.facebook.views import fb_complete_login
#from allauth.socialaccount.helpers import complete_social_login
#import allauth.account
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework.parsers import JSONParser

# Create your views here.

class ResidentialBuildingClassificationSet(ViewSet):
    parser_classes = [JSONParser]
    #Introducir valores de la clasificacion de edificios nuevos
    @swagger_auto_schema(
        operation_description='Crea les diferents classificacions per a edificis nous amb el valors de la classificacio',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona la lletra de la classificacio i les diferents metriques de classificacio',
            properties= {
                'classificacio': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la lletra corresponent a la classificacio',
                                    example= 'A'),
                'min_C1': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor minim de C1 que la classificacio pot obtenir',
                                    example= '1.5'),
                'max_C1': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor maxim de C1 que la classificacio pot obtenir',
                                    example= '2.5'),
                'min_C2': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor minim de C2 que la classificacio pot obtenir',
                                    example= '1.7'),
                'max_C2': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor maxim de C2 que la classificacio pot obtenir',
                                    example= '1.9'),
            },
            required=["classificacio", "min_C1", "max_C1"],
        ),
        responses= {404: 'classificacio no trobada', 200: 'classificacio creada correctament', 401: 'No has proporcionat cap API key'})
    def create(self, request):
        c = ClassificationResidentialBuilding(calification = request.data['classificacio'], min_C1 = request.data['min_C1'], max_C1 = request.data['max_C1'],min_C2 = request.data['min_C2'],max_C2 = request.data['max_C2'])
        #queryset = ClassificationResidentialBuilding.objects.get(classification = c.classification)
        serializer = ClassificationResidentialBuildingSerializer(c)
        return Response(serializer.data)

#Actualizar los valores de una classificacion para un edificio nuevo
    @swagger_auto_schema(
        operation_description='Actualitza els valors de les classificacions per a edificis nous',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona la lletra de la classificacio i les diferents metriques de classificacio',
            properties= {
                'classificacio': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la lletra corresponent a la classificacio',
                                    example= 'A'),
                'min_C1': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor minim de C1 que la classificacio pot obtenir',
                                    example= '1.5'),
                'max_C1': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor maxim de C1 que la classificacio pot obtenir',
                                    example= '2.5'),
                'min_C2': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor minim de C2 que la classificacio pot obtenir',
                                    example= '1.7'),
                'max_C2': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor maxim de C2 que la classificacio pot obtenir',
                                    example= '1.9'),
            },
            required=["classificacio", "min_C1", "max_C1"],
        ),
        responses= {404: 'Classificacio no trobada', 200: 'Classificacio actualitzada correctament', 401: 'No has proporcionat cap API key'})
    def update(self, request, pk=None):
        c = ClassificationResidentialBuilding.objects.get(calification = request.data['classificacio'])
        c.min_C1 = request.data['min_C1']
        c.max_C1 = request.data['max_C1']
        c.min_C2 = request.data['min_C2']
        c.max_C2 = request.data['max_C2']
        c.save()
        #queryset = ClassificationResidentialBuilding.objects.get(classification = c.classification)
        serializer = ClassificationResidentialBuildingSerializer(c)
        return Response(serializer.data)

    #Obtener la clasificacion rerlacionada a un valor que se envia para un edificio nuevo
    @swagger_auto_schema(
        operation_description='Obtè el valor de la classificacio per un valor introduit d\'un edifici residencial',
        manual_parameters=[
            openapi.Parameter(
                'C1',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True,
                description='Proporciona el valor de C1 calculat',
            ),
        ],
        responses= {401:  'No has proporcionat cap API key', 200: openapi.Schema(type = openapi.TYPE_STRING, description='Categoria pertanyent als valors proporcionats')})
    def retrieve(self, request):
        classification = ClassificationResidentialBuilding.objects.filter(min_C1__lt = request.data['C1'], max_C1__gt=request.data['C1']).values('classification')
        serializer = ClassificationResidentialBuildingSerializer(classification)
        return(Response.data)
    
    @swagger_auto_schema(
        operation_description='Obtè el valor de la classificacio per un valor introduit d\'un edifici residencial',
        manual_parameters=[
            openapi.Parameter(
                'C1',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True,
                description='Proporciona el valor de C1 calculat',
            ),
            openapi.Parameter(
                'C2',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True,
                description='Proporciona el valor de C2 calculat',
            ),
        ],
        responses= {401:  'No has proporcionat cap API key', 200: openapi.Schema(type = openapi.TYPE_STRING, description='Categoria pertanyent als valors proporcionats')})
    def retrieve(self, request):
        classification = ClassificationResidentialBuilding.objects.filter(min_C1__lt = request.data['C1'], max_C1__gt = request.data['C1'], min_C2__lt =request.data['C2'], max_C2__gt = request.data['C2']).values('classification')
        serializer = ClassificationResidentialBuildingSerializer(classification)
        return(Response.data)