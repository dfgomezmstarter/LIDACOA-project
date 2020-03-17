from ..configuracion import *

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')