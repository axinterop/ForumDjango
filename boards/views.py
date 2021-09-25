from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from boards.forms import NewTopicForm
from boards.models import Board, Post, Topic


def home(request):
    boards = Board.objects.all()
    context = {'boards': boards}
    return render(request, 'home.html', context)


def board_topics(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    context = {'board': board}
    return render(request, 'topics.html', context)


@login_required
def new_topic(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user,
            )
            return redirect('board_topics', board_id=board.id)
    else:
        form = NewTopicForm()

    context = {
        'board': board,
        'form': form,
    }
    return render(request, 'new_topic.html', context)


def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board_id=board_id, id=topic_id)
    context = {
        'topic': topic,
    }
    return render(request, 'topic_posts.html', context)
