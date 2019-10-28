<template>
	<view>
    <view class="page">
      <view class="page__bd">
        <view class="weui-tab">
          <view class="weui-navbar">
            <block v-for="(item, index) in tabs" v-key="index">
              <view :id="index" style="background-color: #fff" class="weui-navbar__item" @tap="tabClick" :class="{weui_bar__item_on:activeIndex == index }">
                <view class="weui-navbar__title" style="display:flex; width:100%;justify-content: center;">
                  <view>{{item}}</view>
                  <view class="barge" v-if="index===0&&user_info.disread_like_topic>0">{{user_info.disread_like_topic}}</view>
                  <view class="barge" v-if="index===1&&user_info.disread_like_comment>0">{{user_info.disread_like_comment}}</view>
                  <view class="barge" v-if="index===2&&user_info.disread_comment>0">{{user_info.disread_comment}}</view>
                  <view class="barge" v-if="index===3&&user_info.disread_reply>0">{{user_info.disread_reply}}</view>
                </view>
              </view>
            </block>
            <view class="weui-navbar__slider" :style="{'left': sliderLeft+'px', 'transform': 'translateX('+sliderOffset+'px'+')', '-webkit-transform': 'translateX('+sliderOffset+'px'+')'}"></view>
          </view>
          <view class="weui-tab__panel">
            <view class="weui-tab__content" v-if="activeIndex == 0">
              <view class="tip" v-if="topic_like_data.length===0">当前还没有用户赞你哦</view>
              <view v-for="(item, index) in topic_like_data" class="box"
                    :style="{'background-color':item.is_read?'':'rgba(255,255,0,0.2)'}">
                <navigator hover-class="none" :url="'../user_info/user_info?id='+item.clicker.id" class="left">
                  <image :src="item.clicker.user_image" mode="aspectFill"></image>
                </navigator>
                <view @tap="to_topic_detail" :data-index="index" :id="item.topic_id" class="right">
                  <view class="head">
                    <view style="color: #017">{{item.clicker.name}}</view>
                    <view style="color: #777;font-size: 14px">{{item.creatime}}</view>
                  </view>
                  <text style="font-size: 14px;color: #555">赞了我的话题</text>
                  <view class="in_topic">
                    {{item.topic_title}}
                  </view>
                </view>
              </view>
            </view>
            <view class="weui-tab__content" v-if="activeIndex == 1">
              <view class="tip" v-if="comment_like_data.length===0">当前还没有用户赞你哦</view>
              <view v-for="(item, index) in comment_like_data" class="box"
                    :style="{'background-color':item.is_read?'':'rgba(255,255,0,0.2)'}">
                <navigator hover-class="none" :url="'../user_info/user_info?id='+item.clicker.id" class="left">
                  <image :src="item.clicker.user_image" mode="aspectFill"></image>
                </navigator>
                <view @tap="to_topic_detail" :data-index="index" :id="item.topic_id" class="right">
                  <view class="head">
                    <view style="color: #017">{{item.clicker.name}}</view>
                    <view style="color: #777;font-size: 14px">{{item.creatime}}</view>
                  </view>
                  <text style="font-size: 14px;color: #555">赞了我的评论</text>
                  <view style="font-size: 14px">
                    {{item.comment_content}}
                  </view>
                  <view class="in_topic" >
                    {{item.topic_title}}
                  </view>
                </view>
              </view>
            </view>
            <view class="weui-tab__content" v-if="activeIndex == 2">
              <view class="tip" v-if="comment_data.length===0">当前还没有用户评论你的话题哦</view>
              <view v-for="(item, index) in comment_data" class="box"
                    :style="{'background-color':item.is_read?'':'rgba(255,255,0,0.2)'}">
                <navigator hover-class="none" :url="'../user_info/user_info?id='+item.commenter.id" class="left">
                  <image :src="item.commenter.user_image" mode="aspectFill"></image>
                </navigator>
                <view @tap="to_topic_detail" :data-index="index" :id="item.topic_id" class="right">
                  <view class="head">
                    <view style="color: #017">{{item.commenter.name}}</view>
                    <view style="color: #777;font-size: 14px">
                      {{item.date}}
                    </view>
                  </view>
                  <view>
                    <text style="font-size: 14px;color: #555">评论我:</text>
                    <text style="font-size: 14px">{{item.content}}</text>
                  </view>
                  <view class="in_topic">
                    {{item.topic_title}}
                  </view>
                </view>
              </view>
            </view>
            <view class="weui-tab__content" v-if="activeIndex == 3">
              <view class="tip" v-if="reply_data.length===0">当前还没有用户回复你哦</view>
              <view v-for="(item, index) in reply_data" class="box"
                    :style="{'background-color':item.is_read?'':'rgba(255,255,0,0.2)'}">
                <navigator hover-class="none" :url="'../user_info/user_info?id='+item.replyer.id" class="left">
                  <image :src="item.replyer.user_image" mode="aspectFill"></image>
                </navigator>
                <view @tap="to_topic_detail" :data-index="index" :id="item.topic_id" class="right">
                  <view class="head">
                    <view style="color: #017">{{item.replyer.name}}</view>
                    <view style="color: #777;font-size: 14px">
                      {{item.date}}
                    </view>
                  </view>
                  <view>
                    <text style="font-size: 14px;color: #555">回复我:</text>
                    <text style="font-size: 14px"> {{item.content}}</text>
                  </view>
                  <view class="in_comment">
                    <text style="font-size: 14px">所在评论: {{item.comment_content}}</text>
                  </view>
                  <view class="in_topic" >
                    {{item.topic_title}}
                  </view>
                </view>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>
    <view v-if="!is_display" @tap.stop="display" class="circle">
      <image src="../../static/img/circle.png"></image>
    </view>
    <view class="select" v-if="is_display">
      <view @tap.stop="display">
        <image src="../../static/img/right_2.png"></image>
      </view>
      <view class="right_">
        <view class="select-item" @tap.stop="select" v-for="(item, index) in c_days_list" :id="index">
          {{item}}
        </view>
      </view>
    </view>
  </view>
