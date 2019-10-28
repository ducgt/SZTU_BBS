//app.js
App({
  onLaunch: function () {
    // 展示本地存储能力

    var that = this

    // 登录
    wx.login({
      success(res) {
        if (res.code) {
          //发起网络请求
          wx.request({
            url: that.globalData.host+'user/login/',
            data: {
              code: res.code,
            },
            success(res) {
              if (res.statusCode === 200) {
                console.log(res)
                that.globalData.user_info = res.data.user_info
                wx.setStorageSync('user_info', res.data.user_info)
                that.globalData.user_id = res.data.id
                wx.setStorageSync('user_id', res.data.user_id)
              } else {
                wx.showToast({
                  title: '登陆失败',
                  icon: "none"
                })
              }
            }
          })
        } else {
          wx.showToast({
            title: '网络异常,登陆失败',
            icon: "none"
          })
        }
      }
    })
  },
  globalData: {
    user_info: wx.getStorageSync('user_info'),
    user_id: wx.getStorageSync('user_id'),
    host: "******************", // API地址
    web_view_host: "**********", // webview地址
  },
})
