from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.db.models import Q

import datetime

from web.models import Alumnum, Chapter, House, Job, Scholarship, \
    Dues, Project, Event


SALARIES = ['1000-2000', '2000-5000', '5000-10000', ]

DEGREES = ['Bachelors Degree', 'Masters Degree', 'PhD', ]

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


YEARS = [str(y) for y in range(1952, 2019)]

PROFESSIONS = ['Accountant', 'Administrative Assistant', 'Advertising copywriter', 'Advertising executive', 'Architect', 'Automobile mechanic', 'Bank manager', 'Bookkeeper', 'Business strategy consultant', 'Carpenter', 'Chief executive officer', 'Chief financial officer', 'Child-care worker', 'City planner', 'Civil engineer', 'Clerical worker', 'Computer software designer', 'Computer systems analyst', 'Credit manager', 'Development manager', 'Diplomat', 'Director of human resources', 'Director of nonprofit organization', 'Economist', 'Elected public official', 'Electrical engineer', 'Electrician', 'Emergency medical technician', 'Entertainer (singer, comedian, etc.)', 'Entrepreneur', 'Event planner', 'Fiction writer', 'Financial analyst', 'Fine artist', 'Firefighter', 'Foreign trade negotiator', 'Graphic Designer', 'High school teacher', 'Homemaker', 'Investigative reporter', 'Investment banker', 'Investment manager', 'Leader of a product- development team', 'Librarian', 'Litigator (courtroom lawyer)', 'Logistical planner', 'Manager at a manufacturing plant', 'Manager of a restaurant', 'Manager of a retail store', 'Manager of a stock or bond mutual fund',
               'Manager of information systems', 'Manufacturing process engineer', 'Marketing brand manager', 'Marketing researcher', 'Mayor of a city or town', 'Medical researcher', 'Military serviceperson', 'Military strategist', 'Motivational speaker', 'Music composer', 'Newscaster', 'Newspaper editor', 'Nurse', 'Office manager', 'Optometrist', 'Personal financial advisor', 'Police officer', 'President of a community charity', 'Professional actor', 'Professional athlete', 'Professor of political science', 'Proofreader', 'Psychotherapist', 'Public relations professional', 'Real estate developer', 'Real estate salesperson', 'Religious counselor', 'Research and', 'Research sociologist', 'Salesperson for high-tech products', 'Salesperson in a retail store', 'School superintendent', 'Secretary', 'Senior hospital manager', 'Senior manager of a', 'Senior military leader', 'Ship captain', 'Social services professional', 'Speech therapist', 'Sports coach', 'Statistician', 'Stockbroker', 'Surgeon', 'TV or film director', 'TV talk show host', 'Theologian', 'Theoretical physicist', 'University professor', 'Vacation resort manager', 'Venture capitalist', 'Veterinarian', 'manufacturing business']


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
        "exam_types": get_exam_types(),
        "years": YEARS,
        "professions": PROFESSIONS
    }

    error = False

    if request.method == 'POST':
        # validation
        clean_data = clean_registration_form(request, True)
        context.update(clean_data)

        if not len(context['password']) > 7:
            context['error'] = "Password should be more than 7 characters long."
            error = True

        if not len(context['ref_2_name']) or not len(context['ref_2_y']) or not len(context['ref_2_h']) or not (len(context['ref_2_p']) in range(10, 14)):
            context['error'] = "Please provide all fields for Reference 2"
            error = True

        if not len(context['ref_1_name']) or not len(context['ref_1_y']) or not len(context['ref_1_h']) or not (len(context['ref_1_p']) in range(10, 14)):
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
        
        print(request.POST)

    return render(request, "web/registration.html", context)


def done(request):
    return render(request, "web/registration_complete.html")


@login_required
def jobs(request):
    q_jobs = Job.objects.all()
    context = {
        "professions": PROFESSIONS
    }

    if request.GET.get('f', 0):
        profession = request.GET.get('profession', 'all')
        if not profession == 'all':
            q_jobs = q_jobs.filter(profession_type=profession)

        context['profession'] = profession
    
    context['jobs'] = q_jobs.all()
    
    return render(request, "web/jobs.html", context)


@login_required
def create_job(request):
    error = False

    context = {
        "professions": PROFESSIONS
    }

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
    profession = context['profession'] = request.POST.get('profession', '')

    if request.method == 'POST':
        # validation
        if not (title and position and s_description and j_description and company and
                location and qualifications and salary_range and deadline and hta and profession):
                context['error'] = "Please fill in all fields"
                error = True
        
        if not error:
            job_post = Job.objects.create(post_title=title,
                                        position=position,
                                        short_description=s_description,
                                        job_description=j_description,
                                        salary_range=SALARIES[int(salary_range)],
                                        location=location,
                                        company=company,
                                        profession_type=profession,
                                        how_to_apply=hta,
                                        qualifications=qualifications,
                                        deadline=get_date(deadline),
                                        posted_by=Alumnum.objects.get(user=request.user))
            if job_post:
                return redirect('web:jobs')
        print(context)
    return render(request, "web/create_job.html", context)


