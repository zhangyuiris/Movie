<template>
  <Row class="top">
    <Col span="24" align="center">
      <h1>Movie Recommendation</h1>
    </Col>
    <Col span="6" offset="1" style="padding-top: 120px;">
      <h2>输入五个你感兴趣的电影吧：</h2>
    </Col>
    <Col span="22" offset="1" class="top">
      <Row>
        <Col span="4">
          <AutoComplete
            v-model="one"
            @on-change="handleOne"
            placeholder="输入第一个喜欢的："
            style="width:200px">
            <Option v-for="item in dataOne" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col span="4">
          <AutoComplete
            v-model="two"
            @on-change="handleTwo"
            placeholder="输入第二个喜欢的："
            style="width:200px">
            <Option v-for="item in dataTwo" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col span="4">
          <AutoComplete
            v-model="three"
            placeholder="输入第三个喜欢的："
            style="width:200px">
            <Option v-for="item in dataThree" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col span="4">
          <AutoComplete
            v-model="four"
            placeholder="输入第四个喜欢的："
            style="width:200px">
            <Option v-for="item in dataFour" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col span="4">
          <AutoComplete
            v-model="five"
            placeholder="输入第五个喜欢的："
            style="width:200px">
            <Option v-for="item in dataFive" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col span="4">
          <Button type="info" @click="recommend">进行推荐</Button>
          <Button type="warning" @click="reset">重置</Button>
        </Col>
      </Row>
    </Col>
    <Col span="22" offset="1" class="top">
      <h2 v-if="recommendation === ''">还没输入哦！</h2>
      <h2 v-else>你也许会喜欢：<span style="color: #57c5f7">{{recommendation}}</span></h2>
    </Col>
  </Row>
</template>

<script>
  import movie from '../assets/json'
  import { Button } from 'iview'
  export default {
    name: 'landing-page',
    components: {
      Button
    },
    data () {
      return {
        one: '',
        two: '',
        three: '',
        four: '',
        five: '',
        dataOne: [],
        dataTwo: [],
        dataThree: [],
        dataFour: [],
        dataFive: [],
        all: [],
        recommendation: '',

      }
    },
    methods: {
      handleOne () {
        const that = this
        this.two = ''
        this.three = ''
        this.dataTwo = []
        this.dataThree = []
        this.dataFour = []
        this.dataFive = []
        let filteredMovie = this.requireThree.filter(item => item.favor[0] === that.one)
        filteredMovie.forEach(item => {
          if (that.dataTwo.indexOf(item.favor[1]) === -1) {
            that.dataTwo.push(item.favor[1])
          }
          if (that.dataThree.indexOf(item.favor[2]) === -1) {
            that.dataThree.push(item.favor[2])
          }
          if (that.dataFour.indexOf(item.favor[3]) === -1) {
            that.dataFour.push(item.favor[3])
          }
          if (that.dataFive.indexOf(item.favor[4]) === -1) {
            that.dataFive.push(item.favor[4])
          }
        })
      },
      handleTwo () {
        const that = this
        this.three = ''
        this.dataThree = []
        let filteredMovie = this.requireThree.filter(item => (item.favor[0] === that.one && item.favor[1] === that.two))
        filteredMovie.forEach(item => {
          if (that.dataThree.indexOf(item.favor[2]) === -1) {
            that.dataThree.push(item.favor[2])
          }
          if (that.dataFour.indexOf(item.favor[3]) === -1) {
            that.dataThree.push(item.favor[3])
          }
          if (that.dataFive.indexOf(item.favor[4]) === -1) {
            that.dataThree.push(item.favor[4])
          }
        })
      },
      recommend () {
        const that = this
        let filteredMovie = this.requireThree.filter(item => (item.favor[0] === that.one && item.favor[1] === that.two && item.favor[2] === that.three))
        this.recommendation = filteredMovie[0].recomondation
      },
      reset () {
        this.one = ''
        this.two = ''
        this.three = ''
        this.four = ''
        this.five = ''
        this.recommendation = ''
      },
      getMovie () {
        const that = this
        movie.forEach(item => {
          that.all.push(item)
        })
        that.requireFive.forEach(item => {
          if (that.dataOne.indexOf(item.favor[0]) === -1) {
            that.dataOne.push(item.favor[0])
          }
          if (that.dataTwo.indexOf(item.favor[1]) === -1) {
            that.dataTwo.push(item.favor[1])
          }
          if (that.dataThree.indexOf(item.favor[2]) === -1) {
            that.dataThree.push(item.favor[2])
          }
        })
      }
    },
    created () {
      this.getMovie()
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro');
</style>
