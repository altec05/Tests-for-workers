from django.db import models
from django.urls import reverse
from users.models import User


# Категория теста
class TestCategory(models.Model):
    category_name = models.CharField(max_length=200, verbose_name='Наименование категории', unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['category_name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Тест
class Test(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование теста', unique=True)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    category = models.ForeignKey(TestCategory, on_delete=models.PROTECT, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликован')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    visibility = models.BooleanField(default=True, verbose_name='Видимость')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('test', kwargs={"slug": self.slug})

    class Meta:
        ordering = ['name']
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


# Вопросы
class Question(models.Model):
    class qtype(models.TextChoices):
        single = 'single'
        multiple = 'multiple'

    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    question_text = models.CharField(max_length=500, verbose_name='Текст вопроса', null=False)
    qtype = models.CharField(max_length=8, choices=qtype.choices, default=qtype.single, verbose_name='Формат ответа')
    visibility = models.BooleanField(default=True, verbose_name='Видимость')

    def __str__(self):
        return self.question_text

    def get_choices(self):
        if self.qtype == 'single':
            return self.answer_set.filter(is_correct=True).first()
        else:
            qs = self.answer_set.filter(is_correct=True).values()
            return [i.get('answer_text') for i in qs]

    def user_can_answer(self, user):
        user_choices = user.choice_set.all()
        done = user_choices.filter(question=self)
        print('user_can_answer', user_choices, done)
        if done.exists():
            return False
        return True

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Ответ к вопросу')
    answer_text = models.CharField(max_length=200, verbose_name='Текст ответа', null=False)
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


# Выбранные ответы
class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


# Результат теста
class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    correct = models.IntegerField(default=0, verbose_name='Правильных ответов')
    wrong = models.IntegerField(default=0, verbose_name='Неправильных ответов')

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
