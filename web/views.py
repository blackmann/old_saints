from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db.models import Q

import datetime

from web.models import Alumnum, Chapter, House, Job, Scholarship, \
    Dues, Project


SALARIES = ['1000-2000', '2000-5000', '5000-10000', ]

EXECUTIVES = [
    {
        "name": "Dr. Henry Benyah",
        "position": "GEC President",
        "image": "/static/web/images/henrypres.jpg"
    },
    {
        "name": "Robert Nana Mensah",
        "position": "GEC Executive Member",
        "image": "/static/web/images/robertgec.jpg"
    },
    {
        "name": "Kwame Akaba",
        "position": "GEC Treasurer President",
        "image": "/static/web/images/akabagec.jpg"
    },
    {
        "name": "Adjamah Codjoe",
        "position": "GEC Secretary",
        "image": "/static/web/images/adjamahgec.jpg"
    }, ]


def get_chapters():
    return [c.name for c in Chapter.objects.all()]


def get_houses():
    return [h.name for h in House.objects.all()]


def get_exam_types():
    return ["O'Level", "A'Level", "SSSCE", "WASSCE", ]


def get_date(date_str):
    """
    Convert date in the form mm/dd/yyyy to date object
    """
    split_date = [int(val) for val in date_str.split('/')]

    return datetime.date(day=split_date[0],
                         month=split_date[1],
                         year=split_date[2])


def get_reference(pos, context):
    name = context["ref_%d_name" % pos]
    year = context["ref_%d_y" % pos]
    house = context["ref_%d_h" % pos]
    phone = context["ref_%d_p" % pos]

    return "%s\n%s\n%s\n%s" % (name, year, house, phone, )


def clean_registration_form(request, all=False):
    res = {}
    res['first_name'] = request.POST['first_name'].strip()
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
        res['ref_1_p'] = request.POST['ref_1_p'].strip()
        res['ref_2_p'] = request.POST['ref_2_p'].strip()
        res['ref_2_name'] = request.POST['ref_2_n'].strip()
        res['ref_2_y'] = request.POST['ref_2_y'].strip()
        res['ref_2_h'] = request.POST['ref_2_h'].strip()
        res['password'] = request.POST['password']
        res['nickname'] = request.POST['nickname'].strip()

    return res


def home(request):
    context = {"home": True}

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
            context['error'] = "Password should be more than 7 characters long."
            error = True

        if not len(context['ref_2_name']) or not len(context['ref_2_y']) or not len(context['ref_2_h']) or not (len(context['ref_2_p']) in range(10, 13)):
            context['error'] = "Please provide all fields for Reference 2"
            error = True

        if not len(context['ref_1_name']) or not len(context['ref_1_y']) or not len(context['ref_1_h']) or not (len(context['ref_1_p']) in range(10, 13)):
            context['error'] = "Please provide all fields for Reference 1"
            error = True

        if not len(context['address_line_1']) or not len(context['address_line_2']):
            context['error'] = "Please fill out both address line 1 and 2"
            error = True

        if len(context['phone_1']) not in range(10, 14):
            context['error'] = "Please provide a valid phone number"
            error = True

        if not len(context['email']):
            context['error'] = "Please provide an email"
            error = True

        if not len(context['first_name']) or not len(context['last_name']):
            context['error'] = "Please provide your full name"
            error = True

        if User.objects.filter(email=context['email']).exists():
            context['error'] = "There is an account with this email. Please log in instead"
            error = True

        if not error:
            # create user
            user = User.objects.create_user(email=context['email'],
                                            username=context['email'].replace(
                                                '@', '_'),
                                            first_name=context['first_name'],
                                            last_name=context['last_name'],
                                            password=context['password'])

            chapter = Chapter.objects.get(name=context['chapter'])
            house = House.objects.get(name=context['house'])

            reference_1 = get_reference(1, context)
            reference_2 = get_reference(2, context)

            alumnus = Alumnum.objects.create(user=user,
                                             mobile=context['phone_1'],
                                             telephone=context['phone_2'],
                                             whatsapp=context['whatsapp'],
                                             facebook=context['facebook'],
                                             twitter=context['twitter'],
                                             instagram=context['instagram'],
                                             address_line_1=context['address_line_1'],
                                             address_line_2=context['address_line_2'],
                                             year_of_completion=int(
                                                 context['year_of_completion']),
                                             exam_type=context['exam_type'],
                                             house=house,
                                             profession=context['profession'],
                                             chapter=chapter,
                                             nickname=context['nickname'],
                                             reference_1=reference_1,
                                             reference_2=reference_2)

            return redirect('web:registration_done')

    print(context)

    return render(request, "web/registration.html", context)


