<template>
	<view>
    <!--pages/result/result.wxml-->
    <view class="page">
      <view class="weui-msg">
        <view class="weui-msg__icon-area">
          <image src="../../static/img/pass.png" style="width: 200upx;height: 200upx"></image>
        </view>
        <view class="weui-msg__text-area">
          <view class="weui-msg__title">发布{{result?'成功':'失败'}}</view>
        </view>
        <view class="weui-msg__opr-area">
          <view class="weui-btn-area">
            <button class="weui-btn" type="primary" @tap="to_my_topic">查看发布的话题</button>
            <button class="weui-btn" type="default" @tap="back_to_index">回到首页</button>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
	export default {
		data() {
			return {
        result: true,
        topic_id: 0,
        model_name: ''
			}
		},
    onLoad: function (options) {
      console.log(options)
      this.result = options.flag==='1'
      this.topic_id = options.topic_id
      this.model_name = options.model_name
    },
		methods: {
      back_to_index(){
        console.log('回到首页')
        uni.switchTab({
          url: '../index/index'
        })
      },
      to_my_topic(){
        var that = this
        if(that.model_name=='匿名表白墙'){
          uni.navigateTo({
            url: '../anouym_detail/anouym_detail?model_name='+that.model_name+'&topic_id='+that.topic_id
          })
        }else {
          uni.navigateTo({
            url: '../topic_detail/topic_detail?model_name='+that.model_name+'&topic_id='+that.topic_id
          })
        }
      },
    }
	}
</script>

<style>

</style>
