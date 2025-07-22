from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from .models import CompanyProfile

def send_invoice_email(invoice, recipient_email, user):
    company_profile, _ = CompanyProfile.objects.get_or_create(user=user)
    html_string = render_to_string('main/invoice_pdf.html', {
        'invoice': invoice,
        'company_profile': company_profile,
    })
    pdf_file = HTML(string=html_string).write_pdf()
    pdf_io = BytesIO(pdf_file)
    email = EmailMessage(
        subject=f"Invoice #{invoice.invoice_number}",
        body="Dear client,\n\nPlease find attached the invoice.\n\nBest regards,\nYour Company",
        from_email="yourcompany@example.com",
        to=[recipient_email],
    )
    email.attach(f"invoice_{invoice.invoice_number}.pdf", pdf_io.getvalue(), 'application/pdf')
    email.send()
