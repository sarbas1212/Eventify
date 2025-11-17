from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking, HeroBanner,Service,ServiceType
from django.shortcuts import render, get_object_or_404
# Create your views here

def home(request):
    banners = HeroBanner.objects.filter(is_active=True).order_by('-created_at')
    services = Service.objects.all()
    return render(request, 'home.html', {'banners': banners, 'service': services})

def about(request):
    return render(request, 'about.html')
from django.shortcuts import render, get_object_or_404
from .models import Service

def services(request):
    dict_service = {
        'service': Service.objects.all()
    }
    return render(request, 'services.html', dict_service)


def service_types(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    types = service.types.all()  # ✅ Correct related_name

    context = {
        'service': service,
        'types': types,
    }
    return render(request, 'service_types.html', context)


def service_detail(request, service_id, type_id):
    service_type = get_object_or_404(ServiceType, id=type_id, service_id=service_id)
    context = {
        'service_type': service_type,
    }
    return render(request, 'service_detail.html', context)




def contact(request):
    return render(request, 'contact.html')


@login_required
def book(request):
    services = Service.objects.all()
    service_types = ServiceType.objects.all()
    if request.method == "POST":
        # Collect all booking/customer fields
        booking_data = request.POST.dict()
        # For lists/sections, you may want to grab the full multi-value lists explicitly
        for key in ['section_service', 'section_service_type', 'section_service_id', 'section_service_type_id',
                    'section_budget', 'section_date', 'section_time', 'section_notes']:
            if request.POST.getlist(key):
                booking_data[key] = request.POST.getlist(key)
        # Store booking data temporarily in session
        request.session['booking_data'] = booking_data
        return redirect('payment:payment_review')
    return render(request, "book.html", {
        "services": services,
        "service_types": service_types
    })

@login_required
def booking_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "booking_view.html", {"bookings": bookings})

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, "booking_detail.html", {"booking": booking})
