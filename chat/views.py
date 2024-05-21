from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import OuterRef, Subquery
from django.db.models import Q
from Base.models import Profile
from .models import  ChatMessage
from django.contrib.auth.models import User
from rest_framework import generics
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 
from rest_framework.response import Response

class MyInbox(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        messages = ChatMessage.objects.filter(
            id__in =  Subquery(
                User.objects.filter(
                    Q(sender__reciever=user_id) |
                    Q(reciever__sender=user_id)
                ).distinct().annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'),reciever=user_id) |
                            Q(reciever=OuterRef('id'),sender=user_id)
                        ).order_by('-id')[:1].values_list('id',flat=True) 
                    )
                ).values_list('last_msg', flat=True).order_by("-id")
            )
        ).order_by("-id")
            
        return messages
    
class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        reciever_id = self.kwargs['reciever_id']
        messages =  ChatMessage.objects.filter(sender__in=[sender_id, reciever_id], reciever__in=[sender_id, reciever_id])
        return messages

class SendMessages(generics.CreateAPIView):
    serializer_class = MessageSerializer



class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]  


class SearchUser(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]  

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        logged_in_user = self.request.user
        users = Profile.objects.filter(Q(user__username__icontains=username) | Q(full_name__icontains=username) | Q(user__email__icontains=username) & 
                                       ~Q(user=logged_in_user))

        if not users.exists():
            return Response(
                {"detail": "No users found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)