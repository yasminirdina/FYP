from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from numpy.lib.type_check import imag
import dashboard.models
import blog.models, quiz.models, re, json, os
from random import randint
from django.db.models import Sum
from .forms import AddPostForm, EditPostForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
from django.db import IntegrityError, transaction
import numpy as np

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

    allBlogPosts = blog.models.BlogPost.objects.filter(show=True, delete=False).order_by('id') #main page show all published & not deleted posts only for both admin & non-admin
    mostPopularPosts = allBlogPosts.order_by('-noOfViews', 'title')[:4]
    latestPosts = allBlogPosts.order_by('-lastDateEdited', '-lastTimeEdited')[:4]
    postIDswithImageList = list(blog.models.BlogPostImage.objects.all().order_by('id').values_list('blogPostID_id', flat=True))
    print("postIDswithImageList: " + str(postIDswithImageList)) #Test
    allBlogPostImages = blog.models.BlogPostImage.objects.all().order_by('id')
    print("allBlogPostImages:"  + str(allBlogPostImages)) #Test
    toAddIds = []
    toShowURLs = []

    for image in allBlogPostImages:
        print("image: " + str(image)) #Test
        if image.blogPostID_id not in toAddIds:
            print("-- first picture for post id " + str(image.blogPostID_id)) #Test
            toAddIds.append(image.blogPostID_id)
            toShowURLs.append(image.blogPostImage)
            print("updated toAddIds: " + str(toAddIds)) #Test
            print("updated toShowURLs: " + str(toShowURLs)) #Test
    
    blogPostImages = blog.models.BlogPostImage.objects.filter(blogPostImage__in=toShowURLs)
    print("blogPostImages: " + str(blogPostImages)) #Test

    allBlogCategoryBridge = blog.models.BlogPostCategory.objects.all().order_by('id')
    postIDsinBridgeCatList =list(allBlogCategoryBridge.values_list('blogPostID_id', flat=True))
    allCategories = blog.models.Category.objects.all().order_by('id')
    allCategoriesByName = allCategories.order_by('name')
    allDatePublishedList = list(allBlogPosts.values_list('datePublished', flat=True).distinct().order_by('-datePublished'))
    allYearList = [0]
    
    for dp in allDatePublishedList:
        if dp.year not in allYearList:
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
        'blogPostImages': blogPostImages,
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

    allBlogPosts = blog.models.BlogPost.objects.filter(delete=False).order_by('id') #no filter sidebar or no filter type or page refreshed
    allBlogCategoryBridge = blog.models.BlogPostCategory.objects.all().order_by('id')
    postIDswithImageList = list(blog.models.BlogPostImage.objects.all().order_by('id').values_list('blogPostID_id', flat=True))
    # print("postIDswithImageList: " + str(postIDswithImageList)) #Test
    allBlogPostImages = blog.models.BlogPostImage.objects.all().order_by('id')
    # print("allBlogPostImages:"  + str(allBlogPostImages)) #Test
    toAddIds = []
    toShowURLs = []

    for image in allBlogPostImages:
        # print("image: " + str(image)) #Test
        if image.blogPostID_id not in toAddIds:
            # print("-- first picture for post id " + str(image.blogPostID_id)) #Test
            toAddIds.append(image.blogPostID_id)
            toShowURLs.append(image.blogPostImage)
            # print("updated toAddIds: " + str(toAddIds)) #Test
            # print("updated toShowURLs: " + str(toShowURLs)) #Test
    
    blogPostImages = blog.models.BlogPostImage.objects.filter(blogPostImage__in=toShowURLs)
    # print("blogPostImages: " + str(blogPostImages)) #Test
    allCategories = blog.models.Category.objects.all().order_by('id')
    allCategoriesByName = allCategories.order_by('name')
    allDatePublishedList = list(allBlogPosts.values_list('datePublished', flat=True).distinct().order_by('-datePublished'))
    allYearList = ['0'] # string

    for dp in allDatePublishedList:
        if str(dp.year) not in allYearList:
            allYearList.append(str(dp.year))

    if request.method == 'POST':
        # print("[POST]") #Test
        if request.is_ajax():
            # print("[ajax]") #Test
            title_text = request.POST['title_text']
            # print("title_text: " + str(title_text)) #Test
            cat_selected = request.POST['cat_selected']
            # print("cat_selected: " + str(cat_selected)) #Test
            yearSelectedList = request.POST.getlist('yearSelectedList[]') #returned in string
            # print("yearSelectedList: " + str(yearSelectedList)) #Test

            # print("user_type: " + user_type)
            if user_type == 'admin':
                typeSelected = request.POST['typeSelected']
                # print("typeSelected type string?: " + str(isinstance(typeSelected, str))) #Test
                # print("typeSelected: " + str(typeSelected)) #Test

            if request.POST['requestType'] == 'submitFormSidebar':
                context = {
                    'user_id': user_id,
                    'user_type': user_type,
                    'allCategoriesByName': allCategoriesByName,
                    'allYearList': allYearList,
                    'title_text': title_text,
                    'cat_selected': cat_selected,
                    'yearSelectedList': yearSelectedList
                }

                return render(request, 'blog/updateFormSidebar.html', context)
    else: #GET
        # print("[GET]") #Test
        if request.is_ajax():
            # print("[ajax]") #Test
            # print("requestType: " + request.GET.get('requestType')) #Test
            title_text = request.GET.get('title_text', None)
            # print("title_text: " + str(title_text)) #Test
            cat_selected = request.GET.get('cat_selected', None)
            # print("cat_selected: " + str(cat_selected)) #Test
            yearSelectedList = request.GET.getlist('yearSelectedList[]') #returned in string
            # print("yearSelectedList: " + str(yearSelectedList)) #Test

            if user_type == 'admin':
                # print("this is admin") #Test
                typeSelected = request.GET.get('typeSelected', None)
                # print("typeSelected type string?: " + str(isinstance(typeSelected, str))) #Test
                # print("typeSelected: " + str(typeSelected)) #Test

            if title_text != '':
                allBlogPosts = allBlogPosts.filter(title__icontains=title_text)
                # print("(1) after title filter: " + str(list(allBlogPosts.values_list('id', flat=True)))) #Test

            if cat_selected is not None:
                if cat_selected != 'Semua':
                    cat_selected_ID = allCategories.get(name = cat_selected).id
                    postIDsList = list(allBlogCategoryBridge.filter(categoryID_id=cat_selected_ID).values_list('blogPostID_id', flat=True))
                    allBlogPosts = allBlogPosts.filter(id__in=postIDsList)
                    # print("(2) after category filter: " + str(list(allBlogPosts.values_list('id', flat=True)))) #Test
            
            currentDatePublishedList = []

            if yearSelectedList:
                if '0' not in yearSelectedList:
                    for year in yearSelectedList:
                        for post in allBlogPosts:
                            # print("ID: " + str(post.id) + ", year: " + str(post.datePublished.year)) #Test
                            if year == str(post.datePublished.year):
                                currentDatePublishedList.append(post.datePublished)
                    allBlogPosts = allBlogPosts.filter(datePublished__in=currentDatePublishedList)
                    # print("(3) after year filter: " + str(list(allBlogPosts.values_list('id', flat=True)))) #Test
            
            if user_type == 'admin':
                if typeSelected != 'Semua Artikel':
                    if typeSelected == 'Telah Diterbitkan':
                        allBlogPosts = allBlogPosts.filter(show=True)
                    elif typeSelected == 'Draf':
                        allBlogPosts = allBlogPosts.filter(show=False)
                    # print("(4 admin) after type filter: " + str(list(allBlogPosts.values_list('id', flat=True)))) #Test
            else:
                allBlogPosts = allBlogPosts.filter(show=True)
                # print("(4 non-admin) after type filter: " + str(list(allBlogPosts.values_list('id', flat=True)))) #Test
            
            allBlogPosts = allBlogPosts.order_by('-datePublished', '-timePublished')
            # print("(5) after sort date & time desc: " + str(list(allBlogPosts.values_list('id', flat=True)))) #Test

            if request.GET.get('requestType') == 'submitFormPostType_1':
                context = {
                    'user_id': user_id,
                    'user_type': user_type,
                    'typeSelected': typeSelected
                }

                return render(request, 'blog/updateDivButtons1.html', context)
            elif request.GET.get('requestType') == 'submitFormPostType_2':
                context = {
                    'user_id': user_id,
                    'user_type': user_type,
                    'typeSelected': typeSelected
                }

                return render(request, 'blog/updateDivButtons2.html', context)
            elif request.GET.get('requestType') == 'updateContent':
                context = {
                    'user_id': user_id,
                    'user_type': user_type,
                    'title_text': title_text,
                    'cat_selected': cat_selected,
                    'yearSelectedList': yearSelectedList,
                    'postIDswithImageList': postIDswithImageList,
                    'allBlogPosts': allBlogPosts,
                    'allBlogPostsCount': allBlogPosts.count()
                }

                return render(request, 'blog/updateContent.html', context)
        else: #Page is refreshed/initial load
            # print("[not ajax]") #Test
            title_text = request.GET.get('tajuk', None)
            # print("title_text: " + str(title_text)) #Test
            cat_selected = request.GET.get('kategori', None)
            # print("cat_selected: " + str(cat_selected)) #Test
            yearSelectedList = request.GET.getlist('tahun[]') #returned in string
            # print("yearSelectedList: " + str(yearSelectedList)) #Test

            if user_type == 'admin':
                typeSelected = request.GET.get('jenis-artikel', None)
                # print("typeSelected type: " + str(isinstance(typeSelected, str))) #Test
                # print("typeSelected: " + str(typeSelected)) #Test
            else:
                typeSelected = ""

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
                    allBlogPosts = allBlogPosts.filter(datePublished__in=currentDatePublishedList)
            
            if user_type == 'admin':
                if typeSelected is not None:
                    if typeSelected == 'Telah Diterbitkan':
                        allBlogPosts = allBlogPosts.filter(show=True)
                    elif typeSelected == 'Draf':
                        allBlogPosts = allBlogPosts.filter(show=False)
            else:
                allBlogPosts = allBlogPosts.filter(show=True)
            
            allBlogPosts = allBlogPosts.order_by('-datePublished', '-timePublished')

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
                'blogPostImages': blogPostImages,
                """ 'allBlogCategoryBridge': allBlogCategoryBridge,
                'postIDsinBridgeCatList': postIDsinBridgeCatList, """
                'allCategories': allCategories,
                'allCategoriesByName': allCategoriesByName,
                'allYearList': allYearList,
                'title_text': title_text,
                'cat_selected': cat_selected,
                'yearSelectedList': yearSelectedList,
                'typeSelected': typeSelected,
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
    allBlogPosts = blog.models.BlogPost.objects.filter(show=True, delete=False).order_by('id')
    mostPopularPosts = allBlogPosts.order_by('-noOfViews', 'title')[:3]
    latestPosts = allBlogPosts.order_by('-lastDateEdited', '-lastTimeEdited')[:3]
    postIDswithImageList = list(blog.models.BlogPostImage.objects.all().order_by('id').values_list('blogPostID_id', flat=True))
    currentBlogCategoryBridge = blog.models.BlogPostCategory.objects.filter(blogPostID_id=post_id).order_by('id')
    allCategories = blog.models.Category.objects.all().order_by('id')
    allCategoriesByName = allCategories.order_by('name')
    allDatePublishedList = list(allBlogPosts.values_list('datePublished', flat=True).distinct().order_by('-datePublished'))
    allYearList = [0]
    
    # print("postIDswithImageList: " + str(postIDswithImageList)) #Test

    for dp in allDatePublishedList:
        if dp.year not in allYearList:
            allYearList.append(dp.year)

    currentUserBookmarkPostIDList = list(blog.models.BlogPostBookmark.objects.filter(userID_id=user_id).order_by('id').values_list('blogPostID_id', flat=True))

    if currentUserBookmarkPostIDList:
        if int(post_id) in currentUserBookmarkPostIDList:
            hasBookmark = True
        else:
            hasBookmark = False
    else:
        hasBookmark = False

    #MATCHING PROCESS 1 (Category): get a list of post IDs which are related by category/tag
    commonCategoryIDsList = list(currentBlogCategoryBridge.values_list('categoryID_id', flat=True))
    otherBridge = blog.models.BlogPostCategory.objects.exclude(blogPostID_id=post_id).order_by('id')
    # print(commonCategoryIDsList) #Test
    commonCategoryPostIDsList = []
    relatedPostIDsList = []

    for bridge in otherBridge:
        if bridge.categoryID_id in commonCategoryIDsList:
            if bridge.blogPostID_id not in commonCategoryPostIDsList:
                commonCategoryPostIDsList.append(bridge.blogPostID_id)

    relatedPostIDsList = commonCategoryPostIDsList
    # print(relatedPostIDsList) #Test

    #Create an empty list to append each id with common category matched earlier (for listing ids to be excluded in the next matching process for title)
    #(cannot directly assign the common list to another list bcs it will affect the original common list later)
    toExcludeList = []

    for ids in relatedPostIDsList:
        toExcludeList.append(ids)
        
    toExcludeList.append(int(post_id)) #append current post id too bcs we should not include this id in matching title process

    # print(relatedPostIDsList) #Test
    # print(toExcludeList) #Test

    # LIST OF STOP WORDS for skipping words that are "common" and does not bring distinctive meaning in the title for it to be assumed relative
    stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
    stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
    stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
    stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
    stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
    stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
    stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
    stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
    stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
    stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
    stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
    stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
    stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
    stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
    stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
    stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
    stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
    stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
    stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
    stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
    stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
    stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
    stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
    stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
    stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
    stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
    stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
    stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
    stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
    stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
    stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
    stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
    stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
    stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
    stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
    stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
    stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
    stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
    stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
    stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
    stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
    stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
    stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
    stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
    stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
    stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
    stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
    stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
    stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
    stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
    stopwords += ['yours', 'yourself', 'yourselves']

    for i in range(len(stopwords)):
        sw = stopwords[i]
        stopwords.append(sw.capitalize())

    # print(stopwords) #Test

    #MATCHING PROCESS 2 (Title): append more post IDs which are related by title
    #Omit characters beside letters, digits, spaces, and hyphens (this is for "double" words like Kanak-kanak etc.)
    title = re.split(" ", re.sub('[^A-Za-z0-9- ]+', '', currentBlogPost.title))
    # print(title) #Test

    #List for posts to be checked this process (excluding ids from the toExcludeList earlier)
    toCheckPosts = allBlogPosts.exclude(id__in=toExcludeList)
    # print("toCheckPosts(title): " + str(list(toCheckPosts.values_list('id', flat=True)))) #Test

    #Check if there is any remaining posts to be checked after round 1 matching, proceed if yes
    if toCheckPosts:
        #iterate through each word in current title
        for word in title:
            # print("current word: " + word) #Test
            # print("word not in stopwords: " + str(word not in stopwords)) #Test
            #Check if the current word is a stopword (cap/low), proceed if not
            if word not in stopwords:
                #iterate through each post to be checked
                for post in toCheckPosts:
                    #Two lists of the words in the current other post title (original and lowered case)
                    clean_title = re.split(" ", re.sub('[^A-Za-z0-9- ]+', '', post.title)) 
                    clean_title_low = [each_word.lower() for each_word in clean_title]

                    # print("current clean_title: " + str(clean_title)) #Test
                    # print("current clean_title_low: " + str(clean_title_low)) #Test

                    #Test
                    #1: in case curr title's word is exactly same (spelling, case) as other title's word - eg: all same case usually proper noun (UPU, SPM, Malaysia), numbers (2021)
                    # print("1: " + str(word in clean_title))

                    #2: in case for other title got same word as current title's word but it's lower-cased/capitalized (basically not same case),
                    #we lowered the cases of current title's word to match the originally lower-cased word in other title
                    #or vice-versa
                    #eg:- curr: Notis, other: notis OR curr: notis, other: Notis --> both become notis (same no matter which word has which case)
                    # print("2: " + str(word.lower() in clean_title_low))

                    #if any of the condition is met, proceed to add current other post id to our related id list
                    #also to include the added id to our toExcludeList so that for next word(s) in current title (real title),
                    #we wont need to check for any match in the post added earlier (bc that post already have match so why check more than once?)
                    if (word in clean_title) or (word.lower() in clean_title_low):
                        # print("postid_other: " + str(post.id)) #Test
                        # print("masuk tak: " + str(post.id not in relatedPostIDsList)) #Test
                        relatedPostIDsList.append(post.id)

                        toExcludeList.append(post.id)
                        # print("updated toExcludeList(title): " + str(toExcludeList)) #Test
                        toCheckPosts = allBlogPosts.exclude(id__in=toExcludeList)
                        # print("updated toCheckPosts(title): " + str(list(toCheckPosts.values_list('id', flat=True)))) #Test

    # print("posts after check title: " + str(relatedPostIDsList)) #Test

    #Getting random related ids (3 max)
    if relatedPostIDsList:
        min_id = min(relatedPostIDsList)
        max_id = max(relatedPostIDsList)
        randomIDList = []
        randomID = 0
        limit = 3

        if len(relatedPostIDsList) <= limit: 
            # print(len(relatedPostIDsList)) #Test
            relatedPosts = allBlogPosts.filter(id__in=relatedPostIDsList)
        else:
            # print(len(relatedPostIDsList))
            while len(randomIDList) < limit:
                randomID = randint(min_id, max_id)
                # print("1: chosen randomID: " + str(randomID)) #Test
                
                #Test
                # print("if 1: " + str(randomID not in relatedPostIDsList)) #generated random ID exists in the related id list?
                # print("if 2: " + str(randomID in randomIDList)) #generated random ID already added to the final random id list?

                #if either one true (we only want ids that exist in related id list or ids that havent been added in our final list)
                while (randomID not in relatedPostIDsList) or (randomID in randomIDList):
                    randomID = randint(min_id, max_id)
                    # print("2: chosen randomID: " + str(randomID)) #Test

                randomIDList.append(randomID)
                # print("length: " + str(len(randomIDList))) #Test

            relatedPosts = allBlogPosts.filter(id__in=randomIDList)
    else:
        relatedPosts = allBlogPosts
 
    finalRelatedPostIDList = list(relatedPosts.values_list('id', flat=True))
    # print("final related posts: " + str(finalRelatedPostIDList)) #Test

    #GET list of images to display
    allRelatedPostImages = blog.models.BlogPostImage.objects.filter(blogPostID_id__in=finalRelatedPostIDList)
    # print("allRelatedPostImages:"  + str(allRelatedPostImages)) #Test
    toAddIds = []
    toShowURLs = []

    for image in allRelatedPostImages:
        # print("image: " + str(image)) #Test
        if image.blogPostID_id not in toAddIds:
            # print("-- first picture for post id " + str(image.blogPostID_id)) #Test
            toAddIds.append(image.blogPostID_id)
            toShowURLs.append(image.blogPostImage)
            # print("updated toAddIds: " + str(toAddIds)) #Test
            # print("updated toShowURLs: " + str(toShowURLs)) #Test
    
    relatedPostImages = blog.models.BlogPostImage.objects.filter(blogPostImage__in=toShowURLs)
    # print("blogPostImages: " + str(relatedPostImages)) #Test

    #COMMENT
    allCurrentPostComments = blog.models.BlogPostComment.objects.filter(blogPostID_id=post_id).order_by('dateTimeComment')
    commentCount = allCurrentPostComments.count()

    # print("comment cnt: " + str(commentCount)) #Test

    #for img-user in add comment (outer)
    if user_type == 'pelajar':
        currentPlayerRecordObject = quiz.models.Player.objects.get(ID=user_id)
        currentAvatarDetailsObject = currentPlayerRecordObject.avatarID
    else:
        currentAvatarDetailsObject = currentUserDetail #Will not be used, this is just for allowing context part below to pass for admin

    #for img-user-inner for all comments/replies from students
    allPlayerRecords = quiz.models.Player.objects.all().order_by('ID')

    #get list of parent comment IDs which have replies 
    parentCmtIDsWithReplies_all = list(blog.models.BlogPostComment.objects.filter(parentCommentID_id__isnull=False).values_list('parentCommentID_id', flat=True))
    parentCmtIDsWithReplies_set = set(parentCmtIDsWithReplies_all)
    parentCmtIDsWithReplies = (list(parentCmtIDsWithReplies_set))

    # print(str(parentCmtIDsWithReplies)) #Test

    if request.method == 'POST':
        if request.is_ajax():
            if request.POST['requestType'] == 'deletePost':
                # print("hi")
                currentBlogCategoryBridgeIDList = list(blog.models.BlogPostCategory.objects.filter(blogPostID_id=post_id).values_list('blogPostID_id', flat=True))
                currentBlogBookmarkIDList = list(blog.models.BlogPostBookmark.objects.filter(blogPostID_id=post_id).values_list('blogPostID_id', flat=True))
                currentBlogCommentIDList = list(blog.models.BlogPostComment.objects.filter(blogPostID_id=post_id).values_list('blogPostID_id', flat=True))
                currentBlogViewsUserIDList = list(blog.models.BlogPostViewsUser.objects.filter(blogPostID_id=post_id).values_list('blogPostID_id', flat=True))
                allBlogPostImageTemp = blog.models.BlogPostImageTemp.objects.all()
                currentBlogImageIDList = list(blog.models.BlogPostImage.objects.filter(blogPostID_id=post_id).values_list('blogPostID_id', flat=True))

                #delete blog category bridge records for current blog ID if current blog post exist in blogPostCategory table
                if int(post_id) in currentBlogCategoryBridgeIDList:
                    # print("(1a) currentBlogCategoryBridgeIDList: " + str(currentBlogCategoryBridgeIDList)) #Test

                    blog.models.BlogPostCategory.objects.filter(blogPostID_id=post_id).delete()

                    currentBlogCategoryBridgeIDList = list(blog.models.BlogPostCategory.objects.filter(blogPostID_id=post_id).values_list('blogPostID_id', flat=True)) #Test
                    # print("(1b) currentBlogCategoryBridgeIDList: " + str(currentBlogCategoryBridgeIDList)) #Test
                
                #delete blog bookmark records for current blog ID if current blog post exist in blogPostBookmark table
                if int(post_id) in currentBlogBookmarkIDList:
                    # print("(2a) currentBlogBookmarkIDList: " + str(currentBlogBookmarkIDList)) #Test

                    blog.models.BlogPostBookmark.objects.filter(blogPostID_id=post_id).delete()

                    currentBlogBookmarkIDList = list(blog.models.BlogPostBookmark.objects.filter(blogPostID_id=post_id).values_list('blogPostID_id', flat=True)) #Test
                    # print("(2b) currentBlogBookmarkIDList: " + str(currentBlogBookmarkIDList)) #Test

                #delete blog comment records for current blog ID if current blog post exist in blogPostComment table
                if int(post_id) in currentBlogCommentIDList:
                    # print("(3a) currentBlogCommentIDList: " + str(currentBlogCommentIDList)) #Test

                    blog.models.BlogPostComment.objects.filter(blogPostID_id=post_id).delete()

                    currentBlogCommentIDList = list(blog.models.BlogPostComment.objects.filter(blogPostID_id=post_id).values_list('blogPostID_id', flat=True)) #Test
                    # print("(3b) currentBlogCommentIDList: " + str(currentBlogCommentIDList)) #Test
                
                #delete blog views user records for current blog ID if current blog post exist in blogPostViewsUser table
                if int(post_id) in currentBlogViewsUserIDList:
                    # print("(4a) currentBlogViewsUserIDList: " + str(currentBlogViewsUserIDList)) #Test

                    blog.models.BlogPostViewsUser.objects.filter(blogPostID_id=post_id).delete()

                    currentBlogViewsUserIDList = list(blog.models.BlogPostViewsUser.objects.filter(blogPostID_id=post_id).values_list('blogPostID_id', flat=True)) #Test
                    # print("(4b) currentBlogViewsUserIDList: " + str(currentBlogViewsUserIDList)) #Test
                
                #delete blog image temp records for url consisting current blog id
                for imageTempRecord in allBlogPostImageTemp:
                    imageTempURL = str(imageTempRecord.blogPostImage)
                    # print("(5a) id portion: " + imageTempURL[:imageTempURL.index("-")]) #Test
                    if str(post_id) ==  imageTempURL[:imageTempURL.index("-")]:
                        # print("(5b) yes") #Test
                        blog.models.BlogPostImageTemp.objects.filter(blogPostImage=imageTempRecord.blogPostImage).delete()

                    # print("(5b) currentBlogImageIDList: " + str(currentBlogImageIDList)) #Test
                    # currentBlogImageIDList = list(blog.models.BlogPostImage.objects.filter(blogPostID_id=post_id).values_list('blogPostID_id', flat=True))

                #delete blog image records for current blog ID if current blog post exist in blogPostImage table
                if int(post_id) in currentBlogImageIDList:
                    # print("(6a) currentBlogImageIDList: " + str(currentBlogImageIDList)) #Test

                    blog.models.BlogPostImage.objects.filter(blogPostID_id=post_id).delete()

                    # print("(6b) currentBlogImageIDList: " + str(currentBlogImageIDList)) #Test
                    currentBlogImageIDList = list(blog.models.BlogPostImage.objects.filter(blogPostID_id=post_id).values_list('blogPostID_id', flat=True))

                currentBlog = blog.models.BlogPost.objects.get(id=post_id)
                currentBlog.show = False
                currentBlog.delete = True
                currentBlog.save()

                context = {
                    'doneDelete': 'Yes'
                }

                return JsonResponse(context)
            elif request.POST['requestType'] == 'deleteComment': # Delete comment or reply
                # print("hi")
                commentIDToDelete = request.POST['commentID']
                currentBlogCommentIDList = list(blog.models.BlogPostComment.objects.filter(blogPostID_id=post_id).values_list('blogPostID_id', flat=True))

                # print("commentIDToDelete: " + str(commentIDToDelete)) #Test

                blog.models.BlogPostComment.objects.get(id=commentIDToDelete).delete()

                context = {
                    'doneDeleteComment': 'Yes'
                }

                return JsonResponse(context)
            elif request.POST['requestType'] == 'addBookmark':
                blog.models.BlogPostBookmark.objects.create(blogPostID_id=post_id, userID_id=user_id)
                hasBookmark = True
                context = {'hasBookmark': hasBookmark}
                
                return render(request, 'blog/updateBookmark.html', context)
            elif request.POST['requestType'] == 'removeBookmark':
                blog.models.BlogPostBookmark.objects.get(blogPostID_id=post_id, userID_id=user_id).delete()
                hasBookmark = False
                context = {'hasBookmark': hasBookmark}

                return render(request, 'blog/updateBookmark.html', context)
            elif request.POST['requestType'] == 'addComment_1':
                newComment = request.POST['newComment']
                currentDateTime = datetime.now 
                newComment = blog.models.BlogPostComment.objects.create(text=newComment, blogPostID_id=post_id, userID_id=user_id, dateTimeComment=currentDateTime)
                
                #create notification (Type id 1 - New comment (for admin ONLY))
                if newComment.userID_id != 'A1':
                    dashboard.models.Notification.objects.create(senderID_id=newComment.userID_id, recipientID_id='A1', blogPostID_id=newComment.blogPostID_id, blogPostCommentID_id=newComment.id, typeID_id=1)

                allCurrentPostComments = blog.models.BlogPostComment.objects.filter(blogPostID_id=post_id).order_by('dateTimeComment')
                commentCount = allCurrentPostComments.count()
                # print("updated comment cnt: " + str(commentCount)) #Test

                context = {
                    'commentCount': commentCount
                }

                return JsonResponse(context)
            elif request.POST['requestType'] == 'addComment_2':
                allCurrentPostComments = blog.models.BlogPostComment.objects.filter(blogPostID_id=post_id).order_by('dateTimeComment')
                newCommentID = allCurrentPostComments.filter(parentCommentID_id__isnull=True, userID_id=user_id).order_by('-id').first().id
                # print("new comment id: " + str(newCommentID)) #Test

                context = {
                    'user_id': user_id,
                    'user_type': user_type,
                    'post_id': int(post_id),
                    'allCurrentPostComments': allCurrentPostComments,
                    'newCommentID': str(newCommentID),
                    'currentAvatarDetailsObject': currentAvatarDetailsObject,
                    'allPlayerRecords': allPlayerRecords,
                    'parentCmtIDsWithReplies': parentCmtIDsWithReplies
                }

                return render(request, 'blog/updateComment.html', context)
            elif request.POST['requestType'] == 'addReply_1': #update replied-to details in modal
                repliedParentID = request.POST['repliedParentID'] #Parent comment ID (available for both repliedTo Parent or Child)
                repliedChildID = request.POST['repliedChildID'] #Child comment ID (repliedTo Parent: 0, repliedTo Child: available)
                repliedTo = request.POST['repliedTo'] #'Parent' or 'Child'
                # print("replied parent id_1: " + str(repliedParentID)) #Test
                # print("replied child id_1: " + str(repliedChildID)) #Test
                # print("replied to_1: " + repliedTo) #Test

                if repliedTo == 'Parent':
                    repliedComment = blog.models.BlogPostComment.objects.get(id=repliedParentID) #Parent comment ID
                    # print("repliedParentComment:" + str(repliedComment.id)) #Test
                elif repliedTo == 'Child':
                    repliedComment = blog.models.BlogPostComment.objects.get(id=repliedChildID) #Child comment ID
                    # print("repliedChildComment: " + str(repliedComment.id)) #Test

                repliedText = repliedComment.text
                repliedUsername = repliedComment.userID.username
                # print("repliedText: " + repliedText) #Test
                # print("repliedUsername: " + repliedUsername) #Test

                context = {
                    'repliedParentID': repliedParentID,
                    'repliedChildID': repliedChildID,
                    'repliedTo': repliedTo,
                    'repliedUsername': repliedUsername,
                    'repliedText': repliedText
                }

                return JsonResponse(context)
            elif request.POST['requestType'] == 'addReply_2': #update total comment count in viewPost.html
                newReply = request.POST['newReply'] #New reply to parent or child comment
                repliedTo = request.POST['repliedTo'] #'Parent' or 'Child'
                # print("new reply: " + newReply) #Test
                # print("replied to_2: " + repliedTo) #Test
                repliedParentID = request.POST['repliedParentID'] #Parent comment ID (available for both repliedTo Parent or Child)
                repliedChildID = request.POST['repliedChildID'] #Child comment ID (repliedTo Parent: 0, repliedTo Child: available)
                # repliedComment = allCurrentPostComments.get(id=repliedCommentID)
                # newParentReply = '@' + repliedComment.userID.username + ' ' + newParentReply
                # print("new parent reply with @: " + newParentReply) #Test
                # print("replied parent id_2: " + str(repliedParentID)) #Test
                # print("replied child id_2: " + str(repliedChildID)) #Test

                currentDateTime = datetime.now 
                if repliedTo == 'Parent': #No need to add childCommentID_id
                    newReply = blog.models.BlogPostComment.objects.create(text=newReply, blogPostID_id=post_id, parentCommentID_id=repliedParentID, userID_id=user_id, dateTimeComment=currentDateTime)

                    #create notification (Type id 2 - New reply (to main comment))
                    parentCommentRecord = blog.models.BlogPostComment.objects.get(id=newReply.parentCommentID_id)

                    # if its not the admin replying to the admin's comment (such as correcting typos etc.)
                    if newReply.userID_id != 'A1':
                        dashboard.models.Notification.objects.create(senderID_id=newReply.userID_id, recipientID_id=parentCommentRecord.userID_id, blogPostID_id=newReply.blogPostID_id, blogPostCommentID_id=newReply.parentCommentID_id, blogCommentReplyID_id=newReply.id, typeID_id=2)
                elif repliedTo == 'Child': #Need to add childCommentID_id
                    newReply = blog.models.BlogPostComment.objects.create(text=newReply, blogPostID_id=post_id, parentCommentID_id=repliedParentID, childCommentID_id=repliedChildID, userID_id=user_id, dateTimeComment=currentDateTime)

                    #create notification (Type id 2 - New reply (to child comment))
                    childCommentRecord = blog.models.BlogPostComment.objects.get(id=newReply.childCommentID_id)
                    
                    # if its not the admin replying to the admin's reply (such as correcting typos etc.)
                    if newReply.userID_id != 'A1':
                        dashboard.models.Notification.objects.create(senderID_id=newReply.userID_id, recipientID_id=childCommentRecord.userID_id, blogPostID_id=newReply.blogPostID_id, blogPostCommentID_id=newReply.parentCommentID_id, blogCommentReplyID_id=newReply.id, typeID_id=2)

                allCurrentPostComments = blog.models.BlogPostComment.objects.filter(blogPostID_id=post_id).order_by('dateTimeComment')
                commentCount = allCurrentPostComments.count()
                # print("updated comment cnt: " + str(commentCount)) #Test

                context = {
                    'commentCount': commentCount
                }

                return JsonResponse(context)
            elif request.POST['requestType'] == 'addReply_3': #update whole comment content with new parent reply
                repliedParentID = request.POST['repliedParentID'] #Parent comment ID (available for both repliedTo Parent or Child)
                repliedChildID = request.POST['repliedChildID'] #Child comment ID (repliedTo Parent: 0, repliedTo Child: available)
                # print("replied parent id_3: " + str(repliedParentID)) #Test
                # print("replied child id_3: " + str(repliedChildID)) #Test
                repliedTo = request.POST['repliedTo'] #'Parent' or 'Child'
                # print("replied to_3: " + repliedTo) #Test

                allCurrentPostComments = blog.models.BlogPostComment.objects.filter(blogPostID_id=post_id).order_by('dateTimeComment')
                
                if repliedTo == 'Parent': #No need to add childCommentID_id
                    newCommentID = allCurrentPostComments.filter(parentCommentID_id=repliedParentID, userID_id=user_id).order_by('-id').first().id
                elif repliedTo == 'Child': #Need to add childCommentID_id
                    newCommentID = allCurrentPostComments.filter(parentCommentID_id=repliedParentID, childCommentID_id=repliedChildID, userID_id=user_id).order_by('-id').first().id
                
                # print("new comment id: " + str(newCommentID)) #Test

                #get list of parent comment IDs which have replies (UPDATE)
                parentCmtIDsWithReplies_all = list(blog.models.BlogPostComment.objects.filter(parentCommentID_id__isnull=False).values_list('parentCommentID_id', flat=True))
                parentCmtIDsWithReplies_set = set(parentCmtIDsWithReplies_all)
                parentCmtIDsWithReplies = (list(parentCmtIDsWithReplies_set))
                # print("updated parentCmtIDsWithReplies: " + str(parentCmtIDsWithReplies)) #Test

                context = {
                    'user_id': user_id,
                    'user_type': user_type,
                    'post_id': int(post_id),
                    'repliedTo': repliedTo,
                    'allCurrentPostComments': allCurrentPostComments,
                    'newCommentID': str(newCommentID),
                    'currentAvatarDetailsObject': currentAvatarDetailsObject,
                    'allPlayerRecords': allPlayerRecords,
                    'parentCmtIDsWithReplies': parentCmtIDsWithReplies
                }

                return render(request, 'blog/updateComment.html', context)
    else: #GET
        if request.is_ajax():
            sort_order = request.GET.get('sort_order', None)
            
            if sort_order == 'Terkini':
                allCurrentPostComments = blog.models.BlogPostComment.objects.filter(blogPostID_id=post_id).order_by('-dateTimeComment')
            elif sort_order == 'Paling Lama':
                allCurrentPostComments = blog.models.BlogPostComment.objects.filter(blogPostID_id=post_id).order_by('dateTimeComment')

            context = {
                    'user_id': user_id,
                    'user_type': user_type,
                    'post_id': int(post_id),
                    'allCurrentPostComments': allCurrentPostComments,
                    'newCommentID': '0', #no need to find current user's latest parent ID for sorting - will always show from top again
                    'currentAvatarDetailsObject': currentAvatarDetailsObject,
                    'allPlayerRecords': allPlayerRecords,
                    'parentCmtIDsWithReplies': parentCmtIDsWithReplies
                }

            return render(request, 'blog/updateComment.html', context)
        else: #Refreshed
            #increment views
            currentViews = currentBlogPost.noOfViews
            currentUserViewRecord = blog.models.BlogPostViewsUser.objects.get_or_create(blogPostID_id=post_id, userID_id=user_id)[0]
            currentUserViews = currentUserViewRecord.noOfViews
            # print("total views: " + str(currentBlogPost.noOfViews)) #Test
            # print("curr user views: " + str(currentUserViewRecord.noOfViews)) #Test
            currentBlogPost.noOfViews = currentViews + 1
            currentUserViewRecord.noOfViews = currentUserViews + 1
            currentBlogPost.save()
            currentUserViewRecord.save()
            # print("updated total views: " + str(currentBlogPost.noOfViews)) #Test
            # print("updated curr user views: " + str(currentUserViewRecord.noOfViews)) #Test

            #Views list
            allUserViews = blog.models.BlogPostViewsUser.objects.filter(blogPostID_id=post_id).order_by('-noOfViews')
            
            adminViews = allUserViews.filter(userID_id='A1')
            studentViews = allUserViews.filter(userID_id__ID__contains='S')
            parentViews = allUserViews.filter(userID_id__ID__contains='P')
            teacherViews = allUserViews.filter(userID_id__ID__contains='T')
            userCnt = [adminViews.count(), studentViews.count(), parentViews.count(), teacherViews.count()]

            userViewsCnt = [
                (adminViews.aggregate(Sum('noOfViews')))['noOfViews__sum'],
                (studentViews.aggregate(Sum('noOfViews')))['noOfViews__sum'],
                (parentViews.aggregate(Sum('noOfViews')))['noOfViews__sum'],
                (teacherViews.aggregate(Sum('noOfViews')))['noOfViews__sum']
            ]

            userViewsCnt = np.array(userViewsCnt)
            userViewsCnt[userViewsCnt==None] = 0

            # print("userCnt: " + str(userCnt)) #Test
            # print("userViewsCnt: " + str(userViewsCnt)) #Test

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
                'hasBookmark': hasBookmark,
                'adminViews': adminViews,
                'studentViews': studentViews,
                'parentViews': parentViews,
                'teacherViews': teacherViews,
                'userCnt': userCnt,
                'userViewsCnt': userViewsCnt,
                'relatedPostIDsList': relatedPostIDsList,
                'relatedPosts': relatedPosts,
                'relatedPostImages': relatedPostImages,
                'allCurrentPostComments': allCurrentPostComments,
                'commentCount': commentCount,
                'currentAvatarDetailsObject': currentAvatarDetailsObject,
                'allPlayerRecords': allPlayerRecords,
                'parentCmtIDsWithReplies': parentCmtIDsWithReplies,
                'newCommentID': '0' #For refreshed page only
            }
            return render(request, 'blog/viewPost.html', context)

