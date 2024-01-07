import { Feature } from "ol";
import { LineString, Polygon, Point } from "ol/geom";
import { transform } from "ol/proj";
import { Style, Stroke, Icon, Circle as CircleStyle, Fill } from "ol/style";
import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import GeoJSON from "ol/format/GeoJSON";

export const editLayerHelper = {
  selectedLayer: null,
  deletedFeatured: [],

  createFeature: (item) => {
    if (!!item.geometry){
      let json = new GeoJSON();
      let feature = json.readFeature(item);

      return feature
    }

    return null;
  },

  addFeatureToSource: (layer, list) => {
    const source = layer.getSource();

    if (list.lenght > 0) {
      source.clear();

      list.forEach((item) => {
        let feature = editLayerHelper.createFeature(item);

        source.addFeature(feature)
      })
    }
  },

  zoomToPoint: (viewMap, item, zoom) => {
    viewMap.animate({
      zoom : zoom,
      duration: 500,
      center: item.geometry.coordinates
    })
  }
}
