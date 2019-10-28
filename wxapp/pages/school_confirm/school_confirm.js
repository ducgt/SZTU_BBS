// pages/school_confirm/school_confirm.js
var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    password: '',
    account: ''
  },

  account(e){
    this.setData({
      account: e.detail.value
    })
  },
  password(e){
    this.setData({
      password: e.detail.value
    })
  },
  submit(){
    var that = this
    if (that.data.account && that.data.password) {
      wx.showLoading({
        title: '请耐心等待'
      })
      wx.request({
        url: app.globalData.host+'user/confirm_school_account/',
        header:{
          token: 'rIhyLkd8OpxStlbk8nYT',
        },
        data: {
          user_id: app.globalData.user_id,
          account: that.data.account,
          password: that.data.password
        },
        success(res) {
          if (res.statusCode === 200) {
            app.globalData.user_info = res.data.user_info
            wx.setStorageSync('user_info', res.data.user_info)
            wx.showModal({
              title: '提示',
              content: res.data.msg,
              showCancel: false,
              success(res) {
                if (res.confirm) {
                  wx.redirectTo({
                    url: '../announce/announce'
                  })
                }
              }
            })
          }else {
            wx.showToast({
              icon: "none",
              title: res.data.msg
            })
          }
        },
        fail(res) {
          wx.showToast({
            icon: "none",
            title: '网络异常'
          })
        },
        complete(res) {
          wx.hideLoading()
        }
      })
    }else {
      wx.showToast({
        icon: "none",
        title: '请先填写信息'
      })
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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
