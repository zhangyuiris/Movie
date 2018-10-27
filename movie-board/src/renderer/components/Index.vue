<template>
  <Row class="top">
    <Col span="24" align="center">
      <h1>Movie Recommendation</h1>
    </Col>
    <Col span="6" offset="1" class="top">
      <h2>输入三个你感兴趣的电影吧：</h2>
    </Col>
    <Col span="22" offset="1" class="top">
      <Row>
        <Col span="6">
          <AutoComplete
            v-model="one"
            @on-change="handleOne"
            @on-select="selectOne"
            placeholder="输入第一个喜欢的："
            style="width:200px">
            <Option v-for="item in dataOne" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col span="6">
          <AutoComplete
            v-model="two"
            @on-change="handleTwo"
            @on-select="selectTwo"
            placeholder="输入第二个喜欢的："
            style="width:200px">
            <Option v-for="item in dataTwo" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col span="6">
          <AutoComplete
            v-model="three"
            @on-change="handleThree"
            @on-select="selectThree"
            placeholder="输入第三个喜欢的："
            style="width:200px">
            <Option v-for="item in dataThree" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col span="6">
          <Button type="info">进行推荐</Button>
        </Col>
      </Row>
    </Col>
    <Col span="22" offset="1" class="top">
      <h2 v-if="recommendation === ''">还没输入哦！</h2>
      <h2 v-else>你也许会喜欢：<span style="color: #2b85e4">{{recommendation}}</span></h2>
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
        dataOne: [],
        dataTwo: [],
        dataThree: [],
        requireThree: [],
        recommendation: ''
        all: []
      }
    },
    methods: {
      handleOne () {
      },
      selectOne () {
      },
      handleTwo () {
      },
      handleThree () {
      },
      getMovie () {
        movie.forEach(item => {
          console.log(item.favor.length)
          switch (item.favor.length) {
            case 3:
              this.requireThree.push(item)
              break
            // case 4:
            //   this.requireFour.push(item)
            //   break
            // case 5:
            //   this.requireFive.push(item)
            //   break
            // case 6:
            //   this.requireSix.push(item)
            //   break
            default:
              break
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
