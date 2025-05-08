from django.utils.deprecation import MiddlewareMixin
from .models import Organisation
from django.conf import settings

class OrganisationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host().split(':')[0]
        base_domain = settings.BASE_DOMAIN
        domain_parts = host.split('.')
        base_parts = base_domain.split('.')

        # Check if host matches the base domain exactly
        if host == base_domain:
            # root
            request.organisation = None
            return

        # Check if it's a subdomain of the base domain
        if len(domain_parts) > len(base_parts) and domain_parts[-len(base_parts):] == base_parts:
            subdomain = '.'.join(domain_parts[:-len(base_parts)])
            try:
                request.organisation = Organisation.objects.get(subdomain=subdomain)
            except Organisation.DoesNotExist:
                request.organisation = None
            return

