from django.http.request import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework import viewsets 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, NotAuthenticated
from rest_framework.views import APIView

from .models import OrganizationComment, OrganizationRating, ProductFavorite
from .serializers import CommentSerializer, ProductFavoriteSerializer
from .permissions import IsAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    queryset = OrganizationComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]


    def get_queryset(self):
        return OrganizationComment.objects.filter(organization=self.kwargs['organization_pk'])
    

    def create(self, request, organization_pk, *args, **kwargs):
        if type(request.data) == QueryDict:
            request.data._mutable = True
        
        request.data.update({'organization': organization_pk})
        
        return super().create(request, *args, **kwargs)
     

    def update(self, request, organization_pk, *args, **kwargs):
        # if request.data.get('organization'):
        #     raise NotAcceptable(detail='Field "organization" not available for update')

        if type(request.data) == QueryDict:
            request.data._mutable = True
        
        request.data.update({'organization': organization_pk})

        return super().update(request, *args, **kwargs)


@api_view(['GET'])
def favorites_list(request):
    if not request.user.is_authenticated:
        raise NotAuthenticated(detail='Authentication required')

    queryset = ProductFavorite.objects.filter(user=request.user)
    serializer = ProductFavoriteSerializer(queryset, many=True)

    return Response(serializer.data, status=200)
