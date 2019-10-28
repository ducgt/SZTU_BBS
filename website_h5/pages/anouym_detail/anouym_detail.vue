<template>
	<view>
    <view class="top">
      <view class="publisher_image">
        <image mode="aspectFill" src="../../static/img/anouym.png"></image>
      </view>
      <view class="publisher_info">
        <view class="pubilsher_name">
          <view class="name">
            <view>匿名用户</view>
            <image :src="gender_list[publisher_info.gender]"></image>
          </view>
          <view class="tip">楼主</view>
        </view>
        <view class="publish_date">
          {{topic_data.publish_date}}
        </view>
      </view>
    </view>
    <view class="header">
      <view class="title">
        <text>{{topic_data.title}}</text>
      </view>
      <view class="counts">
        <view class="left">
          <view>
            <image src="../../static/img/view.png"></image>
            <text>{{topic_data.view_counts}}</text>
          </view>
          <view>
            <image src="../../static/img/comment.png"></image>
            <text>{{topic_data.comment_counts}}</text>
          </view>
          <view>
            <image src="../../static/img/great.png"></image>
            <text>{{topic_data.great_counts}}</text>
          </view>
        </view>
        <view class="right">
          {{topic_data.in_session_name}}
        </view>
      </view>
    </view>
    <view class="body">
      <view>
        <text>
          {{topic_data.content}}
        </text>
      </view>
      <view class="img-list">
        <view v-for="(item, index) in topic_data.src" :id="index" @tap="preview_image">
          <image :src="item.url" mode="widthFix"></image>
        </view>
      </view>
    </view>
    <view class="comment">
      <view class="comment-header">
        <view class="left-border">
          <text>全部评论</text>
        </view>
        <view>
          <view @tap="change_order_way">更换排序方式</view>
        </view>
      </view>
      <view v-if="comment_data.length===0" style="margin: 60upx 0;text-align: center;color:#888">
        <text>当前还没有小伙伴评论哦！赶紧占楼吧！</text>
      </view>
      <view class="comment-item" @longpress="delete_or_up_comment" :data-to_top="item.to_top" :id="item.id" v-for="(item, index_comment) in comment_data">
        <view class="top">
          <view class="commenter_image">
            <image mode="aspectFill" :src="item.commenter_info.user_image" :id="item.commenter_info.id" @tap="to_user_info"></image>
          </view>
          <view class="publisher_info">
            <view class="comment-head">
              <view class="pubilsher_name">
                <view class="name">
                  <view>{{item.commenter_info.name}}</view>
                  <image :src="gender_list[item.commenter_info.gender]"></image>
                </view>
                <view class="tip">{{item.order}}楼</view>
                <view v-if="item.to_top" style="background-color: #ccc" class="tip">置顶</view>
              </view>
              <view class="counts">
                <view class="comment-left">
                  <view>
                    <image :data-index="index_comment" :src="item.had_like_comment?'../../static/img/great_.png':'../../static/img/great.png'"
                           @tap="like_comment"></image>
                    <text>{{item.great_counts}}</text>
                  </view>
                </view>
              </view>
            </view>
            <view class="comment-date">
              {{item.date}}
            </view>
            <view class="comment-content" :data-be_replyer_id="item.commenter_info.id" :id="index_comment" @tap="_is_reply">
              {{item.content}}
            </view>
            <view class="reply" v-if="item.reply_data.length>0">
              <view v-for="item_reply in item.reply_data" class="reply-item">
                <text style="color: deepskyblue;" @tap="to_user_info" :id="item_reply.replyer_id">{{item_reply.replyer_name}}</text>
                <text>回复</text>
                <text style="color: deepskyblue;" @tap="to_user_info" :id="item_reply.be_replyer_id">{{item_reply.be_replyer_name}}</text>
                <text :id="index_comment" data-flag="1" :data-be_replyer_id="item_reply.be_replyer_id" @tap="_is_reply">:{{item_reply.content}}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>
    <view style="height: 180upx"> </view>
    <view class="comment-input" v-if="!is_reply&&user_info.true_name.length>0">
      <view class="inline">
        <input type="text" v-model="comment_input" placeholder="写评论..." maxlength="50"></input>
        <view @tap="submit_comment">评论</view>
        <image :src="had_like_topic?'../../static/img/great_.png':'../../static/img/great.png'" @tap="like_topic"></image>
      </view>
    </view>
    <view class="comment-input" v-if="is_reply&&user_info.true_name.length>0">
      <view class="inline">
        <input type="text" v-model="reply_input" :focus='true' :placeholder="'回复'+comment_data[comment_index].commenter_info.name+'...'" maxlength="50"></input>
        <view @tap="submit_reply">回复</view>
        <view @tap="cancel_reply" style="background-color:#aaa">取消</view>
      </view>
    </view>
    <image src='../../static/img/to_top.png' class='goTop' v-if='floorstatus' @tap="goTop"></image>
  </view>
