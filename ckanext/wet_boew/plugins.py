import ckan as ckan
import ckan.plugins as p
import ckan.lib.helpers as h
import ckan.model as model
import webhelpers.html as html
import dateutil.parser
import json as json
import shapely as shapely
import shapely.wkt as wkt

from webhelpers import paginate
from webhelpers.html import HTML
import re

class WetTheme(p.SingletonPlugin):
    """
    Plugin for public-facing version of data.gc.ca site, aka the "portal"
    This plugin requires the DataGCCAForms plugin
    """
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):

        # add the WET JS directory as a fanstatic resource
        p.toolkit.add_resource('public/dist', 'ckanext-wet')
                
        # add our templates
        p.toolkit.add_template_directory(config, 'templates/ckan')
        p.toolkit.add_public_directory(config, 'public')
        
        # monkey patch helpers.py pagination method
        h.Page.pager = _wet_pager
        
    def get_helpers(self):
      return {'link_to_user': self.link_to_user, 
              'get_datapreview': self.get_datapreview,
              'iso_to_goctime': self.iso_to_goctime,
              'geojson_to_wkt': self.geojson_to_wkt }


    def link_to_user(self, user, maxlength=0):
        """ Return the HTML snippet that returns a link to a user.  """
        
        # Do not link to pseudo accounts
        if user in [model.PSEUDO_USER__LOGGED_IN, model.PSEUDO_USER__VISITOR]:
            return user
        if not isinstance(user, model.User):
            user_name = unicode(user)
            user = model.User.get(user_name)
            if not user:
                return user_name
            
        if user:
            _name = user.name if model.User.VALID_NAME.match(user.name) else user.id
            displayname = user.display_name
            if maxlength and len(user.display_name) > maxlength:
                displayname = displayname[:maxlength] + '...'
            return html.tags.link_to(displayname,
                           h.url_for(controller='user', action='read', id=_name)) 
             

    def get_datapreview(self, res_id):
     
        #import pdb; pdb.set_trace()
        dsq_results = ckan.logic.get_action('datastore_search')({}, {'resource_id': res_id})
        return h.snippet('package/wet_datatable.html', ds_fields=dsq_results['fields'], ds_records=dsq_results['records'])     
      
    def iso_to_goctime(self, isodatestr):
        dateobj = dateutil.parser.parse(isodatestr)
        return dateobj.strftime('%Y-%m-%d')
      
    def geojson_to_wkt(self, gjson_str):
      ## Ths GeoJSON string should look something like:
      ##  u'{"type": "Polygon", "coordinates": [[[-54, 46], [-54, 47], [-52, 47], [-52, 46], [-54, 46]]]}']
      ## Convert this JSON into an object, and load it into a Shapely object. The Shapely library can
      ## then output the geometry in Well-Known-Text format
      
      gjson = json.loads(gjson_str)
      # import pdb; pdb.set_trace()
      shape = shapely.geometry.asShape(gjson)
      wkt_str = wkt.dumps(shape)
      return wkt_str

                                 
def _wet_pager(self, *args, **kwargs):
    ## a custom pagination method, because CKAN doesn't expose the pagination to the templates,
    ## and instead hardcodes the pagination html in helpers.py
    kwargs.update(
        format=u"<div class='pagination pagination-centered'><ul class='menu-horizontal ckan-paginate'>$link_previous ~2~ $link_next</ul></div>",
        symbol_previous=u'previous', symbol_next=u'next',
        curpage_attr={'class': 'disabled_paginator'}, link_attr={'class': 'button button-small'}
    )
    
    return super(h.Page, self).pager(*args, **kwargs)
                          