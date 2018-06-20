from django.shortcuts import render, redirect


def home(request):
    context = {}
    error = False
    if request.method == "POST":
        # check for the important stuffs
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        email = request.POST['email']
        year_of_completion = request.POST['year_of_completion']
        house = request.POST['house']

        if not len(first_name) or not len(last_name):
            context['error'] = "Please provide your full name"
            error = True

        if not len(email):
            context['error'] = "Please provide an email"
            error = True

        print("here")
        if not error:
            return redirect('/register/?f=%s&l=%s&e=%s&y=%s&h=%s' %
                            (first_name, last_name, email, year_of_completion, house, ))
    return render(request, "web/index.html", context)


def register(request):
    context = {
        "pre_form": request.GET
    }

    if request.method == 'POST':
        return redirect('web:registration_done')

    return render(request, "web/registration.html", context)


def done(request):
    return render(request, "web/registration_complete.html")
