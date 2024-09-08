from django.urls import path
from .views.cat_views import CreateCatagorey,CategoryList,CategoryDetail
from .views.item_views import ItemCreate,ItemDetail,ItemList 
from .views.modG_views import GroupModifierCreate,ModifierGroupList,ModifierGroupDetail
from .views.mod_views import ModifierCreate,ModifierList,ModifierDetail

urlpatterns = [
    path('create/category/', CreateCatagorey.as_view(), name='category-create'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),

    path('create/item/',ItemCreate.as_view(), name='item-add'),
    path('items/', ItemList.as_view(), name='item-list'),
    path('item/<int:pk>/', ItemDetail.as_view(), name='item-detail'),


    path('create/modifiers-group/', GroupModifierCreate.as_view(), name='modifier-create'),
    path('modifier-groups/', ModifierGroupList.as_view(), name='modifier-group-list'),
    path('modifier-group/<int:pk>/', ModifierGroupDetail.as_view(), name='modifier-group-detail'),


    path('create/modifiers/', ModifierCreate.as_view(), name='modifier-create'),
    path('modifiers/', ModifierList.as_view(), name='modifier-list'),
    path('modifiers/<int:pk>/', ModifierDetail.as_view(), name='modifier-detail'),
   


 
]