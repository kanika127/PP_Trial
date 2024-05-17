from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound
from rest_framework import serializers
from rest_framework import status
from django.db.models import Q
from django.http import JsonResponse

from app1.models import PassionUser
from app1.serializers import *
