from django.conf import settings


def project_name_processor(request):

    return {"project_name": settings.PROJECT_NAME}
