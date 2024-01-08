<template>
    <q-card class="q-ma-0">
      <q-card-section>
       <q-btn
          color="primary"
          icon="add"
          label="Thêm"
          @click="addNewFeature"/>
        <q-btn
        color="primary"
        icon="add"
        label="Đo chiều dài"
        />
        <q-btn
        color="primary"
        icon="add"
        label="Đo diện tích"
        />
      </q-card-section>
      <q-card-section>
        <MapComponent :heightMap="'calc(100vh - 426px)'"/>
      </q-card-section>
      <q-card-section>
        <q-table
          class="my-table"
          :rows="data"
          :columns="columns"
          row-key="name"
        >
        <template v-slot:body-cell-STT="props">
          <q-td :props="props">
            {{ props.rowIndex + 1 }}
          </q-td>
        </template>

        <template v-slot:body-cell-action="props">
          <q-td :props="props">
            <div v-if="props.row.id === editItem?.id && isEdittingGeometry">
              <q-btn
              color="negative"
              icon-right="clear"
              no-caps
              flat
              dense
              @click="clear"
              >
              <q-tooltip>Hủy</q-tooltip></q-btn>
              <q-btn
              color="primary"
              icon-right="save"
              no-caps
              flat
              dense
              >
              <q-tooltip>Lưu</q-tooltip>
            </q-btn>
            </div>
            <div v-else>
              <q-btn
                color="info"
                icon-right="room"
                no-caps
                flat
                dense
                @click="zoomToFeature(props.row)"
                >
                <q-tooltip>Định vị</q-tooltip>
              </q-btn>
              <q-btn
                color="accent"
                icon-right="edit_square"
                no-caps
                flat
                dense
                @click="editFeature(props.row)"
                >
                <q-tooltip>Sửa</q-tooltip>
              </q-btn>
              <q-btn
                color="accent"
                icon-right="edit_square"
                no-caps
                flat
                dense
                @click="editGeometry(props.row)"
                >
                <q-tooltip>Sửa không gian</q-tooltip>
              </q-btn>
              <q-btn
                color="negative"
                icon-right="delete"
                no-caps
                flat
                dense
                @click="deleteItem(props.row.id)"
                >
              <q-tooltip>Xóa</q-tooltip></q-btn>
            </div>
          </q-td>
        </template>

        </q-table>
      </q-card-section>
    </q-card>

    <q-dialog v-model="editData" persistent>
      <q-card class="my-card" style="width: 700px;">
        <q-card-section class="text-h5 q-ma-none text-bold">
          Nhập thông tin đối tượng
        </q-card-section>
        <q-card-section>
          <q-input dense outlined v-model="editItem['name']" label="Tên đối tượng" />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            v-if="!isEdit"
            label="Xác nhận"
            @click="onSubmit()"
            color="primary" />
            <q-btn
              v-else
              label="Xác nhận"
              @click="saveEdit()"
              color="primary" />
          <q-btn label="Hủy" @click="onReset()" color="secondary" class="q-ml-sm" />
        </q-card-actions>
      </q-card>
    </q-dialog>
</template>

<script>
import { editLayerHelper } from 'src/controllers/OlEditLayerHelper';
import MapComponent from './MapComponent.vue';
import OlBaseController from 'src/controllers/OlBaseControler';

import { OlStyle } from 'src/style/OlStyle';

import VectorSource from 'ol/source/Vector';
import VectorLayer from 'ol/layer/Vector';

import GeoJSON from 'ol/format/GeoJSON';
import { Draw } from 'ol/interaction';
import Tooltip from "ol-ext/overlay/Tooltip"

