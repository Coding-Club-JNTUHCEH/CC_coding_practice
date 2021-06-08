from django.shortcuts import render


def error_404(request, exception):
        data = {}
        return render(request,'404.html', data)

def error_500(request):
        data = {}
        return render(request,'500.html', data)

def error_400(request, exception):
        data = {}
        return render(request,'400.html', data)
    
def error_403(request, exception):
        data = {}
        return render(request,'403.html', data)