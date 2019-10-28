<template>
  <view class="selector">
    <view class="_header">
      <view style="border-right:1px solid #ccc;" :style="{'color':is_display_left?'#222':'#888'}" @tap="_is_display_left">
        <text>{{c_order_way[order_choice]}}</text>
        <image :src="is_display_left?'../../static/img/up.png':'../../static/img/down.png'"></image>
      </view>
      <view @tap="_is_display_right" :style="{'color':is_display_right?'#222':'#888'}">
        <text>{{c_days_list[day_choice]}}</text>
        <image :src="is_display_right?'../../static/img/up.png':'../../static/img/down.png'"></image>
      </view>
    </view>
    <view v-if="is_display_left" class="select" @tap.stop="not_display">
      <view :id="index" @tap.stop="select_left" v-for="(item, index) in c_order_way">{{item}}</view>
    </view>
    <view v-if="is_display_right" class="select" @tap.stop="not_display">
      <view :id="index" @tap.stop="select_right" v-for="(item, index) in c_days_list">{{item}}</view>
    </view>
  </view>
</template>

<script>
  export default {
    name: 'selector',
    props: {
      c_order_way: {
        default: []
      },
      c_days_list:{
        default: []
      },
      order_choice:{
        default: 0
      },
      day_choice:{
        default: 0
      }
    },
    data() {
      return {
        is_display_left: false,
        is_display_right: false
      }
    },
    methods: {
      _is_display_left() {
        this.is_display_left = !this.is_display_left
        this.is_display_right = false
      },
      _is_display_right() {
        this.is_display_right = !this.is_display_right
        this.is_display_left = false
      },
      not_display() {
        this.is_display_right = false
        this.is_display_left = false
      },
      select_left(e) {
        this.is_display_left = false
        console.log(this.$parent)
        this.$parent.$parent.refresh({order_choice:parseInt(e.currentTarget.id),day_choice:this.day_choice})
      },
      select_right(e) {
        this.is_display_right = false
        this.$parent.$parent.refresh({order_choice:this.order_choice,day_choice:parseInt(e.currentTarget.id)})
      },
    }
  }
</script>

<style>
  .select{
    width: 100%;
    position: absolute;
    top: 75upx;
    height: 1500upx;
    background-color: rgba(150,150,150,0.5);
    z-index: 5;
  }
  .select view{
    text-align: center;
    height: 60upx;
    display: flex;
    justify-content: center;
    background-color: rgba(255,255,255,1);
    width: 100%;
    padding: 10upx 0;
    border-bottom: 1px solid #cccccc;
    color: #7ca3cc;
    align-items: center;
  }
  ._header image{
    width: 50upx;
    height: 50upx;
  }
  ._header{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 10upx 2%;
    font-size: 16px;
    border-bottom: #ccc 1px solid;
  }
  ._header view{
    width: 50%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    text-align: center;
  }
  .selector{
    position: relative;
  }
</style>
