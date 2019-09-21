from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from myapp.models import Userdata,Signup,Userrides,Driverdata,Driversignup
from django.core.mail import send_mail
from django.db import connection
from myapp.forms import LoginForm
from random import randint
from django.contrib.auth import authenticate
import json

def index(request):
    if (request.session.has_key('username')):
        return HttpResponseRedirect('/user')
    elif (request.session.has_key('driverusername')):
        return HttpResponseRedirect('/driver')
    else:
        return render(request,'myapp/index.html')

def mail(emailid,otp):
    try:
        send_mail("FROM CARWITHCARE WEBSITE",'Hi \n Enter the following OTP '+str(otp)+' in website to complete your signup.','girishcse11@gmail.com',[emailid],fail_silently=False)
        txt="success"
    except:
        txt="fail"
    return txt

def verifyotp(request):
    if request.method=="POST":
        email_id=request.POST["emailid"]
        otp=request.POST["otp"]
        verify=Signup.objects.filter(emailid = email_id,otp=otp)
        if (verify):
            with connection.cursor() as cursor:
                cursor.execute("update myapp_userdata set status='accepted' where emailid=%s",[email_id])
            txt="Your Signup is success"
            return render(request,'myapp/index.html',{"txt1":txt})
        else:
            txt="OTP is not matched"
            return render(request,'myapp/index.html',{"txt1":txt})
#            return redirect('/myapp',{"txt1":txt})

def verifyotpdriver(request):
    if request.method=="POST":
        email_id=request.POST["emailid"]
        otp=request.POST["otp"]
        verify=Driversignup.objects.filter(emailid = email_id,otp=otp)
        if (verify):
            with connection.cursor() as cursor:
                cursor.execute("update myapp_driverdata set status='accepted' where emailid=%s",[email_id])
            txt="Your Signup is success"
            return render(request,'myapp/index.html',{"txt1":txt})
        else:
            txt="OTP is not matched"
            return render(request,'myapp/index.html',{"txt1":txt})
#            return redirect('/myapp',{"txt1":txt})


def forgotpwd(request):
    if request.method=="POST":
        user_name=request.POST["username"]
        email_id=request.POST["emailid"]
        check=Userdata.objects.filter(emailid=email_id,username=user_name)
        if (check):
            passwd=Userdata.objects.raw("select id,password from myapp_userdata where emailid=%s and username=%s",[email_id,user_name])
            for i in passwd:
             send_mail("Password For Eshwargirish Website",'Hi \n\n Please find the password : '+str(i.password) ,'girishcse11@gmail.com',[email_id],fail_silently=False)
            msg="SENT"
            return render(request,'myapp/index.html',{"msg1":msg})
        else:
            msg="Invalid username or emailid"
            return render(request,'myapp/index.html',{"msg1":msg})

def user(request):
    User=request.session['username']
    rides_count=Userrides.objects.raw("select id,count(*) as count from myapp_userrides where username=%s and status='waiting'",[User])
    if (request.method=="POST"):
        if (request.POST['action']=="USERRIDE"):
         from_long=request.POST['from_long']
         from_lat=request.POST['from_lat']
         from_place=request.POST['from_place']
         to_long=request.POST['to_long']
         to_lat=request.POST['to_lat']
         to_place=request.POST['to_place']
         distance=request.POST['distance']
         time=request.POST['time']
         ride=Userrides(username=User,fromlong=from_long,fromlat=from_lat,fromplace=from_place,tolong=to_long,tolat=to_lat,toplace=to_place,distance=distance,timeinmins=time)
         ride.save()
        elif (request.POST['action']=="HOME"):
            pass
    return render(request,'myapp/user.html',{"User" : User,"ridescount":rides_count})

def rider(request):
    return render(request,'myapp/rider.html')

def userprofile(request):
    User=request.session['username']
    if (request.method=="POST"):
        if (request.POST['action']=="RIDE_CANCEL"):
             idd=request.POST['ride_id']
             with connection.cursor() as cursor:
                 cursor.execute("update myapp_userrides set status='cancelled' where id=%s",[idd])
    user1=Userdata.objects.raw("select * from myapp_userdata where username=%s",[request.session['username']])
    userides=Userrides.objects.raw("select * from myapp_userrides where username=%s order by raisedtime",[request.session['username']])
    return render(request,'myapp/userprofile.html',{'user_name':user1,'userrides':userides})