</template>

<script>
  export default {
		data() {
			return {
        topic_id: 0,
        topic_data: '',
        comment_data: '',
        publisher_info: '',
        had_like_topic: false,
        hot_or_latest: true,
        comment_input: '',
        reply_input: '',
        is_reply: false,
        comment_index: '',
        be_replyer_id: 0,
        flag: false,
        floorstatus: false,
        order_way: ['date', '-great_counts'],
        choice: 1,
        user_info: getApp().globalData.user_info,
        gender_list: ['','../../static/img/boy.png','../../static/img/girl.png']
			}
		},
    onLoad: function (options) {
      console.log(options)
      this.topic_id = options.topic_id
      var that = this
      uni.request({
        url: getApp().globalData.host+'article/get_topic_detail_data/',
        data: {
          token: getApp().globalData.token,
          user_id: that.user_info.id,
          topic_id: that.topic_id,
          order_way: that.order_way[that.choice]
        },
        success(res) {
          if (res.statusCode === 200) {
            console.log(res)
            that.topic_data = res.data.topic_data
            that.publisher_info = res.data.publisher_info
            that.had_like_topic = res.data.had_like_topic
            that.comment_data = res.data.comment_data
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
    // 获取滚动条当前位置
    onPageScroll: function (e) {
      if (e.scrollTop > 100) {
        this.floorstatus = true
      } else {
        this.floorstatus = false
      }
    },
    methods: {
      preview_image(e) {
        var src = this.topic_data.src
        let src_list = []
        var image
        for(var i = 0;i<src.length;i++){
          image = uni.getStorageSync('topic_image_'+src[i].id) || src[i].url
          src_list = src_list.concat(image)
        }
        var that = this;
        uni.previewImage({
          current: src_list[e.currentTarget.id],
          urls: src_list
        })
      },
      // comment_input(e) {
      //   this.setData({
      //     comment_input: e.detail.value
      //   })
      // },
      // reply_input(e) {
      //   this.setData({
      //     reply_input: e.detail.value
      //   })
      // },
      submit_comment() {
        var that = this
        if (that.comment_input.length > 0) {
          uni.request({
            url: getApp().globalData.host+'user/comment_topic/',
            data: {
              token: getApp().globalData.token,
              user_id: that.user_info.id,
              topic_id: that.topic_id,
              content: that.comment_input,
              order_way: that.order_way[that.choice]
            },
            success(res) {
              if (res.statusCode === 200) {
                uni.showToast({
                  title: res.data.msg,
                  icon: "none"
                })
                console.log(res)
                that.topic_data = res.data.topic_data
                that.publisher_info = res.data.publisher_info
                that.had_like_topic = res.data.had_like_topic
                that.comment_data = res.data.comment_data
                that.comment_input = ''
                that.is_reply = false
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
        } else {
          uni.showToast({
            title: '您还未输入内容',
            icon: "none"
          })
        }
      },
      like_topic() {
        var that = this
        uni.request({
          url: getApp().globalData.host+'user/like_topic/',
          data: {
            token: getApp().globalData.token,
            had_like: that.had_like_topic ? 1 : 0,
            user_id: that.user_info.id,
            topic_id: that.topic_id,
          },
          success(res) {
            if (res.statusCode === 200) {
              uni.showToast({
                title: res.data.msg,
                icon: "none"
              })
              that.had_like_topic = !that.had_like_topic
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
      like_comment(e) {
        var that = this
        var index = e.currentTarget.dataset.index
        uni.request({
          url: getApp().globalData.host+'user/like_comment/',
          data: {
            token: getApp().globalData.token,
            had_like: that.comment_data[index].had_like_comment ? 1 : 0,
            user_id: that.user_info.id,
            comment_id: that.comment_data[index].comment_id,
          },
          success(res) {
            if (res.statusCode === 200) {
              uni.showToast({
                title: res.data.msg,
                icon: "none"
              })
              that.comment_data[index].great_counts = that.comment_data[index].had_like_comment ? that.comment_data[index].great_counts - 1 : that.comment_data[index].great_counts + 1
              that.comment_data[index].had_like_comment = !that.comment_data[index].had_like_comment
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
      to_user_info(e) {
        console.log(e)
        var id = e.currentTarget.id
        uni.navigateTo({
          url: '../user_info/user_info?id=' + id
        })
      },
      _is_reply(e) {
          this.is_reply = true
          this.comment_index = e.currentTarget.id
          this.be_replyer_id = e.currentTarget.dataset.be_replyer_id
		  console.log(this.be_replyer_id)
		  console.log(e)
          this.flag = true
      },
      cancel_reply() {
        this.is_reply = false
      },
      submit_reply() {
        var that = this
        if (that.reply_input.length > 0) {
          uni.request({
            url: getApp().globalData.host+'user/reply_in_comment/',
            data: {
              token: getApp().globalData.token,
              comment_id: that.comment_data[that.comment_index].id,
              be_replyer_id: that.flag ? that.be_replyer_id : that.comment_data[that.comment_index].commenter_info.id,
              user_id: that.user_info.id,
              content: that.reply_input,
              order_way: that.order_way[that.choice],
              topic_id: that.topic_id,
            },
            success(res) {
              if (res.statusCode === 200) {
                uni.showToast({
                  title: res.data.msg,
                  icon: "none"
                })
                console.log(res)
                that.topic_data = res.data.topic_data
                that.publisher_info = res.data.publisher_info
                that.had_like_topic = res.data.had_like_topic
                that.comment_data = res.data.comment_data
                that.reply_input = ''
                that.is_reply = false
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
        } else {
          uni.showToast({
            title: '您还未输入内容',
            icon: "none"
          })
        }
      },
      //回到顶部
      goTop: function (e) {  // 一键回到顶部
        if (uni.pageScrollTo) {
          uni.pageScrollTo({
            scrollTop: 0
          })
        } else {
          uni.showModal({
            title: '提示',
            content: '当前微信版本过低，无法使用该功能，请升级到最新微信版本后重试。'
          })
        }
      },
      change_order_way() {
        var that = this
        that.choice = that.choice ? 0 : 1
        uni.request({
          url: getApp().globalData.host+'article/get_topic_detail_data/',
          data: {
            token: getApp().globalData.token,
            user_id: that.user_info.id,
            topic_id: that.topic_id,
            order_way: that.order_way[that.choice]
          },
          success(res) {
            if (res.statusCode === 200) {
              console.log(res)
              that.topic_data = res.data.topic_data
              that.publisher_info = res.data.publisher_info
              that.had_like_topic = res.data.had_like_topic
              that.comment_data = res.data.comment_data
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
      delete_or_up_comment(e) {
        console.log(e)
        if (this.publisher_info.id === this.user_info.id || this.user_info.is_superuser) {
          var that = this
          var to_top = e.currentTarget.dataset.to_top
          var comment_id = e.currentTarget.id
          uni.showActionSheet({
            itemList: [to_top ? '取消置顶' : '置顶', '删除'],
            success(res) {
              if (res.tapIndex === 0) {
                // 置顶或取消置顶评论
                uni.request({
                  url: getApp().globalData.host+'article/to_top_comment/',
                  data: {
                    token: getApp().globalData.token,
                    user_id: that.user_info.id,
                    topic_id: that.topic_id,
                    order_way: that.order_way[that.choice],
                    comment_id: comment_id,
                    to_top: to_top
                  },
                  success(res) {
                    if (res.statusCode === 200) {
                      uni.showToast({
                        title: res.data.msg,
                        icon: "none"
                      })
                      that.topic_data = res.data.topic_data
                      that.publisher_info = res.data.publisher_info
                      that.had_like_topic = res.data.had_like_topic
                      that.comment_data = res.data.comment_data
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
              } else if (res.tapIndex === 1) {
                // 删除评论
                uni.showModal({
                  title: '提示',
                  content: '确定删除该评论吗？',
                  success(res) {
                    if (res.confirm) {
                      console.log('点击了确定')
                      uni.request({
                        url: getApp().globalData.host+'article/delete_comment/',
                        data: {
                          token: getApp().globalData.token,
                          user_id: that.user_info.id,
                          topic_id: that.topic_id,
                          order_way: that.order_way[that.choice],
                          comment_id: comment_id
                        },
                        success(res) {
                          if (res.statusCode === 200) {
                            uni.showToast({
                              title: res.data.msg,
                              icon: "none"
                            })
                            that.topic_data = res.data.topic_data
                            that.publisher_info = res.data.publisher_info
                            that.had_like_topic = res.data.had_like_topic
                            that.comment_data = res.data.comment_data
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
                    } else if (res.cancel) {
                      console.log('用户点了取消')
                    }
                  }
                })
              }
            }
          })
        }
      },
    }
	}
</script>

<style>
  @import "../topic_detail/topic_detail.css";
</style>
