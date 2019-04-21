# Create your views here.


from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .forms import PersonForm
from .cvbackground import get_watercolour_image

def index(request):
    template = loader.get_template("homepage/index.html")
    context = {
        "form": PersonForm(),
        "location": "/",
        "video": True,
        "menu": [],
        "button_text": "Find Candidate",
        "time":60
    }
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        form = PersonForm(request.POST,request.FILES)

        if form.is_valid():
            template = loader.get_template("homepage/sucess.html")
            form.save()
            username = form["name"].value()
            filename = "photo/" + username + "/" + request.FILES['photo'].name
            disp_hee = get_watercolour_image(filename,9,120,username)
            context = {
                "image":"photo/"+username+"/final1.png",
                "heera_msg":disp_hee
            }

    return HttpResponse(template.render(context, request))