def login_view(request):
    context = {
        'next': request.GET.get('next', None)
    }
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect(context['next'] or 'web:home')

            else:
                context['error'] = "The email/password combination is incorrect."

        except User.DoesNotExist:
            context['error'] = "The email/password combination is incorrect."

    return render(request, 'web/login.html', context)


@login_required
def job_detail(request, job_id):
    context = {
        'job': Job.objects.get(pk=job_id)
    }
    return render(request, 'web/job_detail.html', context)


@login_required
def scholarships(request):
    context = {
        'scholarships': Scholarship.objects.all()
    }
    return render(request, 'web/scholarships.html', context)


@login_required
def create_scholarship(request):
    context = {
        'degrees': DEGREES
    }

    if request.method == 'POST':
        title = context['title'] = request.POST.get('title', '')
        certification = context['degree'] = request.POST.get('degree', '')
        description = context['description'] = request.POST.get('description', '')
        school = context['school'] = request.POST.get('school', '')
        location = context['location'] = request.POST.get('location', '')
        how_to_apply = context['hta'] = request.POST.get('hta', '')

        # TODO validation
        scholarship = Scholarship.objects.create(title=title,
                                                 degree=certification,
                                                 description=description,
                                                 school=school,
                                                 location=location,
                                                 how_to_apply=how_to_apply,
                                                 posted_by=Alumnum.objects.get(user=request.user))
        
        if scholarship:
            return redirect('web:scholarships')

    return render(request, 'web/create_scholarship.html', context)


@login_required
def find_mate(request):
    context = {
        'houses': House.objects.all(),
        'chapters': Chapter.objects.all(),
        'years': YEARS
    }

    if request.GET.get('s', None) == '1':
        name = request.GET.get('q', 0)
        if len(name) > 1:
            results = Alumnum.objects.filter(Q(user__first_name__contains=name) |
                                                        Q(user__last_name__contains=name)|
                                                        Q(nickname__contains=name))
            house = request.GET.get('house', 0)
            year = request.GET.get('year', 0)
            chapter = request.GET.get('chapter', 0)
            if house and not house == "All Houses":
                results = results.filter(house=House.objects.get(name=house))

            if year and not year == "All Years":
                results = results.filter(year_of_completion=int(year))
            
            if chapter and not chapter == "All Chapters":
                results = results.filter(chapter=Chapter.objects.get(name=chapter))

            context['results'] = results.all()
            context['q'] = name
            context['year'] = year
            context['chapter'] = chapter
            context['house'] = house

    return render(request, "web/find_mate.html", context)


@login_required
def scholarship_detail(request, scholarship_id):
    scholarship = Scholarship.objects.get(pk=scholarship_id)

    context = {
        'scholarship': scholarship
    }

    return render(request, 'web/scholarship_detail.html', context)


def about(request):

    return render(request, "web/about.html")


@login_required
def general_executives(request):
    context = {
        'executives': EXECUTIVES
    }
    return render(request, "web/global_executives.html", context)


@login_required
def gallery(request):

    return render(request, "web/gallery.html")


@login_required
def projects(request):
    context = {
        "projects": Project.objects.all()
    }

    return render(request, "web/projects.html", context)


@login_required
def dues(request):
    context = {
        "dues": Dues.objects.all(),
        "total": 15.00
    }

    return render(request, "web/dues.html", context)


@login_required
def contributions(request):

    return render(request, "web/contributions.html")


@login_required
def events(request):
    context = {
        "events": Event.objects.all()
    }

    return render(request, 'web/events.html', context)


@login_required
def project_detail(request, project_id):
    project = Project.objects.get(pk=project_id)
    image_attrs = ["image%d" % i for i in range(1, 7)]
    project_images = [getattr(project, img) for img in image_attrs]

    context = {
        "project": project,
        "contributors": Alumnum.objects.all(),
        "project_images": project_images
    }

    return render(request, "web/project_detail.html", context)


@login_required
def profile(request, alumn_id):
    context = {
        "profile": Alumnum.objects.get(pk=alumn_id)
    }
    return render(request, "web/profile.html", context)


def log_out(request):
    logout(request)
    return redirect('web:home')
