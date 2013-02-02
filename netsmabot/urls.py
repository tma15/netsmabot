from django.conf.urls.defaults import patterns, include, url
import view
import movies.views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    ('^hello/$', view.hello),
    ('^nico_video/$', movies.views.nico_movie),
    ('^$', view.home),
#     url(r'^$', 'netsmabot.views.home', name='home'),
#     url(r'^netsmabot/', include('netsmabot.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
