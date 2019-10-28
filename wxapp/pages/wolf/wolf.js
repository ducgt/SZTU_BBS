// pages/wolf/wolf.js
let app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    input_flag: 0,
    input_fucus: false,
    room_name: '',
    room_num: '',
    room_data: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  create(){
    this.setData({
      input_flag: 1,
      input_fucus: true
    })
  },
  join(){
    this.setData({
      input_flag: 2,
      input_fucus: true
    })
  },
  cancel(){
    this.setData({
      input_flag: 0
    })
  },
  // (0, '打卡小分队'),
  // (1, '狼人杀'),
  // (2, '真心话大冒险')
  create_confirm(){
    let that = this
    if (that.data.room_name.length>0){
      wx.request({
        url: app.globalData.host+'game/create_room/',
        data: {
          user_id: app.globalData.user_info.id,
          type: 1,
          topic: that.data.room_name
        },
        success(res) {
          console.log(res)
          that.setData({
            room_name: '',
            input_flag: 0
          })
          wx.navigateTo({
            url: "../wolf_role/wolf_role?room_data="+JSON.stringify(res.data.room_data)
          })
        }
      })
    }else {
      wx.showModal({
        title: "提示",
        content: "房间名不能为空",
        showCancel: false
      })
    }
  },
  my_rooms(){
    this.setData({
      input_flag: 3
    })
    let that = this
    wx.request({
      url: app.globalData.host+'game/my_rooms/',
      data: {
        user_id: app.globalData.user_info.id,
        type: 1
      },
      success(res) {
        console.log(res)
        that.setData({
          room_data: res.data.my_room_data,
        })
      }
    })
  },
  join_confirm(){
    let that = this
    if (that.data.room_num.length>0){
      wx.request({
        url: app.globalData.host+'game/join_room/',
        data: {
          user_id: app.globalData.user_info.id,
          room_number: that.data.room_num,
          type: 1
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
                    url: "../wolf_role/wolf_role?room_data="+JSON.stringify(res.data.room_data)
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
        title: "提示",
        content: "房间号不能为空",
        showCancel: false
      })
    }
  },
  room_name_inp(e){
    this.setData({
      room_name: e.detail.value
    })
  },
  room_num_inp(e){
    this.setData({
      room_num: e.detail.value
    })
  },
  to_room(e){
    console.log(e)
    let that = this
    wx.navigateTo({
      url: "../wolf_role/wolf_role?room_data="+JSON.stringify(that.data.room_data[e.currentTarget.id].room_data)
    })
    this.setData({
      input_flag: 0
    })
  },
  delete_room(e){
    let that = this
    let room_data = that.data.room_data[e.currentTarget.id]
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
                type: 1
              },
              success(res) {
                console.log(res)
                if (res.statusCode===200){
                  that.setData({
                    room_data: res.data.my_room_data
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
                type: 1
              },
              success(res) {
                console.log(res)
                if (res.statusCode===200){
                  that.setData({
                    room_data: res.data.my_room_data
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
