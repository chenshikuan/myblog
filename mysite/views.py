from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Sum
from read_statistics.utils import get_seven_days_read_num, get_today_hot_data, get_yesterday_hot_data, get_7_days_hot_date
from blog.models import Blog
import datetime


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date)\
    .values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num'))\
    .order_by('-read_num_sum')
    return blogs

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_num(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)


    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['get_7_days_hot_date'] = get_7_days_hot_date(blog_content_type)
    return render(request, 'home.html', context)

