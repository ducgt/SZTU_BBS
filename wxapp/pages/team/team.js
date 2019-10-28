// pages/team/team.js
let app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    flag: true,
    room_num: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },
  to_sign_in(){
    wx.navigateTo({
      url: '../team_sign_in/team_sign_in'
    })
  },
  create_room(){
    let that = this
    wx.showActionSheet({
      itemList: ["加入房间", "创建房间"],
      success(res) {
        console.log(res)
        if (res.tapIndex===0){
          that.setData({
            flag: false
          })
        }else if (res.tapIndex===1){
          wx.navigateTo({
            url: '../team_new_room/team_new_room'
          })
        }
      }
    })
  },
  cancel(){
    this.setData({
      flag: true
    })
  },
  room_num_inp(e){
    this.setData({
      room_num: e.detail.value
    })
  },
  join(){
    let that = this
    if (that.data.room_num.length>0){
      wx.request({
        url: app.globalData.host+'game/join_room/',
        data: {
          user_id: app.globalData.user_info.id,
          room_number: that.data.room_num
        },
        success(res) {
          console.log(res)
          if (res.statusCode===200){
            wx.showModal({
              title: '提示',
              content: res.data.msg,
              showCancel: false,
              success(e) {
                if (e.confirm){
                  that.setData({
                    room_num: '',
                    input_flag: 0
                  })
                  wx.navigateTo({
                    url: "../team_sign_in/team_sign_in"
                  })
                }
              }
            })
          }else if (res.statusCode===300){
            wx.showModal({
              title: '提示',
              content: res.data.msg,
              showCancel: false
            })
          }
        }
      })
    }else {
      wx.showModal({
        title: '提示',
        content: "房间号不能为空",
        showCancel: false
      })
    }
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