@csrf_exempt
def upload_image(request, user_type, user_id, post_id):
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_obj.name = re.sub('[ ]+', '_', file_obj.name)
        # print("filename after sub with -: " + file_obj.name) #Test
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "Wrong file format"})

        # print("post_id: " + str(post_id)) #Test

        # If for editPost
        if int(post_id) != 0:
            # print("hi") #Test
            # newImageURL = post_id + '-' + file_obj.name
            file_obj.name = post_id + '-' + file_obj.name
            # print("filename after add current id: " + file_obj.name) #Test
        else:
            # print("hi2") #Test
            latestBlogPost = blog.models.BlogPost.objects.order_by('id').last()
            # newImageURL = str(int(latestBlogPost.id) + 1) + '-' + file_obj.name
            file_obj.name = str(int(latestBlogPost.id) + 1) + '-' + file_obj.name
            # print("filename after add new id: " + file_obj.name) #Test

        blogPostImageTempURls = list(blog.models.BlogPostImageTemp.objects.all().values_list('blogPostImage', flat=True))

        nameInDB = 'images/admin_post_images_temp/' + file_obj.name

        # if newImageURL not in blogPostImageTempURls:
        # if nameInDB not in blogPostImageTempURls:
            # newImageTemp = blog.models.BlogPostImageTemp.objects.create(blogPostImage=newImageURL)
        newImageTemp = blog.models.BlogPostImageTemp.objects.create(blogPostImage=file_obj)
        # print("newly added image temp: " + str(newImageTemp.blogPostImage)) #Test

        """ path = os.path.join(
            settings.MEDIA_ROOT,
            'images',
            'admin_post_images_temp'
            'admin_post_images'
        ) """

        path = settings.MEDIA_ROOT

        # If there is no such path, create
        if not os.path.exists(path):
            os.makedirs(path)

        # file_path = os.path.join(path, newImageURL)
        # file_path = os.path.join(path, file_obj.name)
        file_path = os.path.join(path, newImageTemp.blogPostImage.name)
        # print("file_path: " + str(file_path)) #Test

        # file_url = f'{settings.MEDIA_URL}images/admin_post_images/{newImageURL}'
        file_url = f'{settings.MEDIA_URL}{newImageTemp.blogPostImage.name}'
        # print("file_url: " + str(file_url)) #Test

        if os.path.exists(file_path):
            return JsonResponse({
                "message": "Anda tidak dibenarkan untuk memuat naik gambar yang sama",
                'location': file_url
            })

        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        return JsonResponse({
            'message': 'Gambar berjaya dimuat naik',
            'location': file_url
        })
        """ else:
            return JsonResponse({
                    'message': "Anda tidak dibenarkan untuk memuat naik gambar yang sama. Sila pastikan bahawa nama fail gambar yang yang hendak dimuatnaik adalah berbeza daripada nama fail gambar-gambar sedia ada bagi artikel ini.",
                }) """
    return JsonResponse({'detail': "Wrong request"})

