from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
import dashboard.models
import blog.models

def getDashboardNav(user_id):
    if 'S' in user_id:
        dashboardNav = " Pelajar"
    elif 'P' in user_id:
        dashboardNav = " Penjaga"
    elif 'T' in user_id:
        dashboardNav = " Guru"
    elif 'A' in user_id:
        dashboardNav = " Admin"
    return dashboardNav

def getNavbarURL(user_type):
    if user_type == 'admin':
        urlTest = 'test:index-admin'
        urlQuiz = 'quiz:index-admin'
        urlSearch = 'search:index-admin'
        urlDashboard = 'dashboard:index-admin'
    else:
        urlTest = 'test:index-nonadmin'
        urlQuiz = 'quiz:index-student'
        urlSearch = 'search:index-nonadmin'
        urlDashboard = 'dashboard:index-nonadmin'
    
    context = {'test': urlTest, 'quiz': urlQuiz, 'search': urlSearch, 'dashboard': urlDashboard}
    return context

# Create your views here.
def blogMain(request, user_type, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = getNavbarURL(user_type).get('test')
    urlBlog = 'blog:index'
    urlQuiz = getNavbarURL(user_type).get('quiz')
    urlSearch = getNavbarURL(user_type).get('search')
    urlDashboard = getNavbarURL(user_type).get('dashboard')
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = getDashboardNav(user_id)
    user_type = user_type
    username = currentUserDetail.username

    allBlogPosts = blog.models.BlogPost.objects.all().order_by('id')
    mostPopularPosts = allBlogPosts.order_by('-noOfViews')
    latestPosts = allBlogPosts.order_by('-lastDateEdited', '-lastTimeEdited')
    postIDswithImageList = list(blog.models.BlogPostImage.objects.all().order_by('id').values_list('blogPostID_id', flat=True))
    allBlogCategoryBridge = blog.models.BlogPostCategory.objects.all().order_by('id')
    postIDsinBridgeCatList =list(allBlogCategoryBridge.values_list('blogPostID_id', flat=True))
    allCategories = blog.models.Category.objects.all().order_by('id')
    allCategoriesByName = allCategories.order_by('name')
    allDatePublishedList = list(allBlogPosts.values_list('datePublished', flat=True).distinct().order_by('-datePublished'))
    allYearList = [0]
    
    for dp in allDatePublishedList:
        allYearList.append(dp.year)

    context = {
        'dashboardNav': dashboardNav,
        'user_id': user_id,
        'user_type': user_type,
        'username': username,
        'test': urlTest,
        'blog': urlBlog,
        'quiz': urlQuiz,
        'search': urlSearch,
        'dashboard': urlDashboard,
        'logout': urlLogout,
        'mostPopularPosts': mostPopularPosts,
        'latestPosts': latestPosts,
        'postIDswithImageList': postIDswithImageList,
        'allBlogCategoryBridge': allBlogCategoryBridge,
        'postIDsinBridgeCatList': postIDsinBridgeCatList,
        'allCategories': allCategories,
        'allCategoriesByName': allCategoriesByName,
        'allYearList': allYearList
    }
    return render(request, 'blog/blogMain.html', context)

def blogPostList(request, user_type, user_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = getNavbarURL(user_type).get('test')
    urlBlog = 'blog:index'
    urlQuiz = getNavbarURL(user_type).get('quiz')
    urlSearch = getNavbarURL(user_type).get('search')
    urlDashboard = getNavbarURL(user_type).get('dashboard')
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = getDashboardNav(user_id)
    user_type = user_type
    username = currentUserDetail.username

    allBlogPosts = blog.models.BlogPost.objects.all().order_by('id')
    allBlogCategoryBridge = blog.models.BlogPostCategory.objects.all().order_by('id')
    postIDswithImageList = list(blog.models.BlogPostImage.objects.all().order_by('id').values_list('blogPostID_id', flat=True))
    postIDsinBridgeCatList = list(allBlogCategoryBridge.values_list('blogPostID_id', flat=True))
    allCategories = blog.models.Category.objects.all().order_by('id')
    allCategoriesByName = allCategories.order_by('name')
    allDatePublishedList = list(allBlogPosts.values_list('datePublished', flat=True).distinct().order_by('-datePublished'))
    allYearList = ['0'] # string

    for dp in allDatePublishedList:
        allYearList.append(str(dp.year))

    if request.method == 'GET': # If the form is submitted from blogMain/this page OR refresh page
        title_text = request.GET.get('tajuk', None)
        cat_selected = request.GET.get('kategori', None)
        yearSelectedList = request.GET.getlist('tahun[]') #returned in string

        if title_text is not None:
            allBlogPosts = allBlogPosts.filter(title__icontains=title_text)

        if cat_selected is not None:
            if cat_selected != 'Semua':
                cat_selected_ID = allCategories.get(name = cat_selected).id
                postIDsList = list(allBlogCategoryBridge.filter(categoryID_id=cat_selected_ID).values_list('blogPostID_id', flat=True))
                allBlogPosts = allBlogPosts.filter(id__in=postIDsList)

        currentDatePublishedList = []

        if yearSelectedList:
            if '0' not in yearSelectedList:
                for year in yearSelectedList:
                    for post in allBlogPosts:
                        if year == str(post.datePublished.year):
                            currentDatePublishedList.append(post.datePublished)
                            break
                allBlogPosts = allBlogPosts.filter(datePublished__in=currentDatePublishedList)
    
    allBlogPosts = allBlogPosts.order_by('-datePublished')

    context = {
        'dashboardNav': dashboardNav,
        'user_id': user_id,
        'user_type': user_type,
        'username': username,
        'test': urlTest,
        'blog': urlBlog,
        'quiz': urlQuiz,
        'search': urlSearch,
        'dashboard': urlDashboard,
        'logout': urlLogout,
        'postIDswithImageList': postIDswithImageList,
        'allBlogCategoryBridge': allBlogCategoryBridge,
        'postIDsinBridgeCatList': postIDsinBridgeCatList,
        'allCategories': allCategories,
        'allCategoriesByName': allCategoriesByName,
        'allYearList': allYearList,
        'title_text': title_text,
        'cat_selected': cat_selected,
        'yearSelectedList': yearSelectedList,
        'yearSelectedListCount': len(yearSelectedList),
        'allBlogPosts': allBlogPosts,
        'allBlogPostsCount': allBlogPosts.count()
    }
    return render(request, 'blog/blogPostList.html', context)

def viewPost(request, user_type, user_id, post_id):
    currentUserDetail = dashboard.models.User.objects.get(ID=user_id)

    #check logged in or not
    if currentUserDetail.isActive == False:
        return redirect('home:login')

    urlTest = getNavbarURL(user_type).get('test')
    urlBlog = 'blog:index'
    urlQuiz = getNavbarURL(user_type).get('quiz')
    urlSearch = getNavbarURL(user_type).get('search')
    urlDashboard = getNavbarURL(user_type).get('dashboard')
    urlLogout = 'dashboard:logout-confirm'
    dashboardNav = getDashboardNav(user_id)
    user_type = user_type
    post_id = post_id
    username = currentUserDetail.username

    currentBlogPost = blog.models.BlogPost.objects.get(id=post_id)
    allBlogPosts = blog.models.BlogPost.objects.all().order_by('id')
    mostPopularPosts = allBlogPosts.order_by('-noOfViews')[:3]
    latestPosts = allBlogPosts.order_by('-lastDateEdited', '-lastTimeEdited')[:3]
    postIDswithImageList = list(blog.models.BlogPostImage.objects.all().order_by('id').values_list('blogPostID_id', flat=True))
    currentBlogCategoryBridge = blog.models.BlogPostCategory.objects.filter(blogPostID_id=post_id).order_by('id')
    allCategories = blog.models.Category.objects.all().order_by('id')
    allCategoriesByName = allCategories.order_by('name')
    allDatePublishedList = list(allBlogPosts.values_list('datePublished', flat=True).distinct().order_by('-datePublished'))
    allYearList = [0]
    
    for dp in allDatePublishedList:
        allYearList.append(dp.year)

    currentUserBookmarkPostIDList = list(blog.models.BlogPostBookmark.objects.filter(userID_id=user_id).order_by('id').values_list('blogPostID_id', flat=True))

    if currentUserBookmarkPostIDList:
        if int(post_id) in currentUserBookmarkPostIDList:
            hasBookmark = True
        else:
            hasBookmark = False
    else:
        hasBookmark = False

    if request.is_ajax():
        if request.POST['requestType'] == 'addBookmark':
            blog.models.BlogPostBookmark.objects.create(blogPostID_id=post_id, userID_id=user_id)
            hasBookmark = True
            context = {'hasBookmark': hasBookmark}
            
            return render(request, 'blog/updateBookmark.html', context)
        elif request.POST['requestType'] == 'removeBookmark':
            blog.models.BlogPostBookmark.objects.get(blogPostID_id=post_id, userID_id=user_id).delete()
            hasBookmark = False
            context = {'hasBookmark': hasBookmark}

            return render(request, 'blog/updateBookmark.html', context)

    context = {
        'dashboardNav': dashboardNav,
        'user_id': user_id,
        'user_type': user_type,
        'username': username,
        'test': urlTest,
        'blog': urlBlog,
        'quiz': urlQuiz,
        'search': urlSearch,
        'dashboard': urlDashboard,
        'logout': urlLogout,
        'post_id': int(post_id),
        'currentBlogPost': currentBlogPost,
        'mostPopularPosts': mostPopularPosts,
        'latestPosts': latestPosts,
        'postIDswithImageList': postIDswithImageList,
        'currentBlogCategoryBridge': currentBlogCategoryBridge,
        'allCategories': allCategories,
        'allCategoriesByName': allCategoriesByName,
        'allYearList': allYearList,
        'hasBookmark': hasBookmark
    }
    return render(request, 'blog/viewPost.html', context)