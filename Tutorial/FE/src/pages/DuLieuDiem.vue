<template>
  <div>
    <CSDLChuyenDe
      :typeGeo="'Point'"
      :link="'/du-lieu-chuyen-de/du-lieu-diem/'"/>
  </div>
</template>

<script>
import CSDLChuyenDe from 'components/ol/CSDLChuyenDe.vue'
export default {
  components: {
    CSDLChuyenDe
  },

  setup () {


    return {}
  }
}
</script>

<style lang="scss" scoped>

</style>
