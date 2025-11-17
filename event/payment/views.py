import random
from django.shortcuts import redirect, render
from django.utils.timezone import now
from myapp.models import Service, ServiceType, Booking
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# RAZORPAY CLIENT
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# ==============================
# PAYMENT REVIEW PAGE
# ==============================
def payment_review(request):
    booking = request.session.get('booking_data')
    if not booking:
        return redirect('book')

    sections = []
    total = 0
    section_num = 1

    # Collect all sections dynamically
    while f'service_type_{section_num}' in booking:
        service_type_id = booking.get(f'service_type_{section_num}')
        service_id = booking.get(f'service_{section_num}')
        date = booking.get(f'event_date_{section_num}')
        time = booking.get(f'event_time_{section_num}')
        notes = booking.get(f'notes_{section_num}', "")

        if service_type_id and service_id and date and time:
            st = ServiceType.objects.get(id=service_type_id)
            srv = Service.objects.get(id=service_id)

            item = {
                "service": srv.name,
                "service_type": st.name,
                "service_id": service_id,
                "service_type_id": service_type_id,
                "budget": float(st.budget or 0),
                "date": date,
                "time": time,
                "notes": notes,
            }

            total += item["budget"]
            sections.append(item)

        section_num += 1

    # Generate invoice number
    invoice_no = "BK" + str(random.randint(10000, 99999))

    # Save invoice_no inside booking_data
    booking["invoice_no"] = invoice_no
    booking["payment_type"] = "Online"  # Default for Razorpay

    # Save back
    request.session["booking_data"] = booking

    # 10% advance
    deposit_amount = round(total * 0.10, 2)

    # Create Razorpay Order
    razorpay_order = client.order.create({
        "amount": int(deposit_amount * 100),
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "customer_name": booking.get("customer_name"),
        "phone": booking.get("phone"),
        "secondary_phone": booking.get("secondary_phone"),
        "venue": booking.get("venue"),

        "sections": sections,
        "total": total,
        "deposit_amount": deposit_amount,
        "invoice_no": invoice_no,

        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount_in_paise": int(deposit_amount * 100),

        "payment_types": ["UPI", "Card", "Bank Transfer"],
        "current_date": now().date()
    }

    return render(request, "payment/payment.html", context)



# ==============================
# PAYMENT FINALIZE
# ==============================
@csrf_exempt
@csrf_exempt
def payment_finalize(request):
    if request.method != "POST":
        return redirect("payment:payment_review")
    print("🟢 POST DATA:", request.POST)


    customer_name = request.POST.get("customer_name")
    phone = request.POST.get("phone")
    secondary_phone = request.POST.get("secondary_phone")
    venue = request.POST.get("venue")
    invoice_no = request.POST.get("invoice_no")
    total_amount = request.POST.get("total_amount")
    payment_mode = request.POST.get("payment_mode")
    payment_type = request.POST.get("payment_type")

    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    sections = []
    service_list = request.POST.getlist("section_service")
    service_type_list = request.POST.getlist("section_service_type")
    service_id_list = request.POST.getlist("section_service_id")
    service_type_id_list = request.POST.getlist("section_service_type_id")
    budget_list = request.POST.getlist("section_budget")
    date_list = request.POST.getlist("section_date")
    time_list = request.POST.getlist("section_time")
    notes_list = request.POST.getlist("section_notes")

    for i in range(len(service_list)):
        sections.append({
            "service": service_list[i],
            "service_type": service_type_list[i],
            "service_id": service_id_list[i],
            "service_type_id": service_type_id_list[i],
            "budget": budget_list[i],
            "date": date_list[i],
            "time": time_list[i],
            "notes": notes_list[i],
        })

    context = {
        "invoice_no": invoice_no,
        "customer_name": customer_name,
        "phone": phone,
        "secondary_phone": secondary_phone,
        "venue": venue,
        "total_amount": total_amount,
        "payment_mode": payment_mode,
        "payment_type": payment_type,
        "razorpay_payment_id": razorpay_payment_id,
        "sections": sections,
    }

    return render(request, "payment/success.html", context)

# ==============================
# SUCCESS PAGE
# ==============================
def payment_success(request):
    return render(request, "payment/success.html", {
        "customer_name": request.session.get("customer_name"),
        "invoice_no": request.session.get("invoice_no"),
        "payment_type": request.session.get("payment_type"),
        "sections": request.session.get("sections", []),
        "total": request.session.get("total"),
        "amount_paid": request.session.get("amount_paid"),
    })


# ==============================
# FAILURE PAGE
# ==============================
def payment_failure(request):
    return render(request, "payment/failure.html")
