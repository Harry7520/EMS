from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required ,permission_required
from EMS_HR.models import empcreateModel,genderModel,positionModel,empdetailModel,commentModel,leaveModel,resModel,projectModel,updateModel,User
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def custom_404_view(request):
    return render(request,'404.html')

def to_login(request):
    return redirect('login')

def login_view(request):
    if request.method == "GET":
        return render(request , 'login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dash')
            # return redirect(f'/ems/dashboard/{user.id}')         
        else:
            return redirect('login')
            
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    project = projectModel.objects.all()
    res = resModel.objects.all()
    leave = leaveModel.objects.all()
    empcreates = empcreateModel.objects.all()
    return render(request,"dashboard.html",{'empcreates':empcreates,'res':res,'leave':leave,'project':project})

@permission_required('EMS_HR.add_empcreatemodel', login_url='login')
def emp_create(request):
    if request.method == "GET":
        empcreate = empcreateModel.objects.all()
        user = User.objects.all()
        gender = genderModel.objects.all()
        position = positionModel.objects.all()
        return render(request,'emp_create.html',{'gender':gender,'position':position,'user':user})
    if request.method == "POST":
        try:
            empcreates = empcreateModel.objects.create(
                user_id = request.POST.get('employee'),
                phone = request.POST.get('phone'),
                salary = request.POST.get('salary'),
                gender_id = request.POST.get('gender'),
                position_id = request.POST.get('position'),
                image = request.FILES.get('image'),
                create_at = datetime.now(),
            )
            empcreates.save()
            messages.success(request, "Employee has been employed successfully.")
            return redirect('emp_view')
        except Exception as e:
            messages.error(request, "Employee has been already existed!")
            return redirect('emp_create')

@permission_required('EMS_HR.view_empcreatemodel', login_url='login')
def emp_view(request):
    empcreates = empcreateModel.objects.all().order_by('-create_at')
    paginator = Paginator(empcreates, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'emp_view.html', {"empcreates":page_obj})

@permission_required('EMS_HR.view_empcreatemodel', login_url='login')
def search_by(request):
    search = request.GET.get('search')
    if search:
        empcreates = empcreateModel.objects.filter(
            Q(id__icontains=search)
        )
        return render(request, 'emp_view.html', {'empcreates': empcreates})
    else:
        empcreates = empcreateModel.objects.all().order_by('-create_at')
        return render(request, 'emp_view.html', {'empcreates': empcreates})

@permission_required('EMS_HR.delete_empcreatemodel', login_url='login')
def emp_delete(request, post_id):
    empcreates = empcreateModel.objects.get(id=post_id)
    empcreates.image.delete()
    empcreates.delete()
    messages.info(request, "Employee has been deleted successfully.")
    return redirect('emp_view')

@permission_required('EMS_HR.view_empcreatemodel', login_url='login')
def emp_detail(request, post_id):
    empcreates = empcreateModel.objects.get(id=post_id)
    return render(request,'emp_detail.html',{'empcreates':empcreates})

@permission_required('EMS_HR.change_empcreatemodel', login_url='login')
def emp_update(request, post_id):
    if request.method == "GET":
        gender = genderModel.objects.all()
        position = positionModel.objects.all()
        empcreates = empcreateModel.objects.get(id=post_id)
        return render(request, "emp_update.html",{'empcreates':empcreates,'gender':gender,'position':position})
    if request.method == "POST":
        empcreates = empcreateModel.objects.get(id=post_id)
        empcreates.phone = request.POST.get('phone')
        empcreates.salary = request.POST.get('salary')
        empcreates.gender_id = request.POST.get('gender')
        empcreates.position_id = request.POST.get('position')
        if request.FILES.get('image'):
            empcreates.image.delete()
            empcreates.image = request.FILES.get('image')
        empcreates.save()
        messages.success(request,"Employee has been updated successfully.")
        return redirect('emp_view')

@permission_required('EMS_HR.change_empdetailmodel', login_url='login')
def profile_upload(request,user_id):
    if request.method == "GET":
        empdetails = empdetailModel.objects.get(user_id = user_id)
        empdetails.birthday = empdetails.birthday.strftime('%Y-%m-%d')
        return render(request, 'profile_upload.html',{'empdetails':empdetails})
    if request.method == "POST":
        empdetails = empdetailModel.objects.get(user_id = user_id)
        empdetails.name = request.POST.get('name')
        empdetails.address = request.POST.get('address')
        empdetails.birthday = request.POST.get('birthday')
        if request.FILES.get('image'):
            empdetails.image.delete()
            empdetails.image = request.FILES.get('image')
        empdetails.save()
        messages.success(request, "Profile upload Success")
        return redirect('dash')

@permission_required('EMS_HR.view_empdetailmodel', login_url='login')
def profile(request, user_id):
    try:
        empdetails = empdetailModel.objects.get(user_id=user_id)
        return render(request,'profile.html',{'empdetails':empdetails})
    except Exception as e:
        messages.error(request, "Profile has not been created!")
        return redirect('prof_create')

