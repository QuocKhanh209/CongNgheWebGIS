<template>
  <div>
    <CSDLChuyenDe
      :typeGeo="'Polygon'"
      :link="'/du-lieu-chuyen-de/du-lieu-vung/'" />
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