def driver(request):
    if request.session.has_key('driverusername'):
     user=request.session['driverusername']
     rides=Userrides.objects.raw("select a.*,b.emailid from myapp_userrides a , myapp_userdata b where a.username=b.username and driver=%s and a.status in ('accepted','cancelled','completed') ",[user])
     rides_count=Userrides.objects.raw("select id,count(*) as count from myapp_userrides where driver=%s and status='accepted'",[user])
     user1=Driverdata.objects.raw("select * from myapp_driverdata where username=%s",[request.session['driverusername']])
     wait_rides=Driverdata.objects.raw("select b.image,a.id as id,a.username as username,b.emailid as emailid,a.driveremail as act_driveremail,c.emailid as drivermail ,fromlong,fromlat,fromplace,tolong,tolat,toplace,fromlong-tolong as longdis,fromlat-tolat as latdis from myapp_userrides a,myapp_userdata b,myapp_driverdata c where a.username=b.username and c.username=%s and a.status='waiting' order by 11",[user])
     idd=""
     ids=[ str(x.fromlong)+","+str(x.fromlat)+","+str(x.id) for x in wait_rides]
     options = json.dumps(ids)
     if (request.method=="POST"):
         if (request.POST['action']=="RESPONSE_ACCEPT"):
             idd=request.POST['resp_id']
             emailidd=request.POST['resp_emailid']
             from_placee=request.POST['resp_fromplace']
             to_placee=request.POST['resp_toplace']
             driveremaill=request.POST['resp_driveremail']
             drivername=request.session['driverusername']
             with connection.cursor() as cursor:
                cursor.execute("update myapp_userrides set status='accepted',driver=%s,driveremail=%s where id=%s",[drivername,driveremaill,idd])
             send_mail("RIDE ACCEPTED CARWITHCARE WEBSITE",'Hi, \n Your ride from '+ str(from_placee)+' to '+str(to_placee) +' has been accepted \n driver details : \ndriver name -- '+str(drivername)+'\n driver emailid -- '+str(driveremaill),'girishcse11@gmail.com',[emailidd],fail_silently=False)

         elif (request.POST['action']=="RESPONSE_REJECT"):
             idd=request.POST['resp_id']
             emailidd=request.POST['resp_emailid']
             from_placee=request.POST['resp_fromplace']
             to_placee=request.POST['resp_toplace']
             drivername=request.session['driverusername']
             driveremaill=request.POST['resp_driveremail']
             with connection.cursor() as cursor:
                cursor.execute("update myapp_userrides set status='rejected',driver=%s,driveremail=%s where id=%s",[drivername,driveremaill,idd])
             send_mail("RIDE REJECTED CARWITHCARE WEBSITE",'Hi, \n Your ride from '+ str(from_placee)+' to '+str(to_placee) +' has been rejected','girishcse11@gmail.com',[emailidd],fail_silently=False)
         elif (request.POST['action']=="RIDE_CANCEL"):
             idd=request.POST['ride_id']
             with connection.cursor() as cursor:
                 cursor.execute("update myapp_userrides set status='cancelled' where id=%s",[idd])
         elif (request.POST['action']=="RIDE_COMPLETE"):
             idd=request.POST['ride_id']
             with connection.cursor() as cursor:
                 cursor.execute("update myapp_userrides set status='completed' where id=%s",[idd])
     return render(request,'myapp/driver.html',{"waitrides":wait_rides,'user_name':user1,'id':idd,'myname':user,'ridescount':rides_count,'rides':rides,'options':options})


def login(request):
   username = "not logged in"
   if request.method == "POST":
      #Get the posted form
         MyLoginForm = LoginForm(request.POST)
         print ("Entered")
         username = request.POST['username']
         password = request.POST['pswd']
         user=Userdata(username=username,password=password)
         query="select id from myapp_userdata where username=%s and password=%s and status='accepted'"
         params=[username,password]
         with connection.cursor() as cursor:
             cursor.execute(query,params)
             dbuser=cursor.fetchall()
         query1="select id from myapp_userdata where username=%s and password=%s "
         params=[username,password]
         with connection.cursor() as cursor:
             cursor.execute(query1,params)
             dbuser1=cursor.fetchall()
#         dbuser=Userdata.objects.raw("select id from myapp_userdata where username=%s and password=%s",[username,password])
#         print (dbuser.fetchone())
         if len(dbuser)>0:
            print ("USername "+username+" "+"Password "+password)
            user=authenticate(username=username,password=password)
            request.session['username'] = username
            print(request.session.get_expiry_age)
            query="select a.image from myapp_userdata a where a.username=%s and a.status='accepted'"
            params=[username]
            with connection.cursor() as cursor:
             cursor.execute(query,params)
             dbuser_pro=cursor.fetchall()
            alldata = Userdata.objects.filter(username = username)
            username="Hi "+username+"\n ,Your login is success"
            return HttpResponseRedirect('/user',{"User" : dbuser_pro})
         elif len(dbuser1)>0:
            username="Hi "+username+"\n ,Waiting for the approval."
            htmls='myapp/faillogin.html'
            return render(request, htmls, {"username" : username})
         else:
            username="Hi "+username+"\n ,Entered Username or Password are wrong. Please try again."
            htmls='myapp/faillogin.html'
            response=render(request, htmls, {"username" : username})

            return response
