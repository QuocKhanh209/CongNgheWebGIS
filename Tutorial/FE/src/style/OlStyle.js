import { Style, Stroke, Fill, Circle, Icon } from "ol/style";

export const OlStyle = {
  getHightlightStyle(){
    return [
      new Style({
        fill: new Fill({
          color: "#00E8B3",
        }),
        stroke: new Stroke({
          color: '#FF0000',
          width: 2,
        }),
        image: new Icon({
          src: '/img/pointActivate.png',
          anchor: [0.5, 1],
        })
      })
    ]
  },

  getDefaultStyle(typeGeo){
    return new Style({
      fill: new Fill({
        color: "rgba(255,255,255,0.2)",
      }),

      stroke: new Stroke({
        color: "#0023cd",
        width: 2,
      }),

      image:
        typeGeo === "Point" ?
          new Icon({
            src: '/img/pointActivate.png',
            anchor: [0.5, 1],
          })
          :
          new Circle({
            radius: 2,
            fill: new Fill({
              color: "#009dff",
            })
          })
    })
  }
}