def done(request):
    return render(request, "web/registration_complete.html")


def jobs(request):
    context = {
        "jobs": Job.objects.all()
    }
    return render(request, "web/jobs.html", context)


def create_job(request):
    context = dict()
    title = context['title'] = request.POST.get('title', '')
    position = context['position'] = request.POST.get('position', '')
    s_description = context['short_description'] = request.POST.get(
        'short_description', '')
    j_description = context['job_description'] = request.POST.get(
        'job_description', '')
    company = context['company'] = request.POST.get('company', '')
    location = context['location'] = request.POST.get('location', '')
    qualifications = context['qualifications'] = request.POST.get(
        'qualifications', '')
    salary_range = context['salary_range'] = request.POST.get('salary', '')
    deadline = context['deadline'] = request.POST.get('deadline', '')
    hta = context['hta'] = request.POST.get('hta', '')

    if request.method == 'POST':
        job_post = Job.objects.create(post_title=title,
                                      position=position,
                                      short_description=s_description,
                                      job_description=j_description,
                                      salary_range=SALARIES[int(salary_range)],
                                      location=location,
                                      company=company,
                                      how_to_apply=hta,
                                      qualifications=qualifications,
                                      deadline=get_date(deadline),
                                      posted_by=Alumnum.objects.get(pk=1))
        if job_post:
            return redirect('web:jobs')
    return render(request, "web/create_job.html", context)


def login_view(request):

    context = dict()

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect(request.GET.get('next', None) or 'web:home')

            else:
                context['error'] = "The email/password combination is incorrect."

        except User.DoesNotExist:
            context['error'] = "The email/password combination is incorrect."

    return render(request, 'web/login.html', context)


def job_detail(request, job_id):
    context = {
        'job': Job.objects.get(pk=job_id)
    }
    return render(request, 'web/job_detail.html', context)


def scholarships(request):
    context = {
        'scholarships': Scholarship.objects.all()
    }
    return render(request, 'web/scholarships.html', context)


def create_scholarship(request):

    return render(request, 'web/create_scholarship.html')


def find_mate(request):
    context = {
        'houses': House.objects.all(),
        'chapters': Chapter.objects.all()
    }

    if request.GET.get('s', None) == '1':
        name = request.GET.get('q', 0)
        if name:
            context['results'] = Alumnum.objects.filter(Q(user__first_name__contains=name)|
                                                        Q(user__last_name__contains=name))
            context['q'] = name

    return render(request, "web/find_mate.html", context)


def scholarship_detail(request, scholarship_id):
    scholarship = Scholarship.objects.get(pk=scholarship_id)

    context = {
        'scholarship': scholarship
    }

    return render(request, 'web/scholarship_detail.html', context)


def about(request):

    return render(request, "web/about.html")


def general_executives(request):
    context = {
        'executives': EXECUTIVES
    }
    return render(request, "web/global_executives.html", context)


def gallery(request):

    return render(request, "web/gallery.html")


def projects(request):
    context = {
        "projects": Project.objects.all()
    }

    return render(request, "web/projects.html", context)


def dues(request):
    context = {
        "dues": Dues.objects.all(),
        "total": 15.00
    }

    return render(request, "web/dues.html", context)


def contributions(request):

    return render(request, "web/contributions.html")


def events(request):

    return render(request, 'web/events.html')


def project_detail(request, project_id):
    project = Project.objects.get(pk=project_id)

    context = {
        "project": project,
        "contributors": Alumnum.objects.all()
    }

    return render(request, "web/project_detail.html", context)


def profile(request, alumn_id):
    context = {
        "profile": Alumnum.objects.get(pk=alumn_id)
    }
    return render(request, "web/profile.html", context)
