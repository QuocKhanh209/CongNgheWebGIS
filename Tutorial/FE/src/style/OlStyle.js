import { Style, Stroke, Fill, Circle, Icon } from "ol/style";

export const OlStyle = {
  getHightlightStyle(){
    return [
      new Style({
        fill: new Fill({
          color: "rgba(134, 167, 252, 0.3)",
        }),
        stroke: new Stroke({
          color: 'rgb(52, 104, 192)',
          width: 4,
        }),
        image: new Icon({
          src: '/img/pointActive.png',
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
        width: 4,
      }),

      image:
        typeGeo === "Point" ?
          new Icon({
            src: '/img/pointActive.png',
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
