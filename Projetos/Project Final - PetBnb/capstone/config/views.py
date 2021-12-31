from django.conf import settings
from django.shortcuts import render
# import logging

# logging.basicConfig(
#     handlers=[logging.FileHandler(filename=settings.BASE_DIR / 'logging/handler.log', encoding='utf-8', mode='a+')],
#     format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%D %T', level=logging.INFO)


def handler(fun):
    def response(request, *args, **kwargs):
        exception = str()
        if 'exception' in kwargs:
            exception = kwargs['exception']
        #logging.error(f'{fun.__name__} {exception}')
        return fun(request, *args, **kwargs)

    return response


@handler
def handler400(request, *args, **kwargs):
    template = settings.BASE_DIR / 'templates/error/err_400.html'
    context = {
        'exception': kwargs['exception']
    }
    return render(request, template, context)


@handler
def handler403(request, *args, **kwargs):
    template = settings.BASE_DIR / 'templates/error/err_403.html'
    context = {
        'exception': kwargs['exception']
    }
    return render(request, template, context)


@handler
def handler404(request, *args, **kwargs):
    template = settings.BASE_DIR / 'templates/error/err_404.html'
    context = {
        'exception': kwargs['exception']
    }
    return render(request, template, context)


@handler
def handler500(request, *args, **kwargs):
    template = settings.BASE_DIR / 'templates/error/err_500.html'
    context = {}
    return render(request, template, context)
