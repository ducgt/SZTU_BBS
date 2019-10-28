<template>
	<view>
    <selector :c_order_way="c_order_way" :c_days_list="c_days_list" :order_choice="order_choice" :day_choice="day_choice"></selector>
    <view class="tip" v-if="topic_data.length===0">您当前还未发布过任何话题哦！</view>
    <navigator hover-class="none" class="hot-topic-item" v-for="item in topic_data" :url="'../topic_detail/topic_detail?topic_id='+item.id"
               @longpress="delete_topic" :id="item.id">
      <topic :topic_data="item"></topic>
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
        order_way: ['-great_counts', '-publish_date'],
        c_order_way: ['按热度排序', '按时间排序'],
        order_choice: 0,
        days_list: [3, 7, 30, 2000],
        c_days_list: ['三天内的话题', '七天内的话题', '一个月内的话题', '全部话题'],
        day_choice: 0,
        topic_data: uni.getStorageSync('my_publish_data') || [],
        floorstatus: false
      }
		},
    onLoad: function (options) {
      var that = this
      uni.request({
        url: getApp().globalData.host+'user/get_my_publish/',
        data: {
          token: getApp().globalData.token,
          user_id: getApp().globalData.user_info.id,
          order_way: that.order_way[that.order_choice],
          days: that.days_list[that.day_choice]
        },
        success(res) {
          console.log(res)
          if (res.statusCode === 200) {
            that.topic_data = res.data.topic_data
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
    onUnload: function () {
      uni.setStorageSync('my_publish_data', this.data.topic_data)
    },
    onPageScroll: function (e) {
      if (e.scrollTop > 100) {
        this.setData({
          floorstatus: true
        });
      } else {
        this.setData({
          floorstatus: false
        });
      }
    },
    methods: {
      refresh(e){
        console.log(e)
        var that = this
        this.order_choice = e.order_choice
        this.day_choice = e.day_choice
        uni.request({
          url: getApp().globalData.host+'user/get_my_publish/',
          data: {
            token: getApp().globalData.token,
            user_id: getApp().globalData.user_info.id,
            order_way: that.order_way[that.order_choice],
            days: that.days_list[that.day_choice]
          },
          success(res) {
            console.log(res)
            if (res.statusCode === 200) {
              that.topic_data = res.data.topic_data
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
      //回到顶部
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
      delete_topic(e) {
        var that = this
        var topic_id = e.currentTarget.id
        uni.showModal({
          title: '提示',
          content: '是否删除该话题？',
          success(res) {
            if (res.confirm) {
              uni.request({
                url: getApp().globalData.host+'user/delete_topic/',
                data: {
                  token: getApp().globalData.token,
                  user_id: getApp().globalData.user_info.id,
                  order_way: that.order_way[that.order_choice],
                  days: that.days_list[that.day_choice],
                  topic_id: topic_id
                },
                success(res) {
                  if (res.statusCode === 200) {
                    that.topic_data = res.data.topic_data
                    uni.showToast({
                      title: '删除成功'
                    })
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
            }
          }
        })
      },
    },
	}
</script>

<style>
  .tip{
    margin-top: 100upx;
    text-align: center;
    color: #555;
  }
  .hot-topic-item{
    border-bottom: 4px #f1f0f5 solid;
    /*height: 350rpx;*/
  }

</style>
