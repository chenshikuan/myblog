from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from read_statistics.utils import get_seven_days_read_num, get_today_hot_data, get_yesterday_hot_data, get_7_days_hot_date
from blog.models import Blog


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_num(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
    # hot_blogs_for_7_days =

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['get_7_days_hot_date'] = get_7_days_hot_date(blog_content_type)
    return render(request, 'home.html', context)

