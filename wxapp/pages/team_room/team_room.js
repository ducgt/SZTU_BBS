// pages/team_room/team_room.js
let app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    days: [],
    delete_flag: false,
    user_list: [],
    room_data:'',
    series_days: 0,
    flag: true,
    content: '',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let room_data = JSON.parse(options.room_data)
    let that = this
    console.log(room_data)
    this.setData({
      room_data: room_data,
    })
    wx.request({
      url: app.globalData.host+'game/get_days/',
      data: {
        room_id: room_data.room_data.id,
        user_id: app.globalData.user_info.id
      },
      success(res) {
        console.log(res)
        that.setData({
          days: res.data.days_data,
          series_days: res.data.series_days,
        })
      }
    })

    wx.request({
      url: app.globalData.host+'game/get_user_list/',
      data: {
        room_id: room_data.room_data.id
      },
      success(res) {
        console.log(res)
        that.setData({
          user_list: res.data.user_data
        })
      }
    })
  },
  show_delete(){
    this.setData({
      delete_flag: !this.data.delete_flag,
    })
  },
  to_sign(){
    this.setData({
      flag: false,
    })
  },
  cancel(){
    this.setData({
      flag: true
    })
  },
  content_input(e){
    this.setData({
      content: e.detail.value
    })
  },
  to_person_info(e){
    wx.navigateTo({
      url: "../team_person/team_person?user_id="+this.data.user_list[e.currentTarget.id].id+"&room_id="+this.data.room_data.room_data.id
    })
  },
  sign_in(){
    let that = this
    let room_data = that.data.room_data.room_data
    wx.request({
      url: app.globalData.host+'game/sign_in_room/',
      data: {
        user_id: app.globalData.user_info.id,
        room_id: room_data.id,
        type: 0,
        content: that.data.content
      },
      success(res) {
        console.log(res)
        if (res.statusCode===200){
          that.setData({
            room_data: res.data.my_room_data,
            flag: true,
            content: ""
          })
          wx.showModal({
            title: "提示",
            content: res.data.msg,
            showCancel: false
          })
          wx.request({
            url: app.globalData.host+'game/get_user_list/',
            data: {
              room_id: room_data.id
            },
            success(res) {
              console.log(res)
              that.setData({
                user_list: res.data.user_data
              })
            }
          })
          wx.request({
            url: app.globalData.host+'game/get_days/',
            data: {
              room_id: room_data.id,
              user_id: app.globalData.user_info.id
            },
            success(res) {
              console.log(res)
              that.setData({
                days: res.data.days_data,
                series_days: res.data.series_days,
              })
            }
          })
        }
      }
    })
  },
  delete_user(e){
    console.log(e)
    let that = this
    if (that.data.user_list[e.currentTarget.id].id==that.data.room_data.room_data.user_id){
      wx.showModal({
        title: "提示",
        content: "不可删除房主",
        showCancel: false
      })
    }else if (app.globalData.user_info.id!=that.data.room_data.room_data.user_id){
      wx.showModal({
        title: "提示",
        content: "你没有移除成员的权限",
        showCancel: false
      })
    }else {
      wx.showModal({
        title: "提示",
        content:"确定删除该用户吗？",
        success(re) {
          if (re.confirm){
            wx.request({
              url: app.globalData.host+'game/delete_user/',
              data: {
                room_id: that.data.room_data.id,
                user_id: that.data.user_list[e.currentTarget.id].id
              },
              success(res) {
                console.log(res)
                wx.showModal({
                  title: "提示",
                  content:res.data.msg,
                  showCancel: false
                })
                that.setData({
                  user_list: res.data.user_data
                })
              }
            })
          }
        }
      })
    }
  },
  onDayClick(e){
    console.log(e)
  },
  to_my_diary(){
    wx.navigateTo({
      url: "../my_diary/my_diary?room_id="+this.data.room_data.room_data.id
    })
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})
