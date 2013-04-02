================
ckanext-wet-boew
================

This CKAN extension adds the Web Experience Toolkit base theme to CKAN 2.0. It was developed
using the 3.1 beta of WET. The WET toolkit is not included in this Git repository. To obtain a
copy of the WET distribution, see https://github.com/wet-boew/wet-boew/wiki/Downloads. Copy
the contents of the 'dist' folder into 'ckanext-wet-boew/ckanext/wet_boew/public/dist'::

  cd ckanext/wet_boew/public/dist/

  wget https://github.com/wet-boew/wet-boew/archive/master-dist.zip
  unzip master-dist.zip wet-boew-master-dist/dist/*
  mv wet-boew-master-dist/dist/* .
  rm -r master-dist.zip wet-boew-master-dist/
  
Note: For the temporary mobile initialization fix, download the open-data/wet-boew repo and build the master branch, or download the distribution only from here:

  https://dl.dropbox.com/u/6526141/dist.zip

The WET toolkit distribution includes only minimized versions of the required Javascript files. 
However CKAN uses the Fanstatic resource manager which requires un-minimized Javascript files, so
it is necessary to supply these separately. Copy an unminimized version of the JQuery Mobile 
javascript file (obtained at 'http://jquerymobile.com/blog/2013/02/20/jquery-mobile-1-3-0-released/')
into 'ckanext-wet-boew/ckanext/wet_boew/public/dist/js/jquerymobile/jquery.mobile.js'::

  mkdir -p js/jquerymobile/
  wget http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.js \
    -O js/jquerymobile/jquery.mobile-1.3.0.js

By default, CKAN pages will still display using the default CKAN template. To use the base theme,
override the template for the page and have it extend template page_wet.html instead of the usual
page.html.

To use a WET page with a left hand menu, instead extend template page_sec_menu_wet.html.



