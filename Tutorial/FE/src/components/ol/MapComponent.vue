<template>
  <div id="map" class="map" :style="{ height: heightMap }"></div>
</template>

<script>
import { getCurrentInstance } from "vue";

import { Map, View } from 'ol';
import  OSM from 'ol/source/OSM';
import XYZ from 'ol/source/XYZ'
import TileLayer from 'ol/layer/Tile.js';
import {Control, defaults as defaultControls} from 'ol/control.js';
import LayerSwitcherImage from "ol-ext/control/LayerSwitcherImage";
import { defaults as defaultInteractions } from "ol/interaction";
import DoubleClickZoom from "ol/interaction/DoubleClickZoom";

import Overlay from 'ol/Overlay';
export default {
  name: 'MapComponent',
  props: ['heightMap'],

  data(){
    return{
      zoom : 10,
      center: [105, 21],
      info: {},
      map: null,
      dblClickZoomInteraction: null,
      overlay: null,
    }
  },

  created(){
    const  OSMLayer =  new TileLayer({
      source : new OSM(),
      name: 'OSM',
      visible: true,
      "group": "base_map",
      "baseLayer": true,
    })

    const key = 'Ajvf8tdTFhaHlCN59dOR';

    const  XYZLayer =  new TileLayer({
      source : new XYZ({
        url: 'https://api.maptiler.com/maps/satellite/{z}/{x}/{y}.jpg?key=Ajvf8tdTFhaHlCN59dOR',
      }),
      name: 'XYZ',
      visible: false,
      "group": "base_map",
      "baseLayer": true,
    })

    this.map = new Map({
      layers: [
        OSMLayer,
        XYZLayer
      ],
      view: new View({
        center: this.center,
        zoom: this.zoom,
        projection: "EPSG:4326",
      }),
      interactions: defaultInteractions({
        doubleClickZoom: false,
      }).extend([]),
      controls: defaultControls({
        attribution: false,
        zoom: true,
      }).extend([
        new LayerSwitcherImage()
      ])
    })

    // this.overlay = new Overlay({
    //   element: this.$refs.popup,
    //   autoPan: false,
    //   autoPanMargin: 40,
    //   autoPanAnimation: {
    //     duration: 250,
    //   },
    // })

  },

  mounted(){
    const me = this;

    me.map.setTarget(document.getElementById("map"));

    const app = getCurrentInstance();
    app.appContext.config.globalProperties.$map = me.map;

    me.setUpMapClick();
  },

  methods: {
    setUpMapClick(){
      const me = this;
      const map = me.map;

      me.mapClickListenerKey = map.on("click", (evt) => {
        this.info = {};

        const coordinate = evt.coordinate;

        let selectedFeatures = me.map.getFeaturesAtPixel(evt.pixel, {
          hitTolerance: 4,
        })

        if (selectedFeatures.length > 0){
          this.info = selectedFeatures[0].getProperties();
          delete this.info["geometry"];
          me.showPopup(coordinate);

          console.log(this.info);
        }
      })
    },

    showPopup(coordinate){
      this.map.getView().animate({
        center: coordinate,
        duration: 300,
      })
    }
  }

}
</script>

<style scoped>
#map{
  height: calc(100vh - 50px);
}

</style>
