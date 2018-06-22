from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from web.models import Alumnum, Chapter, House


def get_chapters():
    return [c.name for c in Chapter.objects.all()]

def get_houses():
    return [h.name for h in House.objects.all()]

def get_exam_types():
    return ["O'Level", "A'Level", "SSSCE", "WASSCE", ]


def clean_registration_form(request, all=False):
    res = {}
    res['first_name'] =request.POST['first_name'].strip()
    res['last_name'] = request.POST['last_name'].strip()
    res['email'] = request.POST['email'].strip()
    res['year_of_completion'] = request.POST['year_of_completion']
    res['house'] = request.POST['house']

    if all:
        res['exam_type'] = request.POST['exam_type']
        res['chapter'] = request.POST['chapter']
        res['profession'] = request.POST['profession']
        res['phone_1'] = request.POST['phone_1']
        res['phone_2'] = request.POST['phone_2']
        res['address_line_1'] = request.POST['addr_line_1']
        res['address_line_2'] = request.POST['addr_line_2']
        res['whatsapp'] = request.POST['whatsapp']
        res['twitter'] = request.POST['twitter']
        res['facebook'] = request.POST['facebook']
        res['instagram'] = request.POST['instagram']
        res['ref_1_name'] = request.POST['ref_1_n'].strip()
        res['ref_1_y'] = request.POST['ref_1_y'].strip()
        res['ref_1_h'] = request.POST['ref_1_h'].strip()
        res['ref_2_name'] = request.POST['ref_2_n'].strip()
        res['ref_2_y'] = request.POST['ref_2_y'].strip()
        res['ref_2_h'] = request.POST['ref_2_h'].strip()
        res['password'] = request.POST['password']

    return res


def home(request):

    #TODO the years and house name list

    context = {}
    error = False

    context['first_name'] = ""
    context['last_name'] = ""
    context['email'] = ""

    if request.method == "POST":
        # check for the important stuffs
        context.update(clean_registration_form(request, False))

        if not len(context['first_name']) or not len(context['last_name']):
            context['error'] = "Please provide your full name"
            error = True

        if not len(context['email']):
            context['error'] = "Please provide an email"
            error = True

        if not error:
            return redirect('/register/?f=%s&l=%s&e=%s&y=%s&h=%s' %
                            (context['first_name'],
                             context['last_name'], 
                             context['email'],
                             context['year_of_completion'],
                             context['house'], ))
    return render(request, "web/index.html", context)


def register(request):
    context = {
        "first_name": request.GET.get('f', ''),
        "last_name": request.GET.get('l', ''),
        "year_of_completion": request.GET.get('y', ''),
        "house": request.GET.get('y', ''),
        "email": request.GET.get('e', ''),
        "exam_type": get_exam_types()[0],
        "chapters": get_chapters(),
        "houses": get_houses(),
        "exam_types": get_exam_types()
    }

    error = False

    if request.method == 'POST':
        # validation
        clean_data = clean_registration_form(request, True)
        context.update(clean_data)

        if not len(context['password']) > 7:
            context['error'] = "Password should be more than 7 characters long.ß"
            error = True

        if not len(context['ref_2_name']) or not len(context['ref_2_y']) or not len(context['ref_2_h']):
            context['error'] = "Please provide all fields for Reference 2"
            error = True

        if not len(context['ref_1_name']) or not len(context['ref_1_y']) or not len(context['ref_1_h']):
            context['error'] = "Please provide all fields for Reference 1"
            error = True
        
        if not len(context['address_line_1']) or not len(context['address_line_2']):
            context['error'] = "Please fill out both address line 1 and 2"
            error = True
        
        if not len(context['phone_1']) >= 10:
            context['error'] = "Please provide a valid phone number"
            error = True

        if not len(context['email']):
            context['error'] = "Please provide an email"
            error = True

        if not len(context['first_name']) or not len(context['last_name']):
            context['error'] = "Please provide your full name"
            error = True


        if not error:
            # create user
            user = User.objects.create(email=context['email'],
                                       first_name=context['first_name'],
                                       last_name=context['last_name'],
                                       password=context['password'])

            chapter = Chapter.objects.get(name=context['chapter'])
            house = House.objects.get(name=context['house'])
            alumnus = Alumnum.objects.create(user=user,
                                             mobile=context['phone_1'],
                                             telephone=context['phone_2'],
                                             whatsapp=context['whatsapp'],
                                             facebook=context['facebook'],
                                             twitter=context['twitter'],
                                             instagram=context['instagram'],
                                             address_line_1=context['address_line_1'],
                                             address_line_2=context['address_line_2'],
                                             year_of_completion=int(context['year_of_completion']),
                                             exam_type=context['exam_type'],
                                             house=house,
                                             profession=context['profession'],
                                             chapter=chapter)

            return redirect('web:registration_done')
    
    print(context)

    return render(request, "web/registration.html", context)


def done(request):
    return render(request, "web/registration_complete.html")
