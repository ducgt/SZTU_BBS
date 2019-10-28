// pages/discuss_room/discuss_room.js
var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    user_info: app.globalData.user_info,
    school_account_2: '',
    college: '请选择学院',
    college_list: [
      '中德智能制造学院',
      '大数据与互联网学院',
      '新材料与新能源学院',
      '城市交通与物流学院',
      '健康与环境工程学院',
      '创意设计学院',
      '商学院',
      '工程物理学院',
      '人文社科学院（马克思主义学院）',
      '研究生院',
      '体育学院',
      '国际交流学院'
    ],
    start: '请选择开始时间',
    end: '请选择结束时间',
    discuss_topic: '',
    nums: 2,
    mobile: '',
    multiArray: [['今天', '明天'], [0, 1, 2, 3, 4, 5, 6], [0, 10, 20]],
    multiIndex: [0,0,0],
  },
  start_change(e){
    console.log(e)
    this.setData({
      start: this.data.multiArray[0][e.detail.value[0]]+' '+this.data.multiArray[1][e.detail.value[1]]+':'+this.data.multiArray[2][e.detail.value[2]]
    })
  },
  end_change(e){
    console.log(e)
    this.setData({
      end: this.data.multiArray[0][e.detail.value[0]]+' '+this.data.multiArray[1][e.detail.value[1]]+':'+this.data.multiArray[2][e.detail.value[2]]
    })
  },
  formReset(e){
    this.setData({
      start: '请选择开始时间',
      end: '请选择结束时间',
      college: '请选择学院',
    })
  },
  formSubmit(e){
    console.log(e)
    var that = this
    if(that.data.college === '请选择学院'||that.data.start === '请选择开始时间'||that.data.end === '请选择结束时间'||e.detail.value.nums.length===0||
      e.detail.value.school_account_2.length === 0||e.detail.value.discuss_topic.length === 0||e.detail.value.mobile.length === 0){
      wx.showToast({
        icon: "none",
        title: '请输入正确信息',
      })
    }else if (that.data.user_info.school_account===e.detail.value.school_account_2){
      wx.showToast({
        icon: "none",
        title: '两个学号不能相同',
      })
    }else {
      wx.request({
        url: app.globalData.host+'library/book_discuss_room/',
        data:{
          user_id: that.data.user_info.id,
          school_account_1: that.data.user_info.school_account,
          school_account_2: e.detail.value.school_account_2,
          college:that.data.college,
          start: that.data.start,
          end: that.data.end,
          discuss_topic: e.detail.value.discuss_topic,
          nums: e.detail.value.nums,
          mobile: e.detail.value.mobile
        },
        success(res) {
          console.log(res)
          if (res.statusCode===200){
            wx.showModal({
              title: '提示',
              content: res.data.msg,
              showCancel: false,
              success(res) {
                if(res.confirm){
                  wx.redirectTo({
                    url: '../result/result'
                  })
                }
              }
            })
          }else {
            wx.showModal({
              title: '提示',
              showCancel: false,
              content: res.data.msg
            })
          }
        }
      })
    }
  },
  change_college(e){
    this.setData({
      college: this.data.college_list[e.detail.value]
    })
  },
  pickerTap:function() {
    var date = new Date();

    var monthDay = [];
    var hours = [];

    // 月-日
    for (var i = 0; i <= 7; i++) {
      var date1 = new Date(date);
      date1.setDate(date.getDate() + i);
      var md = (date1.getMonth() + 1) + "月" + date1.getDate()+'日';
      monthDay.push(md);
    }
    // 时
    for (var i = 8; i < 23; i++) {
      hours.push(i);
    }

    var data = {
      multiArray: this.data.multiArray,
      multiIndex: this.data.multiIndex
    };
    data.multiArray[0] = monthDay;
    data.multiArray[1] = hours;
    data.multiArray[2] = ['00',10,20,30,40,50];
    this.setData({
      multiArray: data.multiArray,
      multiIndex: data.multiIndex
    });
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
