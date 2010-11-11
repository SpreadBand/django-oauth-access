========
Facebook
========

Facebook provides a fairly standard OAuth 2.0 endpoint.  Follow the steps below to setup your project to authenticate against Facebook.  Facebook provides some decent `documentation <http://developers.facebook.com/docs/authentication/>`_ on their endpoint, this guide focuses on what you specifically need to do to get it to work with django-oauth-access.

Registration
============

Before you get started, you will need to register your application with Facebook.  You can do so by going to http://developers.facebook.com/setup/.  Note that you will need to perform this step for each environment where there will be a unique top level domain.

Once you complete the initial registration process, you will need to go to your application settings to enable access for your domain.  To do so click on the "developer dashboard" link, then "edit settings", and finally "Web Site".  Once here you should have a form which includes a "Site Domain" field.  Put your domain here to allow oauth requests from your domain.

While on this screen, note your "Application ID" and "Application Secret".  You will need those values later on.

Callback
========

Next you will need to create a callback to define what the application should do, once a user has been authenticated by facebook.  You can look at the base callback classes provided by django-oauth-access at ``oauth_access/callback.py``.  You can also see an example use of setting up callbacks within a Pinax project:

.. code-block:: python

    from django.contrib.auth.models import User

    from pinax.apps.account.utils import get_default_redirect

    from oauth_access.callback import AuthenticationCallback


    class PinaxCallback(AuthenticationCallback):

        def handle_no_user(self, request, access, token, user_data):
            return self.create_user(request, access, token, user_data)

        def create_user(self, request, access, token, user_data):
            identifier = self.identifier_from_data(user_data)
            user = User(username=str(identifier))
            user.set_unusable_password()
            user.save()
            self.login_user(request, user)
            return user

        def redirect_url(self, request):
            return get_default_redirect(request)


    class FacebookCallback(PinaxCallback):

        def fetch_user_data(self, request, access, token):
            url = "https://graph.facebook.com/me"
            return access.make_api_call("json", url, token)

        def identifier_from_data(self, data):
            return "fb-%s" % data["id"]
            
Settings
========

Next you will need to add a few things to your project's settings.py to be up and running.

First you will need to add ``oauth_access`` to your list of installed apps:

.. code-block:: python

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        
        # ... alll your other apps ...
        
        "oauth_access",
    ]

Then you will need to add your oauth access settings.  They should look something like the following:

.. code-block:: python

    OAUTH_ACCESS_SETTINGS = {
        'facebook': {
            'keys': {
                'KEY': 'YOUR_FACEBOOK_APPLICATION_ID',
                'SECRET': 'YOUR_FACEBOOK_APPLICATION_SECRET',
            },
            'endpoints': {
                'access_token': 'https://graph.facebook.com/oauth/access_token',
                'authorize': 'https://graph.facebook.com/oauth/authorize',
                'provider_scope': '',
                'callback': 'your_module.oauth_callbacks.facebook_callback',
            }
        }
    }
    
Remember before when we said to take note of your Facebook "Application ID" and "Application Secret"?  Here is where you need to plug them in.  Use your "Application ID" as your "KEY" and your "Application Secret" as your "SECRET".  Finally you will want to fill in the include string for you the callback object you created previously.

URLs
====

Last but not least, you will need to add an include for the django-oauth-access urls to your URL conf.

.. code-block:: python

    urlpatterns = patterns('', 
        
        # All your other urls
        
        url(r'^auth/', include('oauth_access.urls')),
    )
    
That's it.  You should now be able to login to your site using Facebook by going to ``/auth/login/facebook/``.