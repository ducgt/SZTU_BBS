<template>
	<view class="page">
    <view v-if="!imgSrc" style="font-size: 60upx;font-family: logo;color: white">请选择头像</view>
    <view class='chooseimg' @tap='add_image'>
      <view v-if="!imgSrc" class="weui-uploader__input-box" style="width: 100%;height: 100%;position: absolute;border-width: 0upx"></view>
      <image :src="imgSrc" mode="aspectFill" v-else></image>
    </view>
		<view class="name">
      <view style="font-family: logo;color: white;font-size: 43upx">昵称:</view>
      <input type="text" v-model="name" placeholder="请输入昵称(不超过10个字符)" maxlength="10">
    </view>
    <button type="primary" @tap="next">下一步</button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
        imgSrc: '',
        name: ''
			}
		},
		onLoad() {
			if(getApp().globalData.user_info.name.length > 0){
				uni.switchTab({
					url: '../index/index'
				})
			}
		},
		onShow() {
			if(getApp().globalData.user_info.name.length > 0){
				uni.switchTab({
					url: '../index/index'
				})
			}
		},
		methods: {
      add_image() {
        var that = this
        uni.chooseImage({
          count: 1,
          sizeType: ['compressed'],
          sourceType: ['album', 'camera'],
          success(res) {
            // tempFilePath可以作为img标签的src属性显示图片
            const tempFilePaths = res.tempFilePaths //返回一个url数组
            console.log(tempFilePaths)
            that.imgSrc = tempFilePaths[0]
          }
        })
      },
      next(){
        var that = this
        if (this.name.length===0){
          uni.showToast({
            title: '请输入昵称',
            icon: 'none'
          })
        }else if(this.imgSrc.length===0){
          uni.showToast({
            title: '请选择头像',
            icon: 'none'
          })
        }else {
          uni.showLoading({
            title: '正在注册',
            mask: true
          })
          uni.request({
            url: getApp().globalData.host+'user/register_name/',
            data:{
              user_id: getApp().globalData.user_info.id,
              name: that.name
            },
            success(res) {
              uni.uploadFile({
                url: getApp().globalData.host+'user/register_head_image/',
                filePath: that.imgSrc,
                name: 'file',
                formData:{
                  user_id: getApp().globalData.user_info.id
                },
                success(res) {
                  getApp().globalData.user_info = JSON.parse(res.data).user_info
                  uni.setStorageSync('user_info', JSON.parse(res.data).user_info)
                  uni.setStorageSync('is_first_login', 2)
                  uni.showModal({
                    showCancel: false,
                    title: '提示',
                    content: '注册成功',
                    success(res) {
                      if (res.confirm) {
                        uni.switchTab({
                          url: '../index/index'
                        })
                      }
                    }
                  })
                }
              })
            },
            complete(res) {
              uni.hideLoading()
            }
          })
        }
      }
		}
	}
</script>

<style>
  page{
    background-image: url("https://sztubbs-1259072275.cos.ap-guangzhou.myqcloud.com/background/user_info_bg.jpg");
    background-size: 100% 100%;
  }
  .page{
    display: flex;
    flex-direction: column;
    margin-top: 200upx;
    align-items: center;
    justify-content: center;
  }
  .chooseimg {
    background-color: #f1f0f5;
    width: 400upx;
    height: 400upx;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    position: relative;
    margin: 160upx 0;
  }
  .chooseimg image{
    width: 400upx;
    height: 400upx;
    border-radius: 50%;
  }
  .name{
    width: 90%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40upx;
    margin-top: 40rpx;
  }
  .name input{
    background-color: white;
    border-radius: 20upx;
    height: 80upx;
    font-size: 36upx;
    width: 80%;
    padding-left: 20upx;
    margin-left: 20rpx;
  }
  button{
    margin-top: 50upx;
    width: 90%;
  }
</style>
