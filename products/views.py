from queue import Empty
from django.shortcuts import redirect, render

from adminAndSellers.models import Seller
from .models import Product, Order
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from slugify import slugify

# Create your views here.
def home(request):
    Electronics=Product.objects.filter(noofsales=False).filter(tag="Electronics")
    Clothing=Product.objects.filter(noofsales=False).filter(tag="Clothing")
    Vehicle=Product.objects.filter(noofsales=False).filter(tag="Vehicle")
    Education=Product.objects.filter(noofsales=False).filter(tag="Education")

    return render(request, 'home.html', {"Electronics":Electronics, "Clothing":Clothing, "Vehicle":Vehicle, "Education":Education})

def seller_product(request, slug):
    products=Product.objects.filter(seller_linked_user=slug)
    sellers=Product.objects.filter(seller_linked_user=slug)[0:1]
    
    seller="False"
    if(sellers):
        seller=sellers[0].seller

    return render(request, 'seller.html', {"products":products, "seller":seller})

def your_products(request):
    seller=request.user.seller
    products=Product.objects.filter(seller=seller)
    if(products.exists()):
        return render(request, 'yourproducts.html',{"products":products,"noproducts":"false"})
    else:
        return render(request, 'yourproducts.html',{"noproducts":"true"})

def order_info(request, orderID):
    info=Order.objects.get(orderNumber=orderID)
    if(request.user.seller==info.seller):
        cinfo=User.objects.get(username=info.customer)
        product=Product.objects.get(slug=info.slug)
        return render(request, 'order-info.html', {'orderinfo':info, "customerinfo":cinfo, "product":product})
    else:
        return redirect('/page-not-found')

def add_product(request):
    if (request.method=='POST'):
        title=request.POST['title']
        tag=request.POST['tag']
        description=request.POST['description']
        price=request.POST['price']
        image=request.FILES['image']
        seller=request.user.seller
        seller_linked_user = request.user.seller.user_linked
        slug=slugify(str(seller.shop_name)+" "+str(title))
        fs = FileSystemStorage()
        img = fs.save("uploads/"+str(image.name), image)

        Product.objects.create(seller=seller, seller_linked_user= seller_linked_user, title=title, tag=tag, slug=slug, description=description, price=price,image=img)

        return redirect('/your-products')

    else:
        return render(request, 'add-product.html')
    
def buy_product(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'buy-product.html', {"product":product})

def edit_product(request, slug):
    product = Product.objects.get(slug=slug)
    if(request.method=='POST'):
        title=request.POST['title']
        description=request.POST['description']
        price=request.POST['price']
        seller=request.user.seller
        slug=slugify(str(seller.shop_name)+" "+str(title))
        changeimg = request.POST['changeimg']

        if(changeimg=="true"):
            fs = FileSystemStorage()
            fs.delete(str(product.image))

            image=request.FILES['image']
            fs = FileSystemStorage()
            img = fs.save("uploads/"+str(image.name), image)

            product.title=title
            product.slug=slug
            product.description=description
            product.price=price
            product.image=img
            product.save()
            return redirect('/your-products')
        
        else:
            product.title=title
            product.slug=slug
            product.description=description
            product.price=price
            product.save()
            return redirect('/your-products')

    else:
        return render(request, 'edit-product.html', {"product":product})

def order_product(request, slug):
    product = Product.objects.get(slug=slug)
    if(request.user.is_authenticated):
        if(request.method=='POST'):
            seller = product.seller
            customer = request.user
            title = product.title
            contactNumber = request.POST['contactnumber']
            price = product.price
            order = Order.objects.create(seller=seller, customer=customer, slug=slug, title=title, contactNumber=contactNumber, price=price, image=product.image.url)
            ordernumber = order.orderNumber
            return redirect("/order-success/"+str(ordernumber)+"/delivery")

        else:
            return render(request, 'place-order.html', {"product":product})
    else:
        return redirect('/login')

def mark_as_delivered(request, slug):
    order = Order.objects.get(orderNumber=slug)
    pslug=order.slug
    product=Product.objects.get(slug=pslug)
    product.noofsales = True
    product.save()

    order.delivery_status = "delivered"
    order.save()
    return redirect('/seller-orders')

def mark_as_cancelled(request, slug):
    order = Order.objects.get(orderNumber=slug)
    order.delivery_status = "cancelled"
    order.save()
    return redirect('/seller-orders')

def order_success(request, slug, type):
    orderno = Order.objects.get(orderNumber=slug).customer
    if(orderno==request.user):
        return render(request, 'order.html', {"order":slug, "type": type})
    
    else:
        return redirect('/page-not-found')

def seller_orders(request):
    seller=request.user.seller
    orders=Order.objects.filter(seller=seller)
    return render(request, 'orders.html', {"orders":orders})

def my_orders(request):
    customer = request.user
    orders=Order.objects.filter(customer=customer)
    return render(request, 'my-orders.html', {"orders":orders})

def delete_product(request, slug):
    product = Product.objects.get(slug=slug)
    productimage = product.image
    fs = FileSystemStorage()
    fs.delete(str(productimage))
    product.delete()
    return redirect('/your-products')

def invalid_request(request):
    return render(request, '404.html')

def page_not_found(request, exception):
    return render(request, '404.html')