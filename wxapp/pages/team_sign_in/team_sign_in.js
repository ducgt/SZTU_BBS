// pages/team_sign_in/team_sign_in.js
let app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    room_list: wx.getStorageSync("room_list")|| [],
    flag: true,
    cur_index: 0,
    content: "",
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let that = this
    wx.request({
      url: app.globalData.host+'game/my_rooms/',
      data: {
        user_id: app.globalData.user_info.id,
        type: 0
      },
      success(res) {
        console.log(res)
        that.setData({
          room_list: res.data.my_room_data,
        })
      }
    })
  },
  delete_room(e){
    let that = this
    let room_data = that.data.room_list[e.currentTarget.id]
    if(room_data.is_room_master){
      wx.showModal({
        title: "提示",
        content: "确定删除这个房间吗？",
        success(res) {
          if (res.confirm){
            wx.request({
              url: app.globalData.host+'game/delete_room/',
              data: {
                user_id: app.globalData.user_info.id,
                room_id: room_data.room_data.id,
                type: 0
              },
              success(res) {
                console.log(res)
                if (res.statusCode===200){
                  that.setData({
                    room_list: res.data.my_room_data
                  })
                  wx.showModal({
                    title: "提示",
                    content: res.data.msg,
                    showCancel: false
                  })
                }
              }
            })
          }
        }
      })
    }else {
      wx.showModal({
        title: "提示",
        content: "确定退出这个房间吗？",
        success(res) {
          if (res.confirm){
            wx.request({
              url: app.globalData.host+'game/quit_room/',
              data: {
                user_id: app.globalData.user_info.id,
                user_in_room_id: room_data.id,
                type: 0
              },
              success(res) {
                console.log(res)
                if (res.statusCode===200){
                  that.setData({
                    room_list: res.data.my_room_data
                  })
                  wx.showModal({
                    title: "提示",
                    content: res.data.msg,
                    showCancel: false
                  })
                }
              }
            })
          }
        }
      })
    }
  },
  to_room(e){
    console.log(e)
    let that = this
    wx.navigateTo({
      url: "../team_room/team_room?room_data="+JSON.stringify(that.data.room_list[e.currentTarget.id])
    })
  },
  to_sign(e){
    this.setData({
      flag: false,
      cur_index: e.currentTarget.id
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
  sign_in(){
    let that = this
    let room_data = that.data.room_list[that.data.cur_index].room_data
    wx.request({
      url: app.globalData.host+'game/sign_in/',
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
            room_list: res.data.my_room_data,
            flag: true,
            content: ""
          })
          wx.showModal({
            title: "提示",
            content: res.data.msg,
            showCancel: false
          })
        }
      }
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
    wx.setStorageSync("room_list",this.data.room_list)
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    wx.setStorageSync("room_list",this.data.room_list)
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