@permission_required('EMS_HR.add_empdetailmodel', login_url='login')
def profile_create(request):
    if request.method == "GET":
        try:
            empCheck = empdetailModel.objects.get(user_id=request.user.id)
            return redirect(f'/ems/profile/{request.user.id}')
        except Exception:
            return render(request, "profile_create.html")
    if request.method == "POST":
        try:
            empdetails = empdetailModel.objects.create(
                name = request.POST.get('name'),
                address = request.POST.get('address'),
                image = request.FILES.get('image'),
                birthday = request.POST.get('birthday'),
                user_id = request.user.id,
            )
            empdetails.save()
            messages.success(request, "Profile has been created successfully.")
            return redirect('dash')
        except Exception as e:
            messages.error(request, "Profile has been already created!")
            return redirect('prof_create')

@permission_required('EMS_HR.add_commentmodel', login_url='login')
def mail(request):
    if request.method == "GET":
        mail = commentModel.objects.all()
        return render(request,"mail.html",{'mail':mail})
    if request.method == "POST":
        mail = commentModel.objects.create(
            content = request.POST.get('content'),
            author_id = request.user.id,
            create_at = datetime.now(),
        )
        mail.save()
        return redirect('mail')

@permission_required('EMS_HR.delete_commentmodel', login_url='login')
def mail_delete(request,post_id):
    mail = commentModel.objects.get(id=post_id)
    mail.delete()
    return redirect('mail')

@permission_required('EMS_HR.add_leavemodel', login_url='login')
def leave_create(request):
    if request.method == "GET":
        leave = leaveModel.objects.all().order_by('-create_at')
        return render(request,'leave_create.html',{'leave':leave})
    if request.method == "POST":
        leave = leaveModel.objects.create(
            empid = request.POST.get('empid'),
            name = request.POST.get('name'),
            start_date = request.POST.get('start_date'),
            end_date = request.POST.get('end_date'),
            description = request.POST.get('description'),
            author_id = request.user.id,
            create_at = datetime.now(),
        )
        leave.save()
        messages.success(request, "Leave-report has been reported.")
        return redirect('/ems/leave/create/#leave')

@permission_required('EMS_HR.add_resmodel', login_url='login')
def res_create(request):
    if request.method == "GET":
        res = resModel.objects.all().order_by('-create_at')
        position = positionModel.objects.all()
        return render(request,'res_create.html',{'position':position,'res':res})
    if request.method == "POST":
        res = resModel.objects.create(
            empid = request.POST.get('empid'),
            name = request.POST.get('name'),
            position_id = request.POST.get('position'),
            description = request.POST.get('description'),
            author_id = request.user.id,
            create_at = datetime.now(),
        )
        res.save()
        messages.success(request, "Resignation-report has been reported.")
        return redirect('/ems/res/create/#res')

@permission_required('EMS_HR.view_leavemodel', login_url='login')
def leave_view(request):
    leave = leaveModel.objects.all().order_by('-create_at')
    paginator = Paginator(leave, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'leave_view.html', {"leave":page_obj})

@permission_required('EMS_HR.view_resmodel', login_url='login')
def res_view(request):
    res = resModel.objects.all().order_by('-create_at')
    paginator = Paginator(res, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'res_view.html', {"res":page_obj})

@permission_required('EMS_HR.view_leavemodel', login_url='login')
def search_by1(request):
    search = request.GET.get('search')
    if search:
        leave = leaveModel.objects.filter(
            Q(empid__icontains=search) |
            Q(name__icontains=search)
        )
        return render(request, 'leave_view.html', {'leave': leave})
    else:
        leave = leaveModel.objects.all().order_by('-create_at')
        return render(request, 'leave_view.html', {'leave': leave})

@permission_required('EMS_HR.view_resmodel', login_url='login')
def search_by2(request):
    search = request.GET.get('search')
    if search:
        res = resModel.objects.filter(
            Q(empid__icontains=search) |
            Q(name__icontains=search)
        )
        return render(request, 'res_view.html', {'res': res})
    else:
        res = resModel.objects.all().order_by('-create_at')
        return render(request, 'res_view.html', {'res': res})

@permission_required('EMS_HR.view_leavemodel', login_url='login')
def leave_approve(request,id):
    leave = leaveModel.objects.get(id = id)
    leave.status = 'approve'
    leave.save()
    messages.success(request,"Leave-report has been approved")
    return redirect('leave_view')

@permission_required('EMS_HR.view_leavemodel', login_url='login')
def leave_reject(request,id):
    leave = leaveModel.objects.get(id = id)
    leave.status = 'reject'
    leave.save()
    messages.error(request,"Leave-report has been rejected")
    return redirect('leave_view')

@permission_required('EMS_HR.view_resmodel', login_url='login')
def res_approve(request,id):
    res = resModel.objects.get(id = id)
    res.status = 'approve'
    res.save()
    messages.success(request,"Resignation-report has been approved")
    return redirect('res_view')

@permission_required('EMS_HR.view_resmodel', login_url='login')
def res_reject(request,id):
    res = resModel.objects.get(id = id)
    res.status = 'reject'
    res.save()
    messages.error(request,"Resignation-report has been rejected")
    return redirect('res_view')

