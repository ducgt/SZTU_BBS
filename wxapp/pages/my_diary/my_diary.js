// pages/my_diary/my_diary.js
let app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    diary_list: [],
    MONTHS_EN: ['', 'January.', 'February.', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let room_id = options.room_id
    let that = this
    wx.request({
      url:app.globalData.host+'game/get_diary/',
      data:{
        room_id: room_id,
        user_id: app.globalData.user_info.id
      },
      success(res) {
        that.setData({
          diary_list: res.data.diary_list
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
