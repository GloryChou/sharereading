from django.shortcuts import render_to_response


def authentic(request):
    if request.session.get('user') is None:
        return False
    else:
        return True