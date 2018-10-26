<template>
  <Row class="top">
    <Col span="20" offset="2">

    </Col>
  </Row>
</template>

<script>
  import movie from '../assets/json'
  export default {
    name: 'landing-page',
    components: {},
    data () {
      return {
        requireThree: [],
        requireFour: [],
        requireFive: []
      }
    },
    methods: {
      open (link) {
        this.$electron.shell.openExternal(link)
      }
    },
    created () {
      console.log(movie)
      movie.forEach(item => {
        console.log(item.favor.length)
        // if (item.favor.length === 3) {
        //   this.requireThree.append(item)
        // }
      })
      console.log(this.requireThree)
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro');
</style>
