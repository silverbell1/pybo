from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from ..models import Question, Answer, Comment
from django.utils import timezone
from ..forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .answer_views import *

from ultralytics import YOLO
import os



def yolo_predict(filename, user):

    used_model = YOLO('./media/models/robo_best_20240314_6class_per100.pt')
    source_file = './media/' + str(filename)
    project_fld = './media/answer'
    name = timezone.localtime(timezone.now()).strftime("%Y%m%d%H%M%S")
    results = used_model.predict(source=source_file,
                                 project=project_fld,
                                 name=name,
                                 save=True,
                                 save_txt=True,
                                 conf=0.15)
    return name




@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.imgfile = request.FILES['imgfile']
            question.author = request.user
            question.create_date = timezone.now()
            question.save()

            # Yolo 모델 작동
            name = yolo_predict(question.imgfile, request.user)

            # 자동 답변 처리
            imgfile = str(question.imgfile)
            imgfile = imgfile[imgfile.rfind('/') + 1:]
            result = question.imgfile
            answer_create(request, question.id, 'answer/' + name + '/' + imgfile, result)

            return redirect('pybo:index')
        else:
            messages.error(request, '이미지 파일을 등록해야 합니다.')
            return redirect('pybo:detail', question_id=quesiton_id)

        return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id = question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')