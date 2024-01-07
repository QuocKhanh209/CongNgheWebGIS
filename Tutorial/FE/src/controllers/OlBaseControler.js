import VectorSource from "ol/source/Vector";
import VectorLayer from "ol/layer/Vector";
import { Overlay } from "ol";
import { OlStyle } from "src/style/OlStyle";
import { editLayerHelper } from "./OlEditLayerHelper";
import { Draw, Modify, Snap } from "ol/interaction";

export default class OlBaseController {
  constructor(map){
    super(map);
  }

  createLayer(name, style, opt = {}){
    const me = this;

    const source = new VectorSource({
      wrapX: false,
    });

    const options = Object.assign(opt, {
      name : name,
      displayInLayerList: false,
      zIndex: 3,
      source: source,
      style: style,
      map: me.map,
    });

    const vector = new VectorLayer(options);

    me.source = source;
    me.layer = vector;

    return vector;
  }

  createEditLayer(onFeatureChange, onSourceChange, geoType = null){
    const me = this;

    let style = OlStyle.getDefaultStyle(geoType);

    const layerEdit = me.createLayer("Edit Layer", style, {
      queryable: true,
      editGeometry: geoType,
    });

    return layerEdit;
  }

  createModifyLayer(item){
    const me = this;

    const style = OlStyle.getHightlightStyle();

    this.createLayer("Modify Layer", style, {
      queryable: true,
    })

    const modifyFeature = editLayerHelper.createFeature(item);

    me.source.addFeature(modifyFeature);
  }

  addIntersection(editType,geoType ,start, end, item = null){
    const me = this;

    me.removeIntersection();

    switch(editType){
      case 'add': {
        let style = OlStyle.getDefaultStyle(geoType);

        me.edit = new Draw({
          source: me.source,
          type: geoType,
          style: style,
        });

        me.edit.on("drawstart", start);
        me.edit.on("drawend", end);

        me.snap = new Snap({
          source: me.source,
        })

        break;
      }
      case "modify": {
        const featureModify = editLayerHelper.createFeature(item);

        me.source.addFeature(featureModify);
        me.edit = new Modify({
          source: me.source,
        })

        me.edit.on("modifystart", start);
        me.edit.on("modifyend", end);

        me.snap= new Snap({
          source: me.source,
        });

        break;
      }
      default:
        break;
    }

    if (me.edit) {
      me.map.addIntersection(me.edit)
    }

    if (me.snap) {
      me.map.addIntersection(me.snap)
    }
  }

  removeIntersection(){
    const me = this;

    if (me.edit) {
      me.map.removeIntersection(me.edit);
      me.edit = null;
    }

    if (me.snap) {
      me.map.removeIntersection(me.snap);
    }
  }
}
