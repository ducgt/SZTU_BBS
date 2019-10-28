// pages/team _new_room/team_new_room.js
let app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    start: '2019-10-6',
    end: '2022-10-6',
    date_start: '',
    date_end: '',
    time_start: '00:00',
    time_end: "23:59",
    during: '1095',
    topic: '',
    alert: '',
    flag: true,
    room_data: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let date = new Date()
    this.setData({
      start: date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate(),
      date_start: date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate(),
      end: (date.getFullYear()+3)+"-"+(date.getMonth()+1)+"-"+date.getDate(),
      date_end: (date.getFullYear()+3)+"-"+(date.getMonth()+1)+"-"+date.getDate(),
    })
    console.log(this.data.start)
    console.log(this.data.end)
  },
  date_start_change(e){
    console.log(e)
    let start = new Date(e.detail.value)
    let end = new Date(this.data.date_end)
    let during = parseInt((end.getTime()-start.getTime())/(1000*60*60*24))
    if (during>0){
      this.setData({
        date_start: e.detail.value,
        during: during
      })
    }else {
      wx.showModal({
        title: "提示",
        content: "时间不合法",
        showCancel: false
      })
    }

  },
  date_end_change(e){
    console.log(e)
    let end = new Date(e.detail.value)
    let start = new Date(this.data.date_start)
    let during = parseInt((end.getTime()-start.getTime())/(1000*60*60*24))
    if (during>0){
      this.setData({
        date_end: e.detail.value,
        during: during
      })
    }else {
      wx.showModal({
        title: "提示",
        content: "时间不合法",
        showCancel: false
      })
    }
  },

  time_start_change(e){
    console.log(e)
    let end = parseInt(this.data.time_end.replace(/:/g, ''))
    let start = parseInt(e.detail.value.replace(/:/g, ''))
    if (end-start<=0){
      wx.showModal({
        title: "提示",
        content: "时间不合法",
        showCancel: false
      })
    }else {
      this.setData({
        time_start: e.detail.value
      })
    }
  },

  time_end_change(e){
    console.log(e)
    let start = parseInt(this.data.time_start.replace(/:/g, ''))
    let end = parseInt(e.detail.value.replace(/:/g, ''))
    if (end-start<=0){
      wx.showModal({
        title: "提示",
        content: "时间不合法",
        showCancel: false
      })
    }else {
      this.setData({
        time_end: e.detail.value
      })
    }
  },
  new_room(){
    let that = this
    if (that.data.topic.length>0&&that.data.alert.length>0){
      wx.request({
        url: app.globalData.host+'game/create_room/',
        data: {
          user_id: app.globalData.user_info.id,
          type: 0,
          topic: that.data.topic,
          alert: that.data.alert,
          date_start: that.data.date_start,
          date_end: that.data.date_end,
          time_start: that.data.time_start,
          time_end: that.data.time_end,
          during: that.data.during
        },
        success(res) {
          console.log(res)
          that.setData({
            topic: '',
            alert: '',
            flag: false,
            room_data: res.data.room_data
          })
        }
      })
    }else {
      wx.showModal({
        title: "提示",
        content: "目标和宣言不能为空",
        showCancel: false
      })
    }
  },
  topic_inp(e){
    this.setData({
      topic: e.detail.value
    })
  },
  alert_inp(e){
    this.setData({
      alert: e.detail.value
    })
  },
  to_room(){
    wx.navigateTo({
      url: "../team_room/team_room?room_data="+JSON.stringify(this.data.room_data)
    })
    this.setData({
      flag: true
    })
  },
  copy(){
    let that = this
    wx.setClipboardData({
      data: that.data.room_data.number,
      success(res) {
        wx.showToast({
          title: '复制成功'
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
