
ckanext-wet-boew
================

This CKAN extension adds the Web Experience Toolkit 4.0.x Base theme to CKAN 2.2. This theme is available from the WET-BOEW
website at: [http://wet-boew.github.io/wet-boew/docs/versions/dwnld-en.html].

Please note that this extension does not use the Fanstatic Resource Manager in CKAN. Instead, the WET resources are served
directly from the web server. 

Extract the WET 4.0.x files to folder that can be served directly to the client by the web server.

**Example: Paster**

Copy the WET folder to the public directory in the ckanext-wet-boew CKAN extension:

```
..../ckanext/wet_boew/public/theme-base
```

Configuration Settings
----------------------

The Wet-Boew extension uses two CKAN configuration file settings:

1. **wet_theme.url**: set this value to the base URL of the WET theme

  *Example*
   ```
   wet_theme.url = http://localhost:5000/theme-gcweb
   ```
   
2. **wet_theme.geo_map_type**: set this value to indicate what style of 
[WET Geomap widget](http://wet-boew.github.io/wet-boew/docs/ref/geomap/geomap-en.html) to use. Set this to either 
'static' or 'dynamic'. For more  

  *Example*
   ```
   wet_theme.geo_map_type = static