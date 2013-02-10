================
ckanext-wet-boew
================

This CKAN extension adds the Web Experience Toolkit base theme to CKAN 2.0. It was developed
using the 3.1 beta of WET. The WET toolkit is not included in this Git repository. To obtain a
copy of the WET distribution, see https://github.com/wet-boew/wet-boew/wiki/Downloads. Extract
the 'dist' folder into the 'ckanext-wet-boew/wet_boew/public'.

The WET toolkit distribution includes only minimized versions of the required Javascript files. 
However CKAN uses the Fanstatic resource manager which requires un-minimized Javascript files, so
it is necessary to supply these separately. Copy an unminimized version of the JQuery Mobile 
javascript file (obtained at 'http://jquerymobile.com/blog/2012/10/02/announcing-jquery-mobile-1-2-0-final/')
into 'ckanext-wet-boew/wet_boew/public/dist/js/jquerymobile/jquery.mobile.js'.

By default, CKAN pages will still display using the default CKAN template. To use the base thenme,
override the template for the page and have it extend template page_wet.html instead of the usual
page.html.

To use a WET page with a left hand menu, instead extend template page_sec_menu_wet.html.



