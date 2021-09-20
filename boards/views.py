from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from boards.forms import NewTopicForm
from boards.models import Board, Topic, Post


def home(request):
    boards = Board.objects.all()
    context = {'boards': boards}
    return render(request, 'home.html', context)


def board_topics(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    context = {'board': board}
    return render(request, 'topics.html', context)


def new_topic(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    user = User.objects.first()

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user,
            )
            return redirect('board_topics', board_id=board.id)
    else:
        form = NewTopicForm()

    context = {
        'board': board,
        'form': form,
    }
    return render(request, 'new_topic.html', context)
