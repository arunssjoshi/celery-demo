from celery import shared_task


@shared_task(queue="email_queue")
def send_email_task(to_email, subject, message):
    # Logic for sending an email
    print("sending .... email")
    return f"SMS sent to {to_email}"
    pass


@shared_task(queue="sms_queue")
def send_sms(to, message):
    # Logic to send an SMS
    return f"SMS sent to {to}"


@shared_task(queue="whatsapp_queue")
def send_whatsapp(to, message):
    # Logic to send a WhatsApp message
    return f"WhatsApp message sent to {to}"
