var sliderWidth = 96; // 需要设置slider的宽度，用于计算中间位置
var app = getApp()

Page({
  data: {
    tabs: ["学生工作", "校园生活"],
    activeIndex: 0,
    sliderOffset: 0,
    sliderLeft: 0,
    notice_data_left: wx.getStorageSync('notice_data_left') || [],
    notice_data_right: wx.getStorageSync('notice_data_right') || [],
    user_info: app.globalData.user_info
  },
  onHide(){
    wx.setStorageSync('notice_data_left', this.data.notice_data_left)
    wx.setStorageSync('notice_data_right', this.data.notice_data_right)
  },
  onLoad: function () {
    console.log(app.globalData.user_info)
    var that = this;
    this.setData({
      user_info: app.globalData.user_info
    })
    wx.getSystemInfo({
      success: function(res) {
        that.setData({
          sliderLeft: (res.windowWidth / that.data.tabs.length - sliderWidth) / 2,
          sliderOffset: res.windowWidth / that.data.tabs.length * that.data.activeIndex
        });
      }
    });
    wx.request({
      url: app.globalData.host+'notice/get_student_work_data/',
      header: {
        token: 'rIhyLkd8OpxStlbk8nYT'
      },
      success(res) {
        if (res.statusCode===200){
          console.log(res)
          that.setData({
            notice_data_left: res.data.notice_data
          })
        } else {
          wx.showToast({
            icon: "none",
            title: '服务器连接失败'
          })
        }
      },
      fail(res) {
        wx.showToast({
          icon: "none",
          title: '网络异常'
        })
      }
    })
    wx.request({
      header: {
        token: 'rIhyLkd8OpxStlbk8nYT'
      },
      url: app.globalData.host+'notice/get_school_life_data/',
      success(res) {
        if (res.statusCode===200){
          console.log(res)
          that.setData({
            notice_data_right: res.data.notice_data
          })
        } else {
          wx.showToast({
            icon: "none",
            title: '服务器连接失败'
          })
        }
      },
      fail(res) {
        wx.showToast({
          icon: "none",
          title: '网络异常'
        })
      }
    })
  },
  // to_webview(){
  //   wx.navigateTo({
  //     url: '../web-view/web-view?id='+app.globalData.user_info.id
  //   })
  // },
  getUserInfo(e){
    console.log(e)
    wx.request({
      header: {
        token: 'rIhyLkd8OpxStlbk8nYT'
      },
      url: app.globalData.host+'user/register/',
      // url: 'http://127.0.0.1:8000/user/register/',
      data: {
        name: e.detail.userInfo.nickName,
        id: app.globalData.user_id,
        gender: e.detail.userInfo.gender,
        user_image: e.detail.userInfo.avatarUrl
      },
      success(res) {
        app.globalData.user_info = res.data.user_info
        wx.showToast({
          title: res.data.msg,
          icon: "none"
        })
      }
    })
    wx.navigateTo({
      url: '../school_confirm/school_confirm',
    })
  },
  onShow(){
    this.setData({
      user_info: app.globalData.user_info
    })
  },
  tabClick: function (e) {
    this.setData({
      sliderOffset: e.currentTarget.offsetLeft,
      activeIndex: e.currentTarget.id
    });
  }
});
