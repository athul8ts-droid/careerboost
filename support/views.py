from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from .forms import SupportMessageForm, AdminReplyForm
from .models import SupportMessage


# ===============================
# USER: CONTACT ADMIN
# ===============================
@login_required
def contact_admin(request):

    # 🔒 Blocked user check
    if not request.user.is_active:
        messages.error(
            request,
            "Your account is blocked. Please contact admin via email."
        )
        return redirect("accounts:login")

    if request.method == "POST":
        form = SupportMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.save()

            messages.success(
                request,
                "Your message has been sent to admin."
            )
            return redirect("support:contact_admin")
    else:
        form = SupportMessageForm()

    return render(
        request,
        "support/contact.html",
        {"form": form}
    )


# ===============================
# USER: MY MESSAGES
# ===============================
@login_required
def my_messages(request):
    support_messages = SupportMessage.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, "support/my_messages.html", {
        "support_messages": support_messages
    })



# ===============================
# ADMIN: MESSAGE LIST
# ===============================
@staff_member_required
def admin_message_list(request):
    support_messages = SupportMessage.objects.all().order_by("-created_at")

    return render(
        request,
        "support/admin_message_list.html",
        {"support_messages": support_messages}
    )


# ===============================
# ADMIN: REPLY TO MESSAGE
# ===============================
@staff_member_required
def admin_reply(request, message_id):
    msg = get_object_or_404(SupportMessage, id=message_id)

    if request.method == "POST":
        form = AdminReplyForm(request.POST, instance=msg)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.replied_at = now()
            reply.save()

            messages.success(
                request,
                "Reply sent successfully."
            )
            return redirect("support:admin_message_list")
    else:
        form = AdminReplyForm(instance=msg)

    return render(
        request,
        "support/admin_reply.html",
        {
            "msg": msg,
            "form": form
        }
    )
