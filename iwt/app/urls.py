
from . import views
from django.urls import path
from django.contrib.auth import views as auth_view
from . forms import LoginForm,MyPasswordChangeForm



urlpatterns = [
    path('',views.Homepage,name='home'),
    path('login/',views.Loginpage,name='login'),
    path('contactus/',views.Contactuspage,name='contactus'),
    path('registeration/',views.CustomerRegistrationview.as_view(),name='customerregistration'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('updateaddress/<int:pk>',views.updateAddress.as_view(),name='updateaddress'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='changepassword.html', form_class=MyPasswordChangeForm, success_url='passwordchangedone'),name='passwordchange'),
    path('passwordchange/passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),


    path("category/<slug:val>",views.CategoryView.as_view(),name="category"),
    path("medicine-detail/<int:pk>",views.MedicineDetail.as_view(),name="medicine-detail"),
    path('senddata/',views.senddata,name='senddata'),

    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('checkout/',views.checkout.as_view(),name='checkout'),
    path('orderplaced',views.Orderplaced,name='orderplaced'),
  

    path('backhomepage/',views.backhomepage,name='backhomepage'),
    path('payu_demo',views.payu_demo,name='payu_demo'),
    path('success',views.payu_success,name='payu_success'),
    path('failure',views.payu_failure,name='payu_failure'),
    
]