#      username=dbuser
   else:
        pass


def signup(request):
   username = "not logged in"
   htmls=""
   if request.method == "POST":
      #Get the posted form
         MyLoginForm = LoginForm(request.POST)
         username = request.POST['username']
         password = request.POST['pswd']
         email_id  = request.POST['email']
         otp=randint(1000,9999)
         otpuse=Signup(emailid=email_id,otp=otp)
         user=Userdata(username=username,password=password,emailid=email_id)
         dbuser=Userdata.objects.filter(username = username,status="accepted")
         dbuser1=Userdata.objects.filter(username = username,status="waiting")
         otpuser=Signup.objects.filter(emailid=email_id)
         if otpuser:
             with connection.cursor() as cursor:
                cursor.execute("update myapp_signup set otp=%s where emailid=%s",[otp,email_id])
                mail(email_id,otp)
                username=email_id
                txt="ok"
                htmls="myapp/signedup.html"

         if otpuser and dbuser1:
             with connection.cursor() as cursor:
                cursor.execute("update myapp_signup set otp=%s where emailid=%s",[otp,email_id])
                mail(email_id,otp)
                username=email_id
                txt="ok"
                htmls="myapp/signedup.html"
         if not otpuser:
          if (mail(email_id,otp)=='success'):
           otpuse.save()
         if not dbuser and not dbuser1:
#            user=User.objects.create_user(username=username,password=password)
            user.save()
            username=email_id
            txt="ok"
            htmls='myapp/signedup.html'
         if dbuser:
            username=email_id
            txt="user already exist"
            htmls="myapp/signedup.html"

   else:
#      MyLoginForm = Loginform()
       pass
#   return HttpResponseRedirect('/myapp',{"username" : username})
   return render(request, htmls, {"username" : username,"txt":txt})


def logout(request):
    try:
        del request.session['username']
        return HttpResponseRedirect('/')
    except KeyError:
        pass
        return render(request, 'myapp/index.html',{})


def logindriver(request):
   username = "not logged in"
   if request.method == "POST":
      #Get the posted form
         MyLoginForm = LoginForm(request.POST)
         print ("Entered")
         username = request.POST['username']
         password = request.POST['pswd']
         user=Driverdata(username=username,password=password)
         query="select id from myapp_driverdata where username=%s and password=%s and status='accepted'"
         params=[username,password]
         with connection.cursor() as cursor:
             cursor.execute(query,params)
             dbuser=cursor.fetchall()
         if len(dbuser)>0:
            print ("USername "+username+" "+"Password "+password)
            request.session['driverusername'] = username
            return HttpResponseRedirect('/driver',{'user_name':username})
         else:
            HttpResponseRedirect('/')

   else:
        pass


def signupdriver(request):
   username = "not logged in"
   htmls=""
   if request.method == "POST":
      #Get the posted form
         MyLoginForm = LoginForm(request.POST)
         username = request.POST['username']
         password = request.POST['pswd']
         email_id  = request.POST['email']
         otp=randint(1000,9999)
         otpuse=Driversignup(emailid=email_id,otp=otp)
         user=Driverdata(username=username,password=password,emailid=email_id)
         dbuser=Driverdata.objects.filter(username = username,status="accepted")
         dbuser1=Driverdata.objects.filter(username = username,status="waiting")
         otpuser=Driversignup.objects.filter(emailid=email_id)
         if otpuser and dbuser1:
             with connection.cursor() as cursor:
                cursor.execute("update myapp_driversignup set otp=%s where emailid=%s",[otp,email_id])
                mail(email_id,otp)
                username=email_id
                txt="ok"
                htmls="myapp/driversignedup.html"
         if not otpuser:
          if (mail(email_id,otp)=='success'):
           otpuse.save()
         if not dbuser and not dbuser1:
#            user=User.objects.create_user(username=username,password=password)
            user.save()
            username=email_id
            txt="ok"
            htmls='myapp/driversignedup.html'
         if dbuser:
            username=email_id
            txt="user111 already exist"
            htmls="myapp/driversignedup.html"

   else:
#      MyLoginForm = Loginform()
       pass
#   return HttpResponseRedirect('/myapp',{"username" : username})
   return render(request, htmls, {"username" : username,"txt":txt,dbuser:"dbuser"})


def logoutdriver(request):
    try:
        del request.session['driverusername']
        return HttpResponseRedirect('/')
    except KeyError:
        pass
        return render(request, 'myapp/index.html',{})