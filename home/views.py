import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.views.generic import TemplateView

# ✅ إعداد سجل الأخطاء
logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    """
    ✅ عرض الصفحة الرئيسية باستخدام `TemplateView` لتبسيط الكود.
    """
    template_name = "home/index.html"

    def get(self, request, *args, **kwargs):
        """
        ✅ التحقق من وجود القالب وتسجيل أي أخطاء.
        """
        try:
            get_template(self.template_name)  # ✅ التأكد من أن القالب موجود
        except TemplateDoesNotExist:
            logger.error(f"❌ Template '{self.template_name}' not found. IP: {request.META.get('REMOTE_ADDR')}, User-Agent: {request.META.get('HTTP_USER_AGENT')}")
            return render(request, 'errors/404.html', status=404)
        except Exception as e:
            logger.error(f"❌ Unexpected error while loading template: {e}")
            return render(request, 'errors/500.html', status=500)

        return super().get(request, *args, **kwargs)
