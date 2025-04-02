from django.utils.deprecation import MiddlewareMixin
from .models import Organisation

class OrganisationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host().split(':')[0]
        print(host)
        try:
            request.organisation = Organisation.objects.get(domain=host)
        except Organisation.DoesNotExist:
            request.organisation = None 
