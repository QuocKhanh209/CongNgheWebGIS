<template>
  <div id="map" :style="{ height: heightMap }"></div>
</template>

<script>
import { View, Map } from "ol";

import VectorSource from "ol/source/Vector";
import VectorLayer from "ol/layer/Vector";
import TileLayer from "ol/layer/Tile";

// import the app-wide EventBus

//map Control
import DoubleClickZoom from "ol/interaction/DoubleClickZoom";

import { OSM } from "ol/source";
import GeoJSON from "ol/format/GeoJSON";

import LayerSwitcherImage from "ol-ext/control/LayerSwitcherImage";
export default {
  name: 'MapComponent',
  props: ['heightMap'],

  data(){
    return{
      zoom : 10,
      center: [105, 21],

      info: {},
    }
  },

  created(){
    const me = this;

    const OSMLayer = new TileLayer({
      name: 'OSM',
      source: new OSM({}),
      visible: true,
    })

    me.map = new Map({
      target: 'map',
      layers: [
        OSMLayer,
      ],

      view: new View({
        center: this.center,
        zoom: this.zoom,
        minZoom: 2,
        maxZoom: 18,
        projection: 'EPSG:4326'
      })
    })

    console.log(me.map.getAllLayers());


  },

  mounted(){
    const me = this;

    this.$map = me.map;

  }

}
</script>

<style scoped>
#map{
  height: calc(100vh - 100px);
}

</style>
