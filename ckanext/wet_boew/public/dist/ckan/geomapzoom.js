
pe.document.on('geomap-ready', function() {
        var myMap = pe.fn.geomap.getMap();
        var myExtent = myMap.getLayer('table#spatialfeature'); 
        myMap.zoomToExtent(myExtent, true);    
    });
