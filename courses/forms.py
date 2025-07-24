from django import forms
from .models import Course, Module, Lesson, Quiz, Question, Announcement, LessonComment, CourseReport, LessonFile
from markdownx.fields import MarkdownxFormField
from django.utils.safestring import mark_safe
from django.forms.models import modelformset_factory
from markdownx.fields import MarkdownxFormField
from markdownx.widgets import MarkdownxWidget

TAILWIND_INPUT = 'w-full px-4 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500'
TAILWIND_TEXTAREA = TAILWIND_INPUT + ' resize-y'
TAILWIND_SELECT = TAILWIND_INPUT + ' bg-white'

class CourseForm(forms.ModelForm):
    description = MarkdownxFormField(widget=MarkdownxWidget(attrs={
        'class': TAILWIND_TEXTAREA
    }))

    class Meta:
        model = Course
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'description': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA}),
            'order': forms.NumberInput(attrs={'class': TAILWIND_INPUT}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'video_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'description': forms.Textarea(),
            'video_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': TAILWIND_TEXTAREA})

LessonFileFormSet = modelformset_factory(
    LessonFile,
    fields=('file',),
    extra=0,
    can_delete=True,
    widgets={
        'file': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
    }
)

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'time_limit']
        help_texts = {
            'time_limit': 'Time limit in minutes (0 means no limit)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'time_limit': forms.NumberInput(attrs={'min': 0, 'class': TAILWIND_INPUT}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'choices', 'correct_answer', 'explanation']
        widgets = {
            'question_text': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'question_type': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'choices': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'id': 'id_choices',
                'placeholder': 'Comma-separated choices',
            }),
            'correct_answer': forms.TextInput(attrs={
                'class': f'{TAILWIND_INPUT}',
                'id': 'id_correct_answer',
            }),
            'explanation': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Explain why this answer is correct...',
                'class': TAILWIND_TEXTAREA,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.fields['question_text'].required = True
        self.fields['question_type'].required = True
        self.fields['correct_answer'].required = True
        self.fields['choices'].required = False
        self.fields['explanation'].required = False

    def clean(self):
        cleaned_data = super().clean()
        question_type = cleaned_data.get('question_type')
        choices = cleaned_data.get('choices')

        if question_type == 'MCQ' and not choices:
            self.add_error('choices', 'Choices are required for multiple choice questions.')

class TakeQuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for q in questions:
            field_name = f"question_{q.id}"
            if q.question_type == 'MCQ':
                choices = [(choice.strip(), choice.strip()) for choice in q.choices.split(',')]
                self.fields[field_name] = forms.ChoiceField(
                    label=q.question_text,
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'space-y-2'}),
                    required=False
                )
            elif q.question_type == 'TF':
                self.fields[field_name] = forms.ChoiceField(
                    label=q.question_text,
                    choices=[('True', 'True'), ('False', 'False')],
                    widget=forms.RadioSelect(attrs={'class': 'space-y-2'}),
                    required=False
                )
            elif q.question_type == 'FB':
                label = mark_safe(
                    q.question_text.replace('[blank]', '<u>__________</u>') if '[blank]' in q.question_text
                    else q.question_text + ' <u>__________</u>'
                )
                self.fields[field_name] = forms.CharField(
                    label=label,
                    widget=forms.TextInput(attrs={'class': TAILWIND_INPUT}),
                    required=False
                )

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message']
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'message': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA}),
        }


class LessonCommentForm(forms.ModelForm):
    class Meta:
        model = LessonComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Write a comment...',
                'class': TAILWIND_TEXTAREA,
            }),
        }



class CourseReportForm(forms.ModelForm):
    class Meta:
        model = CourseReport
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe what’s wrong with this course...',
                'class': TAILWIND_TEXTAREA,
            }),
        }
