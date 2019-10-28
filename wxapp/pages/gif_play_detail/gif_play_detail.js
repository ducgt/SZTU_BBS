// pages/gif_play_detail/gif_play_detail.js
var app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    gif_data: '',
    new_gif: '',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    wx.request({
      url:app.globalData.host+'game/get_gif_play_detail/',
      data: {
        gif_id: options.id
      },
      success(res) {
        that.setData({
          gif_data: res.data.gif_data
        })
      }
    })
  },
  preview_image(e) {
    var that = this
    wx.previewImage({
      current: that.data.new_gif,
      urls: [that.data.new_gif]
    })
  },
  preview_image_2(e) {
    var that = this
    wx.previewImage({
      current: that.data.gif_data.gif_url,
      urls: [that.data.gif_data.gif_url]
    })
  },

  submit_form(e){
    console.log(e)
    // var sentences = []
    var dict = e.detail.value
    // for (var key in dict){
    //   sentences.push(dict[key])
    // }
    // console.log(sentences)
    var that = this
    wx.showLoading({
      title: '正在制作，请稍后',
    })

    wx.request({
      // url: 'https://sorry.xuty.tk/sorry/',
      // url: 'http://127.0.0.1:8000/game/gif_play/',
      url: app.globalData.host+'game/gif_play/',
      data: {
        sentences: dict,
        gif_id: that.data.gif_data.id,
      },
        // {
        // gif_id: that.data.gif_data.id,
        // sentences: sentences

      // },
      success(res) {
        console.log(res)
        wx.hideLoading()
        that.setData({
          new_gif: res.data.url
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