def addPost(request, user_type, user_id):
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

    if request.method == 'POST':
        # print("hi")
        form = AddPostForm(request.POST)
        if form.is_valid():
            # print("valid")
            filledList = form.cleaned_data
            filledTitle = filledList['title']
            filledCategories = request.POST.getlist('category')
            filledNewCategories = filledList['new_category']
            filledDesc = filledList['description']
            filledContent = filledList['content']

            filledContent = filledContent.replace("../../../../../", "../../../../../../")

            filledIsDraft = filledList['isDraft']
            # print("filledIsDraft: " + str(filledIsDraft)) #Test

            # print("filledCategories: " + str(filledCategories)) #Test
            
            filledCategoriesIDList = []

            for choice in filledCategories:
                # print("choice: " + choice) #Test
                if int(choice) != 1:
                    # print("int(choice) != 1")
                    filledCategoriesIDList.append(int(choice))

            # print("filledCategoriesIDList: " + str(filledCategoriesIDList)) #Test

            finalCategoriesIDList = []
            allCategoriesName = list(blog.models.Category.objects.all().values_list('name', flat=True).order_by('name'))

            if filledNewCategories:
                newCategoriesNameList = re.split(", ", filledNewCategories)
                newCategoriesIDList = []

                for newCat in newCategoriesNameList:
                    if newCat in allCategoriesName:
                        # print("yes") #Test
                        filledCategoriesIDList.append(1) #For 'others'
                        # print("filledCategoriesIDList: " + str(filledCategoriesIDList)) #Test
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
                            'form': form,
                            'filledCategoriesIDList': filledCategoriesIDList,
                            'errorNewCat': "Nama kategori baharu (" + newCat + ") yang dimasukkan telah wujud. Sila masukkan nama kategori yang lain."
                        }
                        return render(request, 'blog/addPost.html', context)

                for newCat in newCategoriesNameList:
                    newCat_2 = ""
                    newCatSplit = re.split(" ", newCat)
                    for i in range(len(newCatSplit)):
                        if i != len(newCatSplit)-1:
                            if newCatSplit[i].isupper() == True:
                                newCat_2 += newCatSplit[i] + " "
                            else:
                                newCat_2 += newCatSplit[i].capitalize() + " "
                        else:
                            if newCatSplit[i].isupper() == True:
                                newCat_2 += newCatSplit[i]
                            else:
                                newCat_2 += newCatSplit[i].capitalize()

                    newCategory = blog.models.Category.objects.create(name=newCat_2)
                    newCategoriesIDList.append(newCategory.id)

                finalCategoriesIDList = filledCategoriesIDList + newCategoriesIDList
            else:
                finalCategoriesIDList = filledCategoriesIDList

            if filledIsDraft == True:
                # print("filledIsDraft: True") #Test
                newPost = blog.models.BlogPost.objects.create(title=filledTitle, content=filledContent, description=filledDesc, show=False)
            else:
                # print("filledIsDraft: False") #Test
                newPost = blog.models.BlogPost.objects.create(title=filledTitle, content=filledContent, description=filledDesc, show=True)
            newPost.lastDateEdited = newPost.datePublished
            newPost.lastTimeEdited = newPost.timePublished
            newPost.save()

            for catID in finalCategoriesIDList:
                blog.models.BlogPostCategory.objects.create(blogPostID_id=newPost.id, categoryID_id=catID)

            # Saving image
            blogPostImageTempURLs = list(blog.models.BlogPostImageTemp.objects.all().values_list('blogPostImage', flat=True))
            # print("blogPostImageTempURLs: " + str(blogPostImageTempURLs)) #Test

            for imageTempURL in blogPostImageTempURLs:
                # print("id portion: " + imageTempURL[30:imageTempURL.index("-")]) #Test
                # print("imageTempURL: " + imageTempURL) #Test
                if str(newPost.id) == imageTempURL[30:imageTempURL.index("-")]:
                    # print("Yes") #Test
                    blog.models.BlogPostImage.objects.create(blogPostImage=imageTempURL, blogPostID_id=newPost.id)

            return redirect('blog:view-post', user_type, user_id, newPost.id)
        else: #Test
            # print("not valid")
            print(form.errors)
    else:
        # print("hi 2")
        form = AddPostForm()

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
        'form': form,
        'post_id': 0
    }
    return render(request, 'blog/addPost.html', context)

