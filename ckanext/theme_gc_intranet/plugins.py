# coding: utf-8

import ckan as ckan
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

import ckanext.wet_boew.plugins as wb

class GCIntranetTheme(wb.WetTheme):

    p.implements(p.IConfigurer)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        return super(GCIntranetTheme, self).update_config(config)

    def wet_theme(self):
        return 'theme-gc-intranet'