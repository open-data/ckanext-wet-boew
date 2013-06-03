
pe.document.on('geomap-ready', function() {
        var myMap = pe.fn.geomap.getMap();
        var layer = myMap.getLayersByName('spatialfeature')[0];
        myMap.zoomToExtent(layer.getDataExtent().scale(3));
    });
