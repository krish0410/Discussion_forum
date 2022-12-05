from django.shortcuts import render, HttpResponse, redirect
from .models import Post, replyComment
from django.contrib import messages
from .templatetags import get_dict
from django.utils.timezone import now



def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts':allPosts}
    return render(request,'blog/blogHome.html',context)

def postQuery(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        author = request.user
        slug = title.strip(' ')+content[0:1]
        datestamp = now()
        post = Post(title=title,content=content,author=author,slug=slug)
        post.save()
        messages.success ( request , "Query Posted Successfully" )
        return redirect ( f'/blog/{post.slug}' )
    else:
        return HttpResponse ( '404-Not Found' )


def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    comments = replyComment.objects.filter(post=post,parent=None)
    replies = replyComment.objects.filter(post=post).exclude(parent=None)
    repdict = {}
    for reply in replies:
        if reply.parent.sno not in repdict.keys():
            repdict[reply.parent.sno] = [reply]
        else:
            repdict[reply.parent.sno].append(reply)
    # print(repdict)
    context = {'post':post,'comments':comments,'user':request.user,'repdict':repdict}
    return render(request,'blog/blogPost.html',context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno =="":
            comment = replyComment ( comment=comment , user=user , post=post )
            comment.save ()
            messages.success ( request , "Comment Posted Successfully" )
        else:
            parent = replyComment.objects.get(sno=parentSno)
            comment = replyComment ( comment=comment , user=user , post=post,parent=parent )

            comment.save()
            messages.success(request,"Reply Posted Successfully")

    return redirect(f'/blog/{post.slug}')
