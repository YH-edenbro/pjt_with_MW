from django.shortcuts import render, redirect
from .models import Jusik
from .utils import crawl_tossinvest_opinions

# Create your views here.
def index(request):
    comments = Jusik.objects.all()
    context ={
        'comments': comments
    }
    return render(request, 'crawlings/index.html', context)


def delete_comment(request, comment_pk):
    comment = Jusik.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('crawlings:index')

