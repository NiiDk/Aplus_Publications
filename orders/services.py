import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def send_email(subject, recipient_list, template_name, context):
        try:
            # Inject site_url into every email context automatically
            context['site_url'] = settings.SITE_URL
            html_message = render_to_string(template_name, context)
            
            send_mail(
                subject=f"[APLUS PUBLICATIONS] {subject}",
                message="",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")

    @classmethod
    def notify_order_status_change(cls, order):
        subject = f"Order Update: {order.get_status_display()}"
        cls.send_email(
            subject=subject,
            recipient_list=[order.email],
            template_name='emails/order_status_update.html',
            context={'order': order}
        )

    @classmethod
    def alert_admin_new_order(cls, order):
        subject = "New Order Received"
        admin_emails = [admin[1] for admin in settings.ADMINS] if settings.ADMINS else [settings.DEFAULT_FROM_EMAIL]
        cls.send_email(
            subject=subject,
            recipient_list=admin_emails,
            template_name='emails/admin_new_order.html',
            context={'order': order}
        )

    @classmethod
    def alert_admin_new_quote(cls, quote):
        subject = "New Bulk Quote Request"
        admin_emails = [admin[1] for admin in settings.ADMINS] if settings.ADMINS else [settings.DEFAULT_FROM_EMAIL]
        cls.send_email(
            subject=subject,
            recipient_list=admin_emails,
            template_name='emails/admin_new_quote.html',
            context={'quote': quote}
        )

    @classmethod
    def notify_quote_status_change(cls, quote):
        subject = f"Quote Request Update: {quote.get_status_display()}"
        cls.send_email(
            subject=subject,
            recipient_list=[quote.email],
            template_name='emails/quote_status_update.html',
            context={'quote': quote}
        )
