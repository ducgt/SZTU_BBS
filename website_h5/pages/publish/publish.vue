<template>
	<view>
    <view class="form">
      <form @submit="formSubmit" @reset="formReset">
        <picker @change="bindPickerChange" :value="value" :range="model" class="select_model">
          <text v-if="flag" style="color:#888">{{selectedModel}}</text>
          <text v-else style="color:#000">{{selectedModel}}</text>
          <image src="../../static/img/right.png" class="right"></image>
        </picker>
        <view class="title extend-margin">
          <input type="text" class="weui-input" v-model="title_input" placeholder="请输入标题" maxlength="16"></input>
          <text style="color:#888">{{title_input.length}}/16</text>
        </view>
        <view class="content extend-margin">
      <textarea placeholder="请输入内容" v-model="content_input" maxlength="1000"></textarea>
          <view style="color:#888;text-align: right;margin-right: 47upx">{{content_input.length}}/1000</view>
        </view>
        <view class='img-box'>
          <view class='img-list'>
            <block v-for="(item, index) in imgSrc" v-key="index">
              <view class='img-item'>
                <image :src='item' mode="aspectFill" :id='index' @tap="preview_image"></image>
                <image src="../../static/img/delete.png"  :id='index' @tap="delete_image" class="delete" style="width:30upx;height:30upx"></image>
              </view>
            </block>
            <view class='chooseimg' @tap='add_image' v-if="imgSrc.length<6">
              <view class="weui-uploader__input-box"></view>
            </view>
          </view>
        </view>
        <view>
          <button form-type="submit" type="primary" class="btn-sub">发布</button>
          <button form-type="reset" type="default" class="btn-reset">清空</button>
        </view>
      </form>
    </view>
  </view>
</template>

<script>
	export default {
		data() {
			return {
        model: uni.getStorageSync('model_list') || [],
        selectedModel: '请选择话题的版块',
        flag: true,
        title_input: '',
        content_input: '',
        imgSrc: [],
			}
		},
    onLoad: function (options) {
      var that = this
      uni.request({
        url: getApp().globalData.host+'article/get_model_list/',
        data:{
          token: getApp().globalData.token,
          user_id: getApp().globalData.user_info.id
        },
        success(res) {
          if (res.statusCode === 200) {
            that.model = res.data.model
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
    methods: {
      formReset() {
          this.imgSrc = []
          this.selectedModel = '请选择话题的版块'
          this.flag = true
          this.title_counts = 0
          this.content_counts = 0
          this.title_input = ''
          this.content_input = ''
          this.topic_id = 0
      },
      formSubmit(e) {
        var imgs = this.imgSrc
        var success_counts = 0
        var fail_counts = 0
        var that = this
        if (that.selectedModel === '请选择话题的版块') {
          uni.showToast({
            icon: "none",
            title: '请选择版块'
          })
        } else if (that.title_input.length === 0) {
          uni.showToast({
            icon: "none",
            title: '请输入标题'
          })
        } else if (that.content_input.length === 0) {
          uni.showToast({
            icon: "none",
            title: '请输入内容'
          })
        } else {
          uni.showToast({
            duration: 3000,
            icon: "loading",
            title: '正在发布'
          })
          uni.request({
            header: {
              "Content-Type": "application/x-www-form-urlencoded"
            },
            url: getApp().globalData.host+'article/publish_topic/',
            method: "POST",
            data: {
              model: that.selectedModel,
              title: that.title_input,
              user_id: getApp().globalData.user_info.id,
              content: that.content_input
            },
            success(res) {
              if (res.statusCode === 200) {
                console.log('文本发送成功')
                console.log(res)
                that.topic_id = res.data.topic_id
                for (var i = 0; i < imgs.length; i++) {
                  uni.uploadFile({
                    url: getApp().globalData.host+'article/upload_img/',
                    filePath: imgs[i],
                    name: 'file',
                    formData: {
                      topic_id: res.data.topic_id,
                      index: i
                    },
                  })
                }
                uni.navigateTo({
                  url: '../result/result?flag=1&model_name=' + that.selectedModel + '&topic_id=' + res.data.topic_id
                })
                that.formReset()
              } else {
                uni.showToast({
                  title: '服务器连接失败',
                  icon: "none"
                })
              }
            },
            fail(res) {
              uni.showToast({
                title: '发布失败',
                icon: "none"
              })
            }
          })
        }
      },
      preview_image(e) {
        var imgs = this.imgSrc
        var index = e.currentTarget.id
        uni.previewImage({
          current: imgs[index],
          urls: imgs
        })
      },
      delete_image(e) {
        console.log(e)
        var imgs = this.imgSrc
        var index = e.currentTarget.id
        imgs.splice(index, 1)
        console.log(imgs)
        console.log(index)
        this.imgSrc = imgs
        console.log(this.imgSrc)
      },
      add_image() {
        var that = this
        uni.chooseImage({
          count: 6 - that.imgSrc.length,//默认值为9
          sourceType: ['album', 'camera'],
          success(res) {
            // tempFilePath可以作为img标签的src属性显示图片
            const tempFilePaths = res.tempFilePaths //返回一个url数组
            console.log(res)
            that.imgSrc = that.imgSrc.concat(tempFilePaths)
          }
        })
      },
      bindPickerChange(e) {
        console.log(e)
        this.selectedModel = this.model[e.detail.value]
        this.flag = false
      },
    }
	}
</script>

<style>
  @import "publish.css";
</style>