@permission_required('EMS_HR.view_leavemodel', login_url='login')
def leave_detail(request,post_id):
    leave = leaveModel.objects.get(id=post_id)
    return render(request,'leave_detail.html',{'leave':leave})
    
@permission_required('EMS_HR.delete_leavemodel', login_url='login')
def leave_delete(request,post_id):
    leave = leaveModel.objects.get(id=post_id)
    leave.delete()
    messages.info(request, "Leave-report has been deleted successfully.")
    return redirect('leave_view')

@permission_required('EMS_HR.view_resmodel', login_url='login')
def res_detail(request,post_id):
    res = resModel.objects.get(id=post_id)
    return render(request,'res_detail.html',{'res':res})

@permission_required('EMS_HR.delete_resmodel', login_url='login')
def res_delete(request,post_id):
    res = resModel.objects.get(id=post_id)
    res.delete()
    messages.info(request, "Resignation-report has been deleted successfully.")
    return redirect('res_view')

@permission_required('EMS_HR.add_projectmodel', login_url='login')
def proj_create(request):
    if request.method == "GET":
        return render(request,'proj_create.html')
    if request.method == "POST":
        project = projectModel.objects.create(
            client = request.POST.get('client'),
            title = request.POST.get('title'),
            partner = request.POST.get('partner'),
            description = request.POST.get('description'),
            deadline = request.POST.get('deadline'),
            cost = request.POST.get('cost'),
            create_at = datetime.now(),
        )
        project.save()
        messages.success(request, "Project has been created successfully.")
        return redirect('proj_view')

@permission_required('EMS_HR.view_projectmodel', login_url='login')
def proj_view(request):
    project = projectModel.objects.all().order_by('-create_at')
    paginator = Paginator(project, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'proj_view.html', {"project":page_obj})

@permission_required('EMS_HR.view_projectmodel', login_url='login')
def search_by3(request):
    search = request.GET.get('search')
    if search:
        project = projectModel.objects.filter(
            Q(title__icontains=search)
        )
        return render(request, 'proj_view.html', {'project': project})
    else:
        project = projectModel.objects.all().order_by('-create_at')
        return render(request, 'proj_view.html', {'project': project})

@permission_required('EMS_HR.delete_projectmodel', login_url='login')
def Proj_delete(request,post_id):
    project = projectModel.objects.get(id=post_id)
    project.delete()
    messages.info(request, "Project has been deleted successfully.")
    return redirect('proj_view')

@permission_required('EMS_HR.view_projectmodel', login_url='login')
def proj_detail(request,post_id):
    project = projectModel.objects.get(id=post_id)
    return render(request,'proj_detail.html',{'project':project})

@permission_required('EMS_HR.add_updatemodel', login_url='login')
def proj_dev_create(request,post_id):
    if request.method =="GET":
        project = projectModel.objects.get(id=post_id)
        update = updateModel.objects.filter(post_id=post_id).order_by('-create_at')
        paginator = Paginator(update, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,"proj_dev.html",{'project':project,'update':page_obj})
    if request.method == "POST":
        update = updateModel.objects.create(
            division = request.POST.get('division'),
            progress = request.POST.get('progress'),
            image = request.FILES.get('image'),
            post_id = post_id,
            author_id = request.user.id,
            create_at = datetime.now(),
        )
        update.save()
        messages.success(request,"You have been updated successfully!")
        return redirect(f'/ems/proj/dev/create/{post_id}')

@permission_required('EMS_HR.view_projectmodel', login_url='login')
def proj_finish(request,id):
    project = projectModel.objects.get(id = id)
    project.status = 'finished'
    project.save()
    messages.success(request,"Project has been finished")
    return redirect('proj_view')

@permission_required('EMS_HR.change_updatemodel', login_url='login')
def proj_edit(request,proj_id,post_id):
    if request.method == "GET":
        update = updateModel.objects.get(id=proj_id)
        project = projectModel.objects.get(id=post_id)
        return render(request, "proj_edit.html", {"update":update,"project":project})
    if request.method == "POST":
        update = updateModel.objects.get(id=proj_id)
        update.division = request.POST.get('division')
        update.progress = request.POST.get('progress')
        if request.FILES.get('image'):
            update.image.delete()
            update.image = request.FILES.get('image')
        update.save()
        messages.success(request, "Progress has been edited successfully")
        return redirect(f'/ems/proj/dev/create/{post_id}')

@permission_required('EMS_HR.delete_updatemodel', login_url='login')
def proj_delete(request,proj_id,post_id):
    update = updateModel.objects.get(id=proj_id)
    update.image.delete()
    update.delete()
    messages.info(request, "Progress has been deleted successfully.")
    return redirect(f'/ems/proj/dev/create/{post_id}')

# def Sample(request):
#     all_user = User.objects.all()
#     nhave_user = []
#     for u in all_user:
#         try:
#             Employee.objects.filter(user=u.name)
#         except Exception:
#             nhave_user.append(u)
#     return render(request, 'templete', {'nhave_user':nhave_user})