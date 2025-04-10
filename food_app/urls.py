from django.urls import path
from .views import home, manage_items, new_order, place_order,view_order, add_item, edit_item, delete_item

urlpatterns = [
    path('', home, name='home'),
    path('manage-items/', manage_items, name='manage_items'),
    path('add-item/', add_item, name='add_item'),  # ✅ Add this line
    path('edit-item/<int:item_id>/', edit_item, name='edit_item'),
    path('delete-item/<int:item_id>/', delete_item, name='delete_item'),
    path('new-order/', new_order, name='new_order'),
    path('place-order/', place_order, name='place_order'),
    path('view-order/<int:order_id>/', view_order, name='view_order'),

]

