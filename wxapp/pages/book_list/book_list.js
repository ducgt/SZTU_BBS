// pages/book_list/book_list.js
var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    book_info: wx.getStorageSync('book_info') || [],
    user_info: app.globalData.user_info,
    status: ['待审核','已通过','不通过'],
    status_color: ['#00f','#0f0','#f00']
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    wx.request({
      url:app.globalData.host+'library/get_book_info/',
      data:{
        user_id: that.data.user_info.id
      },
      success(res) {
        console.log(res)
        that.setData({
          book_info: res.data.book_info_data
        })
        wx.setStorageSync('book_info', res.data.book_info_data)
      }
    })
  },
  book(){
    wx.navigateTo({
      url: '../discuss_room/discuss_room'
    })
  },
  delete_book(e){
    console.log(e)
    var that = this
    if (e.currentTarget.dataset.status === 1){
      wx.showModal({
        title: '提示',
        content: '已通过的申请无法删除',
        showCancel: false
      })
    }else {
      wx.showModal({
        title: '提示',
        content: '是否删除',
        success(res) {
          if(res.confirm){
            wx.request({
              url: app.globalData.host+'library/delete_book/',
              data: {
                id: e.currentTarget.id,
                user_id: that.data.user_info.id
              },
              success(res) {
                wx.showModal({
                  title: '提示',
                  content: res.data.msg,
                  showCancel: false
                })
                that.setData({
                  book_info: res.data.book_info_data
                })
              }
            })
          }
        }
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
