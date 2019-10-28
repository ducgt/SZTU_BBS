var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    notice_id: 0,
    notice_data: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      notice_id: options.id
    })
    var that = this
    wx.request({
      url: app.globalData.host+'notice/get_notice_detail_data/',
      data: {
        notice_id: options.id
      },
      success(res) {
        that.setData({
          notice_data: res.data
        })
      }
    })
  },
  preview_image(e) {
    var that = this
    wx.previewImage({
      current: that.data.notice_data.detail_image_url,
      urls: [that.data.notice_data.detail_image_url]
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
