from django.shortcuts import render
from .scraping import scraping, ScrapingError
# Create your views here.
def index(request):
    return render(request, "shop/index.html")

def fill_database(request):
    if request.method == 'POST' and request.user.is_staff:
        try:
            scraping()
        except ScrapingError as err:
            print(str(err))
            return render(request, "shop/fill_products.html", {"message" : str(err)})
        
    return render(request, "shop/fill_products.html", {"message" : None}) 