import service from 'src/utils/request';
export default {
  name: 'CSDLChuyenDe',
  props: [
    'typeGeo',
    'link'
  ],
  components: {
    MapComponent,
  },
  data(){
    return {
      layerEdit: null,
      olEditControl: null,
      layerMarker: null,
      editData: false,
      editItem: {},
      layerFeature: null,
      layerSource: null,
      listFeature: [],
      columns: [
        { name: 'STT', align: 'center', label: 'STT', field: 'STT', sortable: false },
        { name: 'action', align: 'center', label: 'Hành động', field: 'action', sortable: false },
        { name: 'name', align: 'center', label: 'Tên đối tượng', field: 'name', sortable: true },
      ],
      data: [],
      isEdittingGeometry: false,
      isEdit: false,
      drawPoly: null,
      drawLine: null,
    }
  },
  mounted(){
    this.initData().then(() => {
      this.onMapBound();
      this.createLayer();
    });

    this.setUpDraw();
  },
  methods: {
    setUpDraw(){
      const me = this;
      this.drawLine = new Draw({ type: 'LineString' });
      me.$map.addInteraction(this.drawLine);
      this.drawPoly = new Draw({ type: 'Polygon' });
      me.$map.addInteraction(this.drawPoly);
      this.drawPoly.setActive(false);

      // Add a tooltip
      var tooltip = new Tooltip();
      me.$map.addOverlay(tooltip);

      // Set feature on drawstart
      this.drawLine.on('drawstart', tooltip.setFeature.bind(tooltip));
      // Remove feature on finish
      this.drawLine.on(['change:active','drawend'], tooltip.removeFeature.bind(tooltip));

      // Set feature on drawstart
      this.drawPoly.on('drawstart', tooltip.setFeature.bind(tooltip));
      // Remove feature on finish
      this.drawPoly.on(['change:active','drawend'], tooltip.removeFeature.bind(tooltip));
    },

    async initData(){
      try {
        const { data } = await service.get(this.link);
        this.listFeature = data.features;

        this.data = this.listFeature.map((item) => {
          item.name = item.properties.name
          return item;
        })

        console.log(this.data);
      }
      catch (e) {
        console.log(e.message);
      }
    },

    onMapBound(){
      this.olEditControl = new OlBaseController(this.$map);

      if (!this.layerEdit){
        this.layerEdit = this.olEditControl.createEditLayer(
          null,
          null,
          this.typeGeo
        );
        editLayerHelper.selectedLayer = this.layerEdit;
      }
    },

    createLayer(){
      if (!this.layerFeature){
        this.layerSource = new VectorSource({
          wrapX: false,
        })

        this.layerFeature = new VectorLayer({
          name : 'Layer Feature',
          opacity: 1,
          visible : true,
          zIndex: 10,
          source: this.layerSource,
          map: this.$map
        })
      }

      if (this.listFeature.length > 0){
        console.log(this.listFeature)
        editLayerHelper.addFeatureToSource(
          this.layerFeature,
          this.listFeature,
          OlStyle.getHightlightStyle()
        )
      }
    },
    addNewFeature(){
      const start = this.onDrawStart;
      const end = this.onDrawEnd;

      this.olEditControl.addIntersection(
        'add',
        this.typeGeo,
        start,
        end,
        null
      )
    },

    editGeometry(item){
      this.isEdittingGeometry = true;
      const start = this.onDrawStart;
      const end = this.onModiFyEnd;

      this.editItem = item;

      this.zoomToFeature(item);

      this.olEditControl.addIntersection(
        'modify',
        this.typeGeo,
        start,
        end,
        item
      )
    },

    editFeature(item){
      console.log(item);
      this.editItem = item;
      this.editData = true;
      this.isEdit = true;
    },

    onDrawStart(){

    },

    onDrawEnd(e){
      this.editData = true;

      const json = new GeoJSON();

      const feature = json.writeFeatureObject(e.feature);

      this.editItem['geom'] = feature.geometry;

      this.olEditControl.removeIntersection();
    },

    onModiFyEnd(e){
      if (e.features.getArray().length > 0) {
        const feature = e.features.getArray()[0];

        const json = new GeoJSON();

        this.editItem['geom'] = json.writeFeatureObject(feature).geometry;
      }
    },

    async onSubmit(){
      try {
        const { data } = await service.post(this.link, { ...this.editItem})
        this.initData().then(() => {
          this.createLayer();
        });
        this.editData = false;
        this.editItem = null;
      }
      catch (e) {
        console.log(e.message);
        this.editData = false;
        this.editItem = null;
      }
    },

    onReset(){
      this.editItem = null;
      this.editData = false;
      this.isEdit = false;
    },

    async deleteItem(id){
      try {
        const { data } = await service.delete(this.link + id + '/');
        this.initData().then(() => {
          this.createLayer();
        });
      }
      catch (e) {
        console.log(e.message);
      }
    },

    async saveEdit(){
      try {
        let id = this.editItem['id'];
        delete this.editItem['id'];
        delete this.editItem['geometry'];
        delete this.editItem['properties'];
        const { data } = await service.put(this.link + id + "/", { ...this.editItem})
        console.log(data);
        this.initData().then(() => {
          this.createLayer();
        });
        this.editData = false;
        this.editItem = null;
        this.isEdit = false;
      }
      catch (e) {
        console.log(e.message);
        this.editData = false;
        this.editItem = null;
      }
    },

    zoomToFeature(item){
      this.$map.updateSize();

      if (item.geometry.type === 'Point'){
        editLayerHelper.zoomToPoint(this.$map.getView(), item, 17);
      }
      else {
        const feature = editLayerHelper.createFeature(item);
        const fitOptions = { duration: 1000 };
        this.$map.getView().fit(feature.getGeometry(), fitOptions);
      }
    },

    stop(){
      this.olEditControl.clear();
    },

    clear(){
      this.stop();
      this.isEdittingGeometry = false;
      this.editItem = {};
      // this.layerMarker.getSource().clear();
    }

  }
}
</script>

<!-- <style scoped>
.my-table{
  height: 250px;
  margin: 0;
}
</style> -->

<style lang="sass">
.my-table
  /* height or max-height is important */
  height: 250px

  .q-table__top,
  .q-table__bottom,
  thead tr:first-child th
    /* bg color is important for th; just specify one */
    background-color: #ffffff

  thead tr th
    position: sticky
    z-index: 1
  thead tr:first-child th
    top: 0

  /* this is when the loading indicator appears */
  &.q-table--loading thead tr:last-child th
    /* height of all previous header rows */
    top: 48px

  /* prevent scrolling behind sticky top row on focus */
  tbody
    /* height of all previous header rows */
    scroll-margin-top: 48px
</style>
