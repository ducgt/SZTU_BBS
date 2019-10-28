// pages/wolf_role/wolf_role.js
let app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    room_data: '',
    role_list: [
      {role:"村民",img: '../../images/CunMing.jpg', counts: 0},
      {role:"狼人",img: '../../images/LangRen.jpg', counts: 0},
      {role:"白狼王",img: '../../images/BaiLangWang.jpg', counts: 0},
      {role:"预言家",img: '../../images/YuYanJia.jpg', counts: 0},
      {role:"女巫",img: '../../images/NvWu.jpg', counts: 0},
      {role:"猎人",img: '../../images/LieRen.jpg', counts: 0},
      {role:"白痴",img: '../../images/BaiChi.jpg', counts: 0},
      {role:"守卫",img: '../../images/ShouWei.jpg', counts: 0},
      {role:"长老",img: '../../images/CunZhang.jpg', counts: 0},
      {role:"丘比特",img: '../../images/QiuBiTe.jpg', counts: 0},
      {role:"盗贼",img: '../../images/DaoZei.jpg', counts: 0},
      {role:"警长",img: '../../images/JingZhang.jpg', counts: 0}
    ],
    user_list:[],
    flag: true,
    nums: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
    user_id: 0
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let room_data = JSON.parse(options.room_data)
    let that = this
    console.log(room_data)
    this.setData({
      room_data: room_data,
      user_id: app.globalData.user_info.id
    })
    wx.request({
      url: app.globalData.host+'game/get_user_list/',
      data: {
        room_id: room_data.id
      },
      success(res) {
        console.log(res)
        that.setData({
          user_list: res.data.user_data
        })
      }
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
  delete_user(e){
    console.log(e)
    let that = this
    if (that.data.user_list[e.currentTarget.id].id==that.data.room_data.user_id){
      wx.showModal({
        title: "提示",
        content: "不可删除房主",
        showCancel: false
      })
    }else if (app.globalData.user_info.id!=that.data.room_data.user_id){
      wx.showModal({
        title: "提示",
        content: "你没有移除成员的权限",
        showCancel: false
      })
    }else {
      wx.showModal({
        title: "提示",
        content:"确定删除该用户吗？",
        success(re) {
          if (re.confirm){
            wx.request({
              url: app.globalData.host+'game/delete_user/',
              data: {
                room_id: that.data.room_data.id,
                user_id: that.data.user_list[e.currentTarget.id].id
              },
              success(res) {
                console.log(res)
                wx.showModal({
                  title: "提示",
                  content:res.data.msg,
                  showCancel: false
                })
                that.setData({
                  user_list: res.data.user_data
                })
              }
            })
          }
        }
      })
    }
  },
  change_counts(e){
    console.log(e)
    let that = this
    let max_count = this.data.nums[e.detail.value]
    if (app.globalData.user_info.id!=that.data.room_data.user_id) {
      wx.showModal({
        title: "提示",
        content: "你没有修改最大人数的权限",
        showCancel: false
      })
    }else {
      wx.request({
        url: app.globalData.host+"game/change_max_counts/",
        data: {
          room_id: that.data.room_data.id,
          max_counts: max_count
        },
        success(res) {
          console.log(res)
          that.setData({
            room_data: res.data.room_data
          })
          wx.showModal({
            title: "提示",
            content: res.data.msg,
            showCancel: false
          })
        }
      })
    }
  },
  auto_distribute(){
    let that = this
    wx.request({
      url: app.globalData.host+"game/auto_distribute/",
      data: {
        room_id: that.data.room_data.id
      },
      success(res) {
        console.log(res)
        if (res.statusCode===200){
          wx.showModal({
            title: "提示",
            showCancel: false,
            content: res.data.msg
          })
        }
      }
    })
  },
  user_distribute(){
    this.setData({
      flag: false
    })
  },
  add(e){
    let i = e.currentTarget.id
    let role = this.data.role_list[i]
    this.setData({
      ['role_list['+i+"].counts"]:role.counts+1
    })
  },
  less(e){
    let i = e.currentTarget.id
    let role = this.data.role_list[i]
    this.setData({
      ['role_list['+i+'].counts']:role.counts?role.counts-1:role.counts
    })
  },
  cancel(){
    this.setData({
      flag: true
    })
  },
  to_distribute(){
    let that = this
    wx.request({
      url: app.globalData.host+"game/user_distribute/",
      data:{
        role_data: that.data.role_list,
        room_id: that.data.room_data.id
      },
      success(res) {
        console.log(res)
        that.setData({
          flag: true
        })
        wx.showModal({
          title: "提示",
          content: res.data.msg,
          showCancel: false
        })
      }
    })
  },
  see_role(){
    wx.navigateTo({
      url: "../wolf_role_2/wolf_role_2?room_id="+this.data.room_data.id
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
    let that = this
    wx.request({
      url: app.globalData.host+'game/get_user_list/',
      data: {
        room_id: that.data.room_data.id
      },
      success(res) {
        console.log(res)
        that.setData({
          user_list: res.data.user_data
        })
        wx.stopPullDownRefresh()
      }
    })
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
