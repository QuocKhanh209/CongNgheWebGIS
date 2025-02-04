addNewFeature(){
  // Tạo sự kiện Draw trên bản đồ
  let edit = new Draw({
    source: source,
    type: "Polygon",
  });
  // Bắt đầu sự kiện
  edit.on("drawstart");
  // Kết thúc sự kiện vẽ trên bản đồ
  edit.on("drawend", (e) => {
    const json = new GeoJSON();
    // Đọc dữ liệu của đối tượng vừa dược tạo ra
    // và lưu vào object editItem để tiếp tục xử lý
    const feature = json.writeFeatureObject(e.feature);
    this.editItem['geom'] = feature.geometry;
  });
  // Tạo sựu kiện Snap cho đối tượng
  // vừa được vẽ
  let snap = new Snap({
    source: source,
  })
  // Thêm sự kiện Draw và Snap cho map
  this.map.addInteraction(edit);
  this.map.addInteraction(snap);
}
