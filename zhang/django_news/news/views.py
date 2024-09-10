from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question,Choice
from django.shortcuts import render,get_object_or_404
from django.urls import reverse,path
from django.views import generic

# Create your views here.

'''
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'news/index.html', context)


# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'news/detail.html', {'question': question})
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'news/detail.html', {'question': question})


# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'news/results.html', {'question': question})
'''


class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'news/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'news/results.html'


# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'news/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('news:results', args=(question.id,)))


def start_main():
    print('hello')
    return 'ok'


def update_pdaq(request):
    if request.META:
        # start_main()
        status = start_main()
        context ={
            'status':status
        }
        return render(request,'news/update.html',context=context)

# def get_urls(self):
#     urls = super().get_urls()
#
#     my_urls = [
#         path('immortal/', self.set_immortal),
#         ]
#     return my_urls + urls
#
#
# def set_immortal(self, request):
#     print('yitioajiao')
#     self.model.objects.all().update(is_immortal=True)
#     self.message_user(request, "All heroes are now immortal")
#     return HttpResponseRedirect("../")
#
# def set_immortal():
#     print('hello')
#     pass