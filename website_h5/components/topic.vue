<template>
	<view>
    <view class="topic-header _margin">
      <view>{{topic_data.title}}</view>
      <view class="right-text">赞 {{topic_data.great_counts}} 评论 {{topic_data.comment_counts}}</view>
    </view>
    <view class="topic-body _margin">
      <view class="hot-topic-text">
        <view class='img-list'>
          <block v-for="(item, index) in topic_data.src" :key="index">
            <view class='img-item' @tap.stop="preview_image" :id="index">
              <image :src='item.url' mode="aspectFill"></image>
            </view>
          </block>
        </view>
        <view  class="footer">
          <view>{{topic_data.publisher_info.name}}</view>
          <view>{{topic_data.publish_date}}</view>
        </view>
      </view>
    </view>
	</view>
</template>

<script>
	export default {
	  name: 'topic',
    props:{
      topic_data:{
        type: Object,
        default: {}
      },
    },
		data() {
			return {

			};
		},
    methods:{
      preview_image(e) {
        var src = this.topic_data.src
        let src_list = []
        var image
        for(var i = 0;i<src.length;i++){
          image = uni.getStorageSync('topic_image_'+src[i].id) || src[i].url
          src_list = src_list.concat(image)
          console.log(image)
          console.log(src_list)
        }
        var that = this;
        uni.previewImage({
          current: src_list[e.currentTarget.id],
          urls: src_list
        })
      },
    }
	}
</script>

<style>
  ._margin{
    margin: 2%;
  }
  .right-text{
    font-size: 14px;
  }
  .topic-header{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  .topic-body{
    font-size: 14px;
    color: #555;
    display: flex;
    flex-direction: row;
    width: 96%;
    position: relative;
    justify-content: space-between;
  }
  .hot-topic-item image{
    width: 25%;
    position: relative;
  }
  .hot-topic-text{
    width: 100%;
  }
  .footer{
    font-size: 12px;
    color: #999;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
  }
  .img-item image {
    width: 180upx;
    height: 180upx;
  }
  .img-item {
    width: 30%;
    text-align: left;
    margin-right: 20upx;
    margin-bottom: 10upx;
    position: relative;
  }
  .img-list {
    display: flex;
    display: -webkit-flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    flex-wrap: wrap;
  }

</style>
