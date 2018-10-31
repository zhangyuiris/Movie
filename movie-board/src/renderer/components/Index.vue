<template>
  <Row class="top">
    <Col span="24" align="center">
      <h1>Movie Recomondation</h1>
    </Col>
    <Col span="22" offset="1" class="choose">
      <h1 style="color: #2db7f5">数据展示</h1>
    </Col>
    <Col span="12">
      <v-chart :options="pie"/>
    </Col>
    <Col span="12">
      <v-chart :options="bar"/>
    </Col>
    <Col span="9" offset="2" class="bottom">
      <h3 style="font-size:16px;">推荐结果中的电影</h3>
    </Col>
    <Col span="9" offset="1" align="center" class="bottom">
      <h3 style="font-size:16px;">生成的频繁项集长度占得比例</h3>
    </Col>
    <Col span="22" offset="1" class="choose">
      <h1 style="color: #2db7f5">推荐</h1>
      <RadioGroup v-model="group" style="font-size: 16px;" @on-change="change()">
        <Radio label="five">输入5个进行推荐</Radio>
        <Radio label="four">输入4个进行推荐</Radio>
        <Radio label="three">输入3个进行推荐</Radio>
      </RadioGroup>
    </Col>
    <Col span="6" offset="1" class="title">
      <h2>输入你感兴趣的电影吧：</h2>
    </Col>
    <Col span="22" offset="1" class="top">
      <Row>
        <Col :span="col">
          <AutoComplete
            v-model="one"
            @on-change="handleOne"
            placeholder="输入第一个喜欢的："
            style="width:200px">
            <Option v-for="item in dataOne" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col :span="col">
          <AutoComplete
            v-model="two"
            @on-change="handleTwo"
            placeholder="输入第二个喜欢的："
            style="width:200px">
            <Option v-for="item in dataTwo" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col :span="col">
          <AutoComplete
            v-model="three"
            @on-change="handleThree"
            placeholder="输入第三个喜欢的："
            style="width:200px">
            <Option v-for="item in dataThree" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col :span="col" v-if="group === 'four' || group === 'five'">
          <AutoComplete
            v-model="four"
            @on-change="handleFour"
            placeholder="输入第四个喜欢的："
            style="width:200px">
            <Option v-for="item in dataFour" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col :span="col" v-if="group === 'five'">
          <AutoComplete
            v-model="five"
            placeholder="输入第五个喜欢的："
            style="width:200px">
            <Option v-for="item in dataFive" :value="item" :key="item">{{ item }}</Option>
          </AutoComplete>
        </Col>
        <Col :span="col">
          <Button type="info" @click="recommend()">进行推荐</Button>
          <Button type="warning" @click="reset">重置</Button>
        </Col>
      </Row>
    </Col>
    <Col span="22" offset="1" class="top bottom">
      <h2 v-if="recomondation === ''">还没输入哦！</h2>
      <h2 v-else>你也许会喜欢：<span style="color: #57c5f7">{{recomondation}}！</span></h2>
    </Col>
  </Row>
</template>

