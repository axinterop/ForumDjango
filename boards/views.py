from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import UpdateView, ListView, DeleteView

from boards.forms import NewTopicForm, PostForm
from boards.models import Board, Post, Topic


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/home.html'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context

    def get_queryset(self):
        self.board = get_object_or_404(Board, id=self.kwargs.get('board_id'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        session_key = f'viewed_topic_{self.topic.id}'
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        context['topic'] = self.topic
        return context

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board_id=self.kwargs.get('board_id'), id=self.kwargs.get('topic_id'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


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
            return redirect('topic_posts', board_id=board_id, topic_id=topic.id)
    else:
        form = NewTopicForm()

    context = {
        'board': board,
        'form': form,
    }
    return render(request, 'boards/new_topic.html', context)


@login_required
def reply_topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board_id=board_id, id=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'board_id': board_id, 'topic_id': topic_id})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.id,
                page=topic.get_page_count()
            )
            return redirect(topic_post_url)
    else:
        form = PostForm()
    context = {
        'topic': topic,
        'form': form,
    }
    return render(request, 'boards/reply_topic.html', context)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'boards/edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Prevents non-owners from editing the post
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()

        topic_url = reverse('topic_posts', kwargs={
            'board_id': post.topic.board.id,
            'topic_id': post.topic.id,
        })
        success_url = '{url}?page={page}#{id}'.format(
            url=topic_url,
            id=post.id,
            page=post.get_page(),
        )
        return redirect(success_url)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'boards/delete_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Prevents non-owners from deleting the post
        return queryset.filter(created_by=self.request.user)

    def get_success_url(self):
        topic_url = reverse('topic_posts', kwargs={
            'board_id': self.kwargs.get('board_id'),
            'topic_id': self.kwargs.get('topic_id'),
        })
        success_url = '{url}?page={page}'.format(
            url=topic_url,
            page=self.object.get_page()
        )
        return success_url
