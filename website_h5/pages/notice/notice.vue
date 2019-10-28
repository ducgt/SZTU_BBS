<template>
	<view>
    <view class="page" v-if="user_info.true_name.length>0">
      <view class="page__bd">
        <view class="weui-tab">
          <view class="weui-navbar" style="background-color: #fff">
            <block v-for="(item, index) in tabs" v-key="index">
              <view :id="index" class="weui-navbar__item" @tap="tabClick" :class="{weui_bar__item_on:activeIndex == index }">
                <view class="weui-navbar__title">{{item}}</view>
              </view>
            </block>
            <view class="weui-navbar__slider" :style="{'left': sliderLeft+'px', 'transform': 'translateX('+sliderOffset+'px'+')', '-webkit-transform': 'translateX('+sliderOffset+'px'+')'}"></view>
          </view>
          <view class="weui-tab__panel">
            <view class="weui-tab__content" v-if="activeIndex == 0">
              <view class="line_">
                <view class="title_">标题</view>
                <view class="date_">发布日期</view>
              </view>
              <navigator :url="'../notice_detail/notice_detail?id='+item.id" class="line" :style="{backgroundColor: index%2===1?'#f1f7fc':''}" v-for="(item, index) in notice_data_left">
                <view class="title">{{item.title}}</view>
                <view class="date">{{item.date}}</view>
              </navigator>
            </view>
            <view class="weui-tab__content" v-if="activeIndex == 1">
              <view class="line_">
                <view class="title_">标题</view>
                <view class="date_">发布日期</view>
              </view>
              <navigator :url="'../notice_detail/notice_detail?id='+item.id" class="line" :style="{backgroundColor: index%2===1?'#f1f7fc':''}" v-for="(item, index) in notice_data_right">
                <view class="title">{{item.title}}</view>
                <view class="date">{{item.date}}</view>
              </navigator>
            </view>
          </view>
        </view>
      </view>
    </view>
    <view v-else class="to_confirm">
      <navigator class="button" url="../school_confirm/school_confirm">点击绑定教务系统</navigator>
    </view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
        tabs: ["学生工作", "校园生活"],
        activeIndex: 0,
        sliderOffset: 0,
        sliderLeft: 0,
        notice_data_left: wx.getStorageSync('notice_data_left') || [],
        notice_data_right: wx.getStorageSync('notice_data_right') || [],
        user_info: getApp().globalData.user_info,
        sliderWidth: 96
			}
		},
		methods: {
      tabClick: function (e) {
        this.sliderOffset = e.currentTarget.offsetLeft
        this.activeIndex = e.currentTarget.id
      }
		},
    onHide(){
      wx.setStorageSync('notice_data_left', this.notice_data_left)
      wx.setStorageSync('notice_data_right', this.notice_data_right)
    },
    onLoad: function () {
      var that = this;
      wx.getSystemInfo({
        success: function(res) {
            that.sliderLeft = (res.windowWidth / that.tabs.length - that.sliderWidth) / 2
            that.sliderOffset = res.windowWidth / that.tabs.length * that.activeIndex
        }
      });
      wx.request({
        url: getApp().globalData.host+'notice/get_student_work_data/',
        data: {

        },
        success(res) {
          if (res.statusCode===200){
            console.log(res)
            that.notice_data_left = res.data.notice_data
          } else {
            wx.showToast({
              icon: "none",
              title: '服务器连接失败'
            })
          }
        },
        fail(res) {
          wx.showToast({
            icon: "none",
            title: '网络异常'
          })
        }
      })
      wx.request({
        url: getApp().globalData.host+'notice/get_school_life_data/',
        data: {
          token: getApp().globalData.token,
        },
        success(res) {
          if (res.statusCode===200){
            console.log(res)
              that.notice_data_right = res.data.notice_data
          } else {
            wx.showToast({
              icon: "none",
              title: '服务器连接失败'
            })
          }
        },
        fail(res) {
          wx.showToast({
            icon: "none",
            title: '网络异常'
          })
        }
      })
    },
    onShow(){
      this.user_info = getApp().globalData.user_info
    },
	}
</script>

<style>
  /* pages/notice/notice.wxss */
  page,
  .page,
  .page__bd{
      height: 100%;
  }
  .page__bd{
      padding-bottom: 0;
  }
  .weui-tab__content{

  }
  .line_{
      display: flex;
      padding: 1% 0;
      background-color: #1e71bf;
  }
  .title_{
      width: 80%;
      font-size: 30upx;
      text-align: center;
      color: white;
  }
  .date_{
      width: 20%;
      font-size: 30upx;
      text-align: center;
      color: white;
  }
  .title{
      width: 80%;
      font-size: 28upx;
      margin: 1%;
  }
  .line{
      display: flex;
      background-color: #f8f8f8;
  }
  .date{
      width: 18%;
      font-size: 25upx;
      text-align: center;
      display: flex;
      justify-content: center;
      align-items: center;
  }
  .to_confirm{
      text-align: center;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
  }
  .button{
      background-color: limegreen;
      padding: 15upx;
      border-radius: 15upx;
      width: 50%;
  }

</style>
