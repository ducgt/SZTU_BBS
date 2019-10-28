// pages/announce/announce.js
var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    announce: wx.getStorageSync('announce') || '',
    had_button: true,
    check: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  checkboxChange(e){
    console.log(e)
    this.setData({
      check: !this.data.check
    })
  },
  onLoad: function (options) {
    var that = this
    wx.request({
      url: app.globalData.host+'user/announce/',
      header:{
        token: 'rIhyLkd8OpxStlbk8nYT'
      },
      success(res) {
        if (res.statusCode === 200) {
          console.log(res)
          that.setData({
            announce: res.data.Announce
          })
        }else {
          wx.showToast({
            title: '服务器请求失败',
            icon: "none"
          })
        }
      },
      fail(res) {
        wx.showToast({
          title: '网络异常',
          icon: "none"
        })
      }
    })
  },
  agree(){
    if(this.data.check){
      wx.redirectTo({
        url: '../notice/notice'
      })
    }else{
      wx.showToast({
        title: '请先同意用户协议',
        icon: 'none'
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
    wx.setStorageSync('announce', this.data.announce)
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
