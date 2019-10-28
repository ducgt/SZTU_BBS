<template>
	<view>
    <selector :c_order_way="c_order_way" :c_days_list="c_days_list" :order_choice="order_choice" :day_choice="day_choice"></selector>
    <view class="tip" v-if="all_data.length===0">您当前还未赞过任何话题哦！</view>
    <navigator hover-class="none" :url="'../topic_detail/topic_detail?topic_id='+item.topic_data.id" class="hot-topic-item"
               v-for="item in all_data">
      <view class="header">
        {{item.like_data.creatime}}
      </view>
      <topic :topic_data="item.topic_data"></topic>
    </navigator>
    <image src='../../static/img/to_top.png' class='goTop' v-if='floorstatus' @tap.stop="goTop"></image>
	</view>
</template>

<script>
  import topic from '@/components/topic.vue'
  import selector from '@/components/selector.vue'
  export default {
    components:{
      selector,
      topic
    },
    data() {
			return {
        all_data: uni.getStorageSync('my_like_topic_data') || [],
        floorstatus: false,
        order_way: ['-creatime', '-topic__great_counts'],
        c_order_way: ['按时间排序', '按热度排序'],
        order_choice: 1,
        days_list: [3, 7, 30, 2000],
        c_days_list: ['三天内的话题', '七天内的话题', '一个月内的话题', '全部话题'],
        day_choice: 0,
			}
		},
    onLoad: function (options) {
      var that = this
      console.log(getApp().globalData.user_info)
      uni.request({
        url: getApp().globalData.host+'user/get_my_like_topic/',
        data: {
          token: getApp().globalData.token,
          user_id: getApp().globalData.user_info.id,
          order_way: that.order_way[that.order_choice],
          days: that.days_list[that.day_choice]
        },
        success(res) {
          console.log(res)
          if (res.statusCode === 200) {
            that.all_data = res.data.all_data
          }else{
            uni.showToast({
              title: '服务器连接失败',
              icon: "none"
            })
          }
        },
        fail(res) {
          uni.showToast({
            title: '网络异常',
            icon: "none"
          })
        }
      })
    },
    onPageScroll: function (e) {
      this.floorstatus = e.scrollTop > 100;
    },
    onUnload: function () {
      uni.setStorageSync('my_like_topic_data', this.all_data)
    },
    methods: {
      goTop: function (e) {  // 一键回到顶部
        if (uni.pageScrollTo) {
          uni.pageScrollTo({
            scrollTop: 0
          })
        } else {
          uni.showModal({
            title: '提示',
            content: '当前微信版本过低，无法使用该功能，请升级到最新微信版本后重试。'
          })
        }
      },
      refresh(e){
        console.log(e)
        var that = this
        this.order_choice = e.order_choice
        this.day_choice = e.day_choice
        uni.request({
          url: getApp().globalData.host+'user/get_my_like_topic/',
          data: {
            token: getApp().globalData.token,
            user_id: getApp().globalData.user_info.id,
            order_way: that.order_way[that.order_choice],
            days: that.days_list[that.day_choice]
          },
          success(res) {
            console.log(res)
            if (res.statusCode === 200) {
              that.all_data = res.data.all_data
            }else{
              uni.showToast({
                title: '服务器连接失败',
                icon: "none"
              })
            }
          },
          fail(res) {
            uni.showToast({
              title: '网络异常',
              icon: "none"
            })
          }
        })
      },


    }
	}
</script>

<style>
  .hot-topic-item{
    border-bottom: 4px #f1f0f5 solid;
    /*height: 350rpx;*/
  }
  .header{
    margin: 1% 2%;
    border-bottom: #e5e5e5 solid 1px;
    width: 96%;
    font-size: 14px;
    color: #999999;
  }
  .tip{
    margin-top: 100rpx;
    text-align: center;
    color: #555;
  }

</style>
