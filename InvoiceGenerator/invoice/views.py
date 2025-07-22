from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice, InvoiceItem, CompanyProfile
from decimal import Decimal

from .forms import CompanyProfileForm, EmailForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string

from .utils import send_invoice_email

from decimal import Decimal, InvalidOperation
import re

from django.db import IntegrityError


# Create your views here.

def clean_decimal(value):
    if not value:
        return Decimal('0')
    cleaned = re.sub(r'[^\d\.-]', '', value)
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return Decimal('0')


def create_invoice(request):
    if request.method == 'POST':
        invoice_number = request.POST.get('invoice_number')
        date = request.POST.get('date')
        due_date = request.POST.get('due_date')
        client_name = request.POST.get('client_name')
        client_address = request.POST.get('client_address')
        client_email = request.POST.get('client_email')
        payment_terms = request.POST.get('payment_terms')
        subtotal_raw = request.POST.get('subtotal', '0')
        tax_raw = request.POST.get('tax', '0')
        total_due_raw = request.POST.get('total_due', '0')

        subtotal = clean_decimal(subtotal_raw)
        tax = clean_decimal(tax_raw)
        total_due = clean_decimal(total_due_raw)

        # Check uniqueness of invoice_number before creating
        if Invoice.objects.filter(invoice_number=invoice_number).exists():
            messages.error(request, "Invoice number already exists. Please choose a unique number.")
            return render(request, 'main/create.html', {
                # optionally pass back entered data for user convenience
                'invoice_number': invoice_number,
                'date': date,
                'due_date': due_date,
                'client_name': client_name,
                'client_address': client_address,
                'client_email': client_email,
                'payment_terms': payment_terms,
                'subtotal': subtotal_raw,
                'tax': tax_raw,
                'total_due': total_due_raw,
            })

        try:
            invoice = Invoice.objects.create(
                invoice_number=invoice_number,
                date=date,
                due_date=due_date,
                client_name=client_name,
                client_address=client_address,
                client_email=client_email,
                payment_terms=payment_terms,
                subtotal=subtotal,
                tax=tax,
                total_due=total_due,
                author=request.user
            )
        except IntegrityError:
            messages.error(request, "Invoice number must be unique. This number is already taken.")
            return render(request, 'main/create.html')

        item_count = int(request.POST.get('item_count', 0))
        for i in range(1, item_count + 1):
            desc = request.POST.get(f'item_description_{i}')
            qty_str = request.POST.get(f'item_quantity_{i}', '0')
            unit_price_str = request.POST.get(f'item_unit_price_{i}', '0')

            try:
                qty = int(qty_str)
            except (ValueError, TypeError):
                qty = 0

            try:
                unit_price = Decimal(unit_price_str)
            except (InvalidOperation, TypeError):
                unit_price = Decimal('0')

            total = qty * unit_price

            InvoiceItem.objects.create(
                invoice=invoice,
                description=desc,
                quantity=qty,
                unit_price=unit_price,
                total=total
            )

        messages.success(request, "Invoice created successfully.")
        return redirect('home')

    return render(request, 'main/create.html')


def update_invoice(request, id):
    invoice = get_object_or_404(Invoice, id=id)

    if request.method == 'POST':
        invoice_number = request.POST.get('invoice_number')

        if Invoice.objects.filter(invoice_number=invoice_number).exclude(pk=invoice.pk).exists():
            messages.error(request, "Invoice number already exists. Please choose a unique number.")
            return render(request, 'main/update.html', {'invoice': invoice, 'items': invoice.items.all()})

        invoice.invoice_number = invoice_number
        invoice.date = request.POST.get('date')
        invoice.due_date = request.POST.get('due_date')
        invoice.client_name = request.POST.get('client_name')
        invoice.client_address = request.POST.get('client_address')
        invoice.client_email = request.POST.get('client_email')
        invoice.payment_terms = request.POST.get('payment_terms')

        try:
            invoice.subtotal = Decimal(request.POST.get('subtotal') or '0')
        except InvalidOperation:
            invoice.subtotal = Decimal('0')

        try:
            invoice.tax = Decimal(request.POST.get('tax') or '0')
        except InvalidOperation:
            invoice.tax = Decimal('0')

        try:
            invoice.total_due = Decimal(request.POST.get('total_due') or '0')
        except InvalidOperation:
            invoice.total_due = Decimal('0')

        try:
            invoice.save()
        except IntegrityError:
            messages.error(request, "Invoice number must be unique. This number is already taken.")
            return render(request, 'main/update.html', {'invoice': invoice, 'items': invoice.items.all()})

        invoice.items.all().delete()

        item_count = int(request.POST.get('item_count', 0))
        for i in range(1, item_count + 1):
            desc = request.POST.get(f'item_description_{i}', '').strip()
            qty_str = request.POST.get(f'item_quantity_{i}', '').strip()
            unit_price_str = request.POST.get(f'item_unit_price_{i}', '').strip()

            if not desc and not qty_str and not unit_price_str:
                continue

            try:
                qty = int(qty_str)
            except (ValueError, TypeError):
                qty = 0

            try:
                unit_price = Decimal(unit_price_str)
            except (InvalidOperation, TypeError):
                unit_price = Decimal('0')

            total = qty * unit_price

            InvoiceItem.objects.create(
                invoice=invoice,
                description=desc,
                quantity=qty,
                unit_price=unit_price,
                total=total
            )

        messages.success(request, "Invoice updated successfully.")
        return redirect('home')

    return render(request, 'main/update.html', {'invoice': invoice, 'items': invoice.items.all()})



def delete_invoice(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    if request.method == 'POST':
        invoice.delete()
        return redirect('home')
    return render(request, 'main/delete.html', {'invoice': invoice})



@login_required
def profile_and_company_edit(request):
    company_profile, created = CompanyProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, instance=company_profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CompanyProfileForm(instance=company_profile)

    context = {
        'form': form,
        'company_profile': company_profile,
    }
    return render(request, 'main/company_profile_form.html', context)



def download_invoice(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    company_profile, _ = CompanyProfile.objects.get_or_create(user=request.user)

    html_string = render_to_string('main/invoice_pdf.html', {
        'invoice': invoice,
        'company_profile': company_profile,
    })

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
    return response


def send_email_view(request, id):
    invoice = get_object_or_404(Invoice, id=id)

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient_email']
            send_invoice_email(invoice, recipient, request.user)
            messages.success(request, "Invoice sent successfully!")
    else:
        form = EmailForm(initial={'recipient_email': invoice.client_email})

    return render(request, 'main/send_email_form.html', {'form': form, 'invoice': invoice})