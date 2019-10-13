from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count

from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read
from read_statistics.models import ReadNum


# Create your views here.
 # the max number of each page
def blog_show(request ,blogs_all_list):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOG_NUMBER)
    blogs_by_page_num = paginator.get_page(page_num)
    page_num_range = list(range(max(int(page_num) - 3, 1), min(int(page_num) + 3, paginator.num_pages) + 1))
    if page_num_range[0] != 1:
        page_num_range[0] = 1
        page_num_range.insert(1, '...')
    if page_num_range[-1] != paginator.num_pages:
        page_num_range[-1] = paginator.num_pages
        page_num_range.insert(-1, '...')
    #obtain the amount of  each blogType containing blog
    blog_types = BlogType.objects.all()
    # blog_types_list=[]
    # for blog_type in blog_types:
    #     blog_type.blog_count = Blog.objects.filter(blog_type = blog_type).count()
    #     blog_types_list.append(blog_type)
    blog_types_list = BlogType.objects.annotate(blog_count=Count('blog')) #效果和上面的相同但是基于数据库层面完成的，比较快，省内存
    # blog_datas = Blog.objects.dates('create_time','month','DESC').annotate(blog_count=Count('create_time'))
    blog_dates = Blog.objects.dates('create_time','month','DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year, create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    #
    # blog_dates_dict = {}
    # for blog_date in blog_datas:


    context = {}
    context['blogs_by_page_num'] = blogs_by_page_num
    context['page_num_range'] = page_num_range
    context['blog_types'] = blog_types_list
    context['blog_dates'] = blog_dates_dict#日期归档
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = blog_show(request, blogs_all_list)
    return render(request, 'blog_list.html', context)


def blog_detail(request, blog_id):
    context = {}
    blog = get_object_or_404(Blog, id = blog_id)#如果取不到，则会返回报错页面
    read_cookie_key = read_statistics_once_read(request, blog)
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()#[-1]
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()#[0]
    response = render(request, 'blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true') #max_age以秒为单位, expires=datetime,过期时间
    return response


def blog_with_type(request,blog_type_id):
    blog_type = get_object_or_404(BlogType, id=blog_type_id)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = blog_show(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request,'blog_with_type.html', context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = blog_show(request, blogs_all_list)
    context['blog_with_date'] = '%s年%s月' % (year,month)
    return render(request,'blog_with_date.html',context)



