from django.conf import settings
# Import Payu from Paywix
import hashlib
from django.views.decorators.csrf import csrf_exempt
from paywix.payu import Payu
#random to generate transaction id unique one randomly
import random
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.views import View
from . forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from . models import Customer,Medicine,Cart
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import Q


def Homepage(request):
    return render(request,'home.html')

def Contactuspage(request):
    return render(request,'contactus.html')

def Orderplaced(request):
    return render(request,'orderplaced.html')


def Loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass1')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('profile')
        else:
            messages.warning(request,"Invalid Username or Password login failed!!!")
    return render(request,'login2.html')


class CustomerRegistrationview(View):
   def get(self,request):
       form=CustomerRegistrationForm()
       return render(request,'customerRegistration.html',locals())
   
   def post(self,request):
       form=CustomerRegistrationForm(request.POST)
       if form.is_valid():
           form.save()
           messages.success(request,"Congratulations! User Register Successfully...")
       else:
           messages.warning(request," Invalid Input data -Register failed!!!")
       return render(request,'customerRegistration.html',locals())

class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm
        return render(request,'profile.html',locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            
            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! profile saved successfully...")
        else:
            messages.warning(request,"Invalid input data")
        return render(request,'profile.html',locals())
    
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,'updateaddress.html',locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! profile Updated successfully...")
        else:
            messages.warning(request,"Invalid input data")
        return redirect("address")
            
def senddata(request):
    with open(r'C:\Users\rakesh\Desktop\demo\proj\newdata.json') as file:
        json_data = json.load(file)
        for item in json_data:
            model_instance = Medicine(id=item['id'],name=item['name'],dosage=item['dosage'],description=item['description'],price=item['price'] if item['price'] else 'Rs.200',image=item['image'],disease=item['disease'])
            model_instance.save()
    return HttpResponse('DATA SAVED')

class CategoryView(View):
    def get(self,request,val):
        medicine=Medicine.objects.filter(disease=val)
        name=Medicine.objects.filter(disease=val).values('name')
        return render(request,"category.html",locals())

class MedicineDetail(View):
    def get(self,request,pk):
        medicine=Medicine.objects.get(pk=pk)
        return render(request,"medicinedetail.html",locals())
    
def add_to_cart(request):
   user=request.user
   if request.user.is_authenticated:
        medicine_id=request.GET.get('med_id')
        medicine=Medicine.objects.get(id=medicine_id)
        Cart(user=user,medicine=medicine).save()
        return redirect("/cart")
   else:
        return redirect("login")
     
       
def show_cart(request):
    user=request.user
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*int(p.medicine.price.replace("Rs.", "")) #replace this with p.medicine.price later
            amount=amount+value
        totalamount=amount+40
        return render(request,'addtocart.html',locals())
    else:
        return redirect("login")

def plus_cart(request):
    if request.method=='GET':
        med_id=request.GET['med_id']
        c=Cart.objects.get(Q(medicine=med_id)&Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*int(p.medicine.price.replace("Rs.", "")) #replace this with p.medicine.price later
            amount=amount+value
        totalamount=amount+40
        data={ 
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)
    

def minus_cart(request):
    if request.method=='GET':
        med_id=request.GET['med_id']
        c=Cart.objects.get(Q(medicine=med_id)&Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*int(p.medicine.price.replace("Rs.", ""))#replace this with p.medicine.price later
            amount=amount+value
        totalamount=amount+40
        data={ 
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method=='GET':
        med_id=request.GET['med_id']
        c=Cart.objects.get(Q(medicine=med_id)&Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*int(p.medicine.price.replace("Rs.", ""))
            amount=amount+value
        totalamount=amount+40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value=p.quantity*int(p.medicine.price.replace("Rs.", ""))
            famount=famount + value
        totalamount=famount + 40
        cart=Cart.objects.filter(user=user)
        return render(request,'checkout.html',locals())
    

payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

# Create Payu Object for making transaction
# The given arguments are mandatory
payu = Payu(merchant_key,merchant_salt, mode)
# Create your views here.

def generate_hash(data,key, salt):
    hash_string = '|'.join([
        key,
        str(data['txnid']),
        str(data['amount']),
        data['productinfo'],
        data['firstname'],
        data['email'],
        data.get('udf1', ''),
        data.get('udf2', ''),
        data.get('udf3', ''),
        data.get('udf4', ''),
        data.get('udf5', ''),
        '', '', '', '', '', '', '', '', '', '', '', '', '',
        salt
    ])
    return hashlib.sha512(hash_string.encode('utf-8')).hexdigest()

def backhomepage(request):
    if not request.user.is_authenticated:
        return redirect('Homepage')
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    famount=0
    for p in cart_items:
        value=p.quantity*int(p.medicine.price.replace("Rs.", ""))
        famount=famount + value
    totalamount=famount + 40
    cart=Cart.objects.filter(user=user)
    for c in cart:
        c.delete();
    return redirect('Homepage')

def payu_demo(request):
    user = request.user
    
    # Check if user is authenticated
    if not user.is_authenticated:
        return redirect('Homepage')  # Redirect to homepage if not authenticated

    # Fetch the customer's details
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        customer = None  # Handle case where customer record doesn't exist

    cart_items = Cart.objects.filter(user=user)
    famount = 0
    product_names = [] 

    # Calculate total amount
    for p in cart_items:
        value = p.quantity * int(p.medicine.price.replace("Rs.", ""))
        famount += value
        product_names.append(f"{p.medicine.name} (x{p.quantity})")
    
    totalamount = famount + 40  # Add any additional fees
    totalamount = int(totalamount)

    # Prepare data for payment processing
    data = {
        'amount': totalamount,
        'firstname': customer.name if customer else 'Guest',  # Default to 'Guest' if no customer
        'email': user.email,  # Use user's email
        'phone': customer.mobile if customer else '0000000000',  # Default phone if no customer
        'productinfo': ', '.join(product_names),
        'lastname': '',  # You can set a default or leave it empty
        'address1': customer.locality if customer else '',  # Locality as address1
        'address2': '',  # Set as needed
        'city': customer.city if customer else '',
        'state': customer.state if customer else '',
        'country': 'India',  # Static value, change as necessary
        'zipcode': customer.zipcode if customer else '000000',
          'udf1': '', 
            'udf2': '', 'udf3': '', 'udf4': '', 'udf5': '',
            'surl': surl,
            'furl': furl,
        }
     
    data.update({"txnid": random.randint(8888888888, 9999999999999)})
    data['hash'] = generate_hash(data,merchant_key, merchant_salt)
    payu_data = payu.transaction(**data)
    return render(request, 'payu_checkout.html', {"posted": payu_data})
    

@csrf_exempt
def payu_success(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.check_transaction(**data)
    return render(request,'success.html')

@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.check_transaction(**data)
    return render(request,'failure.html')
       
        
    

    
