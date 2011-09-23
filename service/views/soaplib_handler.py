


from django.http import HttpResponse


class DjangoSoapApp():

    def __call__(self, request):
        django_response = HttpResponse()
        def start_response(status, headers):
            status, reason = status.split(' ', 1)
            django_response.status_code = int(status)
            for header, value in headers:
                django_response[header] = value
        response = super(SimpleWSGISoapApp, self).__call__(request.META, start_response)
        django_response.content = "\n".join(response)

        return django_response


