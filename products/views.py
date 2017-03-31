from django.shortcuts import render
from  django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from products.models import Product, OrderCart
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, get_object_or_404, Http404, redirect
from django.shortcuts import get_object_or_404
from products.utils import check_product_no
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


# def home_view(request):
#
#     template_name = 'home.html'
#     return render(request,template_name)
class LoginRequiredMixin(object):
	@classmethod
	def as_view(self, *args, **kwargs):
		view = super(LoginRequiredMixin, self).as_view(*args, **kwargs)
		return login_required(view)

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)



class ProductListView( ListView ):
    model = Product
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        print "in context data"
        context = super(ProductListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if not q:
            context['qs'] = None
            print "context::", context
            return context
        if q:
            qs = True
            error_msg, boolean = check_product_no(q)
            print "Error msg, boolean", error_msg, boolean
            if not boolean:
                context['error_msg'] = error_msg
        print "qs::",qs
        context['qs'] = qs
        print "context::", context

        return context

    def get_queryset(self, *args, **kwargs):
        print "in get_queryset"
        print "kwargs::", kwargs
        q = self.request.GET.get('q')
        print "QQ",q
        qs = None
        if q:
            q = q.strip()
            qs = Product.objects.filter(product_code=q)
        return qs

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
    #     instance = self.get_object()
    #     context['related_products'] = sorted(Product.objects.get_related(instance)[:6], key=lambda x:x.title)
    #     return context


class OrderCartListView(ListView):
    model = OrderCart
    template_name = "orders_list.html"

    # @method_decorator(login_required)
    def get_queryset(self, *args, **kwargs):
        print "in Order::getqueryset"
        user_id = self.request.user.id
        qs = OrderCart.objects.filter(user__id = user_id).order_by('-timestamp')
        return qs

    # @method_decorator(login_required)
    # def post(self, request, *args, **kwargs):
    #     if request.user.is_authenticated():
    #         print "In Post of OderListlView...."
    #         print "request.POST", request.POST
    #         user_id = request.POST.get('user_id')
    #         product_id = request.POST.get('product_id')
    #         product = Product.objects.get(id=product_id)
    #         user = User.objects.get(id=user_id)
    #         order_cart = OrderCart(user=user, product=product)
    #         order_cart.save()
    #         print "Order Saved!!!"
    #         return redirect('orders_list')
    #     else:
    #         return HttpResponse("Please Login First")

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        print "In GET of ordercart listview"
        if request.user.is_authenticated():
            print "In GET of OderListlView...."
            print "request.GET", request.GET
            return super(OrderCartListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponse("Please Login First")

class OrderCartDetailView(DetailView):
    model = OrderCart
    template_name = 'ordercart_detail.html'

    # @method_decorator(login_required)
    # def post(self, request, *args, **kwargs):
    #     if request.user.is_authenticated():
    #         print "In Post of OderCartDetailView...."
    #         print "request.POST", request.POST
    #         user_id = request.POST.get('user_id')
    #         product_id = request.POST.get('product_id')
    #         product = Product.objects.get(id=product_id)
    #         user = User.objects.get(id=user_id)
    #         order_cart = OrderCart(user=user, product=product)
    #         order_cart.save()
    #         print "Order Saved!!!"
    #         return redirect('orders_list')
    #     else:
    #         return HttpResponse("Please Login First")
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            print "In GET of OrderDetailView...."
            print "request.GET", request.GET
            user_id = request.user.id
            product_id = request.GET.get('product_id')
            print "product_id::", product_id
            product = Product.objects.get(id=product_id)
            user = User.objects.get(id=user_id)
            order_cart = OrderCart(user=user, product=product)
            order_cart.save()
            print "Order Saved!!!"
            return redirect('orders_list')
        else:
            return HttpResponse("Please Login First")



from easy_pdf.views import PDFTemplateView
class HelloPDFView(PDFTemplateView):
    template_name = "orders_pdf.html"

    def get_context_data(self, **kwargs):
        print "In hellopdfview::get_context_data"
        context = super(HelloPDFView, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs
        )
        user_id = self.request.user.id
        order_carts = OrderCart.objects.filter(user__id = user_id)
        context['orders'] = order_carts
        return context

