// pages/team_person/team_person.js
var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    days: [],
    room_data:'',
    series_days: 0,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let room_id = options.room_id
    let user_id = options.user_id
    let that = this
    wx.request({
      url: app.globalData.host+'game/get_days/',
      data: {
        room_id: room_id,
        user_id: user_id
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
      url: app.globalData.host+'game/get_room_data/',
      data: {
        room_id: room_id,
        user_id: user_id
      },
      success(res) {
        console.log(res)
        that.setData({
          room_data: res.data.room_data
        })
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
