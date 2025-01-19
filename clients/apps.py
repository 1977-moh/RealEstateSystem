from django.apps import AppConfig


class ClientsConfig(AppConfig):
    """
    إعدادات تطبيق العملاء.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clients'
    verbose_name = "Clients Management"  # اسم أكثر وضوحًا في لوحة الإدارة

    def ready(self):
        """
        يتم استدعاؤها عند تحميل التطبيق.
        يمكن استخدامها لربط الإشارات (Signals).
        """
        import clients.signals  # ربط الإشارات عند تحميل التطبيق
