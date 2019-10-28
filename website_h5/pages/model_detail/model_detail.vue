<template>
	<view>
    <view class="header" :style="{'background-color':model_data.color}">
      <view class="logo">
        <image :src="model_data.src" mode="aspectFill"></image>
      </view>
      <view class="info">
        <view class="introduce">
          <text>版块介绍\n</text>
          <text style="font-size:14px;">{{model_data.introduce}}</text>
        </view>
        <view class="topic-counts">
          <text>话题量: {{model_data.topic_counts}}</text>
        </view>
      </view>
    </view>
    <selector :c_order_way="c_order_way" :c_days_list="c_days_list" :order_choice="order_choice" :day_choice="day_choice"></selector>
    <view class="topic">
      <view class="tip_" v-if="topic_data.length===0">当前版块还没有任何话题哦！</view>
      <navigator hover-class="none" @longpress="delete_or_up_topic" :url="'../topic_detail/topic_detail?topic_id='+item.id"
                 class="topic-item" v-for="(item, index_topic) in topic_data" :id="item.id" :data-to_top="item.to_top">
        <view class="topic-header">
          <view class="topic-header-left">
            <image :src="item.publisher_info.user_image" mode="aspectFill"></image>
            <view class="publish_info">
              <view style="font-size: 16px;color: #414141" class="name">
                <text>{{item.publisher_info.name}}</text>
                <image :src="gender_list[item.publisher_info.gender]"></image>
              </view>
              <view style="font-size: 12px;color: #999">{{item.publish_date}}</view>
            </view>
          </view>
          <view class="topic-header-right">
            <text v-if="item.to_top">置顶</text>
          </view>
        </view>
        <view class="content">
          {{item.title}}
        </view>
        <view class='img-list'>
          <block v-for="(item_src, index) in item.src" v-key="index">
            <view class='img-item' :data-topic-index="index_topic" :id="index" @tap.stop="preview_image">
              <image :src='item_src.url' mode="aspectFill"></image>
            </view>
          </block>
        </view>
        <view class="topic-footer">
          <view class="great">
            <image src="../../static/img/comment.png"></image>
            <text>{{item.comment_counts}}</text>
          </view>
          <view class="great">
            <image src="../../static/img/great.png"></image>
            <text>{{item.great_counts}}</text>
          </view>
        </view>
      </navigator>
    </view>
    <image src='../../static/img/to_top.png' class='goTop' v-if='floorstatus' @tap="goTop"></image>

  </view>
</template>

