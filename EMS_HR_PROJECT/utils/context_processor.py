from EMS_HR.models import empdetailModel,empcreateModel

def profile(request):
    try:
        userdetail = empdetailModel.objects.get(user_id = request.user.id)
        return {'userdetail':userdetail}
    except Exception:
        return {'userdetail':None}

def create(request):
    try:
        empdetail = empcreateModel.objects.get(user_id = request.user.id)
        return {'empdetail':empdetail}
    except Exception:
        return {'empdetail':None}