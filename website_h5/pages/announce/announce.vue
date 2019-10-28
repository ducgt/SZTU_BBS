<template>
	<view>
    <view class="page" :style="{'margin-bottom':had_button?'100upx':''}">
      <view class="header">用户协议</view>
      <view v-for="session_item in announce" class="session">
        <view class="title">{{session_item.title}}</view>
        <view v-for="(content_item, index) in session_item.item" class="content">
          <view class="content-item">
            <view class="left">
              第{{index+1}}条
            </view>
            <view class="right">
              {{content_item.content}}
              <view v-for="item in content_item.detail">
                <view class="detail">{{item}}</view>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>
    <button v-if="had_button" class="button" type="primary" @tap="agree">我同意以上用户协议</button>
  </view>
</template>

<script>
	export default {
		data() {
			return {
        announce: uni.getStorageSync('announce') || '',
        had_button: false
			}
		},
    onUnload: function () {
      uni.setStorageSync('announce', this.data.announce)
    },
    onLoad: function (options) {
      var that = this
      that.had_button = !!options.flag
      uni.request({
        url: getApp().globalData.host+'user/announce/',
        data:{
          token: getApp().globalData.token
        },
        success(res) {
          if (res.statusCode === 200) {
            console.log(res)
            that.announce = res.data.Announce
          }else {
            console.log(res)
            uni.showToast({
              title: '服务器请求失败',
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
    methods: {
      agree(){
        uni.switchTab({
          url: '../index/index'
        })
      },
		}
	}
</script>

<style>
  page{
    margin: 20upx 2%;
    width: 96%;
  }
  .page{
    border-radius: 40upx;
    background-color: rgba(255,255,0,0.3);
    padding: 30upx 2%;
  }
  .header{
    font-size: 22px;
    margin-bottom: 30upx;
    text-align: center;
  }
  .session{
    margin-bottom: 20upx;
  }
  .title{
    font-size: 18px;
  }
  .content-item{
    display: flex;
    margin-bottom: 10upx;
  }
  .left{
    width: 15%;
  }
  .right{
    width: 85%;
  }
  .button{
    position: fixed;
    bottom: 0;
    width: 100%;
    left: 0;
  }

</style>
