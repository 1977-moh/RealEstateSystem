from django.apps import AppConfig


class LeadsConfig(AppConfig):
    """
    إعدادات تطبيق Leads.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leads'
    verbose_name = "Leads Management"  # اسم وصفي للتطبيق

    def ready(self):
        """
        يتم استدعاؤها عند تحميل التطبيق.
        يمكن استخدامها لربط الإشارات (signals) تلقائيًا.
        """
        import leads.signals  # استيراد إشارات التطبيق