def editPost(request, user_type, user_id, post_id):
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

    currentBlogPost = blog.models.BlogPost.objects.get(id=post_id)
    currentTitle = currentBlogPost.title
    allCurrentCategories = blog.models.BlogPostCategory.objects.filter(blogPostID_id=post_id).order_by('id')
    currentCategoriesIDList = list(allCurrentCategories.values_list('categoryID_id', flat=True))
    currentDesc = currentBlogPost.description
    currentContent = currentBlogPost.content
    currentIsDraft = False

    if currentBlogPost.show == True:
        currentIsDraft = False #Initial isDraft tickbox: empty
    else:
        currentIsDraft = True #Initial isDraft tickbox: ticked
    
    #TEST
    # print("(1) currentIsDraft: " + str(currentIsDraft))
    # print("(2) currentTitle: " + currentTitle)
    # print("(3) currentCategoriesIDList: " + str(currentCategoriesIDList))
    # print("(5) currentDesc: " + currentDesc)
    # print("currentContent: " + currentContent)

    if request.method == 'POST':
        # print("hi")
        form = EditPostForm(request.POST, initial={'title': currentTitle, 'description': currentDesc, 'content': currentContent,
        'isDraft': currentIsDraft})
        if form.is_valid():
            # print("valid")
            filledList = form.cleaned_data
            filledTitle = filledList['title']
            filledCategories = request.POST.getlist('category')
            filledNewCategories = filledList['new_category']
            filledDesc = filledList['description']
            filledContent = filledList['content']
            filledIsDraft = filledList['isDraft']

            # print("(1) filledIsDraft: " + str(filledIsDraft)) #Test
            # print("(2) filledTitle: " + filledTitle) #Test

            if filledTitle != currentTitle:
                # print(">>> (2) Title not match") #Test
                currentBlogPost.title = filledTitle

            # print("(3) filledCategories: " + str(filledCategories)) #Test

            filledCategoriesIDList = []

            for choice in filledCategories:
                # print("choice: " + choice) #Test
                if int(choice) != 1:
                    # print("int(choice) != 1") #Test
                    filledCategoriesIDList.append(int(choice))
                    
            # print("(3) filledCategoriesIDList: " + str(filledCategoriesIDList)) #Test

            finalCategoriesIDList = []

            if filledNewCategories:
                # print(">>> (4) Has new categories") #Test
                newCategoriesNameList = re.split(", ", filledNewCategories)
                newCategoriesIDList = []

                # print("(4a) newCategoriesNameList: " + str(newCategoriesNameList)) #Test

                allCategoriesName = list(blog.models.Category.objects.all().values_list('name', flat=True).order_by('name'))

                for newCat in newCategoriesNameList:
                    if newCat in allCategoriesName:
                        # print("yes") #Test
                        filledCategoriesIDList.append(1) #For 'others'
                        # print("filledCategoriesIDList: " + str(filledCategoriesIDList)) #Test
                        context = {
                            'dashboardNav': dashboardNav,
                            'user_id': user_id,
                            'user_type': user_type,
                            'post_id': post_id,
                            'username': username,
                            'test': urlTest,
                            'blog': urlBlog,
                            'quiz': urlQuiz,
                            'search': urlSearch,
                            'dashboard': urlDashboard,
                            'logout': urlLogout,
                            'form': form,
                            'currentBlogPost': currentBlogPost,
                            'currentCategoriesIDList': filledCategoriesIDList,
                            'errorNewCat': "Nama kategori baharu (" + newCat + ") yang dimasukkan telah wujud. Sila masukkan nama kategori yang lain."
                        }
                        return render(request, 'blog/editPost.html', context)

                for newCat in newCategoriesNameList:
                    newCat_2 = ""
                    newCatSplit = re.split(" ", newCat)
                    for i in range(len(newCatSplit)):
                        if i != len(newCatSplit)-1:
                            if newCatSplit[i].isupper() == True:
                                newCat_2 += newCatSplit[i] + " "
                            else:
                                newCat_2 += newCatSplit[i].capitalize() + " "
                        else:
                            if newCatSplit[i].isupper() == True:
                                newCat_2 += newCatSplit[i]
                            else:
                                newCat_2 += newCatSplit[i].capitalize()

                    newCategory = blog.models.Category.objects.create(name=newCat_2)
                    newCategoriesIDList.append(newCategory.id)

                finalCategoriesIDList = filledCategoriesIDList + newCategoriesIDList
            else:
                finalCategoriesIDList = filledCategoriesIDList

            # print("(4b) finalCategoriesIDList: " + str(finalCategoriesIDList)) #Test

            # If count of previous categories and filled are the same
                # If the previous categories not same as after edit (some not same)
                    # Delete current post bridges
                    # Add everything again
            # Else (count not same)
                # Delete current post bridges
                # Add everything again
            if len(finalCategoriesIDList) == len(currentCategoriesIDList):
                # print(">>> (3) Same count category") #Test
                finalCategoriesIDList_2 = finalCategoriesIDList

                finalCategoriesIDList.sort()
                currentCategoriesIDList.sort()

                if finalCategoriesIDList != currentCategoriesIDList:
                    # print(">>> (3) But have changed some categories") #Test
                    allCurrentCategories.delete()

                    for catID in finalCategoriesIDList_2:
                        blog.models.BlogPostCategory.objects.create(blogPostID_id=currentBlogPost.id, categoryID_id=catID)
            else:
                # print(">>> (3) Count category different") #Test
                allCurrentCategories.delete()

                for catID in finalCategoriesIDList:
                    blog.models.BlogPostCategory.objects.create(blogPostID_id=currentBlogPost.id, categoryID_id=catID)

            # print("(5) filledDesc: " + filledDesc) #Test

            if filledDesc != currentDesc:
                # print(">>> (5) Desc not match") #Test
                currentBlogPost.description = filledDesc
            
            if filledContent != currentContent:
                # print(">>> (-) Content not match") #Test
                currentBlogPost.content = filledContent

                #If admin remove any existing pic from post content
                # print("---Deleting removed pics from content---") #Test
                blogPostImageTempURLs = list(blog.models.BlogPostImageTemp.objects.all().values_list('blogPostImage', flat=True))
                blogPostImageURLs = list(blog.models.BlogPostImage.objects.filter(blogPostID_id=currentBlogPost.id).values_list('blogPostImage', flat=True))
                # print("blogPostImageTempURLs: " + str(blogPostImageTempURLs)) #Test
                # print("blogPostImageURLs: " + str(blogPostImageURLs)) #Test

                updatedImageURLList = re.findall('admin_post_images_temp/(.*?)"', filledContent)
                # print("updatedImageURLList: " + str(updatedImageURLList)) #Test

                updatedImageURLListWithPrefixes = []

                for url in updatedImageURLList:
                    updatedImageURLListWithPrefixes.append('images/admin_post_images_temp/' + url)

                # print("updatedImageURLListWithPrefixes: " + str(updatedImageURLListWithPrefixes)) #Test

                toDeleteImageURLs = []

                for i in range(len(blogPostImageURLs)):
                    # print("blogPostImageURLs[" + str(i) + "]: " + blogPostImageURLs[i]) #Test
                    if blogPostImageURLs[i] not in updatedImageURLListWithPrefixes:
                        # print("--removed from content") #Test
                        toDeleteImageURLs.append(blogPostImageURLs[i])
                        # print("updated toDeleteImageURLs: " + str(toDeleteImageURLs)) #Test

                if len(toDeleteImageURLs) > 0:
                    # print("--got urls to delete") #Test
                    blog.models.BlogPostImageTemp.objects.filter(blogPostImage__in=toDeleteImageURLs).delete()
                    blog.models.BlogPostImage.objects.filter(blogPostImage__in=toDeleteImageURLs).delete()
                    # print("blogimageurltemp: " + str(blogPostImageTempURLs)) #Test
                    # print("blogimageurl: " + str(blogPostImageURLs)) #Test

            if filledIsDraft != currentIsDraft:
                # print(">>> (1) isDraft not match") #Test
                currentBlogPost.show = not filledIsDraft
                
            currentBlogPost.lastDateEdited = datetime.now().date()
            currentBlogPost.lastTimeEdited = datetime.now().time()
            currentBlogPost.save()

            blogPostImageTempURLs = list(blog.models.BlogPostImageTemp.objects.all().values_list('blogPostImage', flat=True))
            blogPostImageURLs = list(blog.models.BlogPostImage.objects.filter(blogPostID_id=currentBlogPost.id).values_list('blogPostImage', flat=True))
            # print("blogPostImageTempURLs: " + str(blogPostImageTempURLs)) #Test
            # print("blogPostImageURLs: " + str(blogPostImageURLs)) #Test

            for imageTempURL in blogPostImageTempURLs:
                # print("id portion: " + imageTempURL[30:imageTempURL.index("-")]) #Test
                if str(currentBlogPost.id) in imageTempURL[30:imageTempURL.index("-")]:
                    # print("count imageURL: " + str(blogPostImageURLs.count(imageTempURL))) #Test
                    # print("imageTempURL: " + imageTempURL) #Test
                    if imageTempURL not in blogPostImageURLs:
                        # print("yes") 
                        blog.models.BlogPostImage.objects.create(blogPostImage=imageTempURL, blogPostID_id=currentBlogPost.id)

            return redirect('blog:view-post', user_type, user_id, post_id)
        # else: #Test
            # print("not valid")
            # print(form.errors)
    else:
        # print("hi 2")
        form = EditPostForm(initial={'title': currentTitle, 'description': currentDesc, 'content': currentContent,
        'isDraft': currentIsDraft})

    context = {
        'dashboardNav': dashboardNav,
        'user_id': user_id,
        'user_type': user_type,
        'post_id': post_id,
        'username': username,
        'test': urlTest,
        'blog': urlBlog,
        'quiz': urlQuiz,
        'search': urlSearch,
        'dashboard': urlDashboard,
        'logout': urlLogout,
        'form': form,
        'currentBlogPost': currentBlogPost,
        'currentCategoriesIDList': currentCategoriesIDList
    }
    return render(request, 'blog/editPost.html', context)