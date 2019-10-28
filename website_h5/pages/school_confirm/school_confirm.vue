<template>
	<view class="page">
    <view class="header">
      <image src="../../static/img/logo_.png"></image>
      <view style="font-size: 80upx; margin-top: -30upx;font-family: art">技大论坛</view>
      <view>教务系统验证</view>
    </view>
    <view class="form">
      <view class="input">
        <view>
          <image src="../../static/img/account.png"></image>
        </view>
        <input type="number" placeholder="请输入学号" v-model="account"></input>
      </view>
      <view class="input">
        <view>
          <image src="../../static/img/password.png"></image>
        </view>
        <input type="password" placeholder="请输入密码" v-model="password"></input>
      </view>
      <view @tap="submit" class="submit">登录</view>
    </view>
  </view>
</template>

<script>
	export default {
		data() {
			return {
        password: '',
        account: ''
			}
		},
		methods: {
      submit(){
        var that = this
        if (that.account && that.password) {
          uni.showLoading({
            title: '请耐心等待'
          })
          uni.request({
            url: getApp().globalData.host+'user/confirm_school_account/',
            data: {
              token: getApp().globalData.token,
              user_id: getApp().globalData.user_info.id,
              account: that.account,
              password: that.password
            },
            success(res) {
              if (res.statusCode === 200) {
                getApp().globalData.user_info = res.data.user_info
                uni.showModal({
                  title: '提示',
                  content: res.data.msg,
                  showCancel: false,
                  success(res) {
                    if (res.confirm) {
                      uni.switchTab({
                        url: '../index/index'
                      })
                    }
                  }
                })
              }else {
                uni.showToast({
                  icon: "none",
                  title: res.data.msg
                })
              }
            },
            fail(res) {
              uni.showToast({
                icon: "none",
                title: '网络异常'
              })
            },
            complete(res) {
              uni.hideLoading()
            }
          })
        }else {
          uni.showToast({
            icon: "none",
            title: '请先填写信息'
          })
        }
      },
		}
	}
</script>

<style>
  page{
    background-image: url("https://sztubbs-1259072275.cos.ap-guangzhou.myqcloud.com/background/login_bg.jpg");
    background-size: 100% 100%;
  }
  /*page{*/
  /*  background-image: url("https://sztubbs-1259072275.cos.ap-guangzhou.myqcloud.com/background/login_bg.png");*/
  /*  background-size: 100% 100%;*/
  /*}*/
  /*.background{*/
  /*  width: 100%;*/
  /*  height: 100vh;*/
  /*  position: fixed;*/
  /*  z-index: 2;*/
  /*}*/
  .page{
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 1;
  }
  .header{
    text-align: center;
    font-size: 20px;
    color: white;
    padding: 20upx;
    border-radius: 20upx;
    width: 50%;
    margin-top: 200upx;
  }
  .header image{
    width: 320upx;
    height: 190upx;
  }
  .form{
    width: 90%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 500upx;
    background-color: rgba(39, 142, 255, 0.3);
    border-radius: 30upx;
    position: fixed;
    bottom: 80upx;
  }
  .input{
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    border-radius: 10upx;
    font-size: 18px;
    padding: 10upx;
    margin: 30upx;
  }
  .input input{
    text-align: left;
    margin-left: 10upx;
  }
  .input view{
    align-items: center;
    justify-content: center;
    display: flex;
  }
  .input image{
    width: 50upx;
    height: 50upx;
  }
  .submit{
    background-color: #58d021;
    font-size: 18px;
    border-radius: 20upx;
    width: 64%;
    margin: 20upx;
    padding: 5upx;
    color: #fff;
  }

</style>
