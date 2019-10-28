<template>
  <view>
    <image @tap="preview_image" class="img" mode="widthFix" :src="notice_data.detail_image_url"></image>
  </view>
</template>

<script>
  export default {
    data() {
      return {
        notice_id: 0,
        notice_data: '',
      }
    },
    methods: {
      preview_image(e) {
        var that = this
        uni.previewImage({
          current: that.notice_data.detail_image_url,
          urls: [that.notice_data.detail_image_url]
        })
      },
    },
    onLoad: function(options) {
      this.notice_id = options.id
      var that = this
      wx.request({
        url: getApp().globalData.host+'notice/get_notice_detail_data/',
        data: {
          notice_id: options.id
        },
        success(res) {
          that.notice_data = res.data
        }
      })
    },
  }
</script>

<style>
  .img{
    width: 100%;
  }

</style>
