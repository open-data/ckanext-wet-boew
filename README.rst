================
ckanext-wet-boew
================

This CKAN extension adds the Web Experience Toolkit base theme to CKAN 2.0. You will need the https://github.com/open-data/wet-boew fork of WET, branch canada-v3.1 , which adds some minor fixes to the 3.1 release of WET. To obtain a copy of the WET distribution, download: https://dl.dropboxusercontent.com/u/6526141/dist.zip . Copy
the contents of the 'dist' folder into 'ckanext-wet-boew/ckanext/wet_boew/public/dist'::

  cd ckanext/wet_boew/public/dist/

  wget https://dl.dropboxusercontent.com/u/6526141/dist.zip
  unzip dist.zip wet-boew-master-dist/dist/*
  mv wet-boew-master-dist/dist/* .
  rm -r master-dist.zip wet-boew-master-dist/

The WET toolkit distribution includes only minimized versions of the required Javascript files. 
However CKAN uses the Fanstatic resource manager which requires un-minimized Javascript files, so
it is necessary to supply these separately. Copy an unminimized version of the JQuery Mobile 
javascript file (obtained at 'http://jquerymobile.com/blog/2013/02/20/jquery-mobile-1-3-0-released/')
into 'ckanext-wet-boew/ckanext/wet_boew/public/dist/js/jquerymobile/jquery.mobile.js'::

  mkdir -p js/jquerymobile/
  wget http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.js \
    -O js/jquerymobile/jquery.mobile-1.3.0.js

This extension also requires the python json and shapely libraries that are used by the
CKAN spatial extension.

By default, CKAN pages will still display using the default CKAN template. To use the base theme,
override the template for the page and have it extend template page_wet.html instead of the usual
page.html.

To use a WET page with a left hand menu, instead extend template page_sec_menu_wet.html.



