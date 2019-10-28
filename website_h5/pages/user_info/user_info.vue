<template>
	<view>
    <view class="info_form">
      <view class="form-item">
        <text class="line-head">昵称</text>
        <input v-if="input_flag" type="text" maxlength="8" v-model="user_info.name"></input>
        <text v-else>{{user_info.name}}</text>
      </view>
      <view class="form-item">
        <text class="line-head">性别</text>
        <picker style="width:60%" v-if="input_flag" :value="value" :range="gender_select" @change="change_gender">
          {{gender_select[user_info.gender]}}
        </picker>
        <text v-else>{{gender_select[user_info.gender]}}</text>
      </view>
      <view class="form-item" v-if="is_user">
        <text class="line-head">真实姓名</text>
        <text>{{user_info.true_name}}</text>
      </view>
      <view class="form-item" v-if="is_user">
        <text class="line-head">学号</text>
        <text>{{user_info.school_account}}</text>
      </view>
      <view class="form-item">
        <text class="line-head">E-mail</text>
        <input v-if="input_flag" type="text" v-model="user_info.email"></input>
        <text v-else>{{user_info.email===null?'':user_info.email}}</text>
      </view>
      <view class="form-item">
        <text class="line-head">手机号码</text>
        <input v-if="input_flag" type="number" maxlength="11" v-model="user_info.mobile"></input>
        <text v-else>{{user_info.mobile===null?'':user_info.mobile}}</text>
      </view>
      <view class="form-item">
        <text class="line-head">生日</text>
        <picker style="width:60%" v-if="input_flag" mode="date" fields="day" :value="date" start="1900-01-01" end="2018-12-31" @change="birthday_change">
          {{user_info.birthday===null?'请选择日期':user_info.birthday}}
        </picker>
        <text v-else>{{user_info.birthday===null?'':user_info.birthday}}</text>
      </view>
      <view class="_form-item">
        <text class="line-head">个人介绍</text>
        <textarea v-if="input_flag" type="text" style="width:65%" maxlength="200" v-model="user_info.introduce"></textarea>
        <text v-else style="width:65%">{{user_info.introduce===null?'':user_info.introduce}}</text>
      </view>
      <view class="form-item" style="border: 0px">
        <text class="line-head">注册时间</text>
        <text>{{user_info.register_date.split('T')[0]}}</text>
      </view>
    </view>
    <button v-if="is_user" type="primary" @tap="edit_or_submit_info" class="btn">{{edit_or_submit}}</button>
  </view>
</template>

<script>
	export default {
		data() {
			return {
        input_flag: false,
        edit_or_submit: '编 辑',
        gender_select: ['不显示', '男', '女'],
        user_info: null,
        is_user: true
      }
		},
    onLoad: function (options) {
      console.log(options)
      var publisher_id = options.id
      var that = this
      var id
      if (publisher_id == getApp().globalData.user_info.id || !publisher_id) {
        that.user_info = getApp().globalData.user_info
      } else {
        id = publisher_id
        that.is_user = false
        uni.request({
          url: getApp().globalData.host+'user/get_info/',
          data: {
            token: getApp().globalData.token,
            id: id
          },
          success(res) {
            if (res.statusCode === 200) {
              console.log(res)
              that.user_info = res.data
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
      }
    },
    methods: {
      edit_or_submit_info() {
        if (this.input_flag) {
          //结束编辑模式，提交修改后的数据
          if(this.user_info.name==""||this.user_info.name==null){
            uni.showToast({
              icon: 'none',
              title: '名字不能为空'
            })
          }else {
            this.input_flag = false
            this.edit_or_submit = '编 辑'
            var that = this
            //更新数据库数据
            uni.request({
              url: getApp().globalData.host+'user/change_info/',
              data: {
                token: getApp().globalData.token,
                id: getApp().globalData.user_info.id,
                name: that.user_info.name,
                gender: that.user_info.gender,
                email: that.user_info.email,
                mobile: that.user_info.mobile,
                birthday: that.user_info.birthday,
                introduce: that.user_info.introduce,
              },
              success(res) {
                if (res.statusCode === 200) {
                  console.log(res)
                  uni.showToast({
                    title: res.data.msg,
                    icon: 'none'
                  })
                  getApp().globalData.user_info = res.data.user_info
                } else {
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
          }
        } else {
          // 进入编辑模式
          this.input_flag = true
          this.edit_or_submit = '提 交'
        }
      },
      change_gender(e) {
        console.log(e)
        this.user_info.gender = e.detail.value
      },
      birthday_change(e) {
        console.log(e)
        this.user_info.birthday = e.detail.value
      },
    }
	}
</script>

<style>
  page{
    background-image: url("https://sztubbs-1259072275.cos.ap-guangzhou.myqcloud.com/background/user_info_bg.jpg");
    background-size: 100% 100%;
  }
  .info_form{
    display: flex;
    flex-direction: column;
    margin: 0 30upx;
    background-color: white;
    border-radius: 30upx;
    margin-top: 80upx;
  }
  .form-item{
    margin: 0 2%;
    display: flex;
    flex-direction: row;
    border-bottom: lightgrey solid 1px;
    font-size: 16px;
    height: 100upx;
    align-items: center;
  }
  .form-item text{
  }
  .line-head{
	width: 30%;
  }
  .btn{
    position: fixed;
    top: 10upx;
    right: 4%;
    width: 15%;
    font-size: 24upx;
  }
  ._form-item{
    margin: 0 2%;
    padding: 25upx 0;
    display: flex;
    flex-direction: row;
    border-bottom: lightgrey solid 1px;
    font-size: 16px;
  }
  ._form-item text{
    width: 30%;
  }

</style>
