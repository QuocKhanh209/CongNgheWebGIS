import { Style, Stroke, Fill, Circle, Icon } from "ol/style";

export const OlStyle = {
  getHightlightStyle(){
    return new Style({
        fill: new Fill({
          color: "rgba(255, 221, 149, 0.4)",
        }),
        stroke: new Stroke({
          color: 'rgb(255, 152, 67)',
          width: 4,
        }),
        image: new Icon({
          src: '/img/location_red.png',
          anchor: [0.5, 1],
        })
      })
  },

  getDefaultStyle(typeGeo){
    return new Style({
      fill: new Fill({
        color: "rgba(255,255,255,0.4)",
      }),

      stroke: new Stroke({
        color: "#0023cd",
        width: 4,
      }),

      image:
        typeGeo === "Point" ?
          new Icon({
            src: '/img/location_blue.png',
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
