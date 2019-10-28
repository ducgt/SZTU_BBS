<template>
  <view>
    <view class="logo">
      <image src="../../static/img/logo.png"></image>
      <view>技大论坛 SZTUBBS</view>
    </view>
    <view class="body">
      <view style="text-align: left;width: 80%;margin-left: 10%">
        <text>联系我们:\n1. 发送E-mail到963849727@qq.com反馈\n2. 在反馈建议版块发帖反馈，我们会尽快答复</text>
      </view>
    </view>
    <view class="footer">
      技大论坛团队 版权所有
    </view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
        apk_url: '',
        platform: 'android'
			}
		},
    onLoad(){
		  var that = this
		  uni.getSystemInfo({
        success(res) {
          console.log(res)
          that.version = res.version
          that.platform = res.platform
        }
      })
    },
	}
</script>

<style>
  page{
    background-color: #f1f0f5;
    text-align: center;
  }
  .logo{
    margin-top: 100upx;
  }
  .logo image{
    width: 260upx;
    height: 260upx;
    border-radius: 20upx;
    margin-bottom: 50upx;
  }
  .body{
    margin-top: 60upx;
  }
  .footer{
    font-size: 26upx;
    color: #999;
    position: fixed;
    bottom: 50upx;
    width: 100%;
    text-align: center;
  }
  .update{
    margin-top: 280upx;
    width: 80%;
    margin-left: 10%;
  }
</style>
