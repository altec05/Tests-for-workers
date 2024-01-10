from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from users.utils import paginate_objects
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import *


@login_required
def tests(request):
    user = request.user
    tests = Test.objects.all()
    custom_range, tests = paginate_objects(request, tests, 3)
    context = {'tests': tests, 'user': user, 'custom_range': custom_range}
    return render(request, 'tests/tests.html', context)


@login_required
def display_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    question = test.question_set.first()
    questions = test.question_set.all()
    return redirect(reverse('tests:display_question', kwargs={'test_id': test_id, 'question_id': question.pk}))


@login_required
def display_question(request, test_id, question_id):
    user = request.user
    test = get_object_or_404(Test, pk=test_id)
    questions = test.question_set.all()
    current_question, next_question = None, None
    for ind, question in enumerate(questions):
        if question.pk == question_id:
            current_question = question
            if ind != len(questions) - 1:
                next_question = questions[ind + 1]
    context = {'test': test, 'question': current_question, 'next_question': next_question, 'user': user, 'questions': len(questions)}
    return render(request, 'tests/display.html', context)


@login_required
def grade_question(request, test_id, question_id):
    test = get_object_or_404(Test, pk=test_id)
    question = get_object_or_404(Question, pk=question_id)
    can_answer = question.user_can_answer(request.user)
    print(test)
    print(question)
    print(can_answer)
    print('request', request.POST)
    otvet = Answer.objects.get(id=request.POST.get('answer'))
    print(otvet.id)
    try:
        if not can_answer:
            print('Рендерю заново')
            return render(request, 'tests/partial.html', {'question': question, 'error_message': 'Вы уже отвечали на этот вопрос.'})

        print('question.qtype', type(question.qtype), question.qtype == 'single')

        if question.qtype == 'single':
            correct_answer = question.get_answers()
            print('correct_answer', question.get_answers())
            user_answer = Answer.objects.get(id=request.POST.get('answer'))
            print('user_answer', user_answer)
            choice = Choice(user=request.user, question=question, answer=user_answer)
            print('choice', choice)
            choice.save()
            if correct_answer == user_answer:
                is_correct = correct_answer
            print('is_correct', is_correct, correct_answer, user_answer)
            result, created = Result.objects.get_or_create(user=request.user, test=test)
            if is_correct is True:
                result.correct = F('correct') + 1
            else:
                result.wrong = F('wrong') + 1
            result.save()

        elif question.qtype == 'multiple':
            correct_answer = question.get_answers()
            print('correct_answer', correct_answer)
            answers_ids = request.POST.getlist('answer')
            user_answers = []
            if answers_ids:
                for answer_id in answers_ids:
                    user_answer = Answer.objects.get(pk=answer_id)
                    user_answers.append(user_answer.name)
                    choice = Choice(user=request.user, question=question, answer=user_answer)
                    choice.save()
                is_correct = correct_answer == user_answers 
                result, created = Result.objects.get_or_create(user=request.user, test=test)
                if is_correct is True:
                    result.correct = F('correct') + 1
                else:
                    result.wrong = F('wrong') + 1
                result.save()
    except:
        return render(request, 'tests/partial.html', {'question': question})
    return render(request, 'tests/partial.html', {'is_correct': is_correct, 'correct_answer': correct_answer, 'question': question})


@login_required
def test_results(request, test_id):
    user = request.user
    test = get_object_or_404(Test, pk=test_id)
    questions = test.question_set.all()
    results = Result.objects.filter(user=request.user, test=test).values()
    try:
        correct = [i['correct'] for i in results][0]
        wrong = [i['wrong'] for i in results][0]
    except:
        correct = 0
        wrong = 0
    context = {'test': test, 'user': user, 'correct': correct, 'wrong': wrong, 'number': len(questions),
               'skipped': len(questions) - (correct + wrong)}
    return render(request, 'tests/results.html', context)
