from django import forms
from pybo.models import Question, Answer, Comment

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content', 'imgfile']
        labels = {
            'subject': '제목',
            'content': '내용',
            'imgfile': '업로드 파일',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'imgfile']
        labels = {
            'content': '답변내용',
            'imgfile': '업로드 파일',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용'
        }