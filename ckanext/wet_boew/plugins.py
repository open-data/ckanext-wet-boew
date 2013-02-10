import ckan.plugins as p

class WetTheme(p.SingletonPlugin):
    """
    Plugin for public-facing version of data.gc.ca site, aka the "portal"
    This plugin requires the DataGCCAForms plugin
    """
    p.implements(p.IConfigurer)

    def update_config(self, config):

        # add the WET JS directory as a fanstatic resource
        p.toolkit.add_resource('public/dist', 'ckanext-wet')
                
        # add our templates
        p.toolkit.add_template_directory(config, 'templates/ckan')
        p.toolkit.add_public_directory(config, 'public')
        
