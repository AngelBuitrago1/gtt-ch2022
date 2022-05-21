import time
from rest_framework import status
from rest_framework.response import Response
from celery import shared_task

@shared_task
def validation_async(user):
    if user == True:
        stringResponse = {'detail':'Successfully Created'}
        return Response(stringResponse, status=status.HTTP_201_CREATED)
    time.sleep(30)