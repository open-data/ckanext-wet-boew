# coding: utf-8

import ckan as ckan
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h

import ckanext.wet_boew.plugins as wb

class GCWebTheme(wb.WetTheme):

    p.implements(p.IConfigurer)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        super(GCWebTheme, self).update_config(config)
        h.build_nav_main = build_nav_main

    def wet_theme(self):
        return 'GCWeb'

# Monkey Patched to inlude the 'list-group-item' class
# TODO: Clean up and convert to proper HTML templates
def build_nav_main(*args):
    ''' build a set of menu items.

    args: tuples of (menu type, title) eg ('login', _('Login'))
    outputs <li><a href="...">title</a></li>
    '''
    output = ''
    for item in args:
        menu_item, title = item[:2]
        if len(item) == 3 and not h.check_access(item[2]):
            continue
        output += h._make_menu_item(menu_item, title, class_='list-group-item')
    return output