<script>
  import movie from '../assets/json'
  import ECharts from 'vue-echarts/components/ECharts'
  import 'echarts/lib/chart/line'
  import 'echarts/lib/component/polar'
  import { Button } from 'iview'
  export default {
    name: 'landing-page',
    components: {
      'v-chart': ECharts,
      Button
    },
    data () {
      return {
        bar: {
          legend: {},
          tooltip: {},
          dataset: {
            // Provide data.
            source: [
              ['频繁项集长度', '数目'],
              ['2', 93],
              ['3', 295],
              ['4', 593],
              ['5', 785],
              ['6', 677],
              ['7', 373],
              ['8', 126],
              ['9', 24],
              ['10', 10]
            ]
          },
          xAxis: { type: 'category' },
          yAxis: {},
          series: [
            {
              type: 'bar',
              color: ['#93d2f6']
            }
          ]
        },
        pie: {
          title: {
            text: '',
            x: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a}  {b} : {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            data: [2, 3, 4, 5, 6, 7, 8, 9, 10]
          },
          series: [
            {
              name: '',
              type: 'pie',
              radius: '55%',
              center: ['50%', '50%'],
              color: ['#419adf', '#57b4f0', '#3887cb', '#93d2f6', '#6ec1f2', '#66c2f9', '#48a8ee', '#3076b8'],
              data: [
                {value: 952, name: '星球大战(1977)'},
                {value: 535, name: '夺宝奇兵(1981)'},
                {value: 6, name: '低俗小说(1994)'},
                {value: 30, name: '肖申克的救赎(1994)'},
                {value: 169, name: '沉默的羔羊(1991)'},
                {value: 188, name: '星球大战V：帝国反击战(1980)'},
                {value: 11, name: '星球大战VI：绝地归来(1983)'}
              ],
              itemStyle: {
                emphasis: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.8)'
                }
              }
            }
          ],
          animationDuration: 2000
        },
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
        number: 5,
        recomondation: '',
        group: 'five',
        col: 4
      }
    },
    methods: {
      change () {
        this.one = ''
        this.two = ''
        this.three = ''
        this.four = ''
        this.five = ''
        this.dataOne = []
        this.dataTwo = []
        this.dataThree = []
        this.dataFour = []
        this.dataFive = []
        switch (this.group) {
          case 'five': {
            this.number = 5
            break
          }
          case 'four': {
            this.number = 4
            break
          }
          case 'three': {
            this.number = 3
            break
          }
        }
        this.getMovie()
      },
      handleOne () {
        const that = this
        this.two = ''
        this.three = ''
        this.four = ''
        this.five = ''
        this.dataTwo = []
        this.dataThree = []
        this.dataFour = []
        this.dataFive = []
        let filteredMovie = this.all.filter(item => item.favor[0] === that.one)
        filteredMovie.forEach(item => {
          if (that.dataTwo.indexOf(item.favor[1]) === -1) {
            that.dataTwo.push(item.favor[1])
          }
        })
      },
      handleTwo () {
        const that = this
        this.three = ''
        this.four = ''
        this.five = ''
        this.dataThree = []
        this.dataFour = []
        this.dataFive = []
        let filteredMovie = this.all.filter(item => (item.favor[0] === that.one && item.favor[1] === that.two))
        filteredMovie.forEach(item => {
          if (that.dataThree.indexOf(item.favor[2]) === -1) {
            that.dataThree.push(item.favor[2])
          }
        })
      },
      handleThree () {
        const that = this
        this.four = ''
        this.five = ''
        this.dataFour = []
        this.dataFive = []
        let filteredMovie = this.all.filter(item => (item.favor[0] === that.one && item.favor[1] === that.two && item.favor[2] === that.three))
        filteredMovie.forEach(item => {
          if (that.dataFour.indexOf(item.favor[3]) === -1) {
            that.dataFour.push(item.favor[3])
          }
        })
      },
      handleFour () {
        const that = this
        this.five = ''
        this.dataFive = []
        let filteredMovie = this.all.filter(item => (item.favor[0] === that.one && item.favor[1] === that.two && item.favor[2] === that.three && item.favor[3] === that.four))
        filteredMovie.forEach(item => {
          if (that.dataFive.indexOf(item.favor[4]) === -1) {
            that.dataFive.push(item.favor[4])
          }
        })
      },
      recommend () {
        const that = this
        switch (that.number) {
          case 5: {
            if (that.one !== '' && that.two !== '' && that.three !== '' && that.four !== '' && that.five !== '') {
              let filteredMovie = this.all.filter(item => item.favor[0] === that.one && item.favor[1] === that.two && item.favor[2] === that.three && item.favor[3] === that.four && item.favor[4] === that.five)
              that.recomondation = filteredMovie[0].recomondation
            }
            break
          }
          case 4: {
            if (that.one !== '' && that.two !== '' && that.three !== '' && that.four !== '') {
              let filteredMovie = this.all.filter(item => item.favor[0] === that.one && item.favor[1] === that.two && item.favor[2] === that.three && item.favor[3] === that.four)
              that.recomondation = filteredMovie[0].recomondation
            }
            break
          }
          case 3: {
            if (that.one !== '' && that.two !== '' && that.three !== '') {
              let filteredMovie = this.all.filter(item => item.favor[0] === that.one && item.favor[1] === that.two && item.favor[2] === that.three)
              that.recomondation = filteredMovie[0].recomondation
            }
            break
          }
        }
      },
      reset () {
        this.one = ''
        this.two = ''
        this.three = ''
        this.four = ''
        this.five = ''
        this.recomondation = ''
      },
      getMovie () {
        const that = this
        movie.forEach(item => {
          if (item.favor.length === that.number) {
            that.all.push(item)
          }
        })
        that.all.forEach(item => {
          if (that.dataOne.indexOf(item.favor[0]) === -1) {
            that.dataOne.push(item.favor[0])
          }
        })
      }
    },
    created () {
      this.getMovie()
    }
  }
</script>