</template>

<script>
  var sliderWidth = 96; // 需要设置slider的宽度，用于计算中间位置
  var app = getApp()
	export default {
		data() {
			return {
        tabs: ["赞我的话题", '赞我的评论', "评论我的", "回复我的"],
        activeIndex: 0,
        sliderOffset: 0,
        sliderLeft: 0,
        comment_data: uni.getStorageSync('link_to_me_data1') || [],
        reply_data: uni.getStorageSync('link_to_me_data2') || [],
        topic_like_data: uni.getStorageSync('link_to_me_data3') || [],
        comment_like_data: uni.getStorageSync('link_to_me_data4') || [],
        user_info: '',
        days_list: [1, 3, 7, 30, 2000],
        c_days_list: ['一天内的消息','三天内的消息', '七天内的消息', '一个月内的消息', '全部消息'],
        day_choice: 0,
        is_display: false
			}
		},
		methods: {
      display() {
        this.is_display = !this.is_display
      },
      select(e) {
        var that = this
        that.day_choice = e.currentTarget.id
        that.is_display = false
        uni.request({
          url: getApp().globalData.host+'user/get_link_to_me_data1/',
          // url: 'http://127.0.0.1:8000/user/get_link_to_me_data1/',
          data: {
            token: getApp().globalData.token,
            user_id: app.globalData.user_info.id,
            days: that.days_list[that.day_choice]
          },
          success(res) {
            if (res.statusCode === 200) {
              console.log(res)
              that.comment_data = res.data.comment_data
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
        uni.request({
          url: getApp().globalData.host+'user/get_link_to_me_data2/',
          // url: 'http://127.0.0.1:8000/user/get_link_to_me_data2/',
          data: {
            token: getApp().globalData.token,
            user_id: app.globalData.user_info.id,
            days: that.days_list[that.day_choice]
          },
          success(res) {
            if (res.statusCode === 200) {
              console.log(res)
                that.reply_data = res.data.reply_data
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
        uni.request({
          url: getApp().globalData.host+'user/get_link_to_me_data3/',
          // url: 'http://127.0.0.1:8000/user/get_link_to_me_data3/',
          data: {
            token: getApp().globalData.token,
            user_id: app.globalData.user_info.id,
            days: that.days_list[that.day_choice]
          },
          success(res) {
            if (res.statusCode === 200) {
              console.log(res)
              that.topic_like_data = res.data.topic_like_data
              uni.showToast({
                title: '数据加载完毕'
              })
            } else {
              uni.showToast({
                title: '网络异常',
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
        uni.request({
          url: getApp().globalData.host+'user/get_link_to_me_data4/',
          // url: 'http://127.0.0.1:8000/user/get_link_to_me_data4/',
          data: {
            token: getApp().globalData.token,
            user_id: app.globalData.user_info.id,
            days: that.days_list[that.day_choice]
          },
          success(res) {
            if (res.statusCode === 200) {
              console.log(res)
              that.comment_like_data = res.data.comment_like_data
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
      to_topic_detail(e){
        var that = this
        console.log(e)
        switch (parseInt(this.activeIndex)) {
          case 0:
            if (!that.topic_like_data[e.currentTarget.dataset.index].is_read) {
              that.topic_like_data[e.currentTarget.dataset.index].is_read = true
              that.user_info.disread_like_topic = that.user_info.disread_like_topic - 1
            }
            break
          case 1:
            if (!that.comment_like_data[e.currentTarget.dataset.index].is_read) {
              that.comment_like_data[e.currentTarget.dataset.index].is_read = true
              that.user_info.disread_like_comment = that.user_info.disread_like_comment - 1
            }
            break
          case 2:
            if (!that.comment_data[e.currentTarget.dataset.index].is_read) {
              that.comment_data[ e.currentTarget.dataset.index ].is_read = true
              that.user_info.disread_comment = that.user_info.disread_comment - 1
            }
            break
          case 3:
            if (!that.reply_data[e.currentTarget.dataset.index].is_read) {
                that.reply_data[ e.currentTarget.dataset.index].is_read = true
                that.user_info.disread_reply = that.user_info.disread_reply - 1
            }
            break
        }
        uni.navigateTo({
          url: "../topic_detail/topic_detail?topic_id="+e.currentTarget.id
        })
      },
      tabClick: function (e) {
          this.sliderOffset = e.currentTarget.offsetLeft
          this.activeIndex = e.currentTarget.id
      }
		},
    onUnload() {
      for (var i = 0; i < app.globalData.disread_reply; i++) {
          that.reply_data[i].is_read = true
      }
      for (i = 0; i < app.globalData.disread_comment; i++) {
          that.comment_data[i].is_read = true
      }
      for (i = 0; i < app.globalData.disread_like_topic; i++) {
          that.topic_like_data[i].is_read = true
      }
      for (i = 0; i < app.globalData.disread_like_comment; i++) {
          that.comment_like_data[i].is_read = true
      }
      uni.setStorageSync('link_to_me_data1', this.comment_data)
      uni.setStorageSync('link_to_me_data2', this.reply_data)
      uni.setStorageSync('link_to_me_data3', this.topic_like_data)
      uni.setStorageSync('link_to_me_data4', this.comment_like_data)
      app.globalData.user_info.disread_sum = 0
      app.globalData.user_info.disread_reply = 0
      app.globalData.user_info.disread_comment = 0
      app.globalData.user_info.disread_like_topic = 0
      app.globalData.user_info.disread_like_comment = 0
    },
    onLoad: function () {
      var that = this;
      uni.getSystemInfo({
        success: function (res) {
            that.sliderLeft = (res.windowWidth / that.tabs.length - sliderWidth) / 2
            that.sliderOffset = res.windowWidth / that.tabs.length * that.activeIndex
            that.user_info = app.globalData.user_info
            that.activeIndex = 0
        }
      });
      uni.request({
        url: getApp().globalData.host+'user/get_link_to_me_data1/',
        // url: 'http://127.0.0.1:8000/user/get_link_to_me_data1/',
        data: {
          token: getApp().globalData.token,
          user_id: app.globalData.user_info.id,
          days: that.days_list[that.day_choice]
        },
        success(res) {
          if (res.statusCode === 200) {
            console.log(res)
            that.comment_data = res.data.comment_data
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
      uni.request({
        url: getApp().globalData.host+'user/get_link_to_me_data2/',
        // url: 'http://127.0.0.1:8000/user/get_link_to_me_data2/',
        data: {
          token: getApp().globalData.token,
          user_id: app.globalData.user_info.id,
          days: that.days_list[that.day_choice]
        },
        success(res) {
          if (res.statusCode === 200) {
            console.log(res)
            that.reply_data = res.data.reply_data
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
      uni.request({
        url: getApp().globalData.host+'user/get_link_to_me_data3/',
        // url: 'http://127.0.0.1:8000/user/get_link_to_me_data3/',
        data: {
          token: getApp().globalData.token,
          user_id: app.globalData.user_info.id,
          days: that.days_list[that.day_choice]
        },
        success(res) {
          if (res.statusCode === 200) {
            console.log(res)
            that.topic_like_data = res.data.topic_like_data
            uni.showToast({
              title: '数据加载完毕'
            })
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
      uni.request({
        url: getApp().globalData.host+'user/get_link_to_me_data4/',
        // url: 'http://127.0.0.1:8000/user/get_link_to_me_data4/',
        data: {
          token: getApp().globalData.token,
          user_id: app.globalData.user_info.id,
          days: that.days_list[that.day_choice]
        },
        success(res) {
          if (res.statusCode === 200) {
            console.log(res)
            that.comment_like_data = res.data.comment_like_data
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
	}
</script>

<style>
  @import "link_to_me.css";
</style>
