# coding: utf-8

import ckan as ckan
import ckan.plugins as p
import ckan.plugins.toolkit as t
import ckan.lib.helpers as h
import ckan.lib.formatters as formatters
import ckan.model as model
import webhelpers.html as html
import dateutil.parser
import json as json
import shapely as shapely
import shapely.wkt as wkt

from webhelpers.html import HTML, literal
from webhelpers.html.tags import link_to
from pylons import config
from pylons.i18n import gettext

GRAVATAR_SHOW_OPTION = 'ckan.gravatar_show'
GRAVATAR_SHOW_DEFAULT = True
WET_URL = config.get('wet_boew.url', '')
WET_JQUERY_OFFLINE_OPTION = 'wet_boew.jquery.offline'
WET_JQUERY_OFFLINE_DEFAULT = False
GEO_MAP_TYPE_OPTION = 'wet_theme.geo_map_type'
GEO_MAP_TYPE_DEFAULT = 'static'

class WetTheme(p.SingletonPlugin):
    """
    Plugin for public-facing version of data.gc.ca site, aka the "portal"
    This plugin requires the DataGCCAForms plugin
    """
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):

        # add our templates - note that the Web Experience Toolkit distribution
        # files should be installed in the public folder
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_public_directory(config, 'public')

        # monkey patch helpers.py pagination method
        h.Page.pager = _wet_pager
        h.SI_number_span = _SI_number_span_close

    def get_helpers(self):
      return {'link_to_user': self.link_to_user,
              'gravatar_show': self.gravatar_show,
              'get_datapreview': self.get_datapreview,
              'iso_to_goctime': self.iso_to_goctime,
              'geojson_to_wkt': self.geojson_to_wkt,
              'url_for_wet': self.url_for_wet,
              'url_for_wet_theme': self.url_for_wet_theme,
              'wet_theme': self.wet_theme,
              'wet_jquery_offline': self.wet_jquery_offline,
              'get_map_type': self.get_map_type
            }


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

    def gravatar_show(self):
        return t.asbool(config.get(GRAVATAR_SHOW_OPTION, GRAVATAR_SHOW_DEFAULT))

    def get_datapreview(self, res_id):

        #import pdb; pdb.set_trace()
        dsq_results = ckan.logic.get_action('datastore_search')({}, {'resource_id': res_id, 'limit' : 100})
        return h.snippet('package/wet_datatable.html', ds_fields=dsq_results['fields'], ds_records=dsq_results['records'])

    def iso_to_goctime(self, isodatestr):
        dateobj = dateutil.parser.parse(isodatestr)
        return dateobj.strftime('%Y-%m-%d')

    def geojson_to_wkt(self, gjson_str):
        ## Ths GeoJSON string should look something like:
        ##  u'{"type": "Polygon", "coordinates": [[[-54, 46], [-54, 47], [-52, 47], [-52, 46], [-54, 46]]]}']
        ## Convert this JSON into an object, and load it into a Shapely object. The Shapely library can
        ## then output the geometry in Well-Known-Text format

        try:
            gjson = json.loads(gjson_str)
            try:
                gjson = _add_extra_longitude_points(gjson)
            except:
                # this is bad, but all we're trying to do is improve
                # certain shapes and if that fails showing the original
                # is good enough
                pass
            shape = shapely.geometry.asShape(gjson)
        except ValueError:
            return None # avoid 500 error on bad geojson in DB

        wkt_str = wkt.dumps(shape)
        return wkt_str

    def url_for_wet(self, *args, **kw):
        file = args[0] or ''
        theme = kw.get('theme', False)
        return h.url_for_static_or_external(
            WET_URL + '/' + (self.wet_theme() if theme else 'wet-boew') + file
        )

    def url_for_wet_theme(self, *args):
        file = args[0] or ''
        return self.url_for_wet(file, theme = True)

    def wet_theme(self):
        return 'theme-wet-boew'

    def wet_jquery_offline(self):
        return t.asbool(config.get(WET_JQUERY_OFFLINE_OPTION, WET_JQUERY_OFFLINE_DEFAULT))

    def get_map_type(self):
        return str(config.get(GEO_MAP_TYPE_OPTION, GEO_MAP_TYPE_DEFAULT))

def _wet_pager(self, *args, **kwargs):
    ## a custom pagination method, because CKAN doesn't expose the pagination to the templates,
    ## and instead hardcodes the pagination html in helpers.py

    kwargs.update(
        format=u"<ul class='pagination'>$link_previous ~2~ $link_next</ul>",
        symbol_previous=gettext('Previous').decode('utf-8'), symbol_next=gettext('Next').decode('utf-8'),
        curpage_attr={'class': 'active'}
    )

    return super(h.Page, self).pager(*args, **kwargs)

def _SI_number_span_close(number):
    ''' outputs a span with the number in SI unit eg 14700 -> 14.7k '''
    number = int(number)
    if number < 1000:
        output = literal('<span>')
    else:
        output = literal('<span title="' + formatters.localised_number(number) + '">')
    return output + formatters.localised_SI_number(number) + literal('</span>')

def _add_extra_longitude_points(gjson):
    """
    Assume that sides of a polygon with the same latitude should
    be rendered as curves following that latitude instead of
    straight lines on the final map projection
    """
    import math
    fuzz = 0.00001
    if gjson[u'type'] != u'Polygon':
        return gjson
    coords = gjson[u'coordinates'][0]
    plng, plat = coords[0]
    out = [[plng, plat]]
    for lng, lat in coords[1:]:
        if plat - fuzz < lat < plat + fuzz:
            parts = int(abs(lng-plng))
            if parts > 300:
                # something wrong with the data, give up
                return gjson
            for i in range(parts)[1:]:
                out.append([(i*lng + (parts-i)*plng)/parts, lat])
        out.append([lng, lat])
        plng, plat = lng, lat
    return {u'coordinates': [out], u'type': u'Polygon'}