<script>
  import selector from '@/components/selector.vue'
  export default {
    components:{
      selector,
    },
		data() {
			return {
        model_id: 0,
        model_data: '',
        topic_data: [],
        floorstatus: false,
        order_way: ['-publish_date', '-great_counts'],
        c_order_way: ['按时间排序', '按热度排序'],
        order_choice: 1,
        days_list: [3, 7, 30, 2000],
        c_days_list: ['三天内的话题', '七天内的话题', '一个月内的话题', '全部话题'],
        day_choice: 0,
        gender_list: ['','../../static/img/boy.png','../../static/img/girl.png']
			}
		},
    onUnload: function () {
      wx.setStorageSync('model_detail_data' + this.model_id, this.topic_data)
    },
    onLoad: function (options) {
      console.log(options)
      this.model_id = options.model_id
      this.topic_data = uni.getStorageSync('model_detail_data' + options.model_id)

      var that = this
      uni.request({
        // url: 'http://127.0.0.1:8000/article/get_model_detail_data/',
        url: getApp().globalData.host+'article/get_model_detail_data/',
        data: {
          token: getApp().globalData.token,
          model_id: that.model_id,
          order_way: that.order_way[that.order_choice],
          days: that.days_list[that.day_choice]
        },
        success(res) {
          if (res.statusCode === 200) {
            console.log(res)
            that.model_data = res.data.model_data
            that.topic_data = res.data.topic_data
          } else {
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
      if (e.scrollTop > 100) {
        this.floorstatus = true
      } else {
        this.floorstatus = false
      }
    },
    onPullDownRefresh: function () {
      // 标题栏显示刷新图标，转圈圈
      console.log("onPullDownRefresh");

      // 请求最新数据
      var that = this
      uni.request({
        // url: 'http://127.0.0.1:8000/article/get_model_detail_data/',
        url: getApp().globalData.host+'article/get_model_detail_data/',
        data: {
          token: getApp().globalData.token,
          model_id: that.model_id,
          order_way: that.order_way[that.order_choice],
          days: that.days_list[that.day_choice]
        },
        success(res) {
          if (res.statusCode === 200) {
            console.log(res)
            that.model_data = res.data.model_data
            that.topic_data = res.data.topic_data
            uni.showToast({
              title: '刷新成功'
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
      uni.stopPullDownRefresh()
    },
    methods: {
      refresh(e){
        console.log(e)
        var that = this
        this.order_choice = e.order_choice
        this.day_choice = e.day_choice
        uni.request({
          // url: 'http://127.0.0.1:8000/article/get_model_detail_data/',
          url: getApp().globalData.host+'article/get_model_detail_data/',
          data: {
            token: getApp().globalData.token,
            model_id: that.model_id,
            order_way: that.order_way[that.order_choice],
            days: that.days_list[that.day_choice]
          },
          success(res) {
            if (res.statusCode === 200) {
              console.log(res)
              that.model_data = res.data.model_data
              that.topic_data = res.data.topic_data
            } else {
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
      preview_image(e) {
        console.log(e)
        var topic_index = e.currentTarget.dataset.topicIndex
        var src = this.topic_data[topic_index].src
        let src_list = []
        var image
        for(var i = 0;i<src.length;i++){
          image = uni.getStorageSync('topic_image_'+src[i].id) || src[i].url
          src_list = src_list.concat(image)
        }
        var that = this;
        uni.previewImage({
          current: src_list[e.currentTarget.id],
          urls: src_list
        })
      },
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
      delete_or_up_topic(e) {
        console.log(e)
        if (getApp().globalData.user_info.is_superuser) {
          var that = this
          var to_top = e.currentTarget.dataset.to_top
          var topic_id = e.currentTarget.id
          uni.showActionSheet({
            itemList: [to_top ? '取消置顶' : '置顶', '删除'],
            success(res) {
              if (res.tapIndex === 0) {
                // 置顶或取消置顶话题
                uni.request({
                  url: getApp().globalData.host+'article/to_top_topic/',
                  data: {
                    token: getApp().globalData.token,
                    user_id: getApp().globalData.user_info.id,
                    topic_id: topic_id,
                    model_id: that.model_id,
                    order_way: that.order_way[that.order_choice],
                    days: that.days_list[that.day_choice],
                    to_top: to_top
                  },
                  success(res) {
                    if (res.statusCode === 200) {
                      uni.showToast({
                        title: res.data.msg,
                        icon: "none"
                      })
                      that.model_data = res.data.model_data
                      that.topic_data = res.data.topic_data
                    } else {
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
              } else if (res.tapIndex === 1) {
                // 删除话题
                uni.showModal({
                  title: '提示',
                  content: '确定删除该话题吗？',
                  success(res) {
                    if (res.confirm) {
                      console.log('点击了确定')
                      uni.request({
                        url: getApp().globalData.host+'article/delete_topic/',
                        data: {
                          token: getApp().globalData.token,
                          user_id: getApp().globalData.user_info.id,
                          topic_id: topic_id,
                          model_id: that.model_id,
                          order_way: that.order_way[that.order_choice],
                          days: that.days_list[that.day_choice],
                        },
                        success(res) {
                          if (res.statusCode === 200) {
                            uni.showToast({
                              title: res.data.msg,
                              icon: "none"
                            })
                            that.model_data = res.data.model_data
                            that.topic_data = res.data.topic_data
                          } else {
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
                    } else if (res.cancel) {
                      console.log('用户点了取消')
                    }
                  }
                })
              }
            }
          })
        }
      },

    }
	}
</script>

<style>
  @import "model_detail.css";
</style>
