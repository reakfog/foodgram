from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework.backends import DjangoFilterBackend
from djoser import utils
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.views import TokenCreateView, TokenDestroyView
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.filters import IngredientNameFilter, RecipeFilter
from api.paginators import CustomPageNumberPaginator
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (FollowingBaseSerializer, IngredientSerializer,
                             ManageCartSerializer, ManageFavoriteSerializer,
                             RecipeReadSerializer, RecipeWriteSerializer,
                             SimpleFollowSerializer, SubscribersSerializer,
                             TagSerializer)
from api.utils import (custom_delete_author_method,
                       custom_delete_recipe_method, custom_get_method)
from recipes.models import Cart, Favorite, Following, Ingredient, Recipe, Tag
from users.models import User


class ListRetriveViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    pass


class UserViewSet(DjoserUserViewSet):
    '''
    Viewset amends standard djoser viewset in order
    to receive targeted response code 204
    '''
    http_method_names = ['get', 'post']

    @action(['post'], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": self.request.user}
            to = [get_user_email(self.request.user)]
            settings.EMAIL.password_changed_confirmation(
                self.request, context).send(to)

        if settings.LOGOUT_ON_PASSWORD_CHANGE:
            utils.logout_user(self.request)
        elif settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenCreateView(TokenCreateView):
    '''
    Viewset amends standard djoser viewset in order
    to receive targeted response code 201
    '''

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED
        )


class CustomTokenDestroyView(TokenDestroyView):
    '''
    Viewset amends standard djoser viewset in order
    to receive targeted response code 201
    '''

    def post(self, request):
        utils.logout_user(request)
        return Response(status=status.HTTP_201_CREATED)


class TagViewSet(ListRetriveViewSet):
    '''
    Viewset for Tags
    '''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny, ]
    http_method_names = ['get']


class IngredientViewSet(ListRetriveViewSet):
    '''
    Viewset for ingredirents
    '''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientNameFilter
    http_method_names = ['get']


class RecipeViewSet(viewsets.ModelViewSet):
    '''
    Viewset for viewing and managing Recipes
    '''
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    pagination_class = CustomPageNumberPaginator
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        return (
            RecipeReadSerializer
            if self.action in ['get', 'list', 'retrieve']
            else RecipeWriteSerializer
        )


class ListMyFollowingsViewSet(viewsets.ModelViewSet):
    '''
    Viewset for list of followings (subscriptions)
    '''
    serializer_class = SubscribersSerializer
    pagination_class = CustomPageNumberPaginator
    http_method_names = ['get']

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class ManageFollowingsViewSet(views.APIView):
    '''
    Viewset for adding or removing following (subscriptions) for a user
    '''
    SUCCESSFULLY_UNFOLLOWED = _(
        'You have successfully unfollowed user with ID: {}'
    )

    def get_queryset(self):
        return Following.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        return (
            FollowingBaseSerializer(*args, **kwargs) if
            self.request.method == 'GET' else
            SimpleFollowSerializer(*args, **kwargs)
        )

    def get(self, request, user_id):
        key, value = 'author', user_id
        return custom_get_method(
            request,
            self.get_serializer_class,
            key,
            value,
        )

    def delete(self, request, user_id):
        key, value = 'author', user_id
        return custom_delete_author_method(
            request,
            Following,
            self.get_serializer_class,
            key,
            value,
            self.SUCCESSFULLY_UNFOLLOWED,
        )


class ManageFavoritesViewSet(views.APIView):
    '''
    Viewset for adding or removing recipes
    to/from Favorites for a user
    '''
    RECIPE_REMOVED_FROM_FAVORITES = _(
        'Recipe with ID {} successfully removed from your favorites'
    )

    def get(self, request, recipe_id):
        key, value = 'recipe', recipe_id
        return custom_get_method(
            request,
            ManageFavoriteSerializer,
            key,
            value,
        )

    def delete(self, request, recipe_id):
        key, value = 'recipe', recipe_id
        return custom_delete_recipe_method(
            request,
            Favorite,
            ManageFavoriteSerializer,
            key,
            value,
            self.RECIPE_REMOVED_FROM_FAVORITES,
        )


class ManageCartView(views.APIView):
    '''
    Viewset for adding or removing recipes
    to/from Cart (purchase list) of a user
    '''
    RECIPE_REMOVED_FROM_CART = _(
        'Recipe with ID {} has been succefully deleted from from your cart'
    )

    def get(self, request, recipe_id):
        key, value = 'recipe', recipe_id
        return custom_get_method(
            request,
            ManageCartSerializer,
            key,
            value,
        )

    def delete(self, request, recipe_id):
        key, value = 'recipe', recipe_id
        return custom_delete_recipe_method(
            request,
            Cart,
            ManageCartSerializer,
            key,
            value,
            self.RECIPE_REMOVED_FROM_CART,
        )


class DownloadCartView(views.APIView):
    '''
    Viewset for downloading current user's cart content
    decomposed by ingredients in file in .pdf format
    '''
    DOWNLOAD_CART_PRINT_LINE = '{} ({}) - {} \n'
    EMPTY_CART_LIST = _('Cart list is empty')

    def get(self, request):
        cart = request.user.cart_holder.values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
        ).order_by('recipe__ingredients__name').annotate(
            total=Sum('recipe__portioned__amount', distinct=True)
        )

        output_list = []
        for item in cart:
            output_list.append(
                self.DOWNLOAD_CART_PRINT_LINE.format(
                    item.get('recipe__ingredients__name'),
                    item.get('recipe__ingredients__measurement_unit'),
                    item.get('total')
                )
            )

        if len(output_list) == 0:
            output_list = self.EMPTY_CART_LIST
        response = HttpResponse(output_list, 'Content-Type: application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cart.pdf"'
        return response
