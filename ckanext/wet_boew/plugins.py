import ckan.plugins as p
import ckan.lib.helpers as h
import ckan.model as model
import webhelpers.html as html

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
      return {'link_to_user': self.link_to_user}


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
                           
def _wet_pager(self, *args, **kwargs):
    ## a custom pagination method, because CKAN doesn't expose the pagination to the templates,
    ## and instead hardcodes the pagination html in helpers.py
    kwargs.update(
        format=u"<div class='pagination pagination-centered'><ul class='menu-horizontal ckan-paginate'>$link_previous ~2~ $link_next</ul></div>",
        symbol_previous=u'<', symbol_next=u'>',
        curpage_attr={'class': 'active'}, link_attr={'class': 'button button-small'}
    )
    return super(h.Page, self).pager(*args, **kwargs)
                          