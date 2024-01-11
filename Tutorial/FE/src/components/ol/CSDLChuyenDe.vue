<template>
    <q-card class="q-ma-0">
      <q-card-section class="flex justify-between">
        <q-input
          dense
          outlined
          v-model="search"
          type="search"
          label="Tìm kiếm">
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
        </q-input>

        <!-- <q-select
          clearable
          outlined
          dense
          use-input
          input-debounce="0"
          v-model="search"
          :options="options"
          @filter="queryName"
          label="Tìm kiếm">
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey">
                No results
              </q-item-section>
            </q-item>
          </template>
        </q-select> -->

        <q-btn
          class="text-bold"
          dense
          color="primary"
          label="Thêm đối tượng"
          @click="addNewFeature"/>
      </q-card-section>
      <q-card-section class="q-pb-none">
        <MapComponent :heightMap="showTable ? 'calc(100vh - 389px)' : 'calc(100vh - 139px)'"/>
        <div class="tool flex column">
          <q-btn
            class="q-mb-xs"
            round
            size="12px"
            color="secondary"
            icon="straighten"
            @click="getLength">
            <q-tooltip>
              Đo chiều dài
            </q-tooltip>
          </q-btn>
          <q-btn
            class="q-mb-xs"
            round
            size="12px"
            color="secondary"
            icon="design_services"
            @click="getArea">
            <q-tooltip>
              Đo diện tích
            </q-tooltip>
          </q-btn>
          <q-btn
            class="q-mb-xs"
            round
            size="12px"
            color="secondary"
            icon="gps_fixed"
            @click="selectByMouse">
            <q-tooltip>
              Lấy theo điểm
            </q-tooltip>
          </q-btn>
          <q-btn
            class="q-mb-xs"
            round
            size="12px"
            color="secondary"
            icon="radio_button_unchecked"
            @click="selectByCircle">
            <q-tooltip>
              Lấy theo vòng tròn
            </q-tooltip>
          </q-btn>
          <q-btn
            class="q-mb-xs"
            round
            size="12px"
            color="secondary"
            icon="area_chart"
            @click="selectByShape">
            <q-tooltip>
              Lấy theo vùng
            </q-tooltip>
          </q-btn>
          <q-btn
            class="q-mb-xs"
            round
            size="12px"
            color="secondary"
            icon="clear"
            @click="clear">
            <q-tooltip>
              Hủy sự kiện
            </q-tooltip>
          </q-btn>
          <!-- <q-btn-group flat>
          </q-btn-group> -->
        </div>
      </q-card-section>
      <q-btn
        v-if="!showTable"
        class="show-table"
        icon="expand_less"
        @click="showTable = !showTable" />
      <q-card-section v-if="showTable" class="q-py-none ">
        <q-table
          class="my-table"
          :rows="data"
          :columns="columns"
          row-key="id"
          selection="multiple"
          v-model:selected="selected"
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
              @click="saveEdit"
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
                color="warning"
                icon-right="drive_file_rename_outline"
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
import { Draw, Select } from 'ol/interaction';
import Tooltip from "ol-ext/overlay/Tooltip"
import {Style, Icon, Stroke, Fill } from 'ol/style';
import service from 'src/utils/request';
import Source from 'ol/source/Source';
import { click } from 'ol/events/condition';
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
      layerSelect: null,
      selectInteraction: null,
      listFeature: [],
      columns: [
        { name: 'STT', align: 'center', label: 'STT', field: 'STT', sortable: false, width: "50px", divider: true},
        { name: 'name', align: 'center', label: 'Tên đối tượng', field: 'name', sortable: true, divider: true },
        { name: 'action', align: 'center', label: 'Hành động', field: 'action', sortable: false, width: "200px", divider: true },
      ],
      data: [],
      isEdittingGeometry: false,
      isEdit: false,
      drawPoly: null,
      drawLine: null,
      showTable: false,
      layerDrawCircle: null,
      layerDrawShape: null,
      drawCircle: null,
      drawShape: null,
      selected: [],
      search: '',
      queryTimeOut: null,
      options: [],
    }
  },
  mounted(){
    this.initData().then(() => {
      this.createLayer();
      this.onMapBound();
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
      this.drawLine.setActive(false);

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

    getLength(){
      this.clear();
      this.drawPoly.setActive(false);
      this.drawLine.setActive(true);
      this.$EventBus.emit("change-action", true)
    },

    getArea(){
      this.clear();
      this.drawLine.setActive(false);
      this.drawPoly.setActive(true);
      this.$EventBus.emit("change-action", true)
    },

    async initData(){
      try {
        const { data } = await service.get(this.link);
        this.listFeature = data.features;

        this.data = this.listFeature.map((item) => {
          item.name = item.properties.name
          return item;
        })
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

      if (!this.layerMarker){
        this.layerMarker = new VectorLayer({
          name: 'Marker',
          source: new VectorSource({}),
          zIndex: 100,
          visible: true,
          map: this.$map
        });
      }
    },

    createLayer(){
      if (!this.layerFeature){
        this.layerSource = new VectorSource({
          wrapX: false,
        })

        this.layerFeature = new VectorLayer({
          name : 'Feature',
          opacity: 1,
          visible : true,
          zIndex: 10,
          source: this.layerSource,
        })

        this.$map.addLayer(this.layerFeature)
      }

      if (this.listFeature.length > 0){
        editLayerHelper.addFeatureToSource(
          this.layerFeature,
          this.listFeature,
          OlStyle.getDefaultStyle(this.typeGeo)
        )
      }
    },
    addNewFeature(){
      this.$EventBus.emit("change-action", true)
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
      this.$EventBus.emit("change-action", true)
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
      this.olEditControl.clear();
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

    selectByCircle(){
      this.clear();
      this.$EventBus.emit("change-action", true)
      this.layerDrawCircle = new VectorLayer({
        source: new VectorSource({}),
        map: this.$map
      })

      this.drawCircle = new Draw({
        source: this.layerDrawCircle.getSource(),
        type: 'Circle',
      })

      this.$map.addInteraction(this.drawCircle);

      this.drawCircle.on("drawstart", this.onSelectStart )
      this.drawCircle.on("drawend", this.onSelectEnd )
    },

    selectByShape(){
      this.clear();
      this.$EventBus.emit("change-action", true)
      this.layerDrawShape = new VectorLayer({
        source: new VectorSource({}),
        map: this.$map
      })

      this.drawShape = new Draw({
        source: this.layerDrawShape.getSource(),
        type: 'Polygon',
      })

      this.$map.addInteraction(this.drawShape);

      this.drawShape.on("drawstart", this.onSelectStart )
      this.drawShape.on("drawend", this.onSelectEnd )
    },

    onSelectStart(){
      if (this.layerDrawCircle !== null)
        this.layerDrawCircle.getSource().clear();

      if (this.layerDrawShape !== null)
        this.layerDrawShape.getSource().clear();

      this.layerMarker.getSource().clear();
    },

    onSelectEnd(e){
      const feature = e.feature;
      let selectedFeatures = [];
      this.selected = [];

      this.layerFeature
        .getSource()
        .getFeatures()
        .forEach((item) => {
          if (
            feature
              .getGeometry()
              .intersectsExtent(item.getGeometry().getExtent())
          ) {
            const newFeature = item.clone();
            const json = new GeoJSON();


            json.writeFeatureObject(newFeature);
            selectedFeatures.push(newFeature);
            newFeature.setStyle(OlStyle.getHightlightStyle())
            this.layerMarker.getSource().addFeature(newFeature);
          }
        })

      selectedFeatures.forEach((item) => {
        console.log(item);
      })
    },

    selectByMouse(){
      this.clear();
      this.$EventBus.emit("change-action", true)
      this.selectInteraction = new Select({
        condition: click,
      })
      // style: OlStyle.getDefaultStyle("Point")

      this.$map.addInteraction(this.selectInteraction);

      this.selectInteraction.on("select", this.onSelectByMouseEnd)
    },

    onSelectByMouseEnd(e){
      const selectedFeature = e.selected;
      this.layerMarker.getSource().clear();
      selectedFeature.forEach((item) => {
        const newFeature = item.clone();
        const json = new GeoJSON();

        json.writeFeatureObject(newFeature);
        newFeature.setStyle(OlStyle.getHightlightStyle())
        this.layerMarker.getSource().addFeature(newFeature);
      })
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
      this.showTable = false;
      this.$EventBus.emit("change-action", false)
      this.isEdittingGeometry = false;
      this.editItem = {};
      this.layerMarker.getSource().clear();
      if (this.layerEdit !== null) {
        this.layerEdit.getSource().clear();
      }
      if (this.drawLine !== null)
        this.drawLine.setActive(false);
      if (this.drawPoly !== null)
        this.drawPoly.setActive(false);

      if (this.layerDrawCircle !== null){
        this.layerDrawCircle.getSource().clear();
      }

      if (this.drawCircle !== null){
        this.$map.removeInteraction(this.drawCircle);
      }

      if (this.layerDrawShape !== null){
        this.layerDrawShape.getSource().clear();
      }

      if (this.drawShape !== null){
        this.$map.removeInteraction(this.drawShape);
      }

      if (this.selectInteraction !== null){
        this.$map.removeInteraction(this.selectInteraction);
      }
      // this.layerMarker.getSource().clear();
    },

    queryName(val, update){
      console.log(val, update);
      clearTimeout(this.queryTimeOut);
      this.queryTimeOut = setTimeout(async () => {
        if (this.search !== ''){
          try {
            const { data } = await service.get(this.link + `search/?name=${val}`);
            const features = data.features;
            if (features.length > 0){
              console.log(features[0]);
              this.zoomToFeature(features[0]);
            }
          }
          catch (e) {
            console.log(e.message);
          }
        }
      }, 500)
    }
  },

  watch: {
    search(){
      clearTimeout(this.queryTimeOut);
      this.queryTimeOut = setTimeout(async () => {
        if (this.search !== ''){
          try {
            const { data } = await service.get(this.link + `search/?name=${this.search}`);
            const features = data.features;
            if (features.length > 0){
              this.zoomToFeature(features[0]);
            }
          }
          catch (e) {
            console.log(e.message);
          }
        }
      }, 500)
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
.show-table
  position: absolute
  bottom: 0px
  background: #fff
  left: 800px

.tool
  position: absolute
  top: 120px
  right: 24px